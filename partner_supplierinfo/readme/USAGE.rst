To gather a contact's specific supplier reference you'll need a third module that calls the field with the proper context:

  .. code-block:: python

    partner.with_context(supplier_id=supplier.id).supplier_ref

If no supplier is found in the related `partner.supplierinfo` records, we'll get the regular `ref` field content.

To add supplier informations to your contacts:

#. Go to any partner form.
#. In `Supplier Information` tab customer references can be created edited or consulted.
#. In this tab there is a tree view, the following fields are displayed:

  * `Ref` for the customer reference
  * `Supplier` for the supplier it belongs to
