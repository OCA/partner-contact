# -*- coding: utf-8 -*-
# © 2017 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import inspect
from openerp.models import MetaModel


def post_load_hook():
    """We try to be smart here: If the crm module is to be loaded too
    (or is already loaded), we remove our own models again in order not to
    clash with the CRM ones: https://github.com/OCA/partner-contact/issues/283
    """
    for frame, filename, lineno, funcname, line, index in inspect.stack():
        # walk up the stack until we're in load_module_graph
        if 'graph' in frame.f_locals:
            graph = frame.f_locals['graph']
            package = frame.f_locals['package']
            if any(p.name == 'crm' for p in graph):
                # so crm is installed, then we need to remove your model
                # from the list of models to be registered
                # TODO: this could be smarter and only ditch models that need
                # to be ditched (if crm is in their mro)
                MetaModel.module_to_models['base_partner_merge'] = []
                # and in this case, we also don't want to load our xml files
                package.data['data'].remove('views/base_partner_merge.xml')
            break
