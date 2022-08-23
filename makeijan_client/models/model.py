# coding: utf-8

"""
    Makeijan API

    Devo API for machine learning  # noqa: E501

    OpenAPI spec version: 2.0
    Contact: machine.learning@devo.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six


class Model(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'id': 'int',
        'name': 'str',
        'engine': 'str',
        'description': 'str',
        'update_date': 'int',
        'creation_date': 'int',
        'output_type': 'str',
        'image_id': 'int',
        'domain_id': 'str',
        'domain_name': 'str',
        'category': 'str',
        'parent_id': 'int',
        'runtime_size': 'int'
    }

    attribute_map = {
        'id': 'id',
        'name': 'name',
        'engine': 'engine',
        'description': 'description',
        'update_date': 'updateDate',
        'creation_date': 'creationDate',
        'output_type': 'outputType',
        'image_id': 'imageId',
        'domain_id': 'domainId',
        'domain_name': 'domainName',
        'category': 'category',
        'parent_id': 'parentId',
        'runtime_size': 'runtimeSize'
    }

    def __init__(self, id=None, name=None, engine=None, description=None, update_date=None, creation_date=None, output_type=None, image_id=None, domain_id=None, domain_name=None, category=None, parent_id=None, runtime_size=None):  # noqa: E501
        """Model - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._name = None
        self._engine = None
        self._description = None
        self._update_date = None
        self._creation_date = None
        self._output_type = None
        self._image_id = None
        self._domain_id = None
        self._domain_name = None
        self._category = None
        self._parent_id = None
        self._runtime_size = None
        self.discriminator = None
        if id is not None:
            self.id = id
        if name is not None:
            self.name = name
        if engine is not None:
            self.engine = engine
        if description is not None:
            self.description = description
        if update_date is not None:
            self.update_date = update_date
        if creation_date is not None:
            self.creation_date = creation_date
        if output_type is not None:
            self.output_type = output_type
        if image_id is not None:
            self.image_id = image_id
        if domain_id is not None:
            self.domain_id = domain_id
        if domain_name is not None:
            self.domain_name = domain_name
        if category is not None:
            self.category = category
        if parent_id is not None:
            self.parent_id = parent_id
        if runtime_size is not None:
            self.runtime_size = runtime_size

    @property
    def id(self):
        """Gets the id of this Model.  # noqa: E501

        The database generated ID  # noqa: E501

        :return: The id of this Model.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Model.

        The database generated ID  # noqa: E501

        :param id: The id of this Model.  # noqa: E501
        :type: int
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this Model.  # noqa: E501

        The name of the model  # noqa: E501

        :return: The name of this Model.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Model.

        The name of the model  # noqa: E501

        :param name: The name of this Model.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def engine(self):
        """Gets the engine of this Model.  # noqa: E501

        The engine used to train and execute the model  # noqa: E501

        :return: The engine of this Model.  # noqa: E501
        :rtype: str
        """
        return self._engine

    @engine.setter
    def engine(self, engine):
        """Sets the engine of this Model.

        The engine used to train and execute the model  # noqa: E501

        :param engine: The engine of this Model.  # noqa: E501
        :type: str
        """

        self._engine = engine

    @property
    def description(self):
        """Gets the description of this Model.  # noqa: E501

        The description of the model  # noqa: E501

        :return: The description of this Model.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this Model.

        The description of the model  # noqa: E501

        :param description: The description of this Model.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def update_date(self):
        """Gets the update_date of this Model.  # noqa: E501

        The last time the model was modified  # noqa: E501

        :return: The update_date of this Model.  # noqa: E501
        :rtype: int
        """
        return self._update_date

    @update_date.setter
    def update_date(self, update_date):
        """Sets the update_date of this Model.

        The last time the model was modified  # noqa: E501

        :param update_date: The update_date of this Model.  # noqa: E501
        :type: int
        """

        self._update_date = update_date

    @property
    def creation_date(self):
        """Gets the creation_date of this Model.  # noqa: E501

        The time when the model was created  # noqa: E501

        :return: The creation_date of this Model.  # noqa: E501
        :rtype: int
        """
        return self._creation_date

    @creation_date.setter
    def creation_date(self, creation_date):
        """Sets the creation_date of this Model.

        The time when the model was created  # noqa: E501

        :param creation_date: The creation_date of this Model.  # noqa: E501
        :type: int
        """

        self._creation_date = creation_date

    @property
    def output_type(self):
        """Gets the output_type of this Model.  # noqa: E501

        The type of the output value generated by this model as a prediction  # noqa: E501

        :return: The output_type of this Model.  # noqa: E501
        :rtype: str
        """
        return self._output_type

    @output_type.setter
    def output_type(self, output_type):
        """Sets the output_type of this Model.

        The type of the output value generated by this model as a prediction  # noqa: E501

        :param output_type: The output_type of this Model.  # noqa: E501
        :type: str
        """

        self._output_type = output_type

    @property
    def image_id(self):
        """Gets the image_id of this Model.  # noqa: E501

        The id of the uploaded image or file of the model  # noqa: E501

        :return: The image_id of this Model.  # noqa: E501
        :rtype: int
        """
        return self._image_id

    @image_id.setter
    def image_id(self, image_id):
        """Sets the image_id of this Model.

        The id of the uploaded image or file of the model  # noqa: E501

        :param image_id: The image_id of this Model.  # noqa: E501
        :type: int
        """

        self._image_id = image_id

    @property
    def domain_id(self):
        """Gets the domain_id of this Model.  # noqa: E501

        The id of the DEVO domain where this model belongs  # noqa: E501

        :return: The domain_id of this Model.  # noqa: E501
        :rtype: str
        """
        return self._domain_id

    @domain_id.setter
    def domain_id(self, domain_id):
        """Sets the domain_id of this Model.

        The id of the DEVO domain where this model belongs  # noqa: E501

        :param domain_id: The domain_id of this Model.  # noqa: E501
        :type: str
        """

        self._domain_id = domain_id

    @property
    def domain_name(self):
        """Gets the domain_name of this Model.  # noqa: E501

        The name of the DEVO domain where this model belongs  # noqa: E501

        :return: The domain_name of this Model.  # noqa: E501
        :rtype: str
        """
        return self._domain_name

    @domain_name.setter
    def domain_name(self, domain_name):
        """Sets the domain_name of this Model.

        The name of the DEVO domain where this model belongs  # noqa: E501

        :param domain_name: The domain_name of this Model.  # noqa: E501
        :type: str
        """

        self._domain_name = domain_name

    @property
    def category(self):
        """Gets the category of this Model.  # noqa: E501

        The type of model  # noqa: E501

        :return: The category of this Model.  # noqa: E501
        :rtype: str
        """
        return self._category

    @category.setter
    def category(self, category):
        """Sets the category of this Model.

        The type of model  # noqa: E501

        :param category: The category of this Model.  # noqa: E501
        :type: str
        """

        self._category = category

    @property
    def parent_id(self):
        """Gets the parent_id of this Model.  # noqa: E501

        The parent model, if its NULL then by convention this model is a multimodel, if it points to itself then it is a normal model  # noqa: E501

        :return: The parent_id of this Model.  # noqa: E501
        :rtype: int
        """
        return self._parent_id

    @parent_id.setter
    def parent_id(self, parent_id):
        """Sets the parent_id of this Model.

        The parent model, if its NULL then by convention this model is a multimodel, if it points to itself then it is a normal model  # noqa: E501

        :param parent_id: The parent_id of this Model.  # noqa: E501
        :type: int
        """

        self._parent_id = parent_id

    @property
    def runtime_size(self):
        """Gets the runtime_size of this Model.  # noqa: E501

        The size of the model while running in bytes  # noqa: E501

        :return: The runtime_size of this Model.  # noqa: E501
        :rtype: int
        """
        return self._runtime_size

    @runtime_size.setter
    def runtime_size(self, runtime_size):
        """Sets the runtime_size of this Model.

        The size of the model while running in bytes  # noqa: E501

        :param runtime_size: The runtime_size of this Model.  # noqa: E501
        :type: int
        """

        self._runtime_size = runtime_size

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(Model, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, Model):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
