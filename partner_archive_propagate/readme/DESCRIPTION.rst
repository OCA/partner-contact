===========================
Partner Archive Propagation
===========================

This module extends the native archiving mechanism for partners.

When archiving a company or parent contact, it will also handle its descendants
according to business rules — with user control and safeguards.

Features
--------

* Adds a new **"Archive Contact and Children"** button on the Partner form.
* Shows a **wizard** listing contact-type descendants before archiving.
* Automatically skips descendants linked to active users.
* Adds a technical Many2one field (propagated_from_id) that records which parent partner caused the automatic archiving, making propagation fully traceable and reversible.
* Ensures automatic unarchive propagation.
* Includes a system setting to enforce propagation even for non-UI actions
  (imports, RPC, automated jobs, etc.).
