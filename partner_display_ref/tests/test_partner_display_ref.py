# Copyright 2026 ForgeFlow S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestPartnerDisplayRef(TransactionCase):
    """Decoration is gated solely by ``partner_display_ref_field`` naming the
    ``res.partner`` field to prefix.

    Opted-in views inject ``partner_display_ref_field`` into the partner field
    context. Whenever it lands in ``env.context`` (and the named field exists
    and has a value) the ``[value]`` prefix is applied to ``display_name`` in
    every context, leaving partners reached without the key untouched.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Partner = cls.env["res.partner"]
        cls.prefix = "ZZPDR-"
        cls.partner_with_ref = Partner.create(
            {"name": f"{cls.prefix}Acme Corp", "ref": "C00123"}
        )
        cls.partner_without_ref = Partner.create({"name": f"{cls.prefix}Globex"})

    def test_field_key_decorates(self):
        partner = self.partner_with_ref.with_context(partner_display_ref_field="ref")
        self.assertEqual(partner.display_name, "[C00123] ZZPDR-Acme Corp")

    def test_formatted_alone_does_not_decorate(self):
        partner = self.partner_with_ref.with_context(formatted_display_name=True)
        self.assertEqual(partner.display_name, "ZZPDR-Acme Corp")

    def test_plain_display_name_untouched(self):
        self.assertEqual(self.partner_with_ref.display_name, "ZZPDR-Acme Corp")

    def test_no_ref_falls_back_to_name(self):
        self.partner_without_ref.ref = False
        partner = self.partner_without_ref.with_context(partner_display_ref_field="ref")
        self.assertEqual(partner.display_name, "ZZPDR-Globex")

    def test_unknown_field_is_ignored(self):
        partner = self.partner_with_ref.with_context(
            partner_display_ref_field="this_field_does_not_exist",
        )
        self.assertEqual(partner.display_name, "ZZPDR-Acme Corp")

    def test_web_name_search_with_field_key(self):
        Partner = self.env["res.partner"].with_context(partner_display_ref_field="ref")
        domain = [("name", "=like", f"{self.prefix}%")]
        results = Partner.web_name_search(
            "Acme", {"display_name": {}}, domain=domain, limit=10
        )
        match = next(r for r in results if r["id"] == self.partner_with_ref.id)
        self.assertEqual(match["__formatted_display_name"], "[C00123] ZZPDR-Acme Corp")
        self.assertEqual(match["display_name"], "[C00123] ZZPDR-Acme Corp")

    def test_web_name_search_without_context(self):
        Partner = self.env["res.partner"]
        domain = [("name", "=like", f"{self.prefix}%")]
        results = Partner.web_name_search(
            "Acme", {"display_name": {}}, domain=domain, limit=10
        )
        match = next(r for r in results if r["id"] == self.partner_with_ref.id)
        self.assertEqual(match["__formatted_display_name"], "ZZPDR-Acme Corp")
