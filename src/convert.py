import glob
import os
import shutil
from urllib.parse import unquote, urlparse

import numpy as np
import supervisely as sly
from cv2 import connectedComponents
from dataset_tools.convert import unpack_if_archive
from supervisely.io.fs import get_file_name, get_file_name_with_ext
from tqdm import tqdm

import src.settings as s


def download_dataset(teamfiles_dir: str) -> str:
    """Use it for large datasets to convert them on the instance"""
    api = sly.Api.from_env()
    team_id = sly.env.team_id()
    storage_dir = sly.app.get_data_dir()

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, str):
        parsed_url = urlparse(s.DOWNLOAD_ORIGINAL_URL)
        file_name_with_ext = os.path.basename(parsed_url.path)
        file_name_with_ext = unquote(file_name_with_ext)

        sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
        local_path = os.path.join(storage_dir, file_name_with_ext)
        teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

        fsize = api.file.get_directory_size(team_id, teamfiles_dir)
        with tqdm(
            desc=f"Downloading '{file_name_with_ext}' to buffer...",
            total=fsize,
            unit="B",
            unit_scale=True,
        ) as pbar:
            api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)
        dataset_path = unpack_if_archive(local_path)

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, dict):
        for file_name_with_ext, url in s.DOWNLOAD_ORIGINAL_URL.items():
            local_path = os.path.join(storage_dir, file_name_with_ext)
            teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

            if not os.path.exists(get_file_name(local_path)):
                fsize = api.file.get_directory_size(team_id, teamfiles_dir)
                with tqdm(
                    desc=f"Downloading '{file_name_with_ext}' to buffer...",
                    total=fsize,
                    unit="B",
                    unit_scale=True,
                ) as pbar:
                    api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)

                sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
                unpack_if_archive(local_path)
            else:
                sly.logger.info(
                    f"Archive '{file_name_with_ext}' was already unpacked to '{os.path.join(storage_dir, get_file_name(file_name_with_ext))}'. Skipping..."
                )

        dataset_path = storage_dir
    return dataset_path


