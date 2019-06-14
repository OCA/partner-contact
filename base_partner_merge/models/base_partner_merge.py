# -*- coding: utf-8 -*-
# © 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp.addons.crm.base_partner_merge import *  # noqa


class NoCRMResPartner(ResPartner):  # noqa
    _module = 'base_partner_merge'


class NoCRMMergePartnerLine(MergePartnerLine):  # noqa
    _module = 'base_partner_merge'


class NoCRMMergePartnerAutomatic(MergePartnerAutomatic):  # noqa
    _module = 'base_partner_merge'
