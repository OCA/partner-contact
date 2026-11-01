# Copyright 2026 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging

from openupgradelib import openupgrade

logger = logging.getLogger(__name__)


STATEMENT = """\
DELETE FROM ir_ui_view
 WHERE id IN (
     SELECT id FROM ir_ui_view WHERE inherit_id IN (
        SELECT id FROM ir_ui_view WHERE model = 'res.partner.relation.all'
     )
);
"""


@openupgrade.migrate()
def migrate(env, version):
    logger.info("Delete from ir.ui.view, to make sure dropping views succeeds.")
    env.cr.execute(STATEMENT)
