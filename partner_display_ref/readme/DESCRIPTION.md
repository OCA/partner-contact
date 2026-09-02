This module prefixes the customer reference (`res.partner.ref`) to a partner's
`display_name` whenever it is rendered inside an opted-in view — shown as
`[C00123] Acme Corp` in the dropdown, the selected value, and list cells alike.

The decoration is a generic mechanism: it activates only when a view injects
the `partner_display_ref_field` context key naming the field to prefix on a
`res.partner` field. Contacts, CRM,
Invoicing and any other view that does not opt in continue to see the plain
partner name. Companion modules (e.g. `sale_partner_display_ref`) wire this
mechanism into specific apps.
