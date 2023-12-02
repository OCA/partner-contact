# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from lxml import etree

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class Partner(models.Model):
    _name = "res.partner"
    _inherit = ["res.partner"]
    _order = "display_name_en ASC, id DESC"
    _rec_names_search = [
        "display_name_en",
        "email",
        "ref",
        "vat",
        "company_registry",
    ]  # TODO vat must be sanitized the same way for storing/searching

    def partner_name_translate(self, name):
        return name

    name = fields.Char(translate=True)
    street = fields.Char(translate=True)
    street2 = fields.Char(translate=True)
    city = fields.Char(translate=True)
    function = fields.Char(translate=True)
    display_name = fields.Char(
        compute="_compute_display_name_proxy",
        inverse="_inverse_display_name",
        search="_search_display_name",
        store=False,
    )
    display_name_en = fields.Char(
        compute="_compute_display_name_en", recursive=True, store=True, index="trigram"
    )
    company_name = fields.Char(translate=True)
    commercial_company_name = fields.Char(translate=True)

    display_lang = fields.Char(compute="_compute_display_lang")

    def _compute_display_name_proxy(self):
        display_lang = "display_name_en"
        lang_name = f'display_name_{self.env.user.lang.split("_")[0]}'
        for partner in self:
            if lang_name in self._fields:
                display_lang = lang_name
            partner.display_name = getattr(partner, display_lang)

    def _inverse_display_name(self):
        display_lang = "display_name_en"
        lang_name = f'display_name_{self.env.user.lang.split("_")[0]}'
        for partner in self:
            name = partner.display_name
            if lang_name in self._fields:
                display_lang = lang_name
                name = self.partner_name_translate(name)
            partner.display_name = setattr(partner, display_lang, name)

    def _search_display_name(self, operator, value):
        display_lang = "display_name_en"
        lang_name = f'display_name_{self.env.user.lang.split("_")[0]}'
        if lang_name in self._fields:
            display_lang = lang_name
        if operator == "like":
            operator = "ilike"
        return [(display_lang, operator, value)]

    @api.depends(
        "is_company",
        "name",
        "parent_id.display_name_en",
        "type",
        "company_name",
        "commercial_company_name",
    )
    def _compute_display_name_en(self):
        # retrieve name_get() without any fancy feature
        names = dict(self.with_context(**{"lang": "en_US"}).name_get())
        for partner in self:
            partner.display_name = names.get(partner.id)

    def _compute_display_lang(self):
        display_lang = "display_name_en"
        lang_name = f'display_name_{self.env.user.lang.split("_")[0]}'
        if lang_name in self._fields:
            display_lang = lang_name
        for partner in self:
            partner.display_lang = display_lang

    @api.model
    def get_view(self, view_id=None, view_type="form", **options):
        result = super(Partner, self).get_view(
            view_id=view_id, view_type=view_type, **options
        )
        lang_name = f'display_name_{self.env.user.lang.split("_")[0]}'
        if view_type in ["tree", "kanban"] and lang_name in self._fields:
            doc = etree.XML(result["arch"])
            for type_in in ["tree", "kanban"]:
                for node in doc.xpath(f"//{type_in}"):
                    node.set("default_order", lang_name)
            result["arch"] = etree.tostring(doc, encoding="unicode")
        return result

    def _force_address(self, vals):
        partner = self.with_context(**dict(self._context, lang="en_US"))
        lang_name = f'display_name_{self.env.user.lang.split("_")[0]}'
        if lang_name in self._fields:
            if vals.get("city") and partner.city != vals["city"]:
                partner.city = self.partner_name_translate(vals["city"])
            if vals.get("street") and partner.street != vals["street"]:
                partner.street = self.partner_name_translate(vals["street"])

    def _force_display_names(self, vals):
        ctx = {"lang": self.env.user.lang}
        partner = self.with_context(**ctx)
        p = partner.commercial_partner_id
        partner.commercial_company_name = (
            p.is_company and p.name or partner.company_name
        )
        lang_name = f'display_name_{self.env.user.lang.split("_")[0]}'
        if lang_name in self._fields:
            display_name_lang = vals.get(lang_name) or partner._get_name()
            setattr(partner, lang_name, display_name_lang)
        display_name_en = (
            vals.get("display_name_en")
            or partner.with_context(**dict(ctx, lang="en_US"))._get_name()
        )
        partner.display_name_en = display_name_en
        params = (
            display_name_en,
            partner.id,
        )
        # force backport compatible with display_name
        self.env.cr.execute(
            """UPDATE res_partner SET display_name = %s WHERE id = %s""", params
        )

    @api.model_create_multi
    def create(self, vals_list):
        lang_name = f'display_name_{self.env.user.lang.split("_")[0]}'
        for vals in vals_list:
            if lang_name in self._fields:
                vals[lang_name] = vals["name"]
                vals["name"] = self.partner_name_translate(vals["name"])
        partners = super(Partner, self).create(vals_list)
        for partner, vals in zip(partners, vals_list):
            if lang_name in self._fields:
                partner.name = vals[lang_name]
            if vals.get("name"):
                partner._force_display_names({})
            partner._force_address(vals)
        return partners

    def write(self, vals):
        res = super().write(vals)
        for partner in self:
            if vals.get("name"):
                partner._force_display_names({})
            if vals.get("street") or vals.get("city"):
                partner._force_address(vals)
        return res
