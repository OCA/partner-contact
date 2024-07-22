After installation, a import wizard will popup to create NUTS items in Odoo.
You can also run it manually from
Contacts > Configuration > Localization > Import NUTS 2024

This wizard will download from Europe ShowVoc service the metadata to
build NUTS in Odoo. Each localization addon (l10n_es_location_nuts,
l10n_de_location_nuts, ...) will inherit this wizard and
relate each NUTS item with states. So if you install a new localization addon
you must re-build NUTS clicking this wizard again.

As the last RAMON file used in this module was from 2013, you may want to update
your NUTS items by running the wizard again. 
