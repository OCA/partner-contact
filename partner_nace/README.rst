NACE Activities in Partner
==========================

This module adds the concept of NACE activity to the partner. Allows you to
select in partner form:

* Main NACE activity in a dropdown (many2one)
* Secondary NACE activities in a multi label input (many2many)

This addon is inspired in OCA/community-data-files/l10n_eu_nace, but it does
not use partner categories to assign NACE activities to partner.

Applies only to partners marked as companies

After installation, you must click at import wizard to populate NACE items
in Odoo database in:
Sales > Configuration > Address Book > Import NACE Rev.2 from RAMON

This wizard will download from Europe RAMON service the metadata to
build NACE database in Odoo in all installed languages.

If you add a new language (or want to re-build NACE database), you should call
import wizard again.

Only Administrator can manage NACE activity list (it is not neccesary because
it is an European convention) but any registered user can read them,
in order to allow to assign them to partner object.

Credits
=======

Contributors
------------
* Antonio Espinosa <antonioea@antiun.com>
