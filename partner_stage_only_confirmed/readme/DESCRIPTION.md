This module extends the partner stage functionality by implementing a filtering mechanism that ensures only confirmed partners are displayed in Many2one fields on form views. This is particularly useful in business scenarios where you want to prevent users from selecting partners that are not yet confirmed in your system.

### Problem Solved

In standard Odoo, when using Many2one fields that reference partners (like `parent_id`, `contact_id`, etc.), all partners are available for selection regardless of their state or confirmation status. This can lead to:
- Selection of partners that are not yet properly validated
- Accidental linking to partners that are in draft or unconfirmed states
- Data integrity issues when business processes require confirmed partners

### Solution

The module automatically modifies form views at runtime to filter partner-related Many2one fields, showing only partners in the 'confirmed' state. This filtering is configurable via:
- Context parameters
- System configuration parameters
- Default behavior that can be overridden as needed

The filtering is applied transparently without requiring manual domain updates on individual views, making it a robust solution that works across the entire application for any partner-related Many2one field.
