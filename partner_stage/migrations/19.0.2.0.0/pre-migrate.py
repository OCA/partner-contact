"""Reconcile the res_partner stage column name idempotently.

The stock module shipped a ``state`` column on res_partner (a stored
related of ``stage_id.state``). That name collides with
``account_move.state`` in Odoo Enterprise's VAT report SQL
(``account_reports._check_suite_common_vat_report``), which issues an
unqualified ``WHERE state = 'posted'`` against a JOIN of account_move and
res_partner -- Postgres then raises ``column reference "state" is
ambiguous`` and the tax return crashes. This module renames the field to
``stage_state`` (see ``models/res_partner.py``).

A simple ``RENAME state -> stage_state`` only heals a database where the
legacy column is the *only* one. If a database already created
``stage_state`` (e.g. it was reinstalled, or the field rename landed
before this migration), the legacy ``state`` column can linger *alongside*
``stage_state`` and keep the report ambiguous. This migration therefore
reconciles every possible state:

- only ``state`` exists       -> rename it to ``stage_state`` (keeps data)
- both columns exist          -> backfill gaps, then drop legacy ``state``
- only ``stage_state`` exists -> nothing to do
- neither exists              -> ORM schema sync creates ``stage_state``

res_partner has no native ``state`` column (the geographic state is
``state_id``), so dropping a stray ``state`` is safe.
"""

import logging

_logger = logging.getLogger(__name__)


def _stage_columns(cr):
    cr.execute(
        """
        SELECT column_name FROM information_schema.columns
        WHERE table_name = 'res_partner'
          AND column_name IN ('state', 'stage_state')
        """
    )
    return {row[0] for row in cr.fetchall()}


def migrate(cr, version):
    del version
    cols = _stage_columns(cr)
    if "stage_state" in cols and "state" in cols:
        cr.execute(
            "UPDATE res_partner SET stage_state = state "
            "WHERE stage_state IS NULL AND state IS NOT NULL"
        )
        cr.execute("ALTER TABLE res_partner DROP COLUMN state")
        _logger.info(
            "partner_stage: dropped stray legacy res_partner.state column; "
            "stage_state is now canonical."
        )
    elif "state" in cols:
        cr.execute("ALTER TABLE res_partner RENAME COLUMN state TO stage_state")
        _logger.info(
            "partner_stage: renamed res_partner.state -> res_partner.stage_state."
        )
    elif "stage_state" in cols:
        _logger.info("partner_stage: res_partner.stage_state already canonical.")
    else:
        _logger.info(
            "partner_stage: no stage column present; ORM will create stage_state."
        )
