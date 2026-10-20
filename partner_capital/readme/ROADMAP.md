- Add automatic rules to calculate turnover range and company size.
- Allow customization of company sizes.
- Since 20.0, `is_company` is computed (no parent and a VAT) and can't be
  set by hand. The "Capital" group in the partner form is only shown for
  companies, so a company without a VAT doesn't show it.
