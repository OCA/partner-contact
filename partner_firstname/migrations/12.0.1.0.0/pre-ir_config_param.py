def store_ir_config_param(cr):
    """Prior to version 12.0 the default order of partner
    names was last_first.  In order to retain this behaviour we
    store the config parameter if it is not present.
    """
    cr.execute("SELECT 1 FROM ir_config_parameter "
               "WHERE key = 'partner_names_order'")
    if not cr.fetchone():
        cr.execute("INSERT INTO ir_config_parameter (key, value) VALUES "
                   "('partner_names_order', 'last_first')")


def migrate(cr, version):
    store_ir_config_param(cr)
