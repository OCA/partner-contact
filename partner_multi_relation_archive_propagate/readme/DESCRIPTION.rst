=========================================
Partner Multi Relation Archive Propagate
=========================================

This module extends the behaviour of
`partner_archive_propagate` to also propagate archiving and
unarchiving **via partner_multi_relation relations**.

When a company is archived:

* all related partners linked through relation types with
  ``propagate_archive = True`` are considered for propagation;
* related partners without active users are archived and marked with
  ``propagated_from_id`` pointing to the company;
* related partners linked to active users are skipped and listed in a
  message on the company.

When the company is unarchived, all partners that were archived because
of it – whether through the partner hierarchy or through
multi-relations – are restored automatically by the core
`partner_archive_propagate` logic.

Non-company partners do not propagate via this module, even if they are
involved in relations with ``propagate_archive = True``.
