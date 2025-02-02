/** @odoo-module **/
import {registry} from "@web/core/registry";

const execute_query = async function (env, rpc, action) {
    var hash = window.location.hash.substring(1);
    if (hash) {
        var params = $.deparam(hash);
        // Read hash arguments and search for phone_number hash arg
        if (params.phone_number) {
            // Get the closest domain for phone number
            const data = await rpc(`/queries/${params.phone_number}`, {
                model: "res.partner",
                operator: "ilike",
            });
            // Open the list view based on the best domain
            action.doAction({
                type: "ir.actions.act_window",
                name: env._t("Query Phone Numbers"),
                view_mode: "tree,kanban,form",
                res_model: "res.partner",
                views: [
                    [false, "list"],
                    [false, "kanban"],
                    [false, "form"],
                ],
                context: {res_partner_search_mode: "customer"},
                domain: data.domain,
            });
        }
    }
};

export const queryPhoneNumber = {
    dependencies: ["rpc", "action"],
    start(env, {rpc, action}) {
        // Watch change in url hash arguments
        window.addEventListener("hashchange", async () => {
            execute_query(env, rpc, action);
        });
        return {execute_query};
    },
};

registry.category("services").add("query_phone_number", queryPhoneNumber);
