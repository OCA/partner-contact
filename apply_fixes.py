import os
import re

def modify_file(filepath, replacements):
    with open(filepath, 'r') as f:
        content = f.read()
    
    for old, new in replacements:
        content = content.replace(old, new)
        
    with open(filepath, 'w') as f:
        f.write(content)

modify_file('partner_sequence/__manifest__.py', [
    ('        "views/journal_views.xml",\n', ''),
    ('"author": "kalab.rened@outlook.com"', '"author": "Odoo Community Association (OCA), kalab.rened@outlook.com"'),
    ('"website": "https://github.com/OCA/account-financial-tools"', '"website": "https://github.com/OCA/partner-contact"')
])

modify_file('partner_sequence/views/res_partner_views.xml', [
    ('<field name="inherit_id" ref="base.view_partner_form"/>', '<field name="inherit_id" ref="base.view_partner_form"/>\n        <field name="priority">99</field>')
])

modify_file('user_contact_creation_access/__manifest__.py', [
    ('"author": "kalab.rened@outlook.com"', '"author": "Odoo Community Association (OCA), kalab.rened@outlook.com"'),
    ('"website": "https://github.com/OCA/account-financial-tools"', '"website": "https://github.com/OCA/partner-contact"')
])

modify_file('user_contact_creation_access/models/res_users.py', [
    ('        string="Can Create Contacts",\n', '')
])

try:
    modify_file('base_location_nuts/wizard/nuts_import.py', [
        ('# ruff: noqa: B950', '# noqa: E501'),
        ('# ruff: noqa at', '# noqa: E501') # Just in case it's formatted differently
    ])
    # Let's just use regex for ruff just in case
    with open('base_location_nuts/wizard/nuts_import.py', 'r') as f:
        c = f.read()
    c = re.sub(r'#\s*ruff:\s*noqa:?\s*B950', '# noqa: E501', c)
    with open('base_location_nuts/wizard/nuts_import.py', 'w') as f:
        f.write(c)
except Exception as e:
    print(f"Failed to fix nuts_import.py: {e}")

print("Done applying fixes.")
