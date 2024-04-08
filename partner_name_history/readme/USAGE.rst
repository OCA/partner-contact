When a partner changes its name:

#. Open the partner and change its name as usual, a new line is automatically added in its `Name history`.
#. In the `Name history`, you can edit the date if necessary

The old name of a partner can be retrieved in many ways:

- `partner._get_name_at_date(<date>)`
- `partner.with_context(partner_name_date=<date>).name`

A more dynamic behavior is enabled when `use_partner_name_history` is in the context: a model can declare a `_partner_name_history_field_map`:

.. code-block::

  class AccountMove(models.Model):
      _inherit = "account.move"
      _partner_name_history_field_map = {
          "partner_id": "invoice_date",
      }

This means that `move.partner_id.name` will actually be `move.partner_id.with_context(partner_name_date=move.invoice_date).name`.

The values of the map can also be method names:

.. code-block::

  class AccountMove(models.Model):
      _inherit = "account.move"
      _partner_name_history_field_map = {
          "partner_id": "_get_partner_name_history_date",
      }

This means that `move.partner_id.name` will actually be `move.partner_id.with_context(partner_name_date=move._get_partner_name_history_date()).name`.

This can be useful in reports because it allows to show the old name of partners with no QWeb change.

The above example is extracted from `account_move_partner_name_history`.
