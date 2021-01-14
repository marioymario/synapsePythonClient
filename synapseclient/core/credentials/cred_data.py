import abc
import base64
import collections
import hashlib
import hmac
import keyring
import requests.auth
import time
import urllib.parse as urllib_parse

import synapseclient.core.utils


class SynapseCredentials(requests.auth.AuthBase, abc.ABC):

    def __init__(self, username):
        self._username = username

    @property
    def username(self):
        return self._username

    @classmethod
    @abc.abstractmethod
    def get_from_keyring(cls, username: str) -> 'SynapseCredentials':
        pass

    @abc.abstractmethod
    def delete_from_keyring(self):
        pass

    @abc.abstractmethod
    def store_to_keyring(self):
        pass


class SynapseApiKeyCredentials(SynapseCredentials):
    """
    Credentials used to make requests to Synapse.
    """

    # cannot change without losing access to existing client's stored api keys
    API_KEY_KEYRING_SERVICE_NAME = "SYNAPSE.ORG_CLIENT"

    # setting and getting api_key it will use the base64 encoded string representation
    @property
    def api_key(self):
        return base64.b64encode(self._api_key).decode()

    @api_key.setter
    def api_key(self, value):
        self._api_key = base64.b64decode(value)

    def __init__(self, username, api_key_string):
        super().__init__(username)
        self.api_key = api_key_string

    def get_signed_headers(self, url):
        """
        Generates signed HTTP headers for accessing Synapse urls
        :param url:
        :return:
        """
        sig_timestamp = time.strftime(synapseclient.core.utils.ISO_FORMAT, time.gmtime())
        url = urllib_parse.urlparse(url).path
        sig_data = self.username + url + sig_timestamp
        signature = base64.b64encode(hmac.new(self._api_key,
                                              sig_data.encode('utf-8'),
                                              hashlib.sha1).digest())

        return {'userId': self.username,
                'signatureTimestamp': sig_timestamp,
                'signature': signature}

    @classmethod
    def get_from_keyring(cls, username) -> 'SynapseCredentials':
        api_key = keyring.get_password(cls.API_KEY_KEYRING_SERVICE_NAME, username)
        return SynapseApiKeyCredentials(username, api_key) if api_key else None

    def delete_from_keyring(self):
        try:
            keyring.delete_password(self.API_KEY_KEYRING_SERVICE_NAME, self.username)
        except keyring.errors.PasswordDeleteError:
            # The api key does not exist, but that is fine
            pass

    def store_to_keyring(self):
        keyring.set_password(self.API_KEY_KEYRING_SERVICE_NAME, self.username, self.api_key)

    def __call__(self, r):
        signed_headers = self.get_signed_headers(r.url)
        r.headers.update(signed_headers)
        return r

    def __repr__(self):
        return f"SynapseCredentials(username='{self.username}', api_key='{self.api_key}')"


# a class that just contains args passed form synapse client login
# TODO remove deprecated sessionToken
UserLoginArgs = collections.namedtuple('UserLoginArgs',
                                       ['username', 'password', 'api_key', 'skip_cache', 'session_token'])
# make the namedtuple's arguments optional instead of positional. All values default to None
UserLoginArgs.__new__.__defaults__ = (None,) * len(UserLoginArgs._fields)
