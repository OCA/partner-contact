# Copyright 2022 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from extendable_pydantic import ExtendableModelMeta
from pydantic import BaseModel


class PartnerSearchFilter(BaseModel, metaclass=ExtendableModelMeta):

    id: int = None
    name: str = None
    ref: str = None
