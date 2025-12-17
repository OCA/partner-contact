This addon extends "Partner Identification Numbers" to provide number
categories for GLN and GCP registration.

A GLN (Global Location Number) is a GS1 identification key used to uniquely
identify legal entities, functional entities, and physical locations involved
in business processes. A GCP (GS1 Company Prefix) is the company-specific
prefix issued by GS1 that is used as a building block to create GS1
identification keys, including GLNs.

In this module, GLN values are validated as GS1/EAN-based identifiers, while
GCP values are stored as company prefixes with a length between 1 and 12 digits.

See:
- https://www.gs1.org/standards/id-keys/gln/physical-location
- https://www.gs1.org/standards/id-keys/company-prefix
- https://support.gs1.org/support/solutions/articles/43000734241-how-do-i-use-a-global-location-number-to-identify-a-physical-location-
