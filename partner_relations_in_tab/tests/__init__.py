# -*- coding: utf-8 -*-
# Copyright 2017-2018 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from . import common
from . import test_tab
from . import test_res_partner_relation_type
from . import test_res_partner
from . import test_res_partner_relation

checks = [
    test_tab,
    test_res_partner_relation_type,
    test_res_partner,
    test_res_partner_relation,
]
