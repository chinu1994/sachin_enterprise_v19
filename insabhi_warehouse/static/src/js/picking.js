/** @odoo-module **/

console.log("🚀 [Internal Location Filter] JS loaded");

import { patch } from "@web/core/utils/patch";
import { Many2OneField } from "@web/views/fields/many2one/many2one_field";

patch(Many2OneField.prototype, {
    getDomain() {
        let domain = super.getDomain?.();

        // 🔒 Always normalize domain
        if (!Array.isArray(domain)) {
            domain = [];
        }

        const record = this.props.record;

        console.log(
            "📌 getDomain",
            "model:", record?.resModel,
            "field:", this.props.name
        );

        // Only for stock.picking
        if (!record || record.resModel !== "stock.picking") {
            return domain;
        }

        // ✅ SAFE FIELD (always available)
        const pickingTypeCode = record.data?.picking_type_code;

        console.log("📦 Picking Type:", pickingTypeCode);

        if (!pickingTypeCode) {
            return domain;
        }

        // 🚚 Delivery Order → Source internal only
        if (
            pickingTypeCode === "outgoing" &&
            this.props.name === "location_id"
        ) {
            console.log("✅ Internal SOURCE (Delivery)");
            domain.push(["usage", "=", "internal"]);
        }

        // 📦 Receipt → Destination internal only
        if (
            pickingTypeCode === "incoming" &&
            this.props.name === "location_dest_id"
        ) {
            console.log("✅ Internal DESTINATION (Receipt)");
            domain.push(["usage", "=", "internal"]);
        }

        // 🔁 Internal Transfer → Both internal
        if (
            pickingTypeCode === "internal" &&
            ["location_id", "location_dest_id"].includes(this.props.name)
        ) {
            console.log("✅ Internal BOTH (Internal Transfer)");
            domain.push(["usage", "=", "internal"]);
        }

        console.log("🧪 Final domain:", domain);
        return domain;
    },
});
