# Copyright 2023 ForgeFlow S.L. <http://www.forgeflow.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tools import drop_constraint


def migrate(cr, version):

    drop_constraint(
        cr, "res_partner_company_type", "res_partner_company_type_name_uniq"
    )
