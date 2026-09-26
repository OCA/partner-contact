# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from unittest.mock import patch

from odoo.models import BaseModel
from odoo.tests.common import TransactionCase


class TestCreateBatch(TransactionCase):
    def _create(self, vals_list, **context):
        """Create partners and return them with the batch sizes that reached
        the database."""
        batches = []
        original = BaseModel._create

        def _create(model, data_list):
            if model._name == "res.partner":
                batches.append(len(data_list))
            return original(model, data_list)

        with patch.object(BaseModel, "_create", _create):
            partners = self.env["res.partner"].with_context(**context).create(vals_list)
        return partners, batches

    def test_partners_are_created_in_one_batch(self):
        partners, batches = self._create(
            [
                {"firstname": "Ana", "lastname": "Pérez", "name": "Ana Pérez"},
                {"name": "Luis García"},
                {"lastname": "Ruiz"},
                {"name": "Tecnativa", "is_company": True},
            ]
        )
        self.assertEqual(
            partners.mapped("name"),
            ["Ana Pérez", "Luis García", "Ruiz", "Tecnativa"],
        )
        self.assertEqual(partners.mapped("firstname"), ["Ana", "Luis", False, False])
        self.assertEqual(
            partners.mapped("lastname"), ["Pérez", "García", "Ruiz", "Tecnativa"]
        )
        self.assertEqual(batches, [4])

    def test_default_name_dropped_for_all_partners(self):
        partners, batches = self._create(
            [
                {"firstname": "Ana", "lastname": "Pérez", "name": "Ana Pérez"},
                {"name": "Luis García"},
                {"lastname": "Ruiz"},
            ],
            default_name="Default Name",
        )
        # without a name, the first name comes from the default name
        self.assertEqual(
            partners.mapped("name"), ["Ana Pérez", "Luis García", "Default Ruiz"]
        )
        self.assertEqual(batches, [3])

    def test_default_name_kept_for_some_partners(self):
        company = self.env["res.partner"].create(
            {"name": "Tecnativa", "is_company": True}
        )
        partners, batches = self._create(
            [
                {"firstname": "Ana", "lastname": "Pérez", "name": "Ana Pérez"},
                # no name to split, so this address keeps the default name
                {"name": None, "type": "invoice", "parent_id": company.id},
                {"lastname": "Ruiz"},
            ],
            default_name="Default Name",
        )
        self.assertEqual(partners.mapped("type"), ["contact", "invoice", "contact"])
        self.assertEqual(
            [partner.name for partner in partners],
            ["Ana Pérez", False, "Default Ruiz"],
        )
        self.assertEqual(batches, [1, 1, 1])
