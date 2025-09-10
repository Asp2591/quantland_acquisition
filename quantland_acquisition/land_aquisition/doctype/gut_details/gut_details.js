// Copyright (c) 2025, Quantbit Tech and contributors
// For license information, please see license.txt


frappe.ui.form.on('Gut Details', {
    gut_number: async frm => {
        await fetch_prastav_detail(frm);
        await set_gut_names(frm);
    },
    prastav_id: async frm => {
        await fetch_prastav_detail(frm);
        await set_gut_names(frm);
    },
    village_id: async frm => {
        await fetch_prastav_detail(frm);
        await set_gut_names(frm);
    },
    onload: frm => {
        frm.set_query("subdivision_id", function() {
            return {
                filters: {
                    "division_id": frm.doc.division_id
                }
            };
        });
    },
    current_stage: function(frm) {
        append_stage_history(frm);
    },
    stage_date: function(frm) {
        append_stage_history(frm);
    },
    srno: function(frm) {
        append_stage_history(frm);
    },
    onload: function(frm) {
        frm.set_df_property("attach", "hidden", 1);
    },
    purchase_deed: function(frm) {
        if(frm.doc.purchase_deed === "Available") {
            frm.set_df_property("attach", "hidden", 0); 
        } else {
            frm.set_df_property("attach", "hidden", 1);
        }
    }
});

async function fetch_prastav_detail(frm) {
    if (!frm.doc.prastav_id || !frm.doc.gut_number || !frm.doc.village_id) return;

    let prastav = await frappe.db.get_doc("Prastav", frm.doc.prastav_id);
    let d = (prastav.prastav_details || []).find(r =>
        String(r.gut_number).trim() === String(frm.doc.gut_number).trim() &&
        String(r.village_id).trim() === String(frm.doc.village_id).trim()
    ) || {};

    frm.set_value({
        total_area: d.total_area || 0,
        affected_area: d.affected_area || 0,
        waste_area: d.waste_area || 0,
        aquisition_type: d.aquisition_type || "",
        landholder: d.landholder || "",
        land_type: d.land_type || "",
        group_number: d.group_number || "",
        cultivated_area: d.cultivated_area || 0,
        size_on_paper: d.size_on_paper || 0,
        hectare_size: d.hectare_size || 0,
        per_hectare_rate_by_district_level_committee: d.per_hectare_rate_by_district_level_committee || 0,
        value_of_acquired_land: d.value_of_acquired_land || 0,
        factor: d.factor || "",
        land_price_by_factor: d.land_price_by_factor || "",
        private_acquisition_area: d.private_acquisition_area || "",
        property_valuation_direct_purchase: d.property_valuation_direct_purchase || "",
        total_value_factor_and_direct_purchase: d.factor_purchase_total || "",
        relief_amt: d.relief_amt || "",
        grand_total: d.grand_total || "",
        additional_amt: d.additional_amount_25_by_govt || "",
        total_renumeration_amount: d.total_renumeration || "",
        total_amount_of_compensation: d.total_amount_of_compensation || "",
        trees: d.trees || "",
        houses: d.houses || "",
        others: d.others || "",
        well_pipeline: d.well_pipeline || "",
        deductible_amount: d.deductible_amount || "",
        village_id: d.village_id
    });
}

async function set_gut_names(frm) {
    const { village_id, gut_number, prastav_id } = frm.doc;
    if (!village_id || !gut_number || !prastav_id) return;

    frm.set_value("gut", `${village_id}-${gut_number}-${prastav_id}`);

    const [p, v] = await Promise.all([
        frappe.db.get_value("Prastav", prastav_id, "prastav_name"),
        frappe.db.get_value("Village", village_id, "village_name")
    ]);

    let prastav_name = p.message?.prastav_name || "";
    let village_name = v.message?.village_name || "";

    if (prastav_name && village_name) {
        frm.set_value("gut_name", `${village_name}-${gut_number}-${prastav_name}`);
    }
}
function append_stage_history(frm) {
    if (frm.doc.current_stage && frm.doc.stage_date && frm.doc.srno) {
        let new_row = frm.add_child('stage_history');
        new_row.current_stage = frm.doc.current_stage;
        new_row.date = frm.doc.stage_date;
        new_row.srno = frm.doc.srno;

        frm.refresh_field('stage_history');

        
    }
}
