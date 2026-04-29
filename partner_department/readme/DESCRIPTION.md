This module adds *Department* as a native partner type in Odoo's address book.

Unlike a standalone department model, a department is a real ``res.partner``
record (``type = 'department'``) and can therefore be selected anywhere a
partner is expected — for example as the partner of a sale order.

Key features:

- Contacts (non-company partners) have a **Department** field that links them
  to a department partner.
- Opening a department partner shows a **Members** smart button and a tab
  listing all contacts assigned to it.
- Partners can be searched and grouped by department.

> **Incompatibility notice:** This module is **not compatible** with
> `partner_contact_department`. Both modules provide a *Department* field on
> contacts but use different approaches; installing both at the same time will
> cause conflicts.
