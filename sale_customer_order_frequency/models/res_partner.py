from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    average_order_duration = fields.Float(
        string="Average Duration Between Orders",
        compute="_compute_order_frequency_stats",
        store=True,
        help="Average number of days between orders",
    )
    days_since_last_order = fields.Integer(
        compute="_compute_order_frequency_stats",
        store=True,
        help="Number of days since the last order",
    )
    days_until_next_order = fields.Integer(
        string="Days Before Next Order",
        compute="_compute_order_frequency_stats",
        store=True,
        help="Number of days before the next theoretical order",
    )

    @api.depends("sale_order_ids.date_order", "sale_order_ids.state")
    def _compute_order_frequency_stats(self):
        today = fields.Date.context_today(self)
        for partner in self:
            # We consider confirmed orders
            orders = (
                partner.sale_order_ids.sudo()
                .filtered(lambda o: o.state == "sale" and o.date_order)
                .sorted("date_order")
            )

            if not orders:
                partner.average_order_duration = 0.0
                partner.days_since_last_order = 0
                partner.days_until_next_order = 0
                continue

            last_order_date = orders[-1].date_order.date()
            partner.days_since_last_order = (today - last_order_date).days

            if len(orders) > 1:
                first_order_date = fields.first(orders).date_order.date()
                days_diff = (last_order_date - first_order_date).days
                avg_duration = days_diff / (len(orders) - 1)
                partner.average_order_duration = avg_duration

                # Calculation: Date last order + Avg Duration - Today
                # This is equivalent to: Avg Duration - Days since last order
                partner.days_until_next_order = int(
                    avg_duration - partner.days_since_last_order
                )
            else:
                partner.average_order_duration = 0.0
                partner.days_until_next_order = 0
