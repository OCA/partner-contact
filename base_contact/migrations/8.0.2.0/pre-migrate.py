# -*- encoding: utf-8 -*-

# Odoo, Open Source Management Solution
# Copyright (C) 2014-2015  Grupo ESOC <www.grupoesoc.es>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


def migrate(cr, version):
    """Update fields owner module to avoid Odoo deleting them on uninstall."""
    # partner_contact_birthdate
    cr.execute("""UPDATE ir_model_data
                  SET module='partner_contact_birthdate'
                  WHERE module='base_contact'
                    AND name in ('field_res_partner_birthdate_date')""")

    # partner_contact_nationality
    cr.execute("""UPDATE ir_model_data
                  SET module='partner_contact_nationality'
                  WHERE module='base_contact'
                    AND name in ('field_res_partner_nationality_id')""")

    # partner_contact_in_several_companies
    cr.execute("""UPDATE ir_model_data
                  SET module='partner_contact_in_several_companies'
                  WHERE module='base_contact'
                    AND name LIKE 'field_%'""")
