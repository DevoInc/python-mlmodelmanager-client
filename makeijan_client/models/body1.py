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


class Body1(object):
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
        'email': 'str',
        'domain': 'str',
        'password': 'str'
    }

    attribute_map = {
        'email': 'email',
        'domain': 'domain',
        'password': 'password'
    }

    def __init__(self, email=None, domain=None, password=None):  # noqa: E501
        """Body1 - a model defined in Swagger"""  # noqa: E501
        self._email = None
        self._domain = None
        self._password = None
        self.discriminator = None
        if email is not None:
            self.email = email
        if domain is not None:
            self.domain = domain
        if password is not None:
            self.password = password

    @property
    def email(self):
        """Gets the email of this Body1.  # noqa: E501


        :return: The email of this Body1.  # noqa: E501
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email):
        """Sets the email of this Body1.


        :param email: The email of this Body1.  # noqa: E501
        :type: str
        """

        self._email = email

    @property
    def domain(self):
        """Gets the domain of this Body1.  # noqa: E501


        :return: The domain of this Body1.  # noqa: E501
        :rtype: str
        """
        return self._domain

    @domain.setter
    def domain(self, domain):
        """Sets the domain of this Body1.


        :param domain: The domain of this Body1.  # noqa: E501
        :type: str
        """

        self._domain = domain

    @property
    def password(self):
        """Gets the password of this Body1.  # noqa: E501


        :return: The password of this Body1.  # noqa: E501
        :rtype: str
        """
        return self._password

    @password.setter
    def password(self, password):
        """Sets the password of this Body1.


        :param password: The password of this Body1.  # noqa: E501
        :type: str
        """

        self._password = password

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
        if issubclass(Body1, dict):
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
        if not isinstance(other, Body1):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
