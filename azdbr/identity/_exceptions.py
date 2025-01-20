from azure.identity import CredentialUnavailableError


class AuthenticationError(CredentialUnavailableError):
    """
    Most likely this error is returned because the identity builder has failed earlier but the authentication request was made explicitly.
    """

    def __init__(self, e):
        super().__init__(e)


class MissingInfoError(Exception):
    """
    The builder was not provided with all the information required.
    """
    def __init__(self, e: Exception):
        super().__init__(e)

class UnsupportedAuthError(Exception):
    """
    Unsupported authentication attempted error (returned by the Builder)
    """
