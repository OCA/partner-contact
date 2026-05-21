This module adds the use of properties in partners (different for
companies and individuals).

## Relation to Odoo 19.0 core

Odoo 19.0 introduced a single global `properties` field on `res.partner`
via the `properties.base.definition.mixin`. This module remains distinct
because it adds **per-company** definitions
(`properties_type_{company,person}`) keyed off `env.company`, plus the
person/company-type split — both unavailable in core.
