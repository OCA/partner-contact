# Copyright 2004-2010 Tiny SPRL http://tiny.be
# Copyright 2010-2012 ChriCar Beteiligungs- und Beratungs- GmbH
#             http://www.camptocamp.at
# Copyright 2015 Antiun Ingenieria, SL (Madrid, Spain)
#        http://www.antiun.com
#        Antonio Espinosa <antonioea@antiun.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    id_numbers = fields.One2many(
        comodel_name="res.partner.id_number",
        inverse_name="partner_id",
        string="Identification Numbers",
    )

    dea_number = fields.Char(
        string="DEA #",
    )
    dea_expired_date = fields.Date(string="DEA Expiration Date")
    dea_active = fields.Selection([("yes", "Yes"), ("no", "NO")], string="DEA Active")

    medical_license = fields.Char(
        string="Medical License",
    )
    medical_license_expired_date = fields.Date(string="Medical License Expiration Date")

    @api.depends("id_numbers")
    def _compute_identification(self, field_name, category_code):
        """Compute a field that indicates a certain ID type.

        Use this on a field that represents a certain ID type. It will compute
        the desired field as that ID(s).

        This ID can be worked with as if it were a Char field, but it will
        be relating back to a ``res.partner.id_number`` instead.

        Example:

            .. code-block:: python

            social_security = fields.Char(
                compute=lambda s: s._compute_identification(
                    'social_security', 'SSN',
                ),
                inverse=lambda s: s._inverse_identification(
                    'social_security', 'SSN',
                ),
                search=lambda s, *a: s._search_identification(
                    'SSN', *a
                ),
            )

        Args:
            field_name (str): Name of field to set.
            category_code (str): Category code of the Identification type.
        """
        for record in self:
            id_numbers = record.id_numbers.filtered(
                lambda r: r.category_id.code == category_code
            )
            if not id_numbers:
                # As this is used as a compute method
                # we need to assign something
                record[field_name] = False
                continue
            value = id_numbers[0].name
            record[field_name] = value

    def _inverse_identification(self, field_name, category_code):
        """Inverse for an identification field.

        This method will create a new record, or modify the existing one
        in order to allow for the associated field to work like a Char.

        If a category does not exist of the correct code, it will be created
        using `category_code` as both the `name` and `code` values.

        If the value of the target field is unset, the associated ID will
        be deactivated in order to preserve history.

        Example:

            .. code-block:: python

            social_security = fields.Char(
                compute=lambda s: s._compute_identification(
                    'social_security', 'SSN',
                ),
                inverse=lambda s: s._inverse_identification(
                    'social_security', 'SSN',
                ),
                search=lambda s, *a: s._search_identification(
                    'SSN', *a
                ),
            )

        Args:
            field_name (str): Name of field to set.
            category_code (str): Category code of the Identification type.
        """
        for record in self:
            id_number = record.id_numbers.filtered(
                lambda r: r.category_id.code == category_code
            )
            record_len = len(id_number)
            # Record for category is not existent.
            if record_len == 0:
                name = record[field_name]
                if not name:
                    # No value to set
                    continue
                category = self.env["res.partner.id_category"].search(
                    [("code", "=", category_code)]
                )
                if not category:
                    category = self.env["res.partner.id_category"].create(
                        {"code": category_code, "name": category_code}
                    )
                self.env["res.partner.id_number"].create(
                    {"partner_id": record.id, "category_id": category.id, "name": name}
                )
            # There was an identification record singleton found.
            elif record_len == 1:
                value = record[field_name]
                if value:
                    id_number.name = value
                else:
                    id_number.active = False
            # Guard against writing wrong records.
            else:
                raise ValidationError(
                    _(
                        "This %s has multiple IDs of this type (%s), so a write "
                        "via the %s field is not possible. In order to fix this, "
                        "please use the IDs tab."
                    )
                    % (record._name, category_code, field_name)
                )

    @api.model
    def _search_identification(self, category_code, operator, value):
        """Search method for an identification field.

        Example:

            .. code-block:: python

            social_security = fields.Char(
                compute=lambda s: s._compute_identification(
                    'social_security', 'SSN',
                ),
                inverse=lambda s: s._inverse_identification(
                    'social_security', 'SSN',
                ),
                search=lambda s, *a: s._search_identification(
                    'SSN', *a
                ),
            )

        Args:
            category_code (str): Category code of the Identification type.
            operator (str): Operator of domain.
            value (str): Value to search for.

        Returns:
            list: Domain to search with.
        """
        id_numbers = self.env["res.partner.id_number"].search(
            [("name", operator, value), ("category_id.code", "=", category_code)]
        )
        return [("id_numbers.id", "in", id_numbers.ids)]

    @api.model
    def send_expiration_date_notification(self):
        email_dea_template_id = self.env.ref(
            "partner_identification.email_template_dea_notification",
            raise_if_not_found=False,
        )
        email_medical_template_id = self.env.ref(
            "partner_identification.email_template_medical_notification",
            raise_if_not_found=False,
        )
        des_partner_ids = self.search(
            [
                ("dea_expired_date", "=", fields.Date.today() + relativedelta(days=30)),
                ("dea_active", "=", "yes"),
            ]
        )
        medical_partner_ids = self.search(
            [
                (
                    "medical_license_expired_date",
                    "=",
                    fields.Date.today() + relativedelta(days=30),
                )
            ]
        )
        for partner in des_partner_ids:
            email_dea_template_id.send_mail(
                partner.id,
                force_send=True,
            )

        for partner in medical_partner_ids:
            email_medical_template_id.send_mail(
                partner.id,
                force_send=True,
            )
