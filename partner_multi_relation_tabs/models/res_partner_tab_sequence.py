# Copyright 2021 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
# pylint: disable=invalid-name,protected-access
"""
This model is used to keep track of the modifications to tab definitions.

Each time a record is created, updated or deleted in res_partner_tab, the sequence
should be incremented. Workers can use this to check wether their tab definitions
are up to date, and if not, update the new definitions.

For the model defined here _auto is set to False to prevent creating a
database file. The model is based on a SQL sequence.
"""
from odoo import api, fields, models
from odoo.tools import ormcache


class ResPartnerTabSequence(models.AbstractModel):
    """Check for modifications to res.partner.tab model."""

    _name = "res.partner.tab.sequence"
    _description = "Track res.partner.tab modifications"
    _auto = True  # Call _auto_init, despite this being an abstract model

    last_value = fields.Integer()

    @api.model
    def _auto_init(self):
        """Create sequence when module installed."""
        cr = self.env.cr
        cr.execute(
            "CREATE SEQUENCE IF NOT EXISTS res_partner_tab_modification"
            " INCREMENT BY 1 START WITH 1 CYCLE"
        )
        cr.execute(
            "CREATE OR REPLACE VIEW res_partner_tab_sequence"
            " AS(SELECT 1 AS id, last_value FROM res_partner_tab_modification)"
        )

    @api.model
    def increment_sequence(self):
        """Set sequence, creating sequence object if needed."""
        cr = self.env.cr
        cr.execute("SELECT nextval('res_partner_tab_modification')")
        self.env.registry._clear_cache()

    @api.model
    @ormcache()
    def get_sequence(self):
        """Get last sequence for res_partner_tab_sequence."""
        cr = self.env.cr
        cr.execute("SELECT last_value FROM res_partner_tab_sequence")
        return cr.fetchone()[0]
