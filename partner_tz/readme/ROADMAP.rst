* Odoo default value for timezone field uses the tz set on the connected user.
  So if a user creates a partner located in a different timezone than his own,
  the created partner will be set in the user's timezone instead of having the
  timezone from its own location.
  Ideally, we should change this behaviour to get the timezone from the country
  and city of the partner when they are defined.
  http://www.geonames.org/export/web-services.html#timezone might be a good
  starting point.
