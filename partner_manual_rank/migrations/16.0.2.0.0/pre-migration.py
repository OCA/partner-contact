# Copyright (C) 2026 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

# pylint: disable=odoo-addons-relative-import
from odoo.addons.partner_manual_rank.hooks import pre_init_hook


def migrate(cr, version):
    pre_init_hook(cr)
