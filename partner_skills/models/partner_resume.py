# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class Partner(models.Model):
    _inherit = 'res.partner'

    resume_line_ids = fields.One2many('partner.resume.line', 'partner_id', string="Resumé lines")
    partner_skill_ids = fields.One2many('partner.skills', 'partner_id', string="Skills")

    @api.model_create_multi
    def create(self, vals_list):
        res = super(Partner, self).create(vals_list)
        resume_lines_values = []
        for partner in res:
            line_type = self.env.ref('partner_skills.resume_type_experience', raise_if_not_found=False)
            resume_lines_values.append({
                'partner_id': partner.id,
                'name': partner.company_id.name or '',
                'date_start': partner.create_date.date(),
                'description': partner.job_title or '',
                'line_type_id': line_type and line_type.id,
            })
        self.env['partner.resume.line'].create(resume_lines_values)
        return res


class PartnerPublic(models.Model):
    _inherit = 'res.partner'

    resume_line_ids = fields.One2many('partner.resume.line', 'partner_id', string="Resumé lines")
    partner_skill_ids = fields.One2many('partner.skills', 'partner_id', string="Skills")


class ResumeLine(models.Model):
    _name = 'partner.resume.line'
    _description = "Resumé line of an Partner"
    _order = "line_type_id, date_end desc, date_start desc"

    partner_id = fields.Many2one('res.partner', required=True, ondelete='cascade')
    name = fields.Char(required=True)
    date_start = fields.Date(required=True)
    date_end = fields.Date()
    description = fields.Text(string="Description")
    line_type_id = fields.Many2one('partner.resume.line.type', string="Type")

    # Used to apply specific template on a line
    display_type = fields.Selection([('classic', 'Classic'),('certification', 'Certification'),('course', 'Course')], string="Display Type", default='classic')

    _sql_constraints = [
        ('date_check', "CHECK ((date_start <= date_end OR date_end = NULL))", "The start date must be anterior to the end date."),
    ]


class ResumeLineType(models.Model):
    _name = 'partner.resume.line.type'
    _description = "Type of a resumé line"
    _order = "sequence"

    name = fields.Char(required=True)
    sequence = fields.Integer('Sequence', default=10)
