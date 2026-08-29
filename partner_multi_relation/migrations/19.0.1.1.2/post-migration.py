# Copyright 2026 Vauxoo <https://www.vauxoo.com>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import logging

from openupgradelib import openupgrade

logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    """Clear this module's menus that still name an action 19.0 removed.

    ``menu_res_partner_relation`` has been a plain container since 18.0, but
    databases coming from older versions still carry the action it used to have,
    ``action_res_partner_relation_all``. A ``<menuitem>`` without an ``action``
    attribute emits no such field, and ``_load_records`` only writes the fields it
    is given, so that value is never rewritten: it sits there, valid but claimed by
    no data file, until something deletes what it points at.

    19.0 is what deletes it. The action targets ``res.partner.relation.all``, the
    SQL view ``migrations/19.0.1.0.0/pre-migration.py`` drops, so the record goes
    with the model. And ``ir_ui_menu.action`` is a reference column holding
    ``'<model>,<id>'`` as plain text, with no foreign key to cascade, so the menu
    keeps naming a record that no longer exists.

    The cost is out of proportion to the cause: ``/web/webclient/load_menus`` raises
    ``Record does not exist or has been deleted`` and answers 404, the webclient
    gets HTML where it expects JSON, and the backend renders blank for every user.

    Cleared rather than repointed, because guessing which action the menu meant is
    wrong exactly when it matters -- one that silently opens the wrong action is
    worse than one that opens nothing. The XML agrees: this menu is a container and
    its two children carry the actions.

    This runs post- and not pre-migration on purpose. The records are removed while
    this module's own data reloads, so a pre-migration would still find the action
    alive and nothing to clean.
    """
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE ir_ui_menu AS menu
           SET action = NULL
          FROM ir_model_data AS data
         WHERE data.model = 'ir.ui.menu'
           AND data.res_id = menu.id
           AND data.module = 'partner_multi_relation'
           AND menu.action LIKE 'ir.actions.act_window,%%'
           AND NOT EXISTS (
               SELECT 1
                 FROM ir_act_window AS action
                WHERE action.id = split_part(menu.action, ',', 2)::integer
           )
        """,
    )
