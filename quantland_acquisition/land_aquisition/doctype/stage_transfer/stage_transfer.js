// Copyright (c) 2025, Quantbit Tech and contributors
// For license information, please see license.txt


frappe.ui.form.on('Stage Transfer', {
    prastav_id: function(frm) {
        if (!frm.doc.prastav_id) return;

        frappe.db.get_doc("Prastav", frm.doc.prastav_id).then(prastav => {
            frm._available_villages = (prastav.prastav_details || []).map(r => ({
                village_id: r.village_id,
                village_name: r.village_name
            }));
        });
    },
    new_stage: function(frm) {
        if (!frm.doc.new_stage) return;

        frm.doc.stage_transfer_details.forEach(row => {
            frappe.model.set_value(row.doctype, row.name, 'new_stage', frm.doc.new_stage);
        });
        frm.refresh_field('stage_transfer_details');
    },
    gut_name: function(frm) {
    if (!frm.doc.gut_name) return;

    frappe.db.get_value("Gut Details", frm.doc.gut_name, "current_stage")
        .then(r => {
            if (r && r.message) {
                frm.set_value("new_stage", r.message.current_stage);
                console.log("current_stage:", r.message.current_stage, "new_stage:", frm.doc.new_stage);
            }
        });
    }
});

frappe.ui.form.on('Stage Transfer Details', {
    gut_number: function(frm, cdt, cdn) {
        auto_fill_by_gut(frm, cdt, cdn);
    }
});

function auto_fill_by_gut(frm, cdt, cdn) {
    let row = locals[cdt][cdn];

    if (!frm.doc.prastav_id || !row.gut_number) return;

    frappe.db.get_doc("Prastav", frm.doc.prastav_id).then(prastav => {
        let detail_row = (prastav.prastav_details || []).find(r =>
            String(r.gut_number).trim() === String(row.gut_number).trim()
        );

        if (detail_row) {
            frappe.model.set_value(cdt, cdn, 'village_id', detail_row.village_id);
            frappe.model.set_value(cdt, cdn, 'village_name', detail_row.village_name);
            frappe.model.set_value(cdt, cdn, 'total_area', detail_row.total_area);
            frappe.model.set_value(cdt, cdn, 'affected_area', detail_row.affected_area);
            frappe.model.set_value(cdt, cdn, 'aquisition_type', detail_row.aquisition_type);
            frappe.model.set_value(cdt, cdn, 'landholder', detail_row.landholder);
            frappe.model.set_value(cdt, cdn, 'land_type', detail_row.land_type);
        } else {
            frappe.model.set_value(cdt, cdn, 'village_id', '');
            frappe.model.set_value(cdt, cdn, 'village_name', '');
            frappe.model.set_value(cdt, cdn, 'total_area', 0);
            frappe.model.set_value(cdt, cdn, 'affected_area', 0);
            frappe.model.set_value(cdt, cdn, 'aquisition_type', '');
            frappe.model.set_value(cdt, cdn, 'landholder', '');
            frappe.model.set_value(cdt, cdn, 'land_type', '');
        }
    });
}
