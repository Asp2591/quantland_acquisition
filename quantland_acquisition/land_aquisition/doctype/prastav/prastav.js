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
});

frappe.ui.form.on("Prastav Details", {
    aquisition_type: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        direct_purchase_by_private_nego(frm, cdt, cdn);
        if (row.aquisition_type === "खाजगी वाटाघाटी" || row.aquisition_type === "Dec 2013" || row.aquisition_type === "1894") {
            calculate_value_of_acquired_land(frm, cdt, cdn);
        }
    },

    cultivated_area: calculate_area,
    waste_area: calculate_area,

    affected_area: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (row.aquisition_type === "खाजगी वाटाघाटी" || row.aquisition_type === "Dec 2013" || row.aquisition_type === "1894") {
            calculate_value_of_acquired_land(frm, cdt, cdn);
        }
    },

    per_hectare_rate_by_district_level_committee: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (row.aquisition_type === "खाजगी वाटाघाटी" || row.aquisition_type === "Dec 2013" || row.aquisition_type === "1894") {
            calculate_value_of_acquired_land(frm, cdt, cdn);
        }
    },

    amt_collection: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (row.aquisition_type === "Dec 2013" || row.aquisition_type === "1894") {
            calculate_market_value(frm, cdt, cdn);
        }
    },

    value_of_acquired_land: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (row.aquisition_type === "खाजगी वाटाघाटी") {
            land_price_by_factor(frm, cdt, cdn);
        } else if (row.aquisition_type === "Dec 2013" || row.aquisition_type === "1894") {
            calculate_market_value(frm, cdt, cdn);
        }
    },

    market_value: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (row.aquisition_type === "Dec 2013" || row.aquisition_type === "1894") {
            land_price_by_factor(frm, cdt, cdn);
        }
    },

    factor: land_price_by_factor,

    trees: direct_purchase_by_private_nego,
    houses: direct_purchase_by_private_nego,
    well_pipeline: direct_purchase_by_private_nego,
    others: direct_purchase_by_private_nego,

    property_valuation_direct_purchase: factor_plus_direct_purchase_amt,

    factor_purchase_total: [set_relief_for_old, grand_total_amt_calc],

    relief_amt: grand_total_amt_calc,

    grand_total: additional_perc_amt,

    additional_amount_25_by_govt: total_renum,

    deductible_amount: amount_of_compensation_calc,
    total_renumeration: amount_of_compensation_calc,

    prastav_details_add: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (frm.doc.village_id) {
            frappe.model.set_value(cdt, cdn, 'village_id', frm.doc.village_id);
        }
    },
});

function calculate_area(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    frappe.model.set_value(cdt, cdn, "total_area", (row.cultivated_area || 0) + (row.waste_area || 0));
}

function calculate_value_of_acquired_land(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    frappe.model.set_value(cdt, cdn, "value_of_acquired_land", (row.affected_area || 0) * (row.per_hectare_rate_by_district_level_committee || 0));
    calculate_market_value(frm, cdt, cdn);
}

function calculate_market_value(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    frappe.model.set_value(cdt, cdn, "market_value", (row.amt_collection || 0) + (row.value_of_acquired_land || 0));
    land_price_by_factor(frm, cdt, cdn);
}

function land_price_by_factor(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    let base_value = (row.aquisition_type === "खाजगी वाटाघाटी") ? (row.value_of_acquired_land || 0) : (row.market_value || 0);
    let new_lpf = (row.factor || 0) * base_value;
    frappe.model.set_value(cdt, cdn, "land_price_by_factor", new_lpf);
    
    let new_property = (row.property_valuation_direct_purchase || 0);
    let new_fpt = new_lpf + new_property;
    frappe.model.set_value(cdt, cdn, "factor_purchase_total", new_fpt);
    
    let new_relief;
    if (row.aquisition_type === "खाजगी वाटाघाटी") {
        new_relief = new_lpf;
        frappe.model.set_value(cdt, cdn, "relief_amt", new_relief);
    } else if (row.aquisition_type === "Dec 2013" || row.aquisition_type === "1894") {
        new_relief = new_fpt;
        frappe.model.set_value(cdt, cdn, "relief_amt", new_relief);
    }
    
    let new_gt = new_fpt + (new_relief || (row.relief_amt || 0));
    frappe.model.set_value(cdt, cdn, "grand_total", new_gt);
    
    frm.refresh_field('prastav_details');
}

function direct_purchase_by_private_nego(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    frappe.model.set_value(
        cdt, cdn, "property_valuation_direct_purchase",
        (row.trees || 0) + (row.houses || 0) + (row.well_pipeline || 0) + (row.others || 0)
    );
    factor_plus_direct_purchase_amt(frm, cdt, cdn);
}

function factor_plus_direct_purchase_amt(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    let lpf = row.land_price_by_factor || 0;
    let property = row.property_valuation_direct_purchase || 0;
    let new_fpt = lpf + property;
    frappe.model.set_value(
        cdt, cdn, "factor_purchase_total",
        new_fpt
    );
    if (row.aquisition_type === "Dec 2013" || row.aquisition_type === "1894") {
        frappe.model.set_value(cdt, cdn, "relief_amt", new_fpt);
        frappe.model.set_value(cdt, cdn, "grand_total", new_fpt * 2); 
    } else if (row.aquisition_type === "खाजगी वाटाघाटी") {
        
        frappe.model.set_value(cdt, cdn, "grand_total", (lpf * 2) + property);
    }
    frm.refresh_field('prastav_details');
}

function total_relief_amt(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    if (row.aquisition_type === "खाजगी वाटाघाटी") {
        frappe.model.set_value(cdt, cdn, "relief_amt", (row.land_price_by_factor || 0));
    }
}

function set_relief_for_old(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    if (row.aquisition_type === "Dec 2013" || row.aquisition_type === "1894") {
        frappe.model.set_value(cdt, cdn, "relief_amt", (row.factor_purchase_total || 0));
    }
}

function grand_total_amt_calc(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    let gt = (row.factor_purchase_total || 0) + (row.relief_amt || 0);
    frappe.model.set_value(cdt, cdn, "grand_total", gt);
    frm.refresh_field('prastav_details');
}

function additional_perc_amt(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    frappe.model.set_value(cdt, cdn, "additional_amount_25_by_govt", (row.grand_total || 0)*0.25);
}

function total_renum(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    let tr;
    if (row.aquisition_type === "Dec 2013" || row.aquisition_type === "1894") {
        tr = (row.relief_amt || 0) + (row.additional_amount_25_by_govt || 0) + (row.factor_purchase_total || 0);
    } else {
        tr = (row.grand_total || 0) + (row.additional_amount_25_by_govt || 0);
    }
    frappe.model.set_value(cdt, cdn, "total_renumeration", tr);
}

function amount_of_compensation_calc(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    frappe.model.set_value(
        cdt, cdn,
        "total_amount_of_compensation",
        (row.total_renumeration || 0) - (row.deductible_amount || 0)
    );
    frm.refresh_field('prastav_details');
}

function fetch_prastav_details(frm) {
    if (!frm.doc.village_id) return;

    frm.set_value('subdivision_id', frm.doc.subdivision_id || '');
    frm.set_value('yojana_id', frm.doc.yojana_id || '');
}