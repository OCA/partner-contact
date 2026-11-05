To opt a view into the reference prefix, add the `partner_display_ref_field`
context key naming the `res.partner` field to prefix:

    <field name="partner_id" context="{'partner_display_ref_field': 'ref'}" />

Any `res.partner` field can be named (e.g. `ref`, `supplier_ref`). Set a value
on that field for a contact. In the opted-in view, the value is prefixed
wherever the partner is shown — the autocomplete dropdown, the selected value,
and list cells:

    [C00123] Acme Corp

Views that do not opt in keep the plain partner name, so reports and exports
stay clean. If the named field is not installed, no prefix is applied.
