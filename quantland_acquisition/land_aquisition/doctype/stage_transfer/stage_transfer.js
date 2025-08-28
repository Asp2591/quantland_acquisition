// Copyright (c) 2025, Quantbit Tech and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Stage Transfer", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on('Stage Transfer', {
    prastav_id: function(frm) {
        if (!frm.doc.prastav_id) return;

        frappe.db.get_doc("Prastav", frm.doc.prastav_id).then(prastav => {
            frm._available_villages = (prastav.prastav_details || []).map(r => ({
                village_id: r.village_id,
                village_name: r.village_name
            }));
        });
    }
});

frappe.ui.form.on('Stage Transfer Details', {
    village_id: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (!frm.doc.prastav_id || !row.village_id) return;

        frappe.db.get_doc("Prastav", frm.doc.prastav_id).then(prastav => {
            let detail_row = (prastav.prastav_details || []).find(r =>
                String(r.village_id).trim() === String(row.village_id).trim()
            );

            if (detail_row) {
                row.village_name = detail_row.village_name;
                row.gut_number = detail_row.gut_number;
                row.total_area = detail_row.total_area;
                row.affected_area = detail_row.affected_area;
                row.aquisition_type = detail_row.aquisition_type;
                row.landholder = detail_row.landholder;
                row.land_type = detail_row.land_type;

                frm.refresh_field('stage_transfer_details');
            } else {
                row.village_name = '';
                row.gut_number = '';
                row.total_area = 0;
                row.affected_area = 0;
                row.aquisition_type = '';
                row.landholder = '';
                row.land_type = '';
                frm.refresh_field('stage_transfer_details');
            }
        });
    }
});
