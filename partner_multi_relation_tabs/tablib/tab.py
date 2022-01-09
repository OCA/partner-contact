# Copyright 2014-2020 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
"""Encapsulate the information on a tab in the database."""
import logging
from lxml import etree

from odoo import _

# Note: next function moved in 13.0 to odoo/addons/base/models/ir_ui_view.py
from odoo.osv.orm import transfer_modifiers_to_node


_logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


NAME_PREFIX = "relation_ids_tab"


class Tab:
    """Encapsulate the information on a tab in the database."""

    def __init__(self, tab_record):
        """Create tab from tab_record.

        In this version tab_record can be assumed to be a partner.relation.tab.
        """
        self.tab_record = tab_record
        self.name = tab_record.code

    def get_fieldname(self):
        """Fieldname will be concattenation of prefix and tab record id."""
        return "%s_%s" % (NAME_PREFIX, self.tab_record.id)

    def get_visible_fieldname(self):
        """The field with suffix visible will control display of corresponding field."""
        return "%s_visible" % self.get_fieldname()

    def create_page(self):
        """Create single tabpage that will be added to form notebook."""
        tab_page = etree.Element("page")
        self._set_page_attrs(tab_page)
        field = etree.Element(
            "field",
            name=self.get_fieldname(),
            context="{"
            '"default_this_partner_id": id,'
            '"default_tab_id": %d}' % self.tab_record.id,
        )
        tab_page.append(field)
        tree = etree.Element(
            "tree",
            attrib={
                "editable": "bottom",
                "default_order": "active desc, other_partner_id",
                "decoration-success":
                "active and not date_end and"
                " (not date_start or date_start <= current_date)",
                "decoration-primary": "date_start and date_start >= current_date",
                "decoration-warning": "active and date_end",
                "decoration-muted": "date_end and date_end <= current_date",
            },
        )
        field.append(tree)
        # Now add fields for the editable tree view in the tab.
        tree.append(etree.Element("field", name="active", invisible="1"))
        tree.append(
            etree.Element("field", name="other_partner_id_domain", invisible="1")
        )
        type_field = etree.Element("field", name="type_selection_id", widget="many2one")
        type_field.set("domain", repr([("tab_id", "=", self.tab_record.id)]))
        type_field.set("options", repr({"no_create": True}))
        tree.append(type_field)
        other_partner_field = etree.Element(
            "field", string=_("Partner"), name="other_partner_id", widget="many2one",
            domain="other_partner_id_domain"
        )
        other_partner_field.set("options", repr({"no_create": True}))
        tree.append(other_partner_field)
        tree.append(etree.Element("field", name="date_start"))
        tree.append(etree.Element("field", name="date_end"))
        return tab_page

    def _set_page_attrs(self, tab_page):
        tab_page.set("string", self.tab_record.name)
        attrs = {"invisible": [(self.get_visible_fieldname(), "=", False)]}
        tab_page.set("attrs", repr(attrs))
        transfer_modifiers_to_node(attrs, tab_page)

    def compute_visibility(self, partner):
        """Compute visibility, dependent on partner and conditions."""
        tab = self.tab_record
        if tab.partner_ids:
            return partner in tab.partner_ids
        if tab.contact_type:
            is_company_tab = tab.contact_type == "c"
            if partner.is_company != is_company_tab:
                return False
        if tab.partner_category_id:
            if tab.partner_category_id not in partner.category_id:
                return False
        return True
