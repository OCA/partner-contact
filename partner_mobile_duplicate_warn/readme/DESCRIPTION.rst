This module adds a warning banner on the partner form view if another partner
has the same mobile phone number. It helps spot duplicate partners. If the
duplication is confirmed, the user can then use the native partner merge wizard
available from the partner tree view (menu *Action > Merge*).

.. figure:: static/description/partner_warn_banner.png
   :alt: Warning banner on partner form

This module depend on the module *phone_validation* from the official addons which
handle the automatic reformatting of phone numbers to the E.164 format depending on
the country of the partner.

For example, for a French partner, if you write **06.23.45.67.78** in the *Mobile*
field, it will be automatically reformatted to **+33623456778** (via the onchange).
Thanks to this reformatting, this module can easily find identical phone numbers on
other partners.

It is similar to the native warning banner when another partner has the same VAT number.
This module has a twin brother named **partner_email_duplicate_warn** which adds a
warning banner when another partner has the same email.

The module has been written to be extendable. For instance other modules might
limit the check to partners of type 'contact', or allow the same mobile on a
partner and its parent. To extend a module you have to extend two methods:

* _get_same_mobile_domain(self): Append new conditions to the domain.
* _get_same_mobile_depends(self): Add the fields used in the appended domain conditions.

The method _find_same_mobile_partner() might be used in extention modules.
For instance if you want to define a constraint that prevents duplicate
mobiles (as defined by method _get_same_mobile_domain()) to get into the
database at all.

