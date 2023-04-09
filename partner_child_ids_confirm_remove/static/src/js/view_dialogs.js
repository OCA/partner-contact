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

                var def = new Promise(function (resolve, reject) {
                    var message = _t(
                        "Confirming this will delete child contact from database. Do you still want to proceed?"
                    );
                    Dialog.confirm(self, message, {
                        title: _t("Warning"),
                        confirm_callback: function () {
                            resolve(self.on_remove());
                            self.close();
                        },
                        cancel_callback: reject,
                    }).on("closed", self, reject);
                });
                return def;
            }
            // Classic workflow if model is not res.partner
            return Promise.resolve(this.on_remove());
        },
    });
});
