# Copyright 2026 Bosd
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import importlib.util
from pathlib import Path

from odoo.tests.common import TransactionCase


def _load_pre_migrate():
    """Load the 19.0.2.0.0 pre-migrate module by path (migrations are not a
    package)."""
    path = (
        Path(__file__).resolve().parent.parent
        / "migrations"
        / "19.0.2.0.0"
        / "pre-migrate.py"
    )
    spec = importlib.util.spec_from_file_location("partner_stage_pre_migrate", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestPartnerStageMigration(TransactionCase):
    """Exercise the idempotent res_partner stage-column reconciliation.

    The schema changes (ALTER TABLE) run inside the test transaction and are
    rolled back on teardown (Postgres has transactional DDL).
    """

    def setUp(self):
        super().setUp()
        self.migration = _load_pre_migrate()
        self.cr = self.env.cr

    def _columns(self):
        return self.migration._stage_columns(self.cr)

    def test_noop_when_only_stage_state(self):
        """Fork already applied: only stage_state exists -> migration no-ops."""
        self.assertEqual(self._columns(), {"stage_state"})
        self.migration.migrate(self.cr, None)
        self.assertEqual(self._columns(), {"stage_state"})

    def test_rename_when_only_legacy_state(self):
        """Legacy DB: only `state` exists -> renamed to stage_state."""
        self.cr.execute("ALTER TABLE res_partner RENAME COLUMN stage_state TO state")
        self.assertEqual(self._columns(), {"state"})
        self.migration.migrate(self.cr, None)
        self.assertEqual(self._columns(), {"stage_state"})

    def test_drop_legacy_when_both_columns_exist(self):
        """Drifted DB: both columns exist -> stray `state` is dropped."""
        self.cr.execute("ALTER TABLE res_partner ADD COLUMN state varchar")
        self.assertEqual(self._columns(), {"state", "stage_state"})
        self.migration.migrate(self.cr, None)
        self.assertEqual(self._columns(), {"stage_state"})
