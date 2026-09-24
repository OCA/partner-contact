### System-Level Configuration

The module behavior can be configured using system parameters without code changes:

1. **Access System Parameters:**
   - Navigate to: `Settings > Technical > Parameters > System Parameters`
   - Or access directly: `[[Technical Settings]] > Parameters > System Parameters`

2. **Configuration Parameter:**
   - Parameter name: `partner_stage.only_confirmed_partners`
   - Default behavior: When not set, the module defaults to `True` (filtering enabled)

3. **Setting Values:**
   - **Enable filtering:** Set value to any non-false string (e.g., "True", "1", "yes")
   - **Disable filtering:** Set value to "False", "false", "0", "", or other false-like strings

### Per-View Configuration

Individual views can override the system default using context:

### In XML Views:
```xml
<!-- Disable filtering for this specific field -->
<field name="partner_id" context="{'only_confirmed_partners': false}"/>

<!-- Explicitly enable filtering (usually not needed, just for clarity) -->
<field name="partner_id" context="{'only_confirmed_partners': true}"/>
```

### In Action Definitions:
```xml
<!-- In action definition -->
<record id="action_partner_form" model="ir.actions.act_window">
    <field name="context">{'only_confirmed_partners': false}</field>
</record>
```

### Programmatic Configuration

In Python code, you can control the behavior:

```python
# Disable filtering for specific operations
partners = self.env['res.partner'].with_context(
    only_confirmed_partners=False
)

# Enable filtering explicitly
partners = self.env['res.partner'].with_context(
    only_confirmed_partners=True
)
```

### Testing Configuration

For testing purposes, you can temporarily modify the behavior:

```python
# In test methods
def test_with_filtering_disabled(self):
    self.env['ir.config_parameter'].sudo().set_param(
        'partner_stage.only_confirmed_partners', 'false'
    )
    # Test code here
```

### Migration from Previous Versions

If you're upgrading from a previous version of this module or have custom configurations:
1. Review existing system parameters related to partner filtering
2. Test the new configuration behavior in a development environment
3. Update any custom code that manually handled partner filtering
4. Ensure user permissions for system parameter access if needed

### Performance Considerations

- The filtering is applied at view generation time (in `get_view` method)
- Only affects form views and only for partner-related Many2one fields
- Minimal performance impact since it only adds a domain condition
- The filtering process is optimized to avoid unnecessary processing
