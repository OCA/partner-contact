import logging
from odoo import fields, models


_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    export_gogocarto_fields = fields.Many2many(
        related='company_id.export_gogocarto_fields',
        relation='ir.model.fields',
        string='GogoCarto Exported fields',
        readonly=False,
        domain=[
            ('model_id', '=', 'res.partner'),
            ('name', 'not in', ['name',
                                'partner_longitude',
                                'partner_latitude',
                                'id'])
        ]
    )
