// Copyright (c) 2025, Quantbit Tech and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Prastav", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on("Prastav", {
    upload_child_data: function(frm) {
        // handle CSV upload if needed
    },
    village_id: function(frm) {
        fetch_prastav_details(frm);
    },
    prastav_id: function(frm) {
        fetch_prastav_details(frm);
    },
    // after_save: function(frm) {
    //     frm.doc.prastav_details.forEach(row => {
    //         if (!row.gut_number || !row.village_id) return;
    //         frappe.db.exists('Gut Details', row.gut_number).then(exists => {
    //             if (!exists) {
    //                 frappe.throw(`Gut Details created: ${row.gut_number}`);
    //             } else {
    //                 frappe.msgprint(`Gut Details already exists: ${row.gut_number}`);
    //             }
    //         });
    //     });
    // }
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

    factor_purchase_total:total_relief_amt,

    relief_amt:grand_total_amt_calc,
    grand_total:additional_perc_amt,

    additional_amount_25_by_govt:total_renum,
    
    deductible_amount:amount_of_compensation_calc,
    total_renumeration:amount_of_compensation_calc
});

function calculate_area(frm, cdt, cdn) {
    let row = frappe.get_doc(cdt, cdn);
    frappe.model.set_value(cdt, cdn, "total_area", (row.cultivated_area || 0) + (row.waste_area || 0));
}



function land_price_by_factor(frm, cdt, cdn) {
    let row = frappe.get_doc(cdt, cdn);
    frappe.model.set_value(cdt, cdn, "land_price_by_factor", (row.factor || 0) * (row.value_of_acquired_land || 0));
}

function direct_purchase_by_private_nego(frm, cdt, cdn) {
    let row = frappe.get_doc(cdt, cdn);
    frappe.model.set_value(
        cdt, cdn,
        "property_valuation_direct_purchase",
        (row.trees || 0) + (row.houses || 0) + (row.well_pipeline || 0) + (row.others || 0)
    );
}

function factor_plus_direct_purchase_amt(frm, cdt, cdn) {
    let row = frappe.get_doc(cdt, cdn);
    frappe.model.set_value(
        cdt, cdn,
        "factor_purchase_total",
        (row.land_price_by_factor || 0) + (row.property_valuation_direct_purchase || 0)
    );
}
function total_relief_amt(frm, cdt, cdn) {
    let row = frappe.get_doc(cdt, cdn);
    frappe.model.set_value(
        cdt, cdn,
        "relief_amt",
        (row.factor_purchase_total || 0)
    );
}
function grand_total_amt_calc(frm,cdt,cdn){
    let row=frappe.get_doc(cdt,cdn);
    frappe.model.set_value(
        cdt,cdn,
        "grand_total",
        (row.relief_amt||0)+(row.factor_purchase_total||0)
    )
}
function additional_perc_amt(frm,cdt,cdn){
    let row=frappe.get_doc(cdt,cdn);
    frappe.model.set_value(
        cdt,cdn,
        "additional_amount_25_by_govt",
        (row.grand_total||0)* 0.25
    )
}
function total_renum(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    frappe.model.set_value(
        cdt,
        cdn,
        "total_renumeration",
        (row.grand_total || 0)+(row.additional_amount_25_by_govt||0)
    );
}

function amount_of_compensation_calc(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    frappe.model.set_value(
        cdt,
        cdn,
        "total_amount_of_compensation",
        (row.total_renumeration || 0)-(row.deductible_amount||0)
    );
    frm.refresh_field("total_amount_of_compensation");

}
function fetch_prastav_details(frm) {
    if (!frm.doc.village_id || !frm.doc.prastav_id) {
        return;
    }

    frappe.db.get_doc('Prastav', frm.doc.prastav_id)
    .then(prastav => {
        if (prastav) {
            // frm.set_value('division_id', prastav.division_id || '');
            frm.set_value('subdivision_id', prastav.subdivision_id || '');
            frm.set_value('yojana_id', prastav.yojana_id || '');
        }
    })
    .catch(err => {
        frappe.msgprint(__('Could not fetch Prastav details'));
        console.error(err);
    });
}
frappe.ui.form.on('Prastav', {
    village_id: function(frm) {
        if (!frm.doc.village_id) return;

        frm.doc.prastav_details.forEach(row => {
            frappe.model.set_value(row.doctype, row.name, 'village_id', frm.doc.village_id);
        });

        frm.refresh_field('prastav_details');
    }
});

