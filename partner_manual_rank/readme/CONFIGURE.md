This module introduces a System Parameter ``partner_manual_rank.partner_rank_auto``
to enable or disable Odoo’s automatic updates of ``res.partner::customer_rank`` and ``res.partner::supplier_rank``.

When disabled, Odoo will not auto-increment these ranks during business flows (e.g., posting invoices/bills, placing orders).
You remain free to set or adjust ranks manually.

To enable/disable:

Go to Settings → Contacts (or search for "rank" in Settings).
Find "Automatically rank partners as customers or suppliers".
Security: Only users in Settings / Administration (group base.group_system) may change it.
