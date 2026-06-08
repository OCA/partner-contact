This module provides two distinct ways to archive a company or parent contact.

**Archive via the action menu (gear icon)**

Clicking **Archive** in the gear (⚙) menu archives **only the company
itself**. Child contacts, invoice/delivery addresses, and related partners
are left completely untouched. Use this when you want a quick archive
without touching any of the company's contacts.

> **Note:** This behaviour is consistent regardless of the *Force propagation
> outside UI* system setting. The gear menu never propagates.

**Archive via the "Archive Contact and Children" button**

1. Open a partner (company or main contact).
2. Click the **"Archive Contact and Children"** button.
3. Review the list of child contacts to be archived. Remove any row to
   keep that contact active after archiving.
4. Confirm the action.
   * Non-contact types (e.g., invoice/delivery addresses) are archived
     silently in the background — they do not appear in the list.
   * Contact-type descendants appear in the wizard for review.
   * Contacts linked to active users are automatically excluded from the
     list; a warning message is posted on the company.

If the company has no contact-type descendants, no wizard opens and the
company (and its non-contact addresses) are archived immediately.

**Unarchiving**

Unarchiving also follows propagation rules: if a parent partner is
unarchived, its propagated descendants are unarchived as well. Partners
that were independently archived are not affected.

**System setting: Force propagation outside UI**

When **Force propagation outside UI** is enabled (under *Settings*),
archiving a company via any non-UI path (imports, RPC calls, automated
jobs, etc.) will also propagate to descendants, just as the wizard button
does. This setting has no effect on the gear menu action.
