### Default Behavior

By default, the module applies the partner filtering automatically to all applicable Many2one fields that reference partners. When selecting a partner in any form view, only partners in the 'confirmed' state will be available.

### Configuration Methods

The filtering behavior can be controlled in several ways:

### 1. Context Parameter
You can disable the filtering for specific views by adding `only_confirmed_partners: false` to the context:

**In views (XML):**
```xml
<field name="parent_id" context="{'only_confirmed_partners': false}"/>
```

**In Python code:**
```python
record.with_context(only_confirmed_partners=False).get_view(...)
```

### 2. System Configuration Parameter
You can set the global filtering behavior using system parameters:

**Enable filtering:**
- Go to Settings > Technical > Parameters > System Parameters
- Create or update parameter: `partner_stage.only_confirmed_partners`
- Set value to any non-false value (e.g., "True", "1", "yes")

**Disable filtering:**
- Set parameter value to: "False", "false", "0", or empty string

### 3. Explicit Enable
To explicitly enable the filtering globally, set the system parameter to any true-like value.

### Common Use Cases

### Case 1: Sales Orders
When creating sales orders, ensure that only confirmed customers can be selected as the main partner, preventing orders from being created for unconfirmed/draft partners.

### Case 2: Invoicing
When creating invoices, ensure that only confirmed partners are available as the billing address partner.

### Case 3: Project Management
When assigning projects to contacts, restrict the selection to only confirmed partners to maintain data quality.

### Technical Implementation

The module uses the `get_view` method override to dynamically modify form view architectures at runtime. This approach ensures that:
- Existing views don't require modifications
- The filtering applies to all partner-related Many2one fields
- Performance impact is minimal and only affects form views
- The filtering is transparent to end users (they simply see fewer options)

### Limitations

- The filtering only applies to form views
- Only affects Many2one fields with comodel_name "res.partner"
- Other view types (tree, search, kanban) are not affected
- Context and system parameters provide override mechanisms for exceptions
