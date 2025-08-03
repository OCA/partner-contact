# Copyright 2015 Antiun Ingenieria S.L. - Antonio Espinosa
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    partner_names_order = fields.Selection(
        selection="_partner_names_order_selection",
        help="Order to compose partner fullname",
        config_parameter="partner_names_order",
        default=lambda a: a._partner_names_order_default(),
        required=True,
        inverse="_inverse_partner_names_order",
    )
    partner_names_order_changed = fields.Boolean(
        config_parameter="partner_names_order_changed"
    )

    def _partner_names_order_selection(self):
        return [
            ("last_first", "Lastname Firstname"),
            ("last_first_comma", "Lastname, Firstname"),
            ("first_last", "Firstname Lastname"),
        ]

    def _partner_names_order_default(self):
        return self.env["res.partner"]._names_order_default()

    def _inverse_partner_names_order(self):
        current = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param(
                "partner_names_order", default=self._partner_names_order_default()
            )
        )
        for record in self:
            record.partner_names_order_changed = bool(
                record.partner_names_order != current
            )

    def _partners_for_recalculating(self):
        return self.env["res.partner"].search(
            [
                ("is_company", "=", False),
                ("firstname", "!=", False),
                ("lastname", "!=", False),
            ]
        )

    def action_recalculate_partners_name(self):
        self.env["ir.config_parameter"].sudo().set_param(
            "partner_names_order", self.partner_names_order
        )
        partners = self._partners_for_recalculating()
        _logger.info("Recalculating names for %d partners.", len(partners))
        partners._compute_name()
        self.partner_names_order_changed = False
        self.execute()
        _logger.info("%d partners updated.", len(partners))
        return True
