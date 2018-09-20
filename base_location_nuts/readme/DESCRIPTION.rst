This module allows to import NUTS locations.

Creates four new fields in Partner object, one per NUTS level

* NUTS L1: Country level
* NUTS L2: Normally state or big region level
* NUTS L3: Normally substate or state level
* NUTS L4: Normally small region or province level

This module allows to set the flag *Not updatable* in a NUTS region so that it gets no more updated nor deleted by the import wizard.

Usually NUTS regions have to stay updated with the real ones, but the user may want to update a region's field (name, parent, ...) or create a new ones.
With this module, flagging such records as *Not updatable* prevents them from being overwritten or deleted by the import wizard.
