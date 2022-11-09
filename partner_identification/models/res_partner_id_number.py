# Copyright 2004-2010 Tiny SPRL http://tiny.be
# Copyright 2010-2012 ChriCar Beteiligungs- und Beratungs- GmbH
#             http://www.camptocamp.at
# Copyright 2015 Antiun Ingenieria, SL (Madrid, Spain)
#        http://www.antiun.com
#        Antonio Espinosa <antonioea@antiun.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import api, fields, models


class ResPartnerIdNumber(models.Model):
    _name = "res.partner.id_number"
    _description = "Partner ID Number"
    _order = "name"

    @api.constrains("name", "category_id")
    def validate_id_number(self):
        for record in self:
            record.category_id.validate_id_number(record)

    name = fields.Char(
        string="ID Number",
        required=True,
        help="The ID itself. For example, Driver License number of this person",
    )
    category_id = fields.Many2one(
        string="Category",
        required=True,
        comodel_name="res.partner.id_category",
        help="ID type defined in configuration. For example, Driver License",
    )
    partner_id = fields.Many2one(
        string="Partner", required=True, comodel_name="res.partner", ondelete="cascade"
    )
    partner_issued_id = fields.Many2one(
        string="Issued by",
        comodel_name="res.partner",
        help="Another partner, who issued this ID. For example, Traffic "
        "National Institution",
    )
    place_issuance = fields.Char(
        string="Place of Issuance",
        help="The place where the ID has been issued. For example the country "
        "for passports and visa",
    )
    date_issued = fields.Date(
        string="Issued on",
        help="Issued date. For example, date when person approved his driving "
        "exam, 21/10/2009",
    )
    valid_from = fields.Date(
        string="Valid from", help="Validation period stating date."
    )
    valid_until = fields.Date(
        string="Valid until",
        help="Expiration date. For example, date when person needs to renew "
        "his driver license, 21/10/2019",
    )
    comment = fields.Text(string="Notes")
    status = fields.Selection(
        [
            ("draft", "New"),
            ("open", "Running"),
            ("pending", "To Renew"),
            ("close", "Expired"),
        ]
    )
    active = fields.Boolean(default=True)

    @api.model
    def default_get(self, fields):
        res = super(ResPartnerIdNumber, self).default_get(fields)
        # It seems to be a bug in native odoo that the field partner_id
        # is not in the fields list by default. A workaround is required
        # to force this.
        if "default_partner_id" in self._context and "partner_id" not in fields:
            fields.append("partner_id")
            res["partner_id"] = self._context.get("default_partner_id")
        return res
