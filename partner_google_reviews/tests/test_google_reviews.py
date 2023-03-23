# Copyright 2023 Akretion (https://www.akretion.com).
# @author Pierrick Brun <pierrick.brun@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from vcr_unittest import VCRMixin

from odoo.exceptions import UserError
from odoo.tests import SavepointCase


class TestPartnerGoogleReviews(VCRMixin, SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env["ir.config_parameter"].set_param(
            "partner_google_reviews.google_places_api_key", "test"
        )
        cls.partner = cls.env["res.partner"].create(
            {"name": "McDonald's Charpennes", "city": "Villeurbanne"}
        )

    def _get_vcr_kwargs(self, **kwargs):
        return {
            "record_mode": "once",
            "match_on": ["method", "path", "query"],
            "filter_query_parameters": ["key"],
            "decode_compressed_response": True,
        }

    def test_update_google_reviews_info(self):
        self.assertEqual(0, self.partner.google_rating)
        self.partner.update_google_reviews_info()
        self.assertEqual(3.2, self.partner.google_rating)
        self.assertEqual("McDonald's", self.partner.google_reviews_result)
        self.assertEqual(2436, self.partner.google_reviews_number)
        self.assertEqual(
            "https://www.google.com/maps/place/?q=place_id:ChIJZVMgfYXq9EcRd1TD3vvTmhU",
            self.partner.google_reviews_url,
        )

    def test_update_google_reviews_info_not_found(self):
        self.partner.name = "fdsfjdfdksjfu"
        self.partner.city = "FDFDFDFDFDFFDFDFDFF"
        self.assertEqual(0, self.partner.google_rating)
        self.partner.update_google_reviews_info()
        self.assertEqual(0, self.partner.google_rating)
        self.assertEqual(False, self.partner.google_reviews_result)
        self.assertEqual(0, self.partner.google_reviews_number)
        self.assertEqual("No results found", self.partner.google_places_err)

    def test_update_google_reviews_info_no_reviews(self):
        self.partner.name = "Bellecombe - Gaité bus"
        self.partner.city = "Lyon"
        self.assertEqual(0, self.partner.google_rating)
        self.partner.update_google_reviews_info()
        self.assertEqual(0, self.partner.google_rating)
        self.assertEqual("Bellecombe - Gaité", self.partner.google_reviews_result)
        self.assertEqual(0, self.partner.google_reviews_number)
        self.assertEqual(
            "No rating or number of reviews found", self.partner.google_places_err
        )
        self.assertEqual(
            "https://www.google.com/maps/place/?q=place_id:ChIJv5Fn4oXq9EcReZcpO3Mkx4w",
            self.partner.google_reviews_url,
        )

    def test_update_google_reviews_info_no_api_key(self):
        self.env["ir.config_parameter"].set_param(
            "partner_google_reviews.google_places_api_key", None
        )
        with self.assertRaises(UserError):
            self.partner.update_google_reviews_info()
