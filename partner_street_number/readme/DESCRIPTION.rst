This module introduces separate fields for street name and street number.

- Introduce two new fields for street name and number
- Keep 'Street' field as a function field to return street name + number
- Data written to the 'Street' field will be parsed into street name and number
  if possible. This will be performed upon installation of the module for
  existing partners.
