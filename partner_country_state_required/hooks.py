# Copyright 2023 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

import logging

_logger = logging.getLogger(__name__)


def post_init_hook(cr, registry):
    """Set state_required to True"""
    _logger.info("Setting state_required to True for all countries.")
    query = """
        UPDATE res_country
        SET state_required = TRUE;
    """
    cr.execute(query)
    _logger.info(f"{cr.rowcount} rows updated in res_country")
