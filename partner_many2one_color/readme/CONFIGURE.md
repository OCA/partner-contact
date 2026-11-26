Open a contact, go to the **Notes** tab and set **Color State** in the
*Highlight in Selection Fields* section to *Warning* or *Critical*. Optionally
enter a message; it is shown as tooltip on the colored field.

A contact without an own color state uses the color state and message of its
parent contact (over any number of levels). The inherited state is then shown
read-only as **Inherited Color State** in the same section; set an own color
state on the contact to override it.

To disable the coloring on a specific field, add the `no_color` widget option
in the view (see `web_many2one_color`):

```xml
<field name="partner_id" options="{'no_color': True}" />
```
