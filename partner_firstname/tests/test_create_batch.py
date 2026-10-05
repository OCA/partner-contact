# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.tests.common import TransactionCase


class TestCreateBatch(TransactionCase):
    def test_partners_created_together(self):
        """Partners created in one call each get the name they would get when
        created alone. The 'default_name' of the context only names the partners
        that give no name, their own name parts winning over it: a partner with a
        name of its own keeps it, and an address without a name to split stays
        without a name."""
        company = self.env["res.partner"].create(
            {"name": "Brixel Holding", "is_company": True}
        )
        partners = (
            self.env["res.partner"]
            .with_context(default_name="Default Name")
            .create(
                [
                    {
                        "firstname": "Quilmar",
                        "lastname": "Zendro",
                        "name": "Quilmar Zendro",
                    },
                    {"name": "Varek Onsby"},
                    {"lastname": "Tolvane"},
                    {},
                    {"name": "Brixel Test Company", "is_company": True},
                    {"name": None, "type": "invoice", "parent_id": company.id},
                ]
            )
        )
        self.assertEqual(
            partners.mapped("name"),
            [
                "Quilmar Zendro",
                "Varek Onsby",
                "Default Tolvane",
                "Default Name",
                "Brixel Test Company",
                False,
            ],
        )
        self.assertEqual(
            partners.mapped("firstname"),
            ["Quilmar", "Varek", "Default", "Default", False, False],
        )
        self.assertEqual(
            partners.mapped("lastname"),
            ["Zendro", "Onsby", "Tolvane", "Name", "Brixel Test Company", False],
        )
