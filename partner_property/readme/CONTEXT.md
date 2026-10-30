Odoo 19.0 introduced a single global `properties` field on
`res.partner` via the `properties.base.definition.mixin`. With core
alone, every partner record — whether an individual or a company —
draws from one shared definition list defined per
`res.partner.category` or similar parent context.

This module remains relevant on 19.0 because it provides two
capabilities the core mixin doesn't:

## 1. Person/Company type split

`res.partner` records carry an `is_company` flag that distinguishes
companies from individuals. The two record subtypes typically need
different property schemas — companies care about VAT registration,
industry classification, ownership structure; individuals care about
preferred contact channel, language, GDPR-consent state, marketing
opt-ins, role within their company.

This module exposes **two separate `Properties` fields** on
`res.partner` — `properties_type_company` and
`properties_type_person` — with independent definition schemas. The
form view shows the right one based on `is_company`. Without this
module, a multi-purpose property like "VAT exempt reason" applied to
companies would also appear (uselessly) on every individual record,
and a property like "preferred pronouns" would appear on every
company record.

## 2. Per-company definition keying

The two property definition schemas live on `res.company`
(`partner_properties_definition_company` and
`partner_properties_definition_person`), not on a global
`ir.config_parameter`. In a multi-company tenant, each company can
define its own set of partner properties without leaking schema
changes across sibling companies.

The form view resolves the active definition off `env.company` at
render time, so a user switching companies sees the property schema
that company has configured. Without this module, the core
`properties` field falls back to a single schema for the whole
database.

**Configuration today:** the definition fields exist on `res.company`
at the model layer but the stock company form view does not surface
them. Definitions are configured via Developer mode (Settings →
Technical → Models → Companies → field debug) or programmatically
(XML-RPC / data files). Wiring a UI section on the company form is a
reasonable follow-up `[IMP]`.

## When to install this module

- You distinguish between company-typed and individual-typed partner
  records and want different property schemas for each.
- You run multiple companies in one Odoo database and want per-company
  property schemas on partners.
- Either of the above; both reinforce the case.

## When the core mixin alone is sufficient

- Single-company database, and you don't need to distinguish company
  vs individual property schemas. The core `properties` field on
  `res.partner` covers it with less surface area.

## Field visibility

The view inheritance adds **only** this module's two fields to the
res.partner form, conditioned on `is_company`:

- `properties_type_company` — rendered when `is_company` is `True`.
- `properties_type_person` — rendered when `is_company` is `False`.

The core `properties` field exists on the model (inherited from the
mixin) but **is not added to the form view by this module**. In
practice that means a partner records sees one Properties widget at a
time — the company schema or the person schema, depending on its
`is_company` flag — with no visible overlap with the core mixin's
global field. If a deployment wants the core surface in addition,
they can add `<field name="properties" widget="properties"/>` via a
per-database view override.
