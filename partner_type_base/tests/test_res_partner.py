from lxml import etree

from odoo.tests.common import TransactionCase


class TestResPartner(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.ResPartner = cls.env["res.partner"]

        cls.Partner_company = cls.ResPartner.create(
            {"name": "Company Partner", "is_company": True, "type": "contact"}
        )
        cls.Partner_contact = cls.ResPartner.create(
            {"name": "Individual Partner", "is_company": False, "type": "contact"}
        )
        cls.Partner_child = cls.ResPartner.create(
            {
                "name": "Child Partner",
                "is_company": False,
                "type": "contact",
                "parent_id": cls.Partner_company.id,
            }
        )
        cls.Partner_other = cls.ResPartner.create(
            {"name": "Other Partner", "is_company": False, "type": "other"}
        )
        cls.Partner_invoice = cls.ResPartner.create(
            {"name": "Invoice Partner", "is_company": False, "type": "invoice"}
        )
        cls.Partner_delivery = cls.ResPartner.create(
            {"name": "Shipping Partner", "is_company": False, "type": "delivery"}
        )

    def test_is_address_readonly(self):
        self.assertFalse(self.Partner_company.is_address_readonly)
        self.assertFalse(self.Partner_contact.is_address_readonly)
        self.assertTrue(self.Partner_child.is_address_readonly)
        self.assertFalse(self.Partner_invoice.is_address_readonly)
        self.assertFalse(self.Partner_delivery.is_address_readonly)

    def test_is_individual_types(self):
        self.assertFalse(self.Partner_company.is_individual)
        self.assertTrue(self.Partner_contact.is_individual)
        self.assertTrue(self.Partner_other.is_individual)
        self.assertFalse(self.Partner_invoice.is_individual)
        self.assertFalse(self.Partner_delivery.is_individual)

    def test_can_be_parent(self):
        self.assertTrue(self.Partner_company.can_be_parent)
        self.assertFalse(self.Partner_contact.can_be_parent)
        self.assertFalse(self.Partner_other.can_be_parent)
        self.assertFalse(self.Partner_invoice.can_be_parent)
        self.assertFalse(self.Partner_delivery.can_be_parent)

    def test_can_be_child(self):
        self.assertFalse(self.Partner_company.can_be_child)
        self.assertTrue(self.Partner_contact.can_be_child)
        self.assertTrue(self.Partner_other.can_be_child)
        self.assertTrue(self.Partner_invoice.can_be_child)
        self.assertTrue(self.Partner_delivery.can_be_child)

    def test_search_can_be_parent(self):
        partners = self.ResPartner.search([("can_be_parent", "=", True)])
        self.assertIn(self.Partner_company, partners)
        self.assertNotIn(self.Partner_contact, partners)
        partners = self.ResPartner.search([("can_be_parent", "!=", True)])
        self.assertNotIn(self.Partner_company, partners)
        self.assertIn(self.Partner_contact, partners)

    def test_search_can_be_child(self):
        partners = self.ResPartner.search([("can_be_child", "=", True)])
        self.assertNotIn(self.Partner_company, partners)
        self.assertIn(self.Partner_contact, partners)
        self.assertIn(self.Partner_invoice, partners)
        partners = self.ResPartner.search([("can_be_child", "=", False)])
        self.assertIn(self.Partner_company, partners)
        self.assertNotIn(self.Partner_contact, partners)

    def _get_partner_form_arch(self):
        view = self.ResPartner.get_view(
            self.env.ref("base.view_partner_form").id, "form"
        )
        return etree.fromstring(view["arch"])

    def test_form_type_selection(self):
        """The address type selection is available again in the partner form."""
        arch = self._get_partner_form_arch()
        type_fields = arch.xpath("//span[@name='address_name']/field[@name='type']")
        self.assertEqual(len(type_fields), 1)
        self.assertEqual(type_fields[0].get("invisible"), "is_company")
        labels = arch.xpath(
            "//span[@name='address_name']/field[@name='type_address_label']"
        )
        self.assertEqual(labels[0].get("invisible"), "1")

    def test_form_address_readonly(self):
        """Address fields are readonly only through is_address_readonly."""
        arch = self._get_partner_form_arch()
        for fname in ("street", "street2", "city", "state_id", "zip", "country_id"):
            nodes = arch.xpath(
                "//span[@name='address_name']/following-sibling::div"
                f"[hasclass('o_address_format')]//field[@name='{fname}']"
            )
            self.assertEqual(len(nodes), 1, fname)
            self.assertEqual(nodes[0].get("readonly"), "is_address_readonly", fname)
