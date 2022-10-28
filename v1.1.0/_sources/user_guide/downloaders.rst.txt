Downloaders
===========

A downloader is a component used to stored the model file in some way.
It is a callable of the type
:const:`DownloaderCallable <devo_ml.modelmanager.downloader.DownloaderCallable>`
that receive a `model`, perform an action to store it and
returns some kind of identification of the action performed.

:class:`Downloader <devo_ml.modelmanager.downloader.Downloader>` is an interface
for downloaders that forces you to make instances of the class callable of type
:const:`DownloaderCallable <devo_ml.modelmanager.downloader.DownloaderCallable>`.
You need to implement the `__call__` method when you inherit from it.


File System Downloader
----------------------

The library provides a downloader implementation capable of stores model files
in a file system;
:class:`FileSystemDownloader <devo_ml.modelmanager.downloader.FileSystemDownloader>`.

.. code-block::

    >>> from devo_ml.modelmanager.downloader import FileSystemDownloader

    >>> downloader = FileSystemDownloader("~/download/models/")

A :class:`FileSystemDownloader <devo_ml.modelmanager.downloader.FileSystemDownloader>`
needs a root path to be constructed, it is where files will be downloaded. The
file name will be the model name plus the inferred extension from the engine.
The extension will be empty if it can not infer, e.g: if there is no extension
associated to the engine.

.. note::

    The :class:`FileSystemDownloader <devo_ml.modelmanager.downloader.FileSystemDownloader>`
    it used as a fallback downloader when a downloader is not provided when creating
    a :class:`Client <devo_ml.modelmanager.client.Client>`, and in places where it
    is not possible passing custom downloaders;
    :ref:`client factories <Factories>` and :ref:`functions facade <Functions Facade>`.


Example AWS S3 Bucket Downloader
--------------------------------

This is example of how to customize the behavior of the client on downloading
the model files. Let's implement a AWS S3 Bucket downloader.

.. code-block::

    import boto3

    from devo_ml.modelmanager.engines import get_default_engine_extension
    from devo_ml.modelmanager.downloader import Downloader
    from devo_ml.modelmanager.downloader import get_image_bytes


    class AwsS3BucketDownloader(Downloader):
        def __init__(
            self,
            bucket: str = None,
            region: str = None,
            access_key: str = None,
            access_secret: str = None
        ) -> None:
            self.bucket = bucket
            self.region = region
            self.access_key = access_key
            self.access_secret = access_secret

        def __call__(self, model: dict) -> str:
            name = model.get("name")
            engine = model.get("engine")
            if not name or not engine:
                raise ValueError("Invalid model")
            image_bytes = get_image_bytes(model.get("image", {}))
            ext = get_default_engine_extension(engine)
            s3 = boto3.client(
                "s3",
                region_name=self.region,
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.access_secret
            )
            s3.upload_fileobj(
                io.BytesIO(image_bytes),
                self.bucket,
                f"{name}{ext}"
            )
            return f"{self.bucket}/{name}{ext}"

.. warning::

    This is not a fully tested code, please, if you are going to use it, test
    and tune it according to your needs.
