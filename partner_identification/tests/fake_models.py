# Copyright 2017 LasLabs Inc.
# Copyright 2018 ACSONE
# Copyright 2018 Camptocamp
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


def setup_test_model(env, model_cls):
    """Pass a test model class and initialize it.

    Courtesy of SBidoul from https://github.com/OCA/mis-builder :)
    """
    model_cls._build_model(env.registry, env.cr)
    env.registry.setup_models(env.cr)
    env.registry.init_models(
        env.cr, [model_cls._name],
        dict(env.context, update_custom_fields=True)
    )


def teardown_test_model(env, model_cls):
    """Pass a test model class and deinitialize it.

    Courtesy of SBidoul from https://github.com/OCA/mis-builder :)
    """
    if not getattr(model_cls, '_teardown_no_delete', False):
        del env.registry.models[model_cls._name]
    env.registry.setup_models(env.cr)


class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'
    _teardown_no_delete = True

    social_security = fields.Char(
        compute=lambda s: s._compute_identification(
            'social_security', 'SSN',
        ),
        inverse=lambda s: s._inverse_identification(
            'social_security', 'SSN',
        ),
        search=lambda s, *a: s._search_identification(
            'SSN', *a
        ),
    )
