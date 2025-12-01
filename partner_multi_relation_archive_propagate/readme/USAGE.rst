1. Install the following modules:

   * ``partner_multi_relation``
   * ``partner_archive_propagate``
   * ``partner_multi_relation_archive_propagate`` (this module)

2. Configure relation types:

   * Go to *Relation Types* menu.
   * Create or edit a relation type.
   * Enable **"Propagate archive"** (``propagate_archive``) on the
     relation type(s) where archiving should cascade.

3. Create relations:

   * Link a company partner to other partners using the configured
     relation types.

4. Archive a company:

   * Archive the company (via the UI wizard or via non-UI operations,
     depending on your configuration in
     `partner_archive_propagate`).
   * All related partners reachable via relation types with
     ``propagate_archive = True`` will be treated like propagated
     descendants:
     * archived if possible,
     * skipped (and mentioned) if they have active users,
     * marked with ``propagated_from_id = <company>``.

5. Unarchive the company:

   * Unarchiving the company triggers the base
     `partner_archive_propagate` logic.
   * All partners (tree descendants or relation-based) that were archived
     because of this company (``propagated_from_id``) are unarchived and
     have the field cleared.
