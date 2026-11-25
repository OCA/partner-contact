# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import tools
from odoo.tests.common import TransactionCase

CORE_CHECK_NAME = "CHECK( (type='contact' AND name IS NOT NULL) or (type!='contact') )"


class TestCoreConstraint(TransactionCase):
    def test_create_with_core_check_name(self):
        """Partners are created while the core check_name constraint is in
        place, as it is during an update that reapplies it from a module loaded
        before this one: their name is already set when they are inserted."""
        tools.drop_constraint(self.env.cr, "res_partner", "res_partner_check_name")
        tools.add_constraint(
            self.env.cr, "res_partner", "res_partner_check_name", CORE_CHECK_NAME
        )
        partners = self.env["res.partner"].create(
            [
                {"name": "Varek Onsby"},
                {"firstname": "Quilmar", "lastname": "Zendro"},
            ]
        )
        self.env.flush_all()
        self.assertEqual(partners.mapped("name"), ["Varek Onsby", "Quilmar Zendro"])
