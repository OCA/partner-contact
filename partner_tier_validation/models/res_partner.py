# Copyright 2019 Open Source Integrators
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ResPartner(models.Model):
    _name = "res.partner"
    _inherit = ['res.partner', 'tier.validation']
    _state_from = ['new', 'to approve']
    _state_to = ['approved']

    # override core odoo to set default value to False
    customer = fields.Boolean(string='Is a Customer', default=False,
                               help="Check this box if this contact is a customer. It can be selected in sales orders.")

    state = fields.Selection(selection=[('new','New'),
                                        ('approved','Approved'),],
                             string='Status',
                             default='new' )
