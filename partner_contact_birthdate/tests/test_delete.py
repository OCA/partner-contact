# -*- coding: utf-8 -*-
# © 2015 Grupo ESOC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class CompanyCase(TransactionCase):
    model = "res.partner"
    context = {"default_is_company": True}

    def test_computing_after_unlink(self):
        """Test what happens if recomputed after unlinking.

        This test might seem useless, but really this happens when module
        ``partner_relations`` is installed.

        See https://github.com/OCA/partner-contact/issues/154.
        """
        data = {"name": u"Söme name", "birthdate": "2015-09-28"}
        record = self.env[self.model].with_context(**self.context).create(data)
        record.unlink()
        record.recompute()


class PersonCase(CompanyCase):
    context = {"default_is_company": False}
