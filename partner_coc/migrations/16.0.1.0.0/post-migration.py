# Copyright 2023 Therp <https://therp.nl/>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    # Model `res.partner.id_category` doesn't exist anymore, so we can't use `env.ref`
    openupgrade.logged_query(
        env.cr,
        """
        SELECT res_id FROM ir_model_data
        WHERE module = 'partner_coc' AND name = 'id_category_coc'
    """,
    )
    coc_category_id = env.cr.fetchone()[0]
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE res_partner rp SET company_registry = r.name
        FROM (
            SELECT partner_id, name FROM res_partner_id_number
            WHERE category_id = %i
        ) AS r
        WHERE rp.id = r.partner_id
    """
        % coc_category_id,
    )
