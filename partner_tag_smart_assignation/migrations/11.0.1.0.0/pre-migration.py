from openupgradelib import openupgrade


def migrate(cr, version):
    if not version:
        return
    openupgrade.update_module_names(cr, [
        ('smart_tagger', 'partner_tag_smart_assignation')])
