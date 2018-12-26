from odoo import api, fields, models, _


class ResPartner(models.Model):
    _inherit = "res.partner"

    legal_name = fields.Char()

    @api.onchange('name')
    def onchange_legal_name(self):
        if self.legal_name == '':
            self.legal_name = self.name

    @api.multi
    def name_get(self):
        res = []
        for partner in self:
            name_legal = partner._get_name()
            res.append((partner.id, name_legal))
        return res

    def _get_name(self):
        partner = self
        name = partner.legal_name or ''

        if partner.company_name or partner.parent_id:
            if not name and partner.type in ['invoice', 'delivery', 'other']:
                name = \
                    dict(self.fields_get(['type'])['type']
                         ['selection'])[partner.type]
            if not partner.is_company:
                name = \
                    "%s, %s" % (partner.commercial_company_name or
                                partner.parent_id.legal_name, name)
        if self._context.get('show_address_only'):
            name = partner._display_address(without_company=True)
        if self._context.get('show_address'):
            name = name + "\n" + partner._display_address(without_company=True)
        name = name.replace('\n\n', '\n')
        name = name.replace('\n\n', '\n')
        if self._context.get('address_inline'):
            name = name.replace('\n', ', ')
        if self._context.get('show_email') and partner.email:
            name = "%s <%s>" % (name, partner.email)
        if self._context.get('html_format'):
            name = name.replace('\n', '<br/>')
        if self._context.get('show_vat') and partner.vat:
            name = "%s - %s" % (name, partner.vat)
        return name

    @api.depends('is_company', 'legal_name', 'parent_id.name',
                 'type', 'company_name')
    def _compute_display_name(self):
        for partner in self:
            partner.display_name = partner.legal_name
