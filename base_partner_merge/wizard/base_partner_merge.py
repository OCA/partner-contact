# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# Copyright 2017 Jarsa Sistemas
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.addons.crm.wizard.base_partner_merge import *  # noqa


class NoCRMMergePartnerLine(MergePartnerLine):  # noqa
    _module = 'base_partner_merge'


class NoCRMMergePartnerAutomatic(MergePartnerAutomatic):  # noqa
    _module = 'base_partner_merge'
