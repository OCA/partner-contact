import logging

from odoo.upgrade import util

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    _logger.info(
        "Installing dependent module 'partner_type_base' "
        "by migration script for version %s.",
        version,
    )
    util.force_install_module(cr, "partner_type_base")
