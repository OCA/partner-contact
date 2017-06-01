# -*- coding: utf-8 -*-
# Copyright 2009 Sharoon Thomas Open Labs Business Solutions
# Copyright 2014 Tecnativa Pedro M. Baeza
# Copyright 2015 Antiun Ingeniería S.L. - Jairo Llopis
# Copyright 2016 Sodexis
# Copyright 2017 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.addons.base_multi_image.hooks import pre_init_hook_for_submodules
from openerp.addons.base_multi_image.hooks import uninstall_hook_for_submodules


def pre_init_hook(cr):
    pre_init_hook_for_submodules(cr, "res.partner", "image")


def uninstall_hook(cr, registry):  # pragma: no cover
    uninstall_hook_for_submodules(cr, registry, "res.partner")
