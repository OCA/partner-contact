# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tests import common


class PartnerContactInSeveralCompaniesCase(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"]
        cls.action = cls.env["ir.actions.act_window"]
        # Build self-contained fixtures rather than relying on demo records:
        # since 19.0 Odoo no longer loads demo data in CI databases, so any
        # ``env.ref`` to a demo record would raise during setup.
        cls.main_partner = cls.partner.create(
            {"name": "YourCompany", "is_company": True}
        )
        roger_company = cls.partner.create(
            {"name": "Roger's Company", "is_company": True}
        )
        # Bob: a standalone contact with a single attached work position.
        cls.bob_contact = cls.partner.create(
            {"name": "Bob Egnops", "email": "bob@hillenburg-oceaninstitute.com"}
        )
        cls.bob_job1 = cls.partner.create(
            {
                "name": "Bob Egnops",
                "function": "Technician",
                "email": "bob@yourcompany.com",
                "parent_id": cls.main_partner.id,
                "contact_id": cls.bob_contact.id,
            }
        )
        # Roger: a standalone contact with a single attached work position.
        cls.roger_contact = cls.partner.create({"name": "Roger Scott"})
        cls.roger_job2 = cls.partner.create(
            {
                "name": "Roger Scott",
                "function": "Consultant",
                "parent_id": roger_company.id,
                "contact_id": cls.roger_contact.id,
            }
        )
        # A custom partner action that already opts into "show all positions".
        # The module must NOT override its context (test_06). It ships as a demo
        # record; recreate it under the same xml-id when demo data is absent
        # (e.g. CI on 19.0) so ``_for_xml_id`` still resolves it.
        action_xmlid = "partner_contact_in_several_companies.action_partner_form"
        if not cls.env.ref(action_xmlid, raise_if_not_found=False):
            custom_action = cls.action.create(
                {
                    "name": "All Customers in All Positions",
                    "res_model": "res.partner",
                    "view_mode": "kanban,list,form",
                    "context": (
                        "{'search_default_customer': 1, "
                        "'search_show_all_positions': "
                        "{'is_set': True, 'set_value': True}}"
                    ),
                }
            )
            cls.env["ir.model.data"].create(
                {
                    "module": "partner_contact_in_several_companies",
                    "name": "action_partner_form",
                    "model": "ir.actions.act_window",
                    "res_id": custom_action.id,
                }
            )

    def test_00_show_only_standalone_contact(self):
        """Check that only standalone contact are shown if context
        explicitly state to not display all positions
        """
        ctx = {"search_show_all_positions": {"is_set": True, "set_value": False}}
        partner_ids = self.partner.with_context(**ctx).search([])
        self.assertTrue(self.bob_job1 not in partner_ids)
        self.assertTrue(self.roger_job2 not in partner_ids)

    def test_01_show_all_positions(self):
        """Check that all contact are show if context is empty or
        explicitly state to display all positions or the "is_set"
        value has been set to False.
        """

        partner_ids = self.partner.search([])
        self.assertTrue(self.bob_job1 in partner_ids)
        self.assertTrue(self.roger_job2 in partner_ids)

        ctx = {"search_show_all_positions": {"is_set": False}}
        partner_ids = self.partner.with_context(**ctx).search([])
        self.assertTrue(self.bob_job1 in partner_ids)
        self.assertTrue(self.roger_job2 in partner_ids)

        ctx = {"search_show_all_positions": {"is_set": True, "set_value": True}}
        partner_ids = self.partner.with_context(**ctx).search([])
        self.assertTrue(self.bob_job1 in partner_ids)
        self.assertTrue(self.roger_job2 in partner_ids)

    def test_02_reading_other_contact_one2many_show_all_positions(self):
        """Check that readonly partner's ``other_contact_ids`` return
        all values whatever the context
        """

        ctx = {}
        self.assertEqual(
            self.bob_job1, self.bob_contact.with_context(**ctx).other_contact_ids
        )
        ctx = {"search_show_all_positions": {"is_set": False}}
        self.assertEqual(
            self.bob_job1, self.bob_contact.with_context(**ctx).other_contact_ids
        )
        ctx = {"search_show_all_positions": {"is_set": True, "set_value": False}}
        self.assertEqual(
            self.bob_job1, self.bob_contact.with_context(**ctx).other_contact_ids
        )
        ctx = {"search_show_all_positions": {"is_set": True, "set_value": True}}
        self.assertEqual(
            self.bob_job1, self.bob_contact.with_context(**ctx).other_contact_ids
        )

        ctx = {}
        self.assertIn(self.bob_job1, self.main_partner.with_context(**ctx).child_ids)
        ctx = {"search_show_all_positions": {"is_set": False}}
        self.assertIn(self.bob_job1, self.main_partner.with_context(**ctx).child_ids)
        ctx = {"search_show_all_positions": {"is_set": True, "set_value": False}}
        self.assertIn(self.bob_job1, self.main_partner.with_context(**ctx).child_ids)
        ctx = {"search_show_all_positions": {"is_set": True, "set_value": True}}
        self.assertIn(self.bob_job1, self.main_partner.with_context(**ctx).child_ids)

    def test_03_search_match_attached_contacts(self):
        """Check that searching partner also return partners having
        attached contacts matching search criteria
        """
        # Bob's contact has one other position which is related to
        # 'YourCompany'
        # so search for all contacts working for 'YourCompany'
        # should contain Bob position.
        partner_ids = self.partner.search([("parent_id", "ilike", "YourCompany")])
        self.assertTrue(self.bob_job1 in partner_ids)

        # but when searching without 'all positions',
        # we should get the position standalone contact instead.
        ctx = {"search_show_all_positions": {"is_set": True, "set_value": False}}
        partner_ids = self.partner.with_context(**ctx).search(
            [("parent_id", "ilike", "YourCompany")]
        )
        self.assertTrue(self.bob_contact in partner_ids)

    def test_04_contact_creation(self):
        """Check that we're begin to create a contact"""

        # Create a contact using only name
        new_contact = self.partner.create({"name": "Bob Egnops"})
        self.assertEqual(new_contact.contact_type, "standalone")

        # Create a contact with only contact_id
        new_contact = self.partner.create({"contact_id": self.bob_contact.id})
        self.assertEqual(new_contact.name, "Bob Egnops")
        self.assertEqual(new_contact.contact_type, "attached")

        # Create a contact with both contact_id and name;
        # contact's name should override provided value in that case
        new_contact = self.partner.create(
            {"contact_id": self.bob_contact.id, "name": "Rob Egnops"}
        )
        self.assertEqual(new_contact.name, "Bob Egnops")

        # Reset contact to standalone
        new_contact.write({"contact_id": False})
        self.assertEqual(new_contact.contact_type, "standalone")

        # Reset contact to attached, and ensure only it is unlinked (i.e.
        # context is ignored).
        new_contact.write({"contact_id": self.bob_contact.id})
        ctx = {"search_show_all_positions": {"is_set": True, "set_value": True}}
        new_contact.with_context(**ctx).unlink()
        partner_ids = self.partner.with_context(**ctx).search(
            [("id", "in", [new_contact.id, self.bob_contact.id])]
        )
        self.assertIn(self.bob_contact, partner_ids)
        self.assertNotIn(new_contact, partner_ids)

    def test_05_contact_fields_sync(self):
        """Check that contact's fields are correctly synced between
        parent contact or related contacts
        """

        # Test DOWNSTREAM sync
        self.bob_contact.write({"name": "Rob Egnops"})
        self.assertEqual(self.bob_job1.name, "Rob Egnops")

        # Test UPSTREAM sync
        self.bob_job1.write({"name": "Bob Egnops"})
        self.assertEqual(
            self.bob_contact.name,
            "Bob Egnops",
        )

    def test_06_ir_action(self):
        """Check ir_action context is auto updated."""

        new_context_val = (
            "'search_show_all_positions': {'is_set': True, 'set_value': False}"
        )

        xmlid = "base.action_partner_form"
        details = self.env["ir.actions.act_window"]._for_xml_id(xmlid)

        self.assertIn(
            new_context_val,
            details["context"],
            msg="Default actions not updated with new context",
        )

        xmlid = "partner_contact_in_several_companies.action_partner_form"
        details = self.env["ir.actions.act_window"]._for_xml_id(xmlid)

        self.assertNotIn(
            new_context_val,
            details["context"],
            msg="Custom actions incorrectly updated with new context",
        )

    def test_07_onchange(self):
        """Check onchange method"""

        new_contact = self.partner.create({"name": "Bob before onchange"})
        new_contact.write({"contact_id": self.bob_contact.id})
        new_contact._onchange_contact_id()
        self.assertEqual(new_contact.name, "Bob Egnops")

        new_contact.write({"contact_type": "standalone"})
        new_contact._onchange_contact_type()
        self.assertEqual(new_contact.contact_id, self.partner)

    def test_08_commercial_partner_compute(self):
        new_contact = self.partner.create({"name": "Bob before onchange"})
        new_contact.write({"contact_id": self.bob_contact.id, "parent_id": False})
        new_contact._compute_commercial_partner()
        self.assertEqual(
            new_contact.commercial_partner_id,
            self.bob_contact,
        )

    def test_09_web_data_path_hides_attached_positions(self):
        """Attached contacts must stay hidden on the web client data path.

        Kanban and list views load their records through ``web_search_read``,
        which bypasses the public ``search`` method on Odoo 17+. This is a
        regression test for attached contacts leaking into the Contacts views.
        """
        ctx = {"search_show_all_positions": {"is_set": True, "set_value": False}}
        partner = self.partner.with_context(**ctx)

        result = partner.web_search_read([], {"id": {}, "contact_type": {}})
        shown_ids = [record["id"] for record in result["records"]]
        self.assertNotIn(self.bob_job1.id, shown_ids)
        self.assertNotIn(self.roger_job2.id, shown_ids)
        self.assertIn(self.bob_contact.id, shown_ids)

    def test_10_filter_does_not_leak_into_access_checks(self):
        """The hide filter must not leak into ``_search``: record-rule access
        checks and ``other_contact_ids`` prefetches must still see attached
        contacts under the hide context. Regression test for an AccessError
        raised when opening a standalone contact's form.
        """
        ctx = {"search_show_all_positions": {"is_set": True, "set_value": False}}
        # Relational prefetch must still return the attached contact.
        self.assertIn(
            self.bob_job1,
            self.bob_contact.with_context(**ctx).other_contact_ids,
        )
        # Reading the attached contact must not be blocked by access checks.
        self.bob_job1.with_context(**ctx).web_read({"id": {}, "display_name": {}})
