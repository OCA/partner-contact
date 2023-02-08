import logging
from ast import literal_eval

from odoo import fields, models

_logger = logging.getLogger(__name__)


class MergePartnerAutomatic(models.TransientModel):
    _inherit = "base.partner.merge.automatic.wizard"

    total_duplicates = fields.Integer()
    duplicate_position = fields.Integer("Duplicate Contact Position")
    associate_contact = fields.Boolean(
        "Partner contacts associated to the contact", default=True
    )
    contact_not_being_customer = fields.Boolean(
        "A contact not being customer", default=True
    )
    without_sales_orders = fields.Boolean(default=True)
    group_by_domain_email = fields.Boolean("Domain Email")

    group_by_phone = fields.Boolean("Phone")
    group_by_mobile = fields.Boolean("Mobile")

    def _action_new_next_screen(self):
        self.invalidate_cache()
        values = {}
        context = {}
        if self.line_ids:
            current_line = self.line_ids[0]
            current_partner_ids = literal_eval(current_line.aggr_ids)[-2:]
            current_partner_ids.sort()

            orders = self.env["sale.order"].search(
                [("partner_id", "in", current_partner_ids)],
                order="date_order desc, id desc",
                limit=1,
            )
            if orders:
                first_partner_id = [orders[0].partner_id.id]
                new_current_partner_ids = list(
                    set(current_partner_ids) - set(first_partner_id)
                )
                current_partner_ids = first_partner_id + new_current_partner_ids
            values.update(
                {
                    "current_line_id": current_line.id,
                    "partner_ids": [(6, 0, current_partner_ids)],
                    "dst_partner_id": current_partner_ids[0],
                    "state": "selection",
                }
            )
            self.write(values)
            partner1 = self.env["res.partner"].browse(
                current_partner_ids[0]
            )  # self.partner_ids[0]
            partner2 = self.env["res.partner"].browse(
                current_partner_ids[1]
            )  # self.partner_ids[1]
            partner_last_order1 = self.env["sale.order"].search(
                [("partner_id", "=", partner1.id)],
                order="date_order desc, id desc",
                limit=1,
            )
            sale_order_date1 = False
            sale_order_num1 = False
            if partner_last_order1:
                sale_order_date1 = partner_last_order1.date_order
                sale_order_num1 = partner_last_order1.name
            partner_last_order2 = self.env["sale.order"].search(
                [("partner_id", "=", partner2.id)],
                order="date_order desc, id desc",
                limit=1,
            )
            sale_order_date2 = False
            sale_order_num2 = False
            if partner_last_order2:
                sale_order_date2 = partner_last_order2.date_order
                sale_order_num2 = partner_last_order2.name

            context = {
                "default_last_changes_date1": partner1.write_date,
                "default_last_changes_uid1": partner1.write_uid.id,
                "default_last_changes_date2": partner2.write_date,
                "default_last_changes_uid2": partner2.write_uid.id,
                "default_last_order1": sale_order_date1,
                "default_last_order2": sale_order_date2,
                "default_last_order_num1": sale_order_num1,
                "default_last_order_num2": sale_order_num2,
                "default_partner_ids": values["partner_ids"],
                "default_current_line_id": values["current_line_id"],
                "default_dst_partner_id": values["dst_partner_id"],
                "default_id1": partner1.id,
                "default_id2": partner2.id,
                "default_partner_id_1": partner1.id,
                "default_partner_id_2": partner2.id,
                "default_company_id": partner1.parent_id.id,
                "default_company_id2": partner2.parent_id.id,
                "default_company_name": partner1.company_name,
                "default_company_name2": partner2.company_name,
                "default_name": partner1.name,
                "default_name2": partner2.name,
                "default_email": partner1.email,
                "default_email2": partner2.email,
                "default_phone": partner1.phone,
                "default_phone2": partner2.phone,
                "default_mobile": partner1.mobile,
                "default_mobile2": partner2.mobile,
                "default_street": partner1.street,
                "default_street2": partner2.street,
                "default_street11": partner1.street2,
                "default_street22": partner2.street2,
                "default_zip": partner1.zip,
                "default_zip2": partner2.zip,
                "default_city": partner1.city,
                "default_city2": partner2.city,
                "default_state_id": partner1.state_id.id,
                "default_state_id2": partner2.state_id.id,
                "default_country_id": partner1.country_id.id,
                "default_country_id2": partner2.country_id.id,
                "default_vat_1": partner1.vat,
                "default_vat_2": partner2.vat,
                "default_is_company": partner1.is_company,
                "default_is_company2": partner2.is_company,
                "default_number_group": self.number_group,
                "default_partner_wizard_id": self.id,
                "default_state": "selection",
                "default_total_duplicates": self.total_duplicates,
                "default_duplicate_position": self.duplicate_position,
                "default_contact_type": partner1.type,
                "default_contact_type2": partner2.type,
            }
        else:
            values.update(
                {
                    "current_line_id": False,
                    "partner_ids": [],
                    "state": "finished",
                }
            )
            return
        return {
            "type": "ir.actions.act_window",
            "name": "Merge Contacts",
            "res_model": "merge.partner.manual.check",
            "view_mode": "form",
            "target": "new",
            "context": context,
        }

    def _generate_query(self, fields, maximum_group=100):
        pass

        text = [
            "SELECT min(id), array_agg(id)",
            "FROM res_partner",
        ]

        sub_query = (
            "substring(email from '@(.*)$') not in ('aikq.de','aol.com','aol.de','arcor.de',"
            "'bluewin.ch','compuserve.com','dismail.de','disroot.org','duck.com','email.de',"
            "'ewe.net','ewetel.net','fastmail.com','fastmail.de','fastmail.fm','fastmail.net',"
            "'free.fr','freenet.de','gmail.com','gmx.at','gmx.ch','gmx.com','gmx.de','gmx.eu',"
            "'gmx.fr','gmx.info','gmx.li','gmx.org','gmxpro.de','gmx-topmail.de',"
            "'googlemail.com','hotmail.ch','hotmail.co.uk','hotmail.com','hotmail.de',"
            "'hotmail.es','hotmail.fr','hotmail.it','hush.com','hushmail.com','icloud.com',"
            "'jpberlin.de','kabelmail.de','laposte.net','lavabit.com','librem.one',"
            "'live.co.uk','live.com','live.de','live.fr','live.nl','mac.com','mail.de',"
            "'mailbox.org','mailfence.com','me.com','meineinkauf.ch','msn.com',"
            "'mykolab.ch','mykolab.com','netcologne.de','online.de','onlinehome.de',"
            "'orange.fr','outlook.com','outlook.de','outlook.es','outlook.fr',"
            "'posteo.at','posteo.ch','posteo.co.uk','posteo.de','posteo.eu',"
            "'posteo.lu','posteo.net','posteo.org','proton.me','protommail.com',"
            "'protonmail.ch','pt.lu','riseup.net','runbox.com','secure.mailbox.org',"
            "'startmail.com','system.li','temp.mailbox.org','t-online.de',"
            "'tuta.io','tutamail.com','tutanota.com','tutanota.de','vodafone.de',"
            "'vodafonemail.de','wanadoo.fr','web.de','xs4all.nl','yahoo.ca','yahoo.co.uk',"
            "'yahoo.com','yahoo.de','yahoo.es','yahoo.fr','yahoo.it')"
        )

        for field in fields:
            if field == "domain_email":
                text.append("WHERE %s" % sub_query)

        return " ".join(text)

    def _process_query(self, query, ignore_occurence=True):
        """
        Execute the select request and write the result in this wizard
        """
        proxy = self.env["base.partner.merge.line"]

        models = self._compute_models()
        self._cr.execute(query)

        counter = 0
        total_duplicates = 0
        data = self._cr.fetchall()
        data = sorted(data, key=lambda x: len(x[1]))
        for min_id, aggr_ids in data:
            if models and self._partner_use_in(aggr_ids, models) and ignore_occurence:
                continue
            values = {
                "wizard_id": self.id,
                "min_id": min_id,
                "aggr_ids": aggr_ids,
            }
            # To ensure that the used partners are accessible by the user
            partners = self.env["res.partner"].search(
                [("id", "in", aggr_ids), ("email", "!=", False)]
            )
            if len(partners) >= 2:
                ordered_partners = self._get_ordered_partner(partners.ids)
                partner_ids = [partner.id for partner in ordered_partners]
                values["aggr_ids"] = partner_ids
                proxy.create(values)
                counter += 1
                total_duplicates += len(partner_ids) - 1

        values = {
            "state": "selection",
            "number_group": counter,
            "total_duplicates": total_duplicates,
            "duplicate_position": 1,
        }
        self.write(values)
        _logger.info("counter: %s", counter)

    def action_start_manual_process(self):
        self.ensure_one()
        context = dict(self._context.copy() or {}, active_test=False)
        groups = self._compute_selected_groupby()
        query = self._generate_query(groups, self.maximum_group)
        self.with_context(context=context)._process_query(query)
        return self._action_new_next_screen()
