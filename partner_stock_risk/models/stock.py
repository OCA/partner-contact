# -*- coding: utf-8 -*-
# Copyright 2016 Carlos Dauden <carlos.dauden@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, exceptions, models


class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.multi
    def action_done(self):
        if not self.env.context.get('bypass_risk'):
            moves = self.filtered(lambda x: (
                x.location_dest_id.usage == 'customer' and
                x.partner_id.risk_exception
            ))
            if moves:
                raise exceptions.UserError(
                    _("Financial risk exceeded in partner:\n%s") %
                    moves.mapped('partner_id.name'))
        return super(StockMove, self).action_done()


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def show_risk_wizard(self, continue_method):
        return self.env['partner.risk.exceeded.wiz'].create({
            'exception_msg': _("Financial risk exceeded \n"),
            'partner_id': self.partner_id.id,
            'origin_reference': '%s,%s' % (self._name, self.id),
            'continue_method': continue_method,
        }).action_show()

    @api.multi
    def action_confirm(self):
        if not self.env.context.get('bypass_risk'):
            if (self.location_dest_id.usage == 'customer' and
                    self.partner_id.risk_exception):
                return self.show_risk_wizard('action_confirm')
        return super(StockPicking, self).action_confirm()

    @api.multi
    def action_assign(self):
        if not self.env.context.get('bypass_risk') and \
                self.filtered('partner_id.risk_exception'):
            params = self.env.context.get('params', {})
            if 'purchase.order' not in params and 'sale.order' not in params:
                return self.show_risk_wizard('action_assign')
        return super(StockPicking, self).action_assign()

    @api.multi
    def force_assign(self):
        if not self.env.context.get('bypass_risk'):
            if (self.location_dest_id.usage == 'customer' and
                    self.partner_id.risk_exception):
                return self.show_risk_wizard('force_assign')
        return super(StockPicking, self).force_assign()

    @api.multi
    def do_new_transfer(self):
        if not self.env.context.get('bypass_risk'):
            if (self.location_dest_id.usage == 'customer' and
                    self.partner_id.risk_exception):
                return self.show_risk_wizard('do_new_transfer')
        return super(StockPicking, self).do_new_transfer()
