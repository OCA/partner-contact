# Copyright 2021 Tobias Zehntner.
# Copyright 2021 Niboo SRL <https://www.niboo.com>.
# Copyright 2025 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from .test_partner_relation_common import TestPartnerRelationCommon


class TestPartnerRelationAction(TestPartnerRelationCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = cls.env["res.users"].create(
            {
                "login": "test_partner_action_user",
                "name": "test_partner_action_user",
                "group_ids": [
                    (4, cls.env.ref("base.group_user").id),
                ],
            }
        )

    def test_call_relation_action(self):
        """Test calling relations action. Should be possible with simple user rights"""
        self.partner_01_person.with_user(self.user).action_view_relations()