def count_files(path, extension):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                count += 1
    return count


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    ### Function should read local dataset and upload it to Supervisely project, then return project info.###
    images_path = "/home/alex/DATASETS/TODO/RUGD/RUGD_frames-with-annotations"
    masks_path = "/home/alex/DATASETS/TODO/RUGD/RUGD_annotations"
    batch_size = 30
    ds_name = "ds"
    images_folder = "RUGD_frames-with-annotations"
    masks_folder = "RUGD_annotations"

    def get_unique_colors(img):
        unique_colors = []
        img = img.astype(np.int32)
        h, w = img.shape[:2]
        colhash = img[:, :, 0] * 256 * 256 + img[:, :, 1] * 256 + img[:, :, 2]
        unq, unq_inv, unq_cnt = np.unique(colhash, return_inverse=True, return_counts=True)
        indxs = np.split(np.argsort(unq_inv), np.cumsum(unq_cnt[:-1]))
        col2indx = {unq[i]: indxs[i][0] for i in range(len(unq))}
        for col, indx in col2indx.items():
            if col != 0:
                unique_colors.append((col // (256**2), (col // 256) % 256, col % 256))

        return unique_colors

    def create_ann(image_path):
        labels = []

        subfolder = image_path.split("/")[-2].split("-")
        tag_meta = meta.get_tag_meta(subfolder[0])
        if len(subfolder) == 1:
            if subfolder[0] == "trail":
                subfolder = sly.Tag(tag_meta, value=0)
            else:
                subfolder = sly.Tag(tag_meta)
        else:
            value = int(subfolder[1])
            subfolder = sly.Tag(tag_meta, value=value)

        # image_np = sly.imaging.image.read(image_path)[:, :, 0]
        img_height = 550  # image_np.shape[0]
        img_wight = 688  # image_np.shape[1]

        mask_path = image_path.replace(images_folder, masks_folder)
        mask_np = sly.imaging.image.read(mask_path)
        unique_colors = get_unique_colors(mask_np)
        for color in unique_colors:
            mask = np.all(mask_np == color, axis=2)
            bitmap = sly.Bitmap(data=mask)
            obj_class = color_to_class[color]
            label = sly.Label(bitmap, obj_class)
            labels.append(label)

        return sly.Annotation(img_size=(img_height, img_wight), labels=labels, img_tags=[subfolder])

    color_to_class = {
        (0, 0, 0): sly.ObjClass("void", sly.Bitmap, color=(0, 0, 0)),
        (108, 64, 20): sly.ObjClass("dirt", sly.Bitmap, color=(108, 64, 20)),
        (255, 229, 204): sly.ObjClass("sand", sly.Bitmap, color=(255, 229, 204)),
        (0, 102, 0): sly.ObjClass("grass", sly.Bitmap, color=(0, 102, 0)),
        (0, 255, 0): sly.ObjClass("tree", sly.Bitmap, color=(0, 255, 0)),
        (0, 153, 153): sly.ObjClass("pole", sly.Bitmap, color=(0, 153, 153)),
        (0, 128, 255): sly.ObjClass("water", sly.Bitmap, color=(0, 128, 255)),
        (0, 0, 255): sly.ObjClass("sky", sly.Bitmap, color=(0, 0, 255)),
        (255, 255, 0): sly.ObjClass("vehicle", sly.Bitmap, color=(255, 255, 0)),
        (255, 0, 127): sly.ObjClass("container", sly.Bitmap, color=(255, 0, 127)),
        (64, 64, 64): sly.ObjClass("asphalt", sly.Bitmap, color=(64, 64, 64)),
        (255, 128, 0): sly.ObjClass("gravel", sly.Bitmap, color=(255, 128, 0)),
        (255, 0, 0): sly.ObjClass("building", sly.Bitmap, color=(255, 0, 0)),
        (153, 76, 0): sly.ObjClass("mulch", sly.Bitmap, color=(153, 76, 0)),
        (102, 102, 0): sly.ObjClass("rock-bed", sly.Bitmap, color=(102, 102, 0)),
        (102, 0, 0): sly.ObjClass("log", sly.Bitmap, color=(102, 0, 0)),
        (0, 255, 128): sly.ObjClass("bicycle", sly.Bitmap, color=(0, 255, 128)),
        (204, 153, 255): sly.ObjClass("person", sly.Bitmap, color=(204, 153, 255)),
        (102, 0, 204): sly.ObjClass("fence", sly.Bitmap, color=(102, 0, 204)),
        (255, 153, 204): sly.ObjClass("bush", sly.Bitmap, color=(255, 153, 204)),
        (0, 102, 102): sly.ObjClass("sign", sly.Bitmap, color=(0, 102, 102)),
        (153, 204, 255): sly.ObjClass("rock", sly.Bitmap, color=(153, 204, 255)),
        (102, 255, 255): sly.ObjClass("bridge", sly.Bitmap, color=(102, 255, 255)),
        (101, 101, 11): sly.ObjClass("concrete", sly.Bitmap, color=(101, 101, 11)),
        (114, 85, 47): sly.ObjClass("picnic-table", sly.Bitmap, color=(114, 85, 47)),
    }

    creek_meta = sly.TagMeta("creek", sly.TagValueType.NONE)
    park_meta = sly.TagMeta("park", sly.TagValueType.ANY_NUMBER)
    trail_meta = sly.TagMeta("trail", sly.TagValueType.ANY_NUMBER)
    village_meta = sly.TagMeta("village", sly.TagValueType.NONE)

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    meta = sly.ProjectMeta(
        obj_classes=list(color_to_class.values()),
        tag_metas=[creek_meta, park_meta, trail_meta, village_meta],
    )
    api.project.update_meta(project.id, meta.to_json())

    dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

    images_pathes = glob.glob(images_path + "/*/*.png")

    progress = sly.Progress("Create dataset {}".format(ds_name), len(images_pathes))

    for img_pathes_batch in sly.batched(images_pathes, batch_size=batch_size):
        img_names_batch = [get_file_name_with_ext(im_path) for im_path in img_pathes_batch]

        img_infos = api.image.upload_paths(dataset.id, img_names_batch, img_pathes_batch)
        img_ids = [im_info.id for im_info in img_infos]

        anns = [create_ann(image_path) for image_path in img_pathes_batch]
        api.annotation.upload_anns(img_ids, anns)

        progress.iters_done_report(len(img_names_batch))

    return project
