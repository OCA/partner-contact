# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from lxml import etree
from odoo import api, models


class Base(models.AbstractModel):
    _inherit = 'base'

    @api.model
    def fields_view_get(self, *args, **kwargs):
        # OVERRIDE: display only confirmed partners on Many2one fields related
        # to ``res.partner`` on form views.
        res = super().fields_view_get(*args, **kwargs)
        if res["type"] == "form" and self._filter_only_confirmed():
            doc = etree.XML(res["arch"])
            for fname, fvalues in tuple(res["fields"].items()):
                ftype, frel = fvalues.get("type"), fvalues.get("relation")
                if (ftype, frel) != ("many2one", "res.partner"):
                    continue
                for node in doc.xpath("//field[@name='%s']" % fname):
                    domain = node.get("domain")
                    if not domain:
                        domain = "[('state', '=', 'confirmed')]"
                    elif isinstance(domain, str):
                        if domain in ("", "[]"):
                            domain = "[('state', '=', 'confirmed')]"
                        else:
                            domain = domain[:-1]
                            domain += ", ('state', '=', 'confirmed')]"
                    else:
                        domain = list(domain)
                        domain.append(('state', '=', 'confirmed'))
                        domain = str(domain)
                    node.set("domain", domain)
            res["arch"] = etree.tostring(doc)
        return res

    @api.model
    def _filter_only_confirmed(self) -> bool:
        """Determines whether only confirmed partners should be shown

        Retrieves condition based on context or system parameters (in this
        order).
        Else, defaults to True.
        """
        # Retrieve value from context (which can be defined in views field by
        # field)
        if "only_confirmed_partners" in self._context:
            return bool(self._context["only_confirmed_partners"])

        # Retrieve value from system parameters
        val = self.env["ir.config_parameter"].sudo().get_param(
            "partner_stage.only_confirmed_partners", default=None
        )
        if val is not None:
            return val not in ("False", "false", "", "0")

        # Return default value
        return True
