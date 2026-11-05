# Copyright 2026 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import Form

from .common import PartnerAffiliateCommon


class TestPartnerAffiliate(PartnerAffiliateCommon):
    def test_00_affiliate_address_survives_parent_save(self):
        """Test an affiliate keeps its own address when an existing parent is saved."""
        with Form(self.parent) as parent_form:
            self._add_affiliate(parent_form)

        affiliate = self.parent.affiliate_ids
        self.assertRecordValues(
            affiliate,
            [
                {
                    **self.affiliate_address,
                    "type": "other",
                    "is_company": True,
                    "parent_id": self.parent.id,
                    "company_id": self.parent.company_id.id,
                }
            ],
        )
        self.assertRecordValues(self.parent, [self.parent_address])
        with Form(self.parent) as parent_form:
            parent_form.name = "Renamed Parent Company"
        self.assertRecordValues(affiliate, [self.affiliate_address])

    def test_01_affiliate_address_survives_new_parent_save(self):
        """Test an affiliate keeps its own address when both companies are new."""
        with Form(self.partner_model) as parent_form:
            parent_form.company_type = "company"
            parent_form.name = "New Parent Company"
            self._fill_address(parent_form, self.parent_address)
            self._add_affiliate(parent_form)

        parent = parent_form.record
        self.assertRecordValues(parent, [self.parent_address])
        self.assertRecordValues(
            parent.affiliate_ids,
            [{**self.affiliate_address, "type": "other", "parent_id": parent.id}],
        )

    def test_02_multiple_affiliates_keep_separate_addresses(self):
        """Test affiliates created together retain their respective addresses."""
        second_address = {**self.affiliate_address, "street": "30 Second Street"}
        with Form(self.parent) as parent_form:
            self._add_affiliate(parent_form)
            self._add_affiliate(parent_form, "Second Affiliate", second_address)

        self.assertRecordValues(
            self.parent.affiliate_ids.sorted("id"),
            [
                {**self.affiliate_address, "type": "other"},
                {**second_address, "type": "other"},
            ],
        )

    def test_03_address_changes_preserve_affiliate_independence(self):
        """Test contacts share address changes while affiliates stay independent."""
        with Form(self.parent) as parent_form:
            self._add_affiliate(parent_form)
        affiliate = self.parent.affiliate_ids
        contact = self.partner_model.create(
            {"name": "Company Contact", "type": "contact", "parent_id": self.parent.id}
        )

        affiliate.write({"street": "Updated Affiliate Street"})
        self.assertRecordValues(self.parent, [self.parent_address])
        self.assertRecordValues(contact, [self.parent_address])

        self.parent.write({"street": "Updated Parent Street"})
        self.assertRecordValues(
            affiliate,
            [{**self.affiliate_address, "street": "Updated Affiliate Street"}],
        )
        self.assertRecordValues(
            contact, [{**self.parent_address, "street": "Updated Parent Street"}]
        )
