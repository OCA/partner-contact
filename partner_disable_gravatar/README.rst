.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

========================
Partner Disable Gravatar
========================

A new feature has been introduced in Odoo v10 in the *base* module: when you enter an email address in the form view of a partner, Odoo will send a query to `gravatar.com <https://www.gravatar.com/>`_ to get a picture corresponding to the email address.

`Gravatar <//www.gravatar.com/>`_, which stands for *Globally Recognized Avatar*, is a website where any user can open an account and register a correspondance between his email address and a picture. That way, his picture/avatar will be automatically set on all websites that are connected to gravatar.com: he won't have to manually configure his picture/avatar on every website.

In Odoo, when you enter an email address in the form view of a partner (i.e. triggered via the *onchange* on the *email* field) and this partner doesn't have any image yet in Odoo, Odoo will automatically send an HTTPS query to `www.gravatar.com <https://www.gravatar.com/>`_ with an MD5 hash of the email of the partner. If it receives an answer from gravatar.com in the form of a picture within the 5 seconds timeout, it will set this picture on the *image* field of the partner in Odoo.

Some people may consider it as a cool feature to easily get picture on partners with no effort.

But other people may consider this as an annoying feature that adds unnecessary network trafic or, worse, as a leak of information. With this feature, gravatar.com is notified of all the email addresses added in the Odoo database, so it may be considered as a leak of information to a third party company (gravatar.com is operated by `Automattic Inc. <https://automattic.com/contact/>`_, an American company). The problem is that there is no way to disable this feature via a configuration parameter of Odoo. This module brings a solution to this problem: once installed, it disables the feature.

Configuration
=============

No configuration required. Installing the module will disable the automatic connection to gravatar.com.

Usage
=====

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/134/10.0

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/partner-contact/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed feedback.

Credits
=======

Contributors
------------

* Alexis de Lattre <alexis.delattre@akretion.com>

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
