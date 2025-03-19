Every time a partner's address or name is modified,
the system automatically saves the previous information along with the modification date.
You can review these records in the "Address History" tab.

*Displaying Historical Data by Date*

To display partner information based on a specific date, you must pass the `date_change` parameter.
The system will then compare this date with the history table.
If the document's date is before the modification date, the system will display the pre-modified data.

*Example: Customer Invoices / Vendor Bills*

When dealing with accounting documents such as `Customer Invoices` or `Vendor Bills`,
you need to pass the following context to ensure the system retrieves the correct historical data:

.. code-block:: xml

    <record id="view_move_form" model="ir.ui.view">
        <field name="name">account.move.form</field>
        <field name="model">account.move</field>
        <field name="inherit_id" ref="account.view_move_form" />
        <field name="arch" type="xml">
            <xpath expr="//group[@id='header_left_group']/field[@name='partner_id']" position="attributes">
                <attribute name="context">
                    {
                        'res_partner_search_mode': (
                            context.get('default_move_type', 'entry') in ('out_invoice', 'out_refund', 'out_receipt') and 'customer'
                        ) or (
                            context.get('default_move_type', 'entry') in ('in_invoice', 'in_refund', 'in_receipt') and 'supplier'
                        ) or False,
                        'show_address': 1,
                        'default_is_company': True,
                        'show_vat': True,
                        'date_change': date,  # Track partner details based on the accounting date
                    }
                </attribute>
            </xpath>
        </field>
    </record>
