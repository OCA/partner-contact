This module extends the standard *Merge Contacts* wizard in Odoo
(`base.partner.merge.automatic.wizard`) so that user accounts are also
consolidated when you merge duplicate contacts.
Odoo allows you to merge two (or more) contacts into one.
This is great for deduplication.

However, when both of those contacts are linked to different users
(`res.users`), Odoo does **not** merge or clean up those users.
After the merge you can end up with:

* Multiple logins pointing at the same final contact.
* Confusing access rights: which login should this person actually use?
* Compliance issues: inactive/old accounts still exist and could still log in.

This module fixes that:


When you merge contacts and Odoo finishes the normal merge:

* If the resulting contact has **0 or 1** linked users:
  
  - Nothing extra happens.

* If the resulting contact has **2+** linked users:
  
  1. The module chooses one user account to keep:
  
     - The account with the most recent login date
       (field ``login_date``, which reflects the last `res.users.log` record).
     - If nobody has ever logged in, it falls back to the most recently created user.

  2. That "kept" user is:
  
     - Forced to stay active.
     - Explicitly linked to the surviving contact partner.

  3. All *other* users are archived:
  
     - They are set inactive.
     - Their ``login`` is scrambled to a unique value like
       ``__merged_user_<id>_oldlogin``
       so they can no longer authenticate and so their old
       login can be reassigned if desired.

  4. Security groups are merged:
  
     - Any groups on the archived users are added to the kept user.
     - Odoo's standard ``res.users`` write() logic will automatically:
       
       * add all implied groups,
       * normalize mutually exclusive role groups,
       * enforce "internal vs portal vs public" constraints.
