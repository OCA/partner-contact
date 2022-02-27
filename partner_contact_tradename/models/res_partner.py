import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"

    tradename = fields.Char(
        size=300,
    )

    @api.model
    def name_search(self, name="", args=None, operator="ilike", limit=100):
        args = args or []
        try:
            recs = self.search(
                [
                    "|",
                    "|",
                    ("tradename", operator, name),
                    ("name", operator, name),
                    ("vat", operator, name),
                ]
                + args,
                limit=limit,
            )
        except Exception:
            _logger.debug("falling back to basic search")
            recs = self.search(
                ["|", ("tradename", operator, name), ("name", operator, name)] + args,
                limit=limit,
            )
        res = recs.name_get()

        # include names from super
        if limit:
            limit_rest = limit - len(recs)
        else:
            limit_rest = limit
        if limit_rest or not limit:
            args += [("id", "not in", recs.ids)]
            res += super().name_search(
                name, args=args, operator=operator, limit=limit_rest
            )
        return res
