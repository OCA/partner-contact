from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    x_customer_id = fields.Char(string="Customer ID", readonly=True, copy=False)
    x_vendor_id = fields.Char(string="Vendor ID", readonly=True, copy=False)
    is_customer = fields.Boolean(
        required=True,
        default=False,
        help="This will assign sequence number for Customer",
    )
    is_vendor = fields.Boolean(
        required=True,
        default=False,
        help="This will assign sequence number for Vendor",
    )
    has_tin = fields.Boolean(string="Has TIN No.", default=True)
    is_employee = fields.Boolean(required=False)
    x_employee_id = fields.Char(string="Employee ID", readonly=True, copy=False)

    # _sql_constraints = [
    #     ('vat_unique', 'unique(vat)', 'The Tax ID must be unique!')
    # ]

    @api.constrains("vat")
    def _check_unique_vat(self):
        for rec in self:
            if rec.vat:
                existing = self.search(
                    [("vat", "=", rec.vat), ("id", "!=", rec.id)], limit=1
                )
                if existing:
                    raise ValidationError(
                        _(
                            "The Tax ID must be unique! \n"
                            "There is a record already registered with this TIN number!"
                        )
                    )

    @api.model
    def create(self, vals):
        partner = super().create(vals)

        updates = {}

        if partner.is_customer and not partner.x_customer_id:
            updates["x_customer_id"] = self.env["ir.sequence"].next_by_code(
                "res.partner.customer"
            )

        if partner.is_vendor and not partner.x_vendor_id:
            updates["x_vendor_id"] = self.env["ir.sequence"].next_by_code(
                "res.partner.vendor"
            )

        if partner.is_employee and not partner.x_employee_id:
            updates["x_employee_id"] = self.env["ir.sequence"].next_by_code(
                "hr.employee.custom"
            )

        if updates:
            super(ResPartner, partner).write(updates)

        return partner

    def write(self, vals):
        result = super().write(vals)

        for rec in self:
            updates = {}
            is_customer = vals.get("is_customer", rec.is_customer)
            is_vendor = vals.get("is_vendor", rec.is_vendor)

            if is_customer and not rec.x_customer_id:
                updates["x_customer_id"] = self.env["ir.sequence"].next_by_code(
                    "res.partner.customer"
                )

            if is_vendor and not rec.x_vendor_id:
                updates["x_vendor_id"] = self.env["ir.sequence"].next_by_code(
                    "res.partner.vendor"
                )

            is_employee = vals.get("is_employee", rec.is_employee)

            if is_employee and not rec.x_employee_id:
                updates["x_employee_id"] = self.env["ir.sequence"].next_by_code(
                    "hr.employee.custom"
                )

            if updates:
                super(ResPartner, rec).write(updates)

        return result
