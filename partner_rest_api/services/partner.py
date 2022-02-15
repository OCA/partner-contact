# Copyright 2022 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from typing import List

from odoo.addons.base_rest import restapi
from odoo.addons.base_rest_pydantic.restapi import PydanticModel, PydanticModelList
from odoo.addons.component.core import Component

from ..pydantic_models.partner_info import PartnerInfo, PartnerShortInfo
from ..pydantic_models.partner_info_update import PartnerInfoUpdate
from ..pydantic_models.partner_search_filter import PartnerSearchFilter


class PartnerService(Component):
    _inherit = "base.partner.rest.service"
    _name = "partner.rest.service"
    _usage = "partner"
    _expose_model = "res.partner"
    _description = __doc__

    @restapi.method(
        routes=[(["/<int:_id>"], "GET")], output_param=PydanticModel(PartnerInfo)
    )
    def get(self, _id: int) -> PartnerInfo:
        partner = self._get(_id)
        return PartnerInfo.from_orm(partner)

    def _get_search_domain(self, filters):
        domain = []
        if filters.name:
            domain.append(("name", "like", filters.name))
        if filters.id:
            domain.append(("id", "=", filters.id))
        if filters.ref:
            domain.append(("ref", "like", filters.ref))
        return domain

    @restapi.method(
        routes=[(["/", "/search"], "GET")],
        input_param=PydanticModel(PartnerSearchFilter),
        output_param=PydanticModelList(PartnerShortInfo),
    )
    def search(
        self, partner_search_filter: PartnerSearchFilter
    ) -> List[PartnerShortInfo]:
        domain = self._get_search_domain(partner_search_filter)
        res: List[PartnerShortInfo] = []
        for e in self.env["res.partner"].sudo().search(domain):
            res.append(PartnerShortInfo.from_orm(e))
        return res

    def _prepare_update_values(self, values, partner):
        return values

    @restapi.method(
        routes=[(["/<int:_id>/update"], "POST")],
        input_param=PydanticModel(PartnerInfoUpdate),
        output_param=PydanticModel(PartnerInfo),
    )
    def update(self, _id: int, partner_info_update: PartnerInfoUpdate) -> PartnerInfo:
        partner = self._get(_id)
        values = self._prepare_update_values(
            partner_info_update.dict(exclude_unset=True), partner
        )
        partner.write(values)
        return PartnerInfo.from_orm(partner)
