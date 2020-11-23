# Copyright 2018 Akretion - Benoît Guillot
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import hashlib
from collections import OrderedDict

from odoo import _, exceptions, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    version_hash = fields.Char(readonly=True, copy=False)
    date_version = fields.Datetime(string="Date version", readonly=True)

    def get_version_fields(self):
        # deprecated uses _version_fields instead
        return self._version_fields()

    def _version_fields(self):
        return [
            "name",
            "street",
            "street2",
            "zip",
            "city",
            "country_id",
            "parent_id",
        ]

    def get_version_hash(self):
        # deprecated uses _version_hash instead
        return self._version_hash()

    def _version_hash(self):
        version_fields = self._version_fields()
        version = OrderedDict()
        for field in version_fields:
            if field == "parent_id":
                parent_id = self.parent_id.id if self.parent_id else self.id
                version[field] = parent_id
            elif self[field]:
                version[field] = self[field]
        version_hash = hashlib.md5(str(version).encode("utf-8")).hexdigest()
        return version_hash

    def _version_impacted_tables(self):
        """
        :return:
            - list of tables to update in case of address versioning
        """
        return []

    def _version_exclude_keys(self):
        """
        :return:
            - dict:
                key = table name
                value = list of columns to ignore in case of address
                        versioning
        """
        return {}

    def _version_need(self):
        """
        This method is supposed to be overriden to determine when
        an address versioning is needed or not
        :return: True if versioning is required else False
        """
        return False

    def _version_apply(self):
        self.ensure_one()
        if self._version_need():
            # the address is used, create a new version and
            # update related tables
            version_p = self._version_create()
            partner_wizard = self.env[
                "base.partner.merge.automatic.wizard"
            ].with_context(address_version=True)
            partner_wizard._update_foreign_keys(self, version_p)
        return False

    def write(self, vals):
        version_fields = self._version_fields()
        has_written_versioned_fields = any((f in version_fields) for f in vals.keys())
        for partner in self:
            if (
                not partner.version_hash
                and not vals.get("version_hash", False)
                and has_written_versioned_fields
            ):
                partner._version_apply()

            if partner.version_hash and has_written_versioned_fields:
                raise exceptions.UserError(
                    _(
                        "You can't modify a versioned field %s on the "
                        "versioned partner %s."
                    )
                    % (version_fields, partner.name)
                )
        return super(ResPartner, self).write(vals)

    def _version_create(self):
        version_hash = self._version_hash()
        default = {
            "active": False,
            "version_hash": version_hash,
            "parent_id": self.parent_id.id if self.parent_id else self.id,
            "date_version": fields.Datetime.now(),
        }
        return self.copy(default=default)
