from odoo import models, fields
import logging
_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    """ Inherits partner, adds Gogocarto fields in the partner form, and functions"""
    _inherit = 'res.partner'

    in_gogocarto = fields.Boolean('In gogocarto')

    def _get_gogocarto_domain(self, company_id):
        # To OVERRIDE in sub_modules to customize the partner selection
        return [('in_gogocarto', '=', True)]

    def _get_gogocarto_parser(self, company_id):
        parser = []
        for field in self._get_export_fields(company_id):
            if field.ttype in [
                    "boolean",
                    "char",
                    "integer",
                    "monetary",
                    "text",
                    "selection",
                    "float",
                    "date_time",
                    "date"]:
                parser.append(field.name)
            elif field.ttype in ["many2one", "one2many", "many2many"]:
                parser.append((field.name, ['id', 'name']))
            elif field.ttype == "binary":
                continue
            elif field.ttype == "html":
                continue  # Not developped so far
            else:
                continue
        return parser

    def _get_export_fields(self, company_id):
        CompanySudo = self.env['res.company'].sudo().search([('id', '=', company_id)])
        default_fields = self.env['ir.model.fields'].sudo().search([
            ('model_id', '=', 'res.partner'),
            ('name', 'in', ['id', 'name', 'partner_longitude', 'partner_latitude'])])
        company_fields = CompanySudo.export_gogocarto_fields
        export_fields = default_fields | company_fields
        return export_fields
