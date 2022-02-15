# Copyright 2022 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import datetime

import pydantic
from extendable_pydantic import ExtendableModelMeta
from pydantic import BaseModel

from odoo.addons.pydantic import utils

from .country import CountryInfo
from .country_state import CountryStateInfo


class PartnerShortInfo(BaseModel, metaclass=ExtendableModelMeta):
    id: int
    name: str
    email: str = None
    street: str = None
    street2: str = None
    city: str = None
    zip: str = None
    state: CountryStateInfo = pydantic.Field(None, alias="state_id")
    country: CountryInfo = pydantic.Field(None, alias="country_id")
    phone: str = None
    mobile: str = None
    ref: str = None
    write_date: datetime

    class Config:
        orm_mode = True
        getter_dict = utils.GenericOdooGetter


class PartnerInfo(PartnerShortInfo):
    pass
