from odoo import models


class ResPartner(models.Model):
    _inherit = "res.partner"

    def name_get(self):
        """Context has only_show_customer_id and not show_address,show_address_only,
        show_email,html_format then return list of tuple partner record
        """
        ctx = self._context.copy() or {}
        if (
            ctx.get("only_show_customer_id")
            and "show_address" not in ctx
            and "show_address_only" not in ctx
            and "show_email" not in ctx
            and "html_format" not in ctx
        ):
            res = []
            for record in self:
                res.append((record.id, str(record.id)))
            return res
        return super(ResPartner, self).name_get()

    def prepare_wizard_data(self):
        return {
            "group_by_name": True,
            "state": "option",
            "number_group": 0,
            "current_line_id": False,
            "line_ids": [],
            "partner_ids": [],
            "exclude_contact": True,
            "maximum_group": 0,
            "total_duplicates": 0,
            "duplicate_position": 0,
            "associate_contact": True,
            "contact_not_being_customer": True,
            "without_sales_orders": True,
        }

    def open_wizard_action(self):
        context = {}
        data = self.prepare_wizard_data()
        wizard = self.env["base.partner.merge.automatic.wizard"].create(data)
        wizard.with_context(context=context)._process_query(
            "select min(id), array_agg(id) from res_partner where id in %s"
            % (tuple(self.ids),),
            ignore_occurence=False,
        )
        return wizard._action_new_next_screen()
