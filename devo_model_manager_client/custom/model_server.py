import copy
import logging
import os
from pathlib import Path
import configparser
from typing import Optional

from devo_model_manager_client import Configuration, ModelDetail, Image, ApiClient
from devo_model_manager_client.api.default_api import DefaultApi

DEFAULT_CREDENTIALS_PATH = \
    (Path.home() / '.devo_credentials').expanduser().resolve()
DEFAULT_PROFILE = 'default'


class ModelServer(object):
    """
  ModelServer class, this class lets a user create, modify and delete models.

  The user can also create multimodels, which are models composed of many
  other models.

  Once a model has been created some properties can be changed, including
  its image.
  """

    def __init__(self,
                 url: Optional[str] = None,
                 domain: Optional[str] = None,
                 token: Optional[str] = None,
                 profile: Optional[str] = DEFAULT_PROFILE,
                 credentials_path: Optional[str] = DEFAULT_CREDENTIALS_PATH):

        self._profile = profile
        self._url = url
        self._domain = domain
        self._token = token
        self._internal_client = None
        self._credentials_path = Path(credentials_path).expanduser().resolve()

        # Read configuration from a config file if specified, parameters
        # passed to the constructor have priority over the config file.
        if self._profile and self._credentials_path:
            self._read_profile()

        if not (self._domain and self._token and self._url):
            raise ValueError('Missing url, domain or token')

    @property
    def profile(self):
        """Getter of 'profile' attribute."""
        return self._profile

    @property
    def url(self):
        """Getter of 'url' attribute."""
        return self._url

    @property
    def domain(self):
        """Getter of 'domain' attribute."""
        return self._domain

    @property
    def token(self):
        """Getter of 'token' attribute."""
        return self._token

    @property
    def internal_client(self):
        """Getter of 'internal_client' attribute."""
        return self._internal_client

    @property
    def credentials_path(self):
        """Getter of 'credentials_path' attribute."""
        return self._credentials_path

    @classmethod
    def create(cls, url: str, domain: str, token: str):
        """
        Configure the client directly with parameters
        :param url: API url
        :param domain: DEVO domain
        :param token: security token
        :return:
        """
        return cls(url, domain, token)

    @classmethod
    def create_from_config(cls,
                           profile: str,
                           credentials_path: Optional[
                               str] = DEFAULT_CREDENTIALS_PATH):
        """
        Configure the client with a configuration file
        :param profile: Id of the configuration profile
        :param credentials_path: Path to the config file
        :return:
        """
        return cls(None, None, None, profile, credentials_path)

    def _read_profile(self):
        """
        Read devo-model-manager credentials from a external
        config file if they are not already provided by the
        constructor.
        Use the parameter `profile` to specify which set of
        credentials to use.
        """
        config = configparser.ConfigParser()
        config.read(self._credentials_path)

        if self._profile in config:
            profile_config = config[self._profile]
            if self._domain is None:
                self._domain = profile_config.get('domain')
            if self._token is None:
                self._token = profile_config.get('oauth_token')
            if self._url is None:
                self._url = profile_config.get('makeijan_url')

    def _connect(self):
        conf = Configuration()
        conf.api_key = {'standAloneToken': self._token}
        conf.host = self._url
        self._internal_client = DefaultApi(ApiClient(conf))

    def __enter__(self):
        self._connect()
        return self

    def __exit__(self, *args):
        pass

    def create_model(self, name, engine, path, description='',
                     parent_id=None, hidden=False):
        """
    Creates a model from a image file
    :param name: The name of the model
    :param engine: The name of the engine
    :param path: The path to the model image
    :param description: The description
    :param parent_id: If this model has a parent you can link it with it by
    setting the parent id
    :param hidden: Whether the model will be visible by users or not
    :return:
    """

        with open(path, "rb") as f:
            review = self._internal_client.upload_model_image(
                self._domain, engine=engine, file_name=f.read())
        model = ModelDetail(
            name=name,
            engine=engine,
            description=description,
            output_type=review.output_type,
            fields=review.fields,
            image=Image(
                id=review.image_id) if review.image_id is not None else None,
            clusters=review.clusters,
            category=review.category,
            hidden=hidden,
            parent_id=parent_id,
            runtime_size=review.runtime_size)

        self._internal_client.save_model(self._domain, body=model)

    def create_multimodel(self, name, engine, path, description=''):
        """
    Creates a multimodel by loading every child model
    :param name: Name of the multimodel
    :param engine: Engine used
    :param path: The path where the images for the child models are stored
    :param description: Description of the model
    :return: A list with the parent and a nested list with the child models
    """

        # Extract the parameters from the first image
        for root, dirs, filenames in os.walk(path):
            with open(os.path.join(root, filenames[0]), "rb") as f:
                review = self._internal_client.upload_model_image(
                    self._domain, engine=engine, file_name=f.read())
            break

        parent = ModelDetail(
            name=name,
            engine=engine,
            description=description,
            output_type=review.output_type,
            fields=review.fields,
            image=None,
            clusters=review.clusters,
            category=review.category,
            hidden=False,
            parent_id=None)

        self.save_model(parent)

        parent = self._internal_client.find_by_name(self._domain, name)

        child_image_paths = []
        child_image_filenames = []
        for root, dirs, filenames in os.walk(path):
            for filename in filenames:
                child_image_filenames.append(filename)
                child_image_paths.append(os.path.join(root, filename))

        for path, filename in zip(child_image_paths, child_image_filenames):
            self.create_model(name + '_' + filename.split('.')[0], engine, path,
                              description + '(Child "' + filename + '")',
                              parent.id,
                              True)

        children = self._internal_client.find_all_children(self._domain, name)

        return [parent, children]

    def update_image(self, model_name, image_path):

        # TODO: this method should be and enpoint because we have to
        # TODO: delete the old image and update the model and do everything
        # TODO: on a single transaction

        model = self._internal_client.find_by_name(self._domain, model_name)

        with open(image_path, "rb") as f:
            review = self._internal_client.upload_model_image(
                self._domain, engine=model.engine, file_name=f.read())

        model.image = Image(review.image_id)

        return self._internal_client.save_model(self._domain, body=model)

    def save_model(self, model):
        """
    Saves a model, only some fields can be modified like field or cluster
    descriptions or the model description.
    :param model: The model
    :return:
    """

        # An image cannot be sent to the server or it will throw
        # an error
        sent = copy.deepcopy(model)
        if sent.image is not None:
            sent.image.image = None

        return self._internal_client.save_model(self._domain, body=sent)

    def delete_model(self, name):
        """
    Deletes the model and every children model if they exist.

    :param name: The name of the model
    :return:
    """
        children = self._internal_client.find_all_children(self._domain, name)

        # TODO: Move this to the server where it can be done inside one
        #  transaction
        for child in children:
            self.delete_model(child.name)

        self._internal_client.delete_model_by_id(self._domain, name)

    def find_model(self, name):
        """
    Retrieves a model with all the information including the binary image
    :param name: The name of the model
    :return: The model
    """
        model = self._internal_client.find_by_name(self._domain, name)
        return None if model.id is None else model

    def find_models(self):
        """
    Finds all models inside a domain. The returned models are
    simplified views.
    :return:  A list of simplified model descriptions
    """
        return self._internal_client.find_all(self._domain)
