# Copyright 2026 Vauxoo <https://www.vauxoo.com>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tests.common import TransactionCase


class TestMenuAction(TransactionCase):
    def test_menu_actions_resolve(self):
        """Every menu this module owns must name an action that exists.

        ``ir_ui_menu.action`` is a reference column holding ``'<model>,<id>'`` as
                plain text, so nothing in the database stops a menu from outliving the action
                it names. One that does is enough to make ``load_menus`` answer 404 and leave
                the whole backend blank, so a stale reference has to fail here, not in a
                browser.
        """
        self.env.cr.execute(
            """
            SELECT data.module || '.' || data.name, menu.action
              FROM ir_ui_menu AS menu
              JOIN ir_model_data AS data
                ON data.model = 'ir.ui.menu' AND data.res_id = menu.id
             WHERE data.module = 'partner_multi_relation'
               AND menu.action IS NOT NULL
               AND menu.action <> ''
            """
        )
        dangling = []
        for xmlid, reference in self.env.cr.fetchall():
            model, _, res_id = reference.partition(",")
            if not self.env[model].browse(int(res_id)).exists():
                dangling.append(f"{xmlid} -> {reference}")
        self.assertFalse(
            dangling,
            f"Menu(s) naming an action that does not exist: {', '.join(dangling)}",
        )
