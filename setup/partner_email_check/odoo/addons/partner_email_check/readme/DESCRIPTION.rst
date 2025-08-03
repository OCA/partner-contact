This module validates and normalizes the field ``email`` in the model
``res.partner``.

As part of the normalization, email addresses are converted to lowercase.

Optionally, multiple partners can not be allowed to have the same address.
This will not work with multiple comma-separated email addresses in the field,
although validation and normalization are still supported in such cases.
