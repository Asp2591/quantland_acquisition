// Copyright (c) 2025, Quantbit Tech and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Gut Details", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on('Gut Details', {
    gut_number: function(frm) {
        fetch_prastav_detail(frm);
        fetch_names(frm);
    },
    prastav_id: function(frm) {
        fetch_prastav_detail(frm);
        fetch_prastav_detail_fields(frm);
        fetch_names(frm);
    }
});

function fetch_prastav_detail(frm) {
    if (!frm.doc.prastav_id || !frm.doc.gut_number) return;

    frappe.db.get_doc("Prastav", frm.doc.prastav_id).then(prastav => {
        let detail_row = (prastav.prastav_details || []).find(r =>
            String(r.gut_number).trim() === String(frm.doc.gut_number).trim()
        );

        if (detail_row) {
            frm.set_value("total_area", detail_row.total_area);
            frm.set_value("affected_area", detail_row.affected_area);
            frm.set_value("aquisition_type", detail_row.aquisition_type);
            frm.set_value("landholder", detail_row.landholder);
            frm.set_value("land_type", detail_row.land_type);
        } else {
            frm.set_value("total_area", 0);
            frm.set_value("affected_area", 0);
            frm.set_value("aquisition_type", "");
            frm.set_value("landholder", "");
            frm.set_value("land_type", "");
        }
    });
}

frappe.ui.form.on("Gut Details", {
    prastav_id: function(frm) { fetch_prastav_detail_fields(frm); },
    village_id: function(frm) { fetch_prastav_detail_fields(frm); },
    division_id: function(frm) { fetch_prastav_detail_fields(frm); },
    subdivision_id: function(frm) { fetch_prastav_detail_fields(frm); }
});

function fetch_names(frm) {
    if(frm.doc.prastav_id) {
        frappe.db.get_value('Prastav', frm.doc.prastav_id, 'prastav_name')
        .then(r => {
            let prastav_name = r.message ? r.message.prastav_name : '';
            update_gut_name_words(frm, prastav_name);
        });
    }

    if(frm.doc.village_id) {
        frappe.db.get_value('Village', frm.doc.village_id, 'village_name')
        .then(r => {
            let village_name = r.message ? r.message.village_name : '';
            update_gut_name_words(frm, null, village_name);
        });
    }
}

frappe.ui.form.on('Gut Details', {
    village_id: function(frm) {
        set_gut_name(frm);
        set_gut_name_words(frm);
    },
    gut_number: function(frm) {
        set_gut_name(frm);
        set_gut_name_words(frm);
    },
    prastav_id: function(frm) {
        set_gut_name(frm);
        set_gut_name_words(frm);
    }
});

function set_gut_name(frm) {
    if(frm.doc.village_id && frm.doc.gut_number && frm.doc.prastav_id) {
        frm.set_value('gut_name', frm.doc.village_id + '-' + frm.doc.gut_number + '-' + frm.doc.prastav_id);
    }
}

function set_gut_name_words(frm) {
    if (!frm.doc.village_id || !frm.doc.prastav_id || !frm.doc.gut_number) return;

    frappe.db.get_value('Village', frm.doc.village_id, 'village_name')
    .then(village_res => {
        let village_name = village_res.message ? village_res.message.village_name : '';

        frappe.db.get_value('Prastav', frm.doc.prastav_id, 'prastav_name')
        .then(prastav_res => {
            let prastav_name = prastav_res.message ? prastav_res.message.prastav_name : '';

            if(village_name && prastav_name) {
                frm.set_value('gut_name_words', village_name + '-' + frm.doc.gut_number + '-' + prastav_name);
            }
        });
    });
}
