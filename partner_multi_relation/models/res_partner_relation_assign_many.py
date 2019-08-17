
from odoo import api, fields, models, _
from odoo.exceptions import UserError


import logging
_logger = logging.getLogger(__name__)

class ResPartnerRelationAssignMany(models.TransientModel):
    _name = 'res.partner.relation.assign.many'
    _description = 'Assign Relation to Many Partners'

    right_partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Destination Partner',
        required=True,
        auto_join=True,
        ondelete='cascade',
    )
    type_id = fields.Many2one(
        comodel_name='res.partner.relation.type',
        string='Type',
        required=True,
        auto_join=True,
    )
    date_start = fields.Date('Starting date')
    date_end = fields.Date('Ending date')

    @api.multi
    def assign_many(self):
        partner_ids = self.env.context['active_ids']
        relation = self.env['res.partner.relation']

        for id in partner_ids:
            relation.create({'left_partner_id': id,
            'right_partner_id': self.right_partner_id.id,
            'type_id': self.type_id.id,
            'date_start':self.date_start,
            'date_end' : self.date_end
            })

        return {'type': 'ir.actions.act_window_close'}

            

        