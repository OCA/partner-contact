#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.api import _
from odoo.exceptions import UserError
from odoo.fields import Many2one

# Monkey patch to use a model's field
# to automatically show the partner name at a specific date
original_convert_to_record = Many2one.convert_to_record


def _get_partner_name_date(self, record):
    """Get date to be used for partner name `record`"""
    model_date_field_map = getattr(record, "_partner_name_history_field_map", {})
    partner_name_date_field = model_date_field_map.get(self.name)
    if partner_name_date_field in record._fields:
        partner_name_date = record[partner_name_date_field]
    elif partner_name_date_field:
        partner_name_date_method_name = partner_name_date_field

        try:
            partner_name_date_method = getattr(record, partner_name_date_method_name)
        except AttributeError as ae:
            raise UserError(
                _(
                    "Method %(method)s not found in model %(model)s",
                    method=partner_name_date_method_name,
                    model=record._name,
                )
            ) from ae
        else:
            partner_name_date = partner_name_date_method()
    else:
        partner_name_date = None
    return partner_name_date


def partner_name_history_convert_to_record(self, value, record):
    partner = original_convert_to_record(self, value, record)
    # Do this only when needed:
    # - specific context key is present
    # - returned record is a partner
    if (
        record.env.context.get("use_partner_name_history")
        and partner._name == "res.partner"
    ):
        partner_name_date = _get_partner_name_date(self, record)
        if partner_name_date is not None:
            # Otherwise the name of the partner
            # is retrieved once and always returned,
            # even if it is requested for different dates
            partner.invalidate_recordset(
                fnames=[
                    "name",
                ],
            )
            partner = partner.with_context(
                partner_name_date=partner_name_date,
            )
    return partner


Many2one.convert_to_record = partner_name_history_convert_to_record
