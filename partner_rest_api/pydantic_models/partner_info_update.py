# Copyright 2022 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from extendable_pydantic import ExtendableModelMeta
from pydantic import BaseModel


class PartnerInfoUpdate(BaseModel, metaclass=ExtendableModelMeta):

    email: str = None
    street: str = None
    street2: str = None
    city: str = None
    zip: str = None
    state_id: int = None
    country_id: int = None
    phone: str = None
    mobile: str = None
