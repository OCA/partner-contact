from odoo.exceptions import UserError
from odoo.tests import common


class TestMobileCheckUnique(common.TransactionCase):
    def _create_partners(self, name, mobile, company_id=False):
        return self.env["res.partner"].create(
            {
                "name": name,
                "mobile": mobile,
                "company_id": company_id,
            }
        )

    def test_01_partner_mobile_unique(self):
        # create partners

        self.env.company.write({"partner_mobile_unique_filter_duplicates": True})

        with self.assertRaises(UserError):
            self._create_partners("Test Partner 1", "12345678")
            self._create_partners("Test Partner 2", "12345678")

        with self.assertRaises(UserError):
            self._create_partners("Test Partner 4", "12345678", self.env.company.id)
