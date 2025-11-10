# Copyright 2025 Camptocamp SA (https://www.camptocamp.com).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import json

from odoo.tests import HttpCase, users


class TextPartnerExport(HttpCase):
    @users("admin")
    def test_export_get_fields(self):
        """Text the export wizard get_fields method.

        Due to the way `properties_company_id` is computed and used in the path of the
        properties definition, the export wizard fails as it expects a stored field.

        A fix is done by implementing the `_field_to_sql` and
        `_search_properties_company_id` methods. This unit test would fail without it.

        .. traceback::

            File "/odoo/src/odoo/addons/web/controllers/export.py", line 400, in get_fields
                exportable_fields.update(self._get_property_fields(fields, model, domain=domain))
                                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            File "/odoo/src/odoo/addons/web/controllers/export.py", line 321, in _get_property_fields
                field_to_get = Model._field_to_sql(Model._table, definition_record, self_subquery)
                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            File "/odoo/src/odoo/odoo/models.py", line 2976, in _field_to_sql
                raise ValueError(f"Cannot convert {field} to SQL because it is not stored")
            ValueError: Cannot convert res.partner.properties_company_id to SQL because it is not stored
        """  # noqa: E501
        self.url_open(
            "/web/export/get_fields",
            data=json.dumps(
                {
                    "params": {
                        "model": "res.partner",
                        "import_compat": True,
                        "domain": [("id", "in", self.env.user.partner_id.ids)],
                    }
                }
            ),
            headers={"Content-Type": "application/json"},
        ).raise_for_status()

    @users("admin")
    def test_export_get_fields_res_users(self):
        """Test also the export of res.users"""
        self.url_open(
            "/web/export/get_fields",
            data=json.dumps(
                {
                    "params": {
                        "model": "res.users",
                        "import_compat": True,
                        "domain": [("id", "in", self.env.user.ids)],
                    }
                }
            ),
            headers={"Content-Type": "application/json"},
        ).raise_for_status()
