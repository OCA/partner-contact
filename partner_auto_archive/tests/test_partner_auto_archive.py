from odoo.tests.common import TransactionCase


class TestPartnerAutoArchive(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.cron = cls.env.ref("partner_auto_archive.ir_cron_archive_contacts")
        cls.contact_1 = cls.env["res.partner"].create(
            {
                "name": "Partner Archive 1",
                "auto_archive": True,
            }
        )
        cls.contact_2 = cls.env["res.partner"].create(
            {
                "name": "Partner Archive 2",
                "auto_archive": True,
            }
        )
        cls.contact_3 = cls.env["res.partner"].create(
            {
                "name": "Partner No Archive",
                "auto_archive": False,
            }
        )

    def test_partner_auto_archive(self):
        self.cron.method_direct_trigger()
        archived_contacts = self.env["res.partner"].search(
            [("active", "=", False), ("name", "ilike", "Partner Archive")]
        )
        self.assertEqual(len(archived_contacts), 2)
        self.assertEqual(archived_contacts[0].auto_archive, False)
