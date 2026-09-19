import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.SignUpForm = publicWidget.Widget.extend({
    selector: ".oe_signup_form",

    events: Object.assign({}, publicWidget.Widget.prototype.events, {
        'click input[name="company_type"]': "_onClickCompanyTypeInput",
    }),

    _onClickCompanyTypeInput: function () {
        if (this.$('input[id="company_type_person"]').prop("checked")) {
            this.$('input[id="name"]').prop("required", "");
            if (
                this.$('input[id="checkbox_config_firstname_required"]').prop("checked")
            ) {
                this.$('input[id="firstname"]').prop("required", "required");
            } else {
                this.$('input[id="firstname"]').prop("required", "");
            }
            if (
                this.$('input[id="checkbox_config_lastname_required"]').prop("checked")
            ) {
                this.$('input[id="lastname"]').prop("required", "required");
            } else {
                this.$('input[id="lastname"]').prop("required", "");
            }
            this.$(".field-name").hide();
            this.$(".field-firstname").show();
            this.$(".field-lastname").show();
        } else {
            this.$('input[id="name"]').prop("required", "required");
            this.$('input[id="firstname"]').prop("required", "");
            this.$('input[id="lastname"]').prop("required", "");

            this.$(".field-name").show();
            this.$(".field-firstname").hide();
            this.$(".field-lastname").hide();
        }
    },
});
