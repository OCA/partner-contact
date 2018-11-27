Relation Type Tabs
~~~~~~~~~~~~~~~~~~

Before being able to show certain types of relations on a tab in the partner
form, you will have to define the tab.

Do that in Contacts / Relations / Relation Tabs.

.. image:: https://raw.githubusercontent.com/OCA/partner-contact/11.0/partner_multi_relation_tabs/static/description/partner_multi_relation_tabs-tab-configuration.png

If you specify nothing, the tab will be shown on all partner forms that have
tabs (page elements). Normally you will select to show the tab only on
partners that are companies/organisations, or only for persons. You can also
select a category to further limit for which partners the tab wil be shown.

The possibility exists to show a tab only on specific partners. For instance
on your own company partner.

Relation Types
~~~~~~~~~~~~~~

In configuring the relation types, you can select which type of relation will
be shown on which tab. It is possible to show multiple types on one tab.

Do that in Contacts / Relations / Relation Types.

For example on a 'executive board' tab, you might want to show the CEO of a
company, but also the CFO, the CTO and normal board members.

You might specify a tab for both the 'left side' of a relation, as for the
'right side' or inverse relation. So a relation 'company has ceo', with
inverse type 'person is ceo of' might specify the 'board' tab for the
company type of the relation, but possibly a 'positions held' tab for the
person side of the relation, so on the partner form of a person you see in
one tab all positions or functions a person has, regardless in which company
or organisation.

For each side of a relation, the partner contact type and the partner category
must be consistent with those specified for the tab.

.. image:: https://raw.githubusercontent.com/OCA/partner-contact/11.0/partner_multi_relation_tabs/static/description/partner_multi_relation_tabs-relation-type-configuration.png

Partner Form
~~~~~~~~~~~~

The partner form will contain extra tab pages, for each tab that is
appropiate for that partner. So a company partner does not show the tabs that
are meant for persons and vice versa. Also tabs meant for partners with
a certain category/label will only show if partners have that label.

When adding relations on a tab, only relation types appropiate for that tab
can be selected.

Example of adding a relation:

.. image:: https://raw.githubusercontent.com/OCA/partner-contact/11.0/partner_multi_relation_tabs/static/description/partner_multi_relation_tabs-partner-edit.png

Example of a filled out board tab:

.. image:: https://raw.githubusercontent.com/OCA/partner-contact/11.0/partner_multi_relation_tabs/static/description/partner_multi_relation_tabs-partner-display.png

Deleting tabs
~~~~~~~~~~~~~

When a tab is deleted, this will in no way effect the existing relations.

However the references on the relation types to the deleted tabs will also be
cleared.

Searching Relations by Tab
~~~~~~~~~~~~~~~~~~~~~~~~~~

You can search relations with the tab on which they are shown. For instance
to find all board members.

Do that in Contacts / Relations / Relations.

.. image:: https://raw.githubusercontent.com/OCA/partner-contact/11.0/partner_multi_relation_tabs/static/description/partner_multi_relation_tabs-relation-search.png
