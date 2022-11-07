# Copyright 2021 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from lxml import html
from markupsafe import Markup

from odoo import models


class IrUiView(models.Model):
    _inherit = "ir.ui.view"

    def _render(self, values=None, engine="ir.qweb", minimal_qcontext=False):
        """Disable inputs converting them into paragraphs and clear form
        buttons. This way, we don't need to go input by input and we can
        support any view extension without further patching"""
        res = super()._render(
            values=values, engine=engine, minimal_qcontext=minimal_qcontext
        )
        if not self.env.context.get("block_portal_data_edit"):
            return res
        fragments = html.fromstring(res.encode("utf-8"))
        for fragment in fragments:
            # The result is a page that looks the same way as the original form
            # but with the input fields shadowed and not editable as they're
            # just `<p>` paragraphs in `form-control` classes disguise.
            for _input in fragment.iterfind(".//form[@action='/my/account']//input"):
                if _input.type in ["text", "tel", "email"]:
                    attrs = _input.attrib
                    text = attrs.pop("value", "")
                    # We don't want this attribute in the `<p>`
                    del attrs["type"]
                    attrs["readonly"] = "1"
                    p_readonly = _input.makeelement("p", attrib=attrs)
                    p_readonly.text = text
                    _input.addprevious(p_readonly)
                    _input.getparent().remove(_input)
            for _select in fragment.iterfind(".//form[@action='/my/account']//select"):
                # Maybe there's a prettier way to extract the selected value
                option = [
                    x
                    for x in _select.getchildren()
                    if x.attrib.get("value", "") == _select.value
                ]
                text = option and option[0].text or ""
                attrs = _select.attrib
                attrs["readonly"] = "1"
                p_readonly = _select.makeelement("p", attrib=attrs)
                p_readonly.text = text
                _select.addprevious(p_readonly)
                _select.getparent().remove(_select)
            for _button in fragment.iterfind(".//form[@action='/my/account']//button"):
                _button.getparent().remove(_button)
        return Markup("".join(html.tostring(f).decode() for f in fragments))
