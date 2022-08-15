# Copyright 2017 Tecnativa - Vicent Cubells
# Copyright 2020 Tecnativa - João Marques
# Copyright 2020 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.exceptions import ValidationError
from odoo.tests import common


class TestResPartnerRefUnique(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestResPartnerRefUnique, cls).setUpClass()
        cls.partner_obj = cls.env["res.partner"]
        cls.company_obj = cls.env["res.company"]
        # look for possible already duplicated refs for being resilient
        cls.partner_obj.search([("ref", "!=", False)]).write({"ref": False})
        cls.company = cls.company_obj.create({"name": "Test company"})
        cls.env.user.write(
            {"company_id": cls.company.id, "company_ids": cls.company.ids}
        )
        cls.partner1 = cls.partner_obj.create({"name": "Partner1", "company_id": False})
        cls.partner2 = cls.partner_obj.create({"name": "Partner2", "company_id": False})

    def test_check_ref_company(self):
        (self.partner1 + self.partner2).write({"company_id": self.company.id})
        # Test that we can create/modify partners with same ref in current situation
        self.partner1.ref = "same_ref"
        partner = self.partner_obj.create({"name": "other", "ref": "same_ref"})
        # Try to activate restriction
        with self.assertRaises(ValidationError):
            self.company.partner_ref_unique = "all"
        # Let the situation without duplicate refs and apply global condition
        partner.unlink()
        self.company.partner_ref_unique = "all"
        with self.assertRaises(ValidationError):
            self.partner2.ref = "same_ref"
        with self.assertRaises(ValidationError):
            self.partner_obj.create(
                {"name": "other", "ref": "same_ref", "company_id": self.company.id}
            )
        # This one should also raise the constraint as the no-company contact
        # collapses with the company specific contact
        with self.assertRaises(ValidationError):
            self.partner_obj.create(
                {"name": "other", "ref": "same_ref", "company_id": False}
            )

    def test_partner1_wo_company_new_partner_w_company(self):
        self.company.partner_ref_unique = "all"
        self.partner1.write({"company_id": False, "ref": "same_ref"})
        with self.assertRaises(ValidationError):
            self.partner_obj.create(
                {"name": "other", "ref": "same_ref", "company_id": self.company.id}
            )
        self.partner1.unlink()

    def test_partner1_w_company_new_partner_wo_company(self):
        self.company.partner_ref_unique = "all"
        self.partner1.ref = "same_ref"
        with self.assertRaises(ValidationError):
            self.partner_obj.create(
                {"name": "other", "ref": "same_ref", "company_id": False}
            )
        self.partner1.unlink()

    def test_check_ref_companies(self):
        self.company.partner_ref_unique = (
            "none"  # Ensure no constraint is applied at beginning
        )
        self.partner1.is_company = True
        self.partner2.is_company = True
        # Test that we can create/modify company partners
        # with same ref in current situation
        self.partner1.ref = "same_ref"
        partner3 = self.partner_obj.create(
            {"name": "Company3", "ref": "same_ref", "is_company": True}
        )
        # Try to activate restriction
        with self.assertRaises(ValidationError):
            self.company.partner_ref_unique = "companies"
        # Let the situation without duplicate refs and apply global condition
        partner3.unlink()
        self.company.partner_ref_unique = "companies"
        with self.assertRaises(ValidationError):
            self.partner2.ref = "same_ref"
        with self.assertRaises(ValidationError):
            self.partner_obj.create(
                {"is_company": True, "name": "other", "ref": "same_ref"}
            )
        # Here there shouldn't be any problem
        self.partner_obj.create(
            {"is_company": False, "name": "other", "ref": "same_ref"}
        )

    def test_merge(self):
        self.company.partner_ref_unique = "all"
        self.partner1.ref = "same_ref"
        wizard = self.env["base.partner.merge.automatic.wizard"].create(
            {
                "partner_ids": [(4, self.partner1.id), (4, self.partner2.id)],
                "dst_partner_id": self.partner2.id,
                "state": "selection",
            }
        )
        # this shouldn't raise error
        wizard.action_merge()
