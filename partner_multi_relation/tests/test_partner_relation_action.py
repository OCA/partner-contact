# © 2021 Tobias Zehntner
# © 2021 Niboo SRL (https://www.niboo.com/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from odoo import exceptions

from .test_partner_relation_common import TestPartnerRelationCommon


class TestPartnerRelationAction(TestPartnerRelationCommon):
    def setUp(self):
        super().setUp()
        self.user = self.env["res.users"].create(
            {
                "login": "test_partner_action_user",
                "name": "test_partner_action_user",
                "groups_id": [
                    (4, self.env.ref("base.group_user").id),
                ],
            }
        )

    def test_call_relation_action(self):
        """Test calling relations action. Should be possible with simple user rights"""
        try:
            self.partner_01_person.with_user(self.user).action_view_relations()
        except exceptions.AccessError:
            self.fail("action_view_relations() raised AccessError unexpectedly!")
