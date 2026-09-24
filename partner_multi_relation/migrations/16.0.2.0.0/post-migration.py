# Copyright 2025 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging

from openupgradelib import openupgrade

logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    logger.info("Delete obsolete SQL views")
    env.cr.execute("DROP VIEW IF EXISTS res_partner_relation_all;")
    env.cr.execute("DROP VIEW IF EXISTS res_partner_relation_type_selection;")
