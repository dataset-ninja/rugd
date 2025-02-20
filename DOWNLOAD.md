Dataset **RUGD** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/remote/eyJsaW5rIjogImZzOi8vYXNzZXRzLzM0MTdfUlVHRC9ydWdkLURhdGFzZXROaW5qYS50YXIiLCAic2lnIjogIkR5YTI2WGpEUHI0VVJjLzNKRWJ6M0t5YkV0ZjF2T2ZENHRnRnQzNVlZejg9In0=)

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
