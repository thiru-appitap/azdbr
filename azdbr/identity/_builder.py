from abc import ABC
import logging
from typing import List, Optional

from azure.identity import (
    ClientSecretCredential,
    UsernamePasswordCredential,
)
from azdbr.core import AzDbrBase

from ._exceptions import AuthenticationError, MissingInfoError, UnsupportedAuthError
from ._enum import AuthType
from ._decorators import func_decorator

from ._constants import (
    SASKey_params,
    SPN_w_secret_params,
    UserCreds_params,
    Unsupported_auth_types,
)

from ._azcred import AzCredential

from ._infostore import AzIdentityInfoStore


class IdentityBuilder(AzDbrBase, ABC):
    """
    Azure Identify Builder interface - specifies type of credentials user prefers and
    creates an abstracted identity object to serve the required identity actions
    """

    def __init__(self, log_level: int = logging.INFO):
        super().__init__(log_level=log_level, name=__name__)

        self._auth_type = AuthType.AZ_SPN_W_SECRET

        self._cred_info = AzIdentityInfoStore()
        self._credential = None

    def with_auth_type(self, authType: AuthType):
        self._auth_type = authType
        return self

    def with_client_secret(self, secret: str):
        self._cred_info.client_secret = secret
        return self

    def with_client_id(self, client_id: str):
        self._cred_info.client_id = client_id
        return self

    def with_tenant_id(self, tenant_id: str):
        self._cred_info.tenant_id = tenant_id
        return self

    def with_user_name(self, username: str):
        self._cred_info.username = username
        return self

    def with_password(self, password: str):
        self._cred_info.password = password
        return self

    def with_authority(self, authority: str):
        self._cred_info.authority = authority
        return self

    def with_account_name(self, accountname):
        self._cred_info.account_name = accountname
        return self

    def with_spn_key(self, key: str):
        self._cred_info.sas_key = key
        return self

    def with_scope(self, scope: Optional[List[str]]):
        self._cred_info.scope = scope
        return self

    auth_fn_map = {}

    def __validate_params(self, attribs: Optional[List[str]]):
        for attrib in attribs:
            _attr = getattr(self._cred_info, attrib, None)
            if not _attr:
                self.error(f"failed: missing {attrib}")
                raise MissingInfoError(
                    f"{self.__class__.__name__}.{self.__validate_params.__name__} failed: missing {attrib}"
                )

    def _validate(self):
        if AuthType.AZ_SPN_W_SECRET == self._auth_type:
            self.__validate_params(SPN_w_secret_params)

        if AuthType.AZ_USER_CREDS == self._auth_type:
            self.__validate_params(UserCreds_params)

        if AuthType.AZ_SPN_CONN_STR == self._auth_type:
            self.__validate_params(SASKey_params)

    auth_fn_map[AuthType.AZ_USER_CREDS] = "_authuser"

    def _authuser(self):
        """
        User authentication provider implementation
        """
        self._validate()

        self._credential = UsernamePasswordCredential(
            **self._cred_info.model_dump(
                exclude=["sas_key", "account_name", "client_secret", "scope"]
            )
        )

    auth_fn_map[AuthType.AZ_SPN_W_SECRET] = "_spnsecret"

    def _spnsecret(self):
        """
        Authenticating as Service Principal using client secret
        """
        self._validate()

        self._credential = ClientSecretCredential(
            **self._cred_info.model_dump(
                exclude=["username", "password", "scope", "sas_key", "account_name"]
            )
        )

    @func_decorator
    def build(self, **kwargs) -> AzCredential:
        """
        Validates the input params and prepares for the credential builder functional task
        """
        if (
            self._cred_info.username
            and self._cred_info.password
            and self._cred_info.client_id
        ):
            self._auth_type = AuthType.AZ_USER_CREDS

        auth_fn = IdentityBuilder.auth_fn_map[self._auth_type]
        if self._auth_type in Unsupported_auth_types or not auth_fn:
            self.error("Unsupported Authentication method: %s", self._auth_type)
            raise UnsupportedAuthError(
                f"{kwargs['d_name']} failed: Unsupported authentication type: {self._auth_type}"
            )

        auth_fn = IdentityBuilder.auth_fn_map[self._auth_type]
        getattr(self, auth_fn)()

        return AzCredential(credential=self._credential, type=self._auth_type)
