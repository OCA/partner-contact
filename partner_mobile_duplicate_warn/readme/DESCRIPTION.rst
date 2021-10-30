This module adds a warning banner on the partner form view if another partner has the same mobile phone number. It helps spot duplicate partners. If the duplication is confirmed, the user can then use the native partner merge wizard available from the partner tree view (menu *Action > Merge*).

.. figure:: static/description/partner_warn_banner.png
   :alt: Warning banner on partner form

This module depend on the module *phone_validation* from the official addons which handle the automatic reformatting of phone numbers to the E.164 format depending on the country of the partner. For exemple, for a French partner, if you write **06.23.45.67.78** in the *Mobile* field, it will be automatically reformatted to **+33 6 23 45 67 78** (via the onchange). Thanks to this reformatting, this module can easily find identical phone numbers on other partners.

It is similar to the native warning banner when another partner has the same VAT number. This module has a twin brother named **partner_email_duplicate_warn** which adds a warning banner when another partner has the same email.
