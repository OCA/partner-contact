# Copyright 2026 Therp BV <http://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import logging

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)


def uninstall_hook(cr, registry):  # pragma: no cover
    env = api.Environment(cr, SUPERUSER_ID, {})
    # Check whether partner_multi_relation_contact installed.
    pmr_contact = env["ir.module.module"].search(
        [
            ("name", "=", "partner_multi_relation_contact"),
        ]
    )
    if not pmr_contact:
        _logger.info(
            "partner_multi_relation_contact not installed."
            " Function information will be lost"
        )
        return
    # Find relations with function and create or update contact for them.
    Relation = env["res.partner.relation"]
    Partner = env["res.partner"]
    function_relations = Relation.search([("contact_function", "!=", False)])
    create_count = 0
    update_count = 0
    for relation in function_relations:
        relation.type_id.allow_function = True
        relation.type_id.allow_contact_partner = True
        if relation.contact_partner_id:
            if relation.contact_partner_id.function:
                continue  # Already migrated or more up to date value.
            relation.contact_partner_id.function = relation.contact_function
            update_count += 1
        else:
            context = relation._get_contact_creation_context()
            vals = Partner.with_context(**context).default_get(
                fields_list=Partner._fields
            )
            vals["function"] = relation.contact_function
            contact = Partner.create(vals)
            relation.contact_partner_id = contact
            create_count += 1
    _logger.info(
        "Created %(create_count)s, updated %(update_count)s contact partners",
        dict(create_count=create_count, update_count=update_count),
    )
