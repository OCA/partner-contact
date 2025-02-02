/** @odoo-module **/
import {registry} from "@web/core/registry";
import {Component, onWillStart, useState} from "@odoo/owl";
import {useService} from "@web/core/utils/hooks";

class MyDashboard extends Component {
    setup() {
        this.rpc = useService("rpc");
        this.action = useService("action");
        this.query_phone_number = useService("query_phone_number");
        this.state = useState({});

        onWillStart(async () => {
            this.query_phone_number.execute_query(this.env, this.rpc, this.action);
        });
    }
}

MyDashboard.template = "phone_query.phone_query_dashboard_template";
registry.category("actions").add("phone_query_dashboard", MyDashboard);
