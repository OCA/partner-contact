from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    env['res.partner.nuts']._parent_store_compute()
