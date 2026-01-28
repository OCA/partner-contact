# Copyright 2016-2018 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


def has_module_partner_title(env):
    return (
        env["ir.module.module"]
        .sudo()
        .search_count([("name", "=", "partner_title"), ("state", "=", "installed")])
        > 0
    )


def post_init_hook(env):
    # This hook checks the title of the partner and if set,
    # sets gender accordingly.
    # The *Title* field on partners was native up to Odoo 18.0
    # and was dropped in 19.0.
    # The OCA module OCA/partner-contact/partner_title reintroduced this field.
    # If this module is installed, the hook is still executed,
    # otherwise skipped.

    if not has_module_partner_title(env):
        return

    gender_mappings = {
        "female": env.ref("partner_title.res_partner_title_madam")
        + env.ref("partner_title.res_partner_title_miss"),
        "male": env.ref("partner_title.res_partner_title_mister"),
    }
    for gender, titles in list(gender_mappings.items()):
        env["res.partner"].with_context(active_test=False).search(
            [("title_id", "in", titles.ids)]
        ).write({"gender": gender})
