.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

=================
Partner Relations
=================

This module aims to provide generic means to model relations between partners.

Examples would be 'is sibling of' or 'is friend of', but also 'has contract X
with' or 'is assistant of'. This way, you can encode your knowledge about your
partners directly in your partner list.

Installation
============

Configuration
=============

Usage
=====

Before being able to use relations, you'll have define some first. Do that in
Contacts / Relations / Partner relations. Here, you need to
name both sides of the relation: To have an assistant-relation, you would name
one side 'is assistant of' and the other side 'has assistant'. This relation
only makes sense between people, so you would choose 'Person' for both partner
types. For the relation 'is a competitor of', both sides would be companies,
while the relation 'has worked for' should have persons on the left side and
companies on the right side. If you leave this field empty, the relation is
applicable to all types of partners.

If you use categories (tags) to further specify the type of partners, you could for
example enforce that the 'is member of' relation can only have companies with
label 'Organization' on the left side.

Now open a partner, click on the 'Relations' smart button and add relations as appropriate.

Searching partners with relations
---------------------------------

Searching for relations is integrated transparently into the partner search
form. To find all assistants in your database, fill in 'is assistant of' and
autocomplete will propose to search for partners having this relation. Now if
you want to find Anna's assistant, you fill in 'Anna' and one of the proposals
is to search for partners having a relation with Anna. This results in Anna's
assistant(s), as you searched for assistants before.

By default, only active, not expired relations are shown. If you need to find
partners that had some relation at a certain date, fill in that date in the
search box and one of the proposals is to search for relations valid at that
date.

More info
---------

For further information, please visit:

 * https://www.odoo.com/forum/help-1


.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/134/11.0

Known issues / Roadmap
======================

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/partner-contact/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smash it by providing detailed and welcomed feedback.

Credits
=======

Contributors
------------

* Holger Brunn <hbrunn@therp.nl>
* Stefan Rijnhart <stefan@therp.nl>
* Ronald Portier <ronald@therp.nl>
* Sandy Carter <sandy.carter@savoirfairelinux.com>
* Bruno Joliveau <bruno.joliveau@savoirfairelinux.com>
* Adriana Ierfino <adriana.ierfino@savoirfairelinux.com>
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit https://odoo-community.org.
