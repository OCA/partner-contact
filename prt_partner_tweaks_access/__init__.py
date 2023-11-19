# Copyright (C) 2023 Cetmix OÜ
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl)

from . import models

from odoo import api, SUPERUSER_ID
from .consts import PREDEFINED_RULES


# -- Restore access rules after module uninstalled
def restore_access_rules(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env["ir.rule"].set_predefined_rules_state(True)
