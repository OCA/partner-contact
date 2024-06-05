- The properties are shared between all the companies accessing the contact, as the
  properties fields in the ORM are very limited in possibilities (they don't admit
  compute methods for example).
- The properties definition is stored in the system parameter
  `partner_property.properties_definition`. Don't touch its value manually for not
  breaking the definition or losing data.
