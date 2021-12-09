# Copyright 2021 Open Source Integrators
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    stages = env["res.partner.stage"].search([])
    for stage in stages:
        _logger.info(
            "Migrating old state %s to stage_id %s...", stage.state, stage.name
        )
        cr.execute(
            """
            UPDATE res_partner
            SET stage_id = %(id)s, state = old_state
            WHERE old_state = %(state)s
            """,
            {"id": stage.id, "state": stage.state},
        )
