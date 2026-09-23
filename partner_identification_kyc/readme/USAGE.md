## Request KYC Button

On the partner form, a "Request KYC" button will appear when:
- There is no KYC identification record in the 'new', 'running', or 'to_renew' states
- OR there is no ID number record of the KYC category at all

The button will be hidden if:
- There is a 'running' or 'to_renew' KYC record
- OR there is already a 'new' status KYC record (to prevent redundant records)

Clicking the button will create a new KYC identification record in the 'new' status, triggering the associated activity for KYC officers to process.

## API Function

For partners created via API, there is a function to trigger the KYC process automatically. If no KYC identification record exists for a partner, calling this function will create a record in the 'new' status.

## Activity Management

KYC identification records are associated with the "Perform KYC Check" activity type, which appears in the activity views for tracking and processing by responsible officers.
