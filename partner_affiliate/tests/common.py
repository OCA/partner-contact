# Copyright 2026 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import TransactionCase, new_test_user


class PartnerAffiliateCommon(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(
            context=dict(cls.env.context, tracking_disable=True, no_reset_password=True)
        )
        cls.contact_manager = new_test_user(
            cls.env,
            login="affiliate_contact_manager",
            groups="base.group_user,base.group_partner_manager",
        )
        parent_country, affiliate_country = cls.env["res.country"].create(
            [
                {"name": "Parent Country", "code": "XA"},
                {"name": "Affiliate Country", "code": "XB"},
            ]
        )
        parent_state, affiliate_state = cls.env["res.country.state"].create(
            [
                {
                    "name": "Parent State",
                    "code": "P",
                    "country_id": parent_country.id,
                },
                {
                    "name": "Affiliate State",
                    "code": "A",
                    "country_id": affiliate_country.id,
                },
            ]
        )
        cls.parent_address = {
            "street": "10 Parent Street",
            "street2": "Parent Building",
            "city": "Parent City",
            "zip": "10000",
            "state_id": parent_state.id,
            "country_id": parent_country.id,
        }
        cls.affiliate_address = {
            "street": "20 Affiliate Street",
            "street2": "Affiliate Building",
            "city": "Affiliate City",
            "zip": "20000",
            "state_id": affiliate_state.id,
            "country_id": affiliate_country.id,
        }
        cls.partner_model = cls.env["res.partner"].with_user(cls.contact_manager)
        cls.parent = cls.partner_model.create(
            {
                "name": "Parent Company",
                "is_company": True,
                "company_id": cls.env.company.id,
                **cls.parent_address,
            }
        )

    def _fill_address(self, partner_form, address):
        """Fill an address through the form, including country and state onchanges.

        :param partner_form: Partner form to fill.
        :param address: Address values with relational fields expressed as IDs.
        """
        partner_form.country_id = self.env["res.country"].browse(address["country_id"])
        partner_form.state_id = self.env["res.country.state"].browse(
            address["state_id"]
        )
        partner_form.street = address["street"]
        partner_form.street2 = address["street2"]
        partner_form.city = address["city"]
        partner_form.zip = address["zip"]

    def _add_affiliate(self, parent_form, name="Affiliate Company", address=None):
        """Create an affiliate through its parent's nested form.

        :param parent_form: Parent form containing the Affiliates tab.
        :param name: Name of the new affiliate.
        :param address: Address values, defaulting to the affiliate fixture.
        """
        with parent_form.affiliate_ids.new() as affiliate_form:
            affiliate_form.name = name
            self._fill_address(affiliate_form, address or self.affiliate_address)
