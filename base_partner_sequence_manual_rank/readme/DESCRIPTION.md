When `base_partner_sequence` is installed, the reference (`ref`) is assigned
to all commercial partners. This causes confusion when `partner_manual_rank` and`partner_supplier_ref`
is also installed,  since a partner that is only a supplier would also get a customer reference.

This module serves as a glue module between `base_partner_sequence` and `partner_manual_rank`.
It updates the assignment logic so that the reference is only set when the partner is flagged as
a customer (`is_customer`).
