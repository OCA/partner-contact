odoo.define("partner_child_ids_confirm_remove.partner_child_dialog_remove", function (
    require
) {
    "use strict";

    var core = require("web.core");
    var Dialog = require("web.Dialog");
    var ViewDialogs = require("web.view_dialogs");
    var _t = core._t;

    ViewDialogs.FormViewDialog.include({
        _remove: function () {
            if (this.res_model === "res.partner") {
                var self = this;
                var args = arguments;
                var _super = this._super;
                var def = new Promise(function (resolve, reject) {
                    var message = _t(
                        "Confirming this will delete child contact from database. Do you still want to proceed?"
                    );
                    Dialog.confirm(self, message, {
                        title: _t("Warning"),
                        confirm_callback: function () {
                            resolve(_super.apply(self, args));
                        },
                        cancel_callback: reject,
                    }).on("closed", self, reject);
                });
                return def;
            }
            return this._super.apply(this, arguments);
        },
    });
});
