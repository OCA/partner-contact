/* Copyright 2021 Tecnativa - David Vidal
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl). */

odoo.define("portal_partner_data_default.tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");
    var base = require("web_editor.base");

    var steps = [
        {
            trigger: "div.o_portal_my_details a:contains('Edit')",
        },
        {
            trigger: "input[name=name]",
            run: 'Mr. Odoo',
        },
        {
            trigger: "button[type=submit]",
        },
    ];
    tour.register("portal_partner_data_no_edit_default_tour",
        {
            url: "/my",
            test: true,
            wait_for: base.ready(),
        },
        steps
    );
    return {
        steps: steps,
    };
});

odoo.define("portal_partner_data_block.tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");
    var base = require("web_editor.base");

    var steps = [
        {
            trigger: "div.o_portal_my_details a:contains('View')",
        },
        {
            trigger: "p[name=name]",
        },
    ];
    tour.register("portal_partner_data_no_edit_block_tour",
        {
            url: "/my",
            test: true,
            wait_for: base.ready(),
        },
        steps
    );
    return {
        steps: steps,
    };
});
