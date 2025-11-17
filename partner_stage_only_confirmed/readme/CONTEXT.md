### Business Context

Many organizations implement partner lifecycle management where contacts move through various stages before being fully confirmed and eligible for business transactions. This workflow typically includes:

- **Draft Stage:** Initial partner entry, possibly pending validation
- **Validation Stage:** Partner details being verified
- **Confirmed Stage:** Fully validated partner ready for business
- **Other Stages:** Potentially archived or suspended partners

### Problem Statement

Without proper filtering mechanisms, users can accidentally select unconfirmed partners in critical business operations:

- Creating sales orders for draft partners
- Generating invoices for unverified contacts
- Assigning projects to partners not yet confirmed
- Linking transactions to partners that may not exist legally

This leads to potential business disruption, data quality issues, and compliance problems.

### Industry Scenarios

### Financial Services
Banks and financial institutions must ensure that all customer references in transactions are to properly verified and confirmed clients. This filter prevents linking to customers who may not have completed the required KYC (Know Your Customer) processes.

### E-commerce and Retail
Online retailers often have a customer validation process before allowing full purchasing capabilities. This module ensures that business transactions only reference validated customers.

### Professional Services
Consulting firms and professional services often have a client onboarding process. This module ensures that only properly onboarded clients appear in selection lists for new projects or contracts.

### Manufacturing and Supply Chain
Manufacturers often have supplier qualification processes. The filtering ensures that only qualified suppliers appear in procurement operations.

### Regulatory Compliance

In many jurisdictions, businesses must maintain proper verification of their partner relationships. This module supports:

- **GDPR Compliance:** Ensuring personal data is properly validated before use
- **Financial Regulations:** Meeting requirements for customer verification in financial transactions
- **Contract Law:** Ensuring legal capacity of contracting partners
- **Industry Standards:** Meeting sector-specific requirements for partner validation

### Technical Context

The module addresses the gap between partner state management (handled by the `partner_stage` module) and user interface behavior. While partner states may be properly managed in the backend, the user interface previously provided no automatic filtering mechanism.

### Integration Considerations

This module works in conjunction with:
- The `partner_stage` module for state management
- Standard Odoo partner management functionality
- Custom partner validation workflows
- Existing business processes that depend on partner confirmation status

### Solution Scope

The module provides an elegant solution that:
- Maintains data integrity without restricting functionality
- Provides configuration flexibility for different business needs
- Integrates seamlessly with existing user interfaces
- Supports both global and granular control over the filtering behavior
