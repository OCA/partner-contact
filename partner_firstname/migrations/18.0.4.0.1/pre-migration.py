import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    _logger.info(
        "Installing dependent module 'partner_type_base' "
        "by migration script for version %s.",
        version,
    )

    modules = ["partner_type_base"]

    cr.execute("SELECT state FROM ir_module_module WHERE name = %s", modules)
    mod_state = cr.fetchone()[0]
    if mod_state in ("installed", "to install", "to upgrade"):
        return

    cr.execute(
        "UPDATE ir_module_module SET state = 'to install' where name = %s", modules
    )

    states = dict(cr.fetchall())
    toinstall = [m for m in states if states[m] == "to install"]

    for module in toinstall:
        _logger.info("force install of module %r", module)
