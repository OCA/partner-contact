# -*- coding: utf-8 -*-
# © 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp.addons.crm.base_partner_merge import *  # noqa


class NoCRMResPartner(ResPartner):
    _module = 'base_partner_merge'


class NoCRMMergePartnerLine(MergePartnerLine):
    _module = 'base_partner_merge'


class NoCRMMergePartnerAutomatic(MergePartnerAutomatic):
    _module = 'base_partner_merge'
