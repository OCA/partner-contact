openerp.partner_credit_limit_pos = function(instance) {
    instance.point_of_sale.PaymentScreenWidget.include({
        validate_order: function(options) {
            var self = this,
                order = this.pos.get('selectedOrder'),
                partner_id = order.get_client() ? order.get_client().id : false,
                super_ = this._super,
                args = arguments;

            // Only check if partner is set.
            if (partner_id) {
                var model = new instance.web.Model('res.partner');
                return model.call('credit_limit_reached', [[partner_id], order.getTotalTaxIncluded(), true]).then(
                    function(data) {
                        return super_.apply(self, args);
                    }).fail(
                    function(error, event) {
                        if (error.code == 200) {
                            self.pos_widget.screen_selector.show_popup('error-traceback', {
                                message: error.data.message,
                                comment: error.data.debug
                            });
                        }
                        event.preventDefault();
                    });
            } else {
                return this._super.apply(self, arguments);
            }
        },
    });
};
