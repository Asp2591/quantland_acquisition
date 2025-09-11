// Copyright (c) 2025, Quantbit Tech and contributors
// For license information, please see license.txt

frappe.ui.form.on("Prastav", {
    village_id: function(frm) {
        fetch_prastav_details(frm);

        if (!frm.doc.village_id) return;

        frm.doc.prastav_details.forEach(row => {
            frappe.model.set_value(row.doctype, row.name, 'village_id', frm.doc.village_id);
        });
        frm.refresh_field('prastav_details');
    },

    prastav_id: function(frm) {
        fetch_prastav_details(frm);
    },

    village_name: function(frm) {
        if (!frm.doc.village_name) return;

        frm.doc.prastav_details.forEach(row => {
            frappe.model.set_value(row.doctype, row.name, 'village_name', frm.doc.village_name);
        });
        frm.refresh_field('prastav_details');
    },
    

    
});

frappe.ui.form.on("Prastav Details", {
    cultivated_area: calculate_area,
    waste_area: calculate_area,

    value_of_acquired_land: land_price_by_factor,
    factor: land_price_by_factor,

    trees: direct_purchase_by_private_nego,
    houses: direct_purchase_by_private_nego,
    well_pipeline: direct_purchase_by_private_nego,
    others: direct_purchase_by_private_nego,

    property_valuation_direct_purchase: factor_plus_direct_purchase_amt,
    land_price_by_factor: factor_plus_direct_purchase_amt,

    factor_purchase_total: total_relief_amt,

    relief_amt: grand_total_amt_calc,
    grand_total: additional_perc_amt,

    additional_amount_25_by_govt: total_renum,

    deductible_amount: amount_of_compensation_calc,
    total_renumeration: amount_of_compensation_calc,
   
    landholder_type: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if(row.landholder_type === "1") {
            if(row.najarana_amount !== "Not Applicable") {
                frappe.model.set_value(cdt, cdn, "najarana_amount", "Not Applicable");
            }
            frm.set_df_property("najarana_amount", "read_only", 1, row.name);
        } else if(row.landholder_type === "2") {
            if(row.najarana_amount === "Not Applicable") {
                frappe.model.set_value(cdt, cdn, "najarana_amount", 0);
            }
            frm.set_df_property("najarana_amount", "read_only", 1, row.name);
        }
    }


});

function calculate_area(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    frappe.model.set_value(cdt, cdn, "total_area", (row.cultivated_area || 0) + (row.waste_area || 0));
}

function land_price_by_factor(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    frappe.model.set_value(cdt, cdn, "land_price_by_factor", (row.factor || 0) * (row.value_of_acquired_land || 0));
}

function direct_purchase_by_private_nego(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    frappe.model.set_value(
        cdt, cdn, "property_valuation_direct_purchase",
        (row.trees || 0) + (row.houses || 0) + (row.well_pipeline || 0) + (row.others || 0)
    );
}

function factor_plus_direct_purchase_amt(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    frappe.model.set_value(
        cdt, cdn, "factor_purchase_total",
        (row.land_price_by_factor || 0) + (row.property_valuation_direct_purchase || 0)
    );
}

function total_relief_amt(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    frappe.model.set_value(cdt, cdn, "relief_amt", (row.factor_purchase_total || 0));
}

function grand_total_amt_calc(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    frappe.model.set_value(cdt, cdn, "grand_total", (row.relief_amt || 0));
}

function additional_perc_amt(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    frappe.model.set_value(cdt, cdn, "additional_amount_25_by_govt", (row.grand_total || 0) * 0.25);
}

function total_renum(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    frappe.model.set_value(cdt, cdn, "total_renumeration", (row.grand_total || 0) + (row.additional_amount_25_by_govt || 0));
}

function amount_of_compensation_calc(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    frappe.model.set_value(
        cdt, cdn,
        "total_amount_of_compensation",
        (row.total_renumeration || 0) - (row.deductible_amount || 0)
    );
    frm.refresh_field("total_amount_of_compensation");
}

function fetch_prastav_details(frm) {
    if (!frm.doc.village_id) return;

    frm.set_value('subdivision_id', frm.doc.subdivision_id || '');
    frm.set_value('yojana_id', frm.doc.yojana_id || '');
}
// function set_child_readonly(frm) {
//     frm.doc.prastav_details.forEach(function(row) {
//         let grid = frm.fields_dict['prastav_details'].grid;
//         if(row.landholder_type === '1') {
//             row.amount = '';
//             grid.set_df_property('najarana_amount', 'read_only', 1);
//         } else if(row.landholder_type === '2') {
//             grid.set_df_property('najarana_amount', 'read_only', 0);
//         }
//     });
//     frm.refresh_field('prastav_details'); 
// }