# Copyright 2023 NathanQj
import json

import requests

from odoo import _, fields, models
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = "res.partner"

    google_reviews_search = fields.Char(
        string="Search Google Reviews for",
        help="If empty, will use the Contact's website."
        "For better results, use the URL of the company's website"
        "or the Company Name and City.",
    )
    google_reviews_result = fields.Char(
        string="Google Reviews Result",
        help="Name of the business found on Google Places",
        readonly=True,
    )
    google_rating = fields.Float(
        string="Google Rating",
        digits=(2, 1),
        help="Google rating out of 5",
        readonly=True,
    )
    google_reviews_number = fields.Integer(
        string="Number of Google Reviews", readonly=True
    )
    google_reviews_url = fields.Char(
        string="Google Reviews URL", help="URL to Google reviews", readonly=True
    )
    google_places_err = fields.Char(
        string="Google Places API Error",
        help="Error message from Google Places API",
        readonly=True,
    )

    def update_google_reviews_info(self):
        api_key = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("partner_google_reviews.google_places_api_key")
        )
        if not api_key:
            raise UserError(_("Google Places API key is missing in General Settings."))

        for contact in self:
            # Define the different search strings to be used
            contact_url = (
                contact.google_reviews_search or f"{contact.name}, {contact.city}"
                if contact.city
                else ""
            ) or contact.website

            # Define the parameters for the API call
            url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
            params = {
                "input": contact_url,
                "inputtype": "textquery",
                "fields": "place_id",
                "key": api_key,
            }

            # Call Google Places API to get the place ID and the reviews
            response = requests.get(url, params=params)
            result = json.loads(response.text)

            if not result["candidates"] or not result["status"] == "OK":
                contact.google_places_err = "No results found"
                continue

            else:
                place_id = result["candidates"][0]["place_id"]
                url = "https://maps.googleapis.com/maps/api/place/details/json"
                params = {
                    "place_id": place_id,
                    "fields": "name,rating,user_ratings_total",
                    "key": api_key,
                }
                response = requests.get(url, params=params)
                result = json.loads(response.text)
                if result["status"] == "OK":
                    # Handle case when the place has no rating
                    try:
                        rating = result["result"]["rating"]
                        ratings_total = result["result"]["user_ratings_total"]
                        err = False
                    except KeyError:
                        rating = ratings_total = 0
                        err = "No rating or number of reviews found"

                    # Write the results to the contact
                    contact.write(
                        {
                            "google_reviews_result": result["result"]["name"],
                            "google_reviews_url": "https://www.google.com/maps/place/"
                            "?q=place_id:%s" % place_id,
                            "google_rating": rating,
                            "google_reviews_number": ratings_total,
                            "google_places_err": err,
                        }
                    )
                else:
                    contact.google_places_err = (
                        "Google Places API Error: %s"
                        % result.get("error_message", "Missing information")
                    )
