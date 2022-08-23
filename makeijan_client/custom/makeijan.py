from pathlib import Path
import configparser

from deprecated import deprecated
from makeijan_client import Configuration, ModelDetail, Image, ApiClient
from makeijan_client.api.default_api import DefaultApi


@deprecated(version='1.2.1', reason="Please use model_server instead")
class Makeijan(object):
    """
    Makeijan Python Client

    Client for the DEVO ML REST API
    """

    def __init__(self, profile=None, domain=None, token=None, host='http://localhost:8081',
                 credential_path=None):
        self.profile = profile
        self.host = host
        self.domain = domain
        self.token = token

        if credential_path is None:
            self.credential_path = Path.home() / '.devo_credentials'
        else:
            self.credential_path = Path(credential_path).expanduser().resolve()

        if not (self.domain and self.token):
            self._read_profile()

        if not (self.domain and self.token):
            raise Exception('Domain name and Token access parameters must be specified or in ~/.devo_credentials')

        conf = Configuration()
        conf.api_key = {'standAloneToken': self.token}
        conf.host = self.host
        self.api = DefaultApi(ApiClient(conf))

    def _read_profile(self):
        """
        Read makeijan credentials from a external config file,
        if they are not provided.
        By default, the file is located in ~/makeijan.ini.

        Use the parameter `profile` to specify which set of
        credentials to use.
        """
        config = configparser.ConfigParser()
        config.read(self.credential_path)

        if self.profile in config:
            profile_config = config[self.profile]
            self.domain = profile_config.get('domain')
            self.token = profile_config.get('token')
            self.host = profile_config.get('host', fallback='http://localhost:8081')

    def check_connection(self):
        """
        Checks if the connection with the backend is working properly
        :return:
        """
        self.api.find_all("*")

    def find_by_name(self, model_name):
        """
        Finds a model by name
        :param model_name: The name of the model
        :return: The found model
        """
        return self.api.find_by_name(self.domain, model_name)

    def find_all(self):
        """
        Finds all models in a given domain
        :return: A list of models
        """
        return self.api.find_all(self.domain)

    def find_image(self, model_name):
        """
        Finds the image of a model
        :param model_name: Name of the model
        :return: The image
        """
        return self.api.find_image(self.domain, model_name)

    def delete_model(self, model_name):
        """
        Deletes a model
        :param model_name: Name of the model
        :return:
        """
        return self.api.delete_model_by_id(self.domain, model_name)

    def create_model(self, model_name, description, engine, file, multimodel,
                     hidden, parent_id):
        """
        Inserts a model
        :param model_name: Name of the model
        :param description: Description
        :param engine: Engine
        :param file: File containing the image
        :param multimodel: Is this model a multimodel or a single model
        :param hidden: Is this model hidden or visible
        :param parent_id: The parent model of this model
        :return: The created model
        """
        with open(file, "rb") as f:
            review = self.api.upload_model_image(self.domain,
                                                 engine=engine,
                                                 file=f.read())

        model = ModelDetail(
            name=model_name,
            engine=engine,
            description=description,
            output_type=review.output_type,
            fields=review.fields,
            image=Image(id=review.image_id) if not multimodel else None,
            clusters=review.clusters,
            category=review.category,
            hidden=hidden,
            parent_id=parent_id)

        self.api.save_model(self.domain, body=model)

        return model

    # TODO: que pasa si se inserta la imagen pero al insertar el modelo hay error??
    # TODO: se puede controlar temporalmente aquí (faltaría endpoint delete image)
    # TODO: otra solución es simular una transacción en el backend con un token aleatorio y único
    def update_model(self, model, file=None):
        """
        Updates a model
        :param model: Model to update
        :param file: File containing the image of the model
        """
        if file:
            review = self.api.upload_model_image(self.domain,
                                                 engine=model.engine, file=file)
            model.fields = review.fields
            model.clusters = review.clusters
            model.image_id = review.image_id
            model.category = review.category

        return self.api.save_model(self.domain, body=model)
