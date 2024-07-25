# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from . import models
from odoo import SUPERUSER_ID, api


def contact_type_post_init_hook(cr, registry):
    """
    This post-init-hook will update contact type
    """
    env = api.Environment(cr, SUPERUSER_ID, {})
    partners = env["res.partner"].search([])
    partners.with_context(no_vat_validation=True)._compute_type()


def contact_type_uninstall_hook(cr, registry):
    cr.execute("""
        UPDATE res_partner
        SET type = 'contact'
    """)
