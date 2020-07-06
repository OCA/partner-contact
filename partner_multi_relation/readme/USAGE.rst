Relation Types
~~~~~~~~~~~~~~

Before being able to use relations, you'll have define some first.
Do that in Contacts / Relations / Partner relations.

.. image:: https://raw.githubusercontent.com/OCA/partner-contact/12.0/partner_multi_relation/static/description/relation_type_list.png

A relation type has a name for both sides.

.. image:: https://raw.githubusercontent.com/OCA/partner-contact/12.0/partner_multi_relation/static/description/relation_type_form_empty.png

To have an assistant-relation, you would name one side 'is assistant of' and the other side 'has assistant'.

.. image:: https://raw.githubusercontent.com/OCA/partner-contact/12.0/partner_multi_relation/static/description/relation_type_form_name_filled.png

Partner Types
~~~~~~~~~~~~~

The `Partner Type` fields allow to constrain what type of partners can be used
on the left and right sides of the relation.

* In the example above, the assistant-relation only makes sense between people, so you would choose 'Person' for both partner types.

.. image:: https://raw.githubusercontent.com/OCA/partner-contact/12.0/partner_multi_relation/static/description/relation_type_form_partner_type_filled.png

* For a relation 'is a competitor of', both sides would be companies.
* A relation 'has worked for' should have persons on the left side and companies on the right side.

If you leave these fields empty, the relation is applicable to all types of partners.

Partner Categories
~~~~~~~~~~~~~~~~~~

You may use categories (tags) to further specify the type of partners.

You could for example enforce the 'is member of' relation to accept only companies with the label 'Organization' on the right side.

.. image:: https://raw.githubusercontent.com/OCA/partner-contact/12.0/partner_multi_relation/static/description/relation_type_form_category_filled.png

Reflexive
~~~~~~~~~

A reflexive relation type allows a partner to be in relation with himself.

For example, the CEO of a company could be his own manager.

.. image:: https://raw.githubusercontent.com/OCA/partner-contact/12.0/partner_multi_relation/static/description/relation_type_reflexive.png

Symmetric
~~~~~~~~~

A symetric relation has the same value for the left and right sides.

For example, in a competitor relation, both companies are competitors of each other.

.. image:: https://raw.githubusercontent.com/OCA/partner-contact/12.0/partner_multi_relation/static/description/relation_type_symmetric.png

Invalid Relation Handling
~~~~~~~~~~~~~~~~~~~~~~~~~

When the configuration of a relation type changes, some relations between 2 partners may become invalid.

For example, if the left partner type is set to `Person` and a relation already exists with a company on the right side,
that relation becomes invalid.

.. image:: https://raw.githubusercontent.com/OCA/partner-contact/12.0/partner_multi_relation/static/description/relation_type_invalid_handling.png

What happens with invalid relations is customizable on the relation type.

4 possible behaviors are available:

* Do not allow change that will result in invalid relations
* Allow existing relations that do not fit changed conditions
* End relations per today, if they do not fit changed conditions
* Delete relations that do not fit changed conditions

Searching Partners With Relations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To search for existing relations, go to `Contacts / Relations / Relations`.

.. image:: https://raw.githubusercontent.com/OCA/partner-contact/12.0/partner_multi_relation/static/description/search_relation.png

To find all assistants in your database, fill in 'assistant' and
autocomplete will propose to search for this type of relation.

.. image:: https://raw.githubusercontent.com/OCA/partner-contact/12.0/partner_multi_relation/static/description/search_relation_2.png

Now if you want to find Colleen's assistant, you fill in 'Colleen' and one of the proposals
is to search for partners having a relation with Colleen.

.. image:: https://raw.githubusercontent.com/OCA/partner-contact/12.0/partner_multi_relation/static/description/search_relation_3.png

Searching Relations From Partner View
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A smart button is available on the partner form view to display the list of relations.

.. image:: https://raw.githubusercontent.com/OCA/partner-contact/12.0/partner_multi_relation/static/description/partner_form_view_smart_button.png

.. image:: https://raw.githubusercontent.com/OCA/partner-contact/12.0/partner_multi_relation/static/description/partner_form_view_smart_button_2.png
