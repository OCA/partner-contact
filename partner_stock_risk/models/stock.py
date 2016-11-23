# -*- coding: utf-8 -*-
# © 2016 Carlos Dauden <carlos.dauden@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import _, api, exceptions, models


class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.multi
    def action_done(self):
        if not self.env.context.get('bypass_risk', False):
            moves = self.filtered(lambda x: (
                x.location_dest_id.usage == 'customer' and
                x.partner_id.risk_exception
            ))
            if moves:
                raise exceptions.UserError(
                    "Financial risk exceeded in partners:\n"
                    "%s" % moves.mapped('partner_id.name'))
        return super(StockMove, self).action_done()


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def action_confirm(self):
        if not self.env.context.get('bypass_risk', False):
            if (self.location_dest_id.usage == 'customer' and
                    self.partner_id.risk_exception):
                exception_msg = _("Financial risk exceeded \n")
                return self.env['partner.risk.exceeded.wiz'].create({
                    'exception_msg': exception_msg,
                    'partner_id': self.partner_id.id,
                    'origin_reference': '%s,%s' % (self._model, self.id),
                    'continue_method': 'action_confirm',
                }).action_show()
        return super(StockPicking, self).action_confirm()

    @api.multi
    def action_assign(self):
        if not self.env.context.get('bypass_risk', False) and any(
                self.mapped('partner_id.risk_exception')):
            exception_msg = _("Financial risk exceeded \n")
            params = self.env.context.get('params', {})
            if 'purchase.order' not in params and 'sale.order' not in params:
                return self.env['partner.risk.exceeded.wiz'].create({
                    'exception_msg': exception_msg,
                    'partner_id': self.mapped('partner_id')[:1].id,
                    'origin_reference': '%s,%s' % (self._model, self.id),
                    'continue_method': 'action_assign',
                }).action_show()
        return super(StockPicking, self).action_assign()

    @api.multi
    def force_assign(self):
        if not self.env.context.get('bypass_risk', False):
            if (self.location_dest_id.usage == 'customer' and
                    self.partner_id.risk_exception):
                exception_msg = _("Financial risk exceeded \n")
                return self.env['partner.risk.exceeded.wiz'].create({
                    'exception_msg': exception_msg,
                    'partner_id': self.partner_id.id,
                    'origin_reference': '%s,%s' % (self._model, self.id),
                    'continue_method': 'force_assign',
                }).action_show()
        return super(StockPicking, self).force_assign()

    @api.multi
    def do_new_transfer(self):
        if not self.env.context.get('bypass_risk', False):
            if (self.location_dest_id.usage == 'customer' and
                    self.partner_id.risk_exception):
                exception_msg = _("Financial risk exceeded \n")
                return self.env['partner.risk.exceeded.wiz'].create({
                    'exception_msg': exception_msg,
                    'partner_id': self.partner_id.id,
                    'origin_reference': '%s,%s' % (self._model, self.id),
                    'continue_method': 'do_new_transfer',
                }).action_show()
        return super(StockPicking, self).do_new_transfer()
