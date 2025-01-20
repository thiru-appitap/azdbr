from typing import Any, Optional, List, Dict

from pydantic import BaseModel


class AzIdentityInfoStore(BaseModel):
    """
    User credentials information store for IdentityBuilder
    """

    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    tenant_id: Optional[str] = None

    username: Optional[str] = None
    password: Optional[str] = None

    authority: Optional[str] = "login.microsoftonline.com"

    scope: Optional[List[str]] = ["Mail.Send"]

    sas_key: Optional[str] = None
    account_name: Optional[str] = None
