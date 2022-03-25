# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class Skill(models.Model):
    _name = 'partner.skill'
    _description = "Skill"

    name = fields.Char(required=True)
    skill_type_id = fields.Many2one('partner.skill.type', ondelete='cascade')


class PartnerSkill(models.Model):
    _name = 'partner.skills'
    _description = "Skill level for an partner"
    _rec_name = 'skill_id'
    _order = "skill_level_id"

    partner_id = fields.Many2one('res.partner', required=True, ondelete='cascade')
    skill_id = fields.Many2one('partner.skill', required=True)
    skill_level_id = fields.Many2one('partner.skill.level', required=True)
    skill_type_id = fields.Many2one('partner.skill.type', required=True)
    level_progress = fields.Integer(related='skill_level_id.level_progress')

    _sql_constraints = [
        ('_unique_skill', 'unique (partner_id, skill_id)', "Two levels for the same skill is not allowed"),
    ]

    @api.constrains('skill_id', 'skill_type_id')
    def _check_skill_type(self):
        for record in self:
            if record.skill_id not in record.skill_type_id.skill_ids:
                raise ValidationError(_("The skill %(name)s and skill type %(type)s doesn't match", name=record.skill_id.name, type=record.skill_type_id.name))

    @api.constrains('skill_type_id', 'skill_level_id')
    def _check_skill_level(self):
        for record in self:
            if record.skill_level_id not in record.skill_type_id.skill_level_ids:
                raise ValidationError(_("The skill level %(level)s is not valid for skill type: %(type)s", level=record.skill_level_id.name, type=record.skill_type_id.name))


class SkillLevel(models.Model):
    _name = 'partner.skill.level'
    _description = "Skill Level"
    _order = "level_progress desc"

    skill_type_id = fields.Many2one('partner.skill.type', ondelete='cascade')
    name = fields.Char(required=True)
    level_progress = fields.Integer(string="Progress", help="Progress from zero knowledge (0%) to fully mastered (100%).")


class SkillType(models.Model):
    _name = 'partner.skill.type'
    _description = "Skill Type"

    name = fields.Char(required=True)
    skill_ids = fields.One2many('partner.skill', 'skill_type_id', string="Skills")
    skill_level_ids = fields.One2many('partner.skill.level', 'skill_type_id', string="Levels")
