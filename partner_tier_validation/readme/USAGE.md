Before using, check Contact Stages configuration to ensure that the
default stage has the "Related State" field set to "To Approve". For
example, having the "Draft" stage the default ensures this.

A validation exception needs to be defined if you want to be able to
change the stage after validation and then make the contact available.

A regular user creates a new Contact and sends it for approval:

1. Create a Contact triggering at least one "Tier Definition". The
   Contact will be in Draft state and marked as Archived until
   approved.
2. Click on *Request Validation* button.
3. In the *Reviews* section, at the bottom of the form, inspect the
   pending reviews and their status.

The approver reviews Contacts to approve:

1. Navigate to the Contacts app, and select the filter "Needs my
   Approval"
2. Open the Contact form to approve. It will display a "This Records
   needs to be validated" banner, with "Validate" and "Reject" options.
3. The approver can change the stage to "Active". This will
   make the record available to be used.

The Approve/Reject actions do not automatically change the State. This
could be a future improvement.
