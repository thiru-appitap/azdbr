from azdbr.identity._enum import AuthType


SPN_w_secret_params = ["tenant_id", "client_id", "client_secret"]
UserCreds_params = ["client_id", "username", "password", "authority", "tenant_id"]
SASKey_params = ["account_name", "sas_key"]

Unsupported_auth_types = [AuthType.AZ_SPN_W_CERT, AuthType.AZ_APP_ID]
