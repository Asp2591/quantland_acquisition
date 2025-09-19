
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

        (frm.doc.stage_transfer_details || []).forEach(row => {
            frappe.model.set_value(row.doctype, row.name, 'new_stage', frm.doc.new_stage);
        });
        frm.refresh_field('stage_transfer_details');
    },
    
    gut_name: function(frm) {
    if (!frm.doc.gut_name) return;

    frappe.db.get_value("Gut Details", frm.doc.gut_name, ["current_stage", "prastav_id","srno", "stage_date"])
        .then(r => {
            if (r && r.message) {
                frm.set_value("current_stage", r.message.current_stage);
                frm.set_value("srno", r.message.srno);
                frm.set_value("date", r.message.stage_date);
                frm.set_value("prastav_id", r.message.prastav_id);
                console.log(r.message,"current_stage:", r.message.current_stage, 
                            "srnno:", r.message.srno, 
                            "date:", r.message.stage_date, 
                            "new_stage:", frm.doc.new_stage);
            }
        });

    (frm.doc.stage_transfer_details || []).forEach(row => {
        frappe.model.set_value(row.doctype, row.name, 'gut_number', frm.doc.gut_name);
    });
    frm.refresh_field('stage_transfer_details');
}

});

frappe.ui.form.on('Stage Transfer Details', {
    stage_transfer_details_add: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];

        if (frm.doc.gut_name) {
            frappe.model.set_value(cdt, cdn, 'gut_number', frm.doc.gut_name);

            frappe.db.get_doc("Gut Details", frm.doc.gut_name).then(gut => {
                if (gut) {
                    frappe.model.set_value(cdt, cdn, 'village_id', gut.village_id || '');
                    frappe.model.set_value(cdt, cdn, 'village_name', gut.village_name || '');
                    frappe.model.set_value(cdt, cdn, 'total_area', gut.total_area || 0);
                    frappe.model.set_value(cdt, cdn, 'affected_area', gut.affected_area || 0);
                    frappe.model.set_value(cdt, cdn, 'acquisition_type', gut.aquisition_type || '');
                    frappe.model.set_value(cdt, cdn, 'landholder', gut.landholder || '');
                    frappe.model.set_value(cdt, cdn, 'land_type', gut.land_type || '');
                    frappe.model.set_value(cdt, cdn, 'current_stage', gut.current_stage || '');
                    frappe.model.set_value(cdt, cdn, '712_record', gut.record || '');
                }
            });
        }

        if (frm.doc.new_stage) {
            frappe.model.set_value(cdt, cdn, 'new_stage', frm.doc.new_stage);
        }
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
