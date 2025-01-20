from typing import Any
from azure.core.credentials import AccessToken, TokenRequestOptions
from azure.core.exceptions import ClientAuthenticationError
from ._exceptions import AuthenticationError
from azdbr.identity._enum import AuthType

from azdbr.core.azdbrbase import AzDbrBase


class AzCredential(AzDbrBase):
    def __init__(self, credential: Any, type: AuthType):
        super().__init__(name=__class__.__name__)
        self._credential = credential
        self._type = type

    @property
    def credential(self) -> Any:
        return self._credential

    @property
    def type(self) -> AuthType:
        return self._type

    def close(self):
        self._credential.close()

    def get_token(
        self,
        scopes: str,
        claims: str | None = None,
        tenant_id: str | None = None,
        enable_case: bool = False,
    ) -> AccessToken:
        try:
            token = self._credential.get_token(
                scopes, claims=claims, tenant_id=tenant_id, enable_case=enable_case
            )
            return token
        except ClientAuthenticationError as cae:
            self.error(msg=f"ClientAuthenticationError: {cae}")
            raise AuthenticationError(cae)
        except ValueError as ve:
            self.error(f"ValueError: {ve}")
            raise AuthenticationError(ve)

    def get_token_info(self, scopes: str, options: TokenRequestOptions = None) -> Any:
        return self._credential.get_token_info(scopes, options)
