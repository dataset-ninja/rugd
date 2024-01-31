Dataset **RUGD** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/supervisely-supervisely-assets-public/teams_storage/n/f/6P/kdtPgnXlKvHXuoXwsTuaWSBlWiUQAWYZO3viE24Ij9K3kJbciGpoG0t1YS87Jj9v2UinSpMf20vnrTaUdtS5zou20KEBpkeMrJib6Wk0WPzPb52Vr7biqkaJ3TJa.tar)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='RUGD', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

The data in original format can be downloaded here:

- [Download Sample](http://rugd.vision/data/RUGD_sample-data.zip)
- [Download Raw Frames](http://rugd.vision/data/RUGD_frames-with-annotations.zip)
- [Download Annotations](http://rugd.vision/data/RUGD_annotations.zip)
