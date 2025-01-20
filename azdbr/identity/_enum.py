from enum import Enum


class AuthType(Enum):
    AZ_SPN_W_SECRET = (0,)
    AZ_SPN_W_CERT = (1,)
    AZ_SPN_CONN_STR = (2,)
    AZ_USER_CREDS = (3,)
    AZ_APP_ID = (4,)
