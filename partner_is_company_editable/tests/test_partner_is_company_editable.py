# Copyright 2026 Ecosoft Co., Ltd. (https://ecosoft.co.th)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import Form
from odoo.tests.common import TransactionCase


class TestPartnerIsCompanyEditable(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.Partner = cls.env["res.partner"]
        cls.vat = "BE0477472701"

    def test_01_manual_value_flow(self):
        """User sets the type in the form; it is kept until vat changes."""
        with Form(self.Partner) as form:
            form.name = "New Company"
            self.assertFalse(form.is_company)
            form.is_company = True
        partner = form.record
        self.assertTrue(partner.is_company)
        partner.phone = "+32 2 290 34 90"
        self.assertTrue(partner.is_company)
        # automatic value with a Tax ID, then corrected by the user
        partner.vat = self.vat
        self.assertTrue(partner.is_company)
        partner.is_company = False
        partner.phone = "+32 2 290 34 91"
        self.assertFalse(partner.is_company)
        # a change of Tax ID computes the value again
        partner.vat = "/"
        partner.vat = self.vat
        self.assertTrue(partner.is_company)

    def test_02_context_default_ignored(self):
        """default_is_company from standard actions does not bypass the rule."""
        Partner = self.Partner.with_context(default_is_company=True)
        person = Partner.create({"name": "Person"})
        self.assertFalse(person.is_company)
        company = Partner.create({"name": "Company", "vat": self.vat})
        self.assertTrue(company.is_company)
        with Form(Partner) as form:
            form.name = "Person From Form"
            self.assertFalse(form.is_company)
        self.assertFalse(form.record.is_company)

    def test_03_explicit_value_on_create(self):
        """An explicit value (e.g. import) is kept on create."""
        company = self.Partner.create({"name": "Company", "is_company": True})
        self.assertTrue(company.is_company)
        person = self.Partner.create(
            {"name": "Person", "vat": self.vat, "is_company": False}
        )
        self.assertFalse(person.is_company)

    def test_04_child_contact(self):
        """Child contacts follow the automatic rule (field hidden in form)."""
        company = self.Partner.create({"name": "Company", "is_company": True})
        contact = self.Partner.create({"name": "Contact", "parent_id": company.id})
        self.assertFalse(contact.is_company)

    def test_05_user_context_default_ignored(self):
        """default_is_company does not reach the partner of a new user."""
        user = (
            self.env["res.users"]
            .with_context(default_is_company=True)
            .create({"name": "User", "login": "partner_is_company_editable_user"})
        )
        self.assertFalse(user.partner_id.is_company)
