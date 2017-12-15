# -*- coding: utf-8 -*-
# © 2017 senseFly, Amaris (Author: Quentin Theuret)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


def migrate(cr, version):
    continents = [
        ('af', 'AF'),
        ('an', 'AN'),
        ('as', 'AS'),
        ('eu', 'EU'),
        ('na', 'NA'),
        ('oc', 'OC'),
        ('sa', 'SA'),
    ]

    for xml_id, code in continents:
        cr.execute("""
        UPDATE res_continent SET code = %(code)s WHERE id = (
            SELECT res_id
                FROM ir_model_data
                WHERE model = 'res.continent' AND name = %(xml_id)s
        );""", {'code': code, 'xml_id': xml_id})
