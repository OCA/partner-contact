# Copyright 2022 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import datetime

import pydantic
from extendable_pydantic import ExtendableModelMeta
from pydantic import BaseModel

from odoo.addons.pydantic import utils

from .country import CountryInfo


class CountryStateInfo(BaseModel, metaclass=ExtendableModelMeta):
    id: int
    name: str
    code: str
    country: CountryInfo = pydantic.Field(..., alias="country_id")
    write_date: datetime

    class Config:
        orm_mode = True
        getter_dict = utils.GenericOdooGetter
