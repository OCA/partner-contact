# Copyright 2026 Moduon Team S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

from odoo.exceptions import AccessError
from odoo.tests import new_test_user
from odoo.tests.common import TransactionCase, users


class TestProjectTaskSecurity(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project_user_a = new_test_user(
            cls.env,
            login="task_log_project_user_a",
            groups="base.group_user,project.group_project_user",
        )
        cls.project_user_b = new_test_user(
            cls.env,
            login="task_log_project_user_b",
            groups="base.group_user,project.group_project_user",
        )
        cls.internal_user = new_test_user(
            cls.env,
            login="task_log_internal_user",
            groups="base.group_user",
        )
        cls.partner = cls.env["res.partner"].create({"name": "Task Log Partner"})
        cls.task_log = cls.env["project.task"].create(
            {
                "name": "Partner log entry",
                "active": False,
                "partner_id": cls.partner.id,
                "user_ids": [(6, 0, cls.project_user_a.ids)],
            }
        )
        cls.private_task = cls.env["project.task"].create(
            {
                "name": "Private task",
                "user_ids": [(6, 0, cls.project_user_a.ids)],
            }
        )

    @users("task_log_project_user_b")
    def test_project_user_can_access_other_user_task_log(self):
        self.task_log.with_user(self.env.user).read(["name"])
        self.task_log.with_user(self.env.user).write({"name": "Updated log entry"})
        self.task_log.with_user(self.env.user).unlink()

    @users("task_log_project_user_b")
    def test_project_user_can_create_task_log(self):
        task = self.env["project.task"].create(
            {
                "name": "New partner log entry",
                "active": False,
                "partner_id": self.partner.id,
            }
        )
        self.assertFalse(task.active)
        self.assertFalse(task.project_id)
        self.assertFalse(task.parent_id)
        self.assertEqual(task.partner_id, self.partner)

    @users("task_log_project_user_b")
    def test_project_user_cannot_access_other_user_private_task(self):
        with self.assertRaises(AccessError):
            self.private_task.with_user(self.env.user).read(["name"])
        with self.assertRaises(AccessError):
            self.private_task.with_user(self.env.user).write(
                {"name": "Updated private"}
            )
        with self.assertRaises(AccessError):
            self.private_task.with_user(self.env.user).unlink()

    @users("task_log_internal_user")
    def test_internal_user_cannot_manage_task_logs(self):
        with self.assertRaises(AccessError):
            self.task_log.with_user(self.env.user).read(["name"])
        with self.assertRaises(AccessError):
            self.task_log.with_user(self.env.user).write({"name": "Updated log entry"})
        with self.assertRaises(AccessError):
            self.task_log.with_user(self.env.user).unlink()

    def test_partner_task_log_action(self):
        action = self.partner.action_view_task_log()
        self.assertIn(("active", "=", False), action["domain"])
        self.assertFalse(action["context"]["active_test"])
        self.assertFalse(action["context"]["default_active"])

    def test_partner_task_log_count(self):
        self.env["project.task"].create(
            {
                "name": "Active partner task",
                "partner_id": self.partner.id,
                "user_ids": [(6, 0, self.project_user_a.ids)],
            }
        )
        self.assertEqual(self.partner.task_log_count, 1)
