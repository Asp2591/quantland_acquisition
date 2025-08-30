// Copyright (c) 2025, Quantbit Tech and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Gut Details", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on('Gut Details', {
    gut_number: frm => {
        fetch_prastav_detail(frm);
        set_gut_names(frm);
    },
    prastav_id: frm => {
        fetch_prastav_detail(frm);
        set_gut_names(frm);
    },
    village_id: frm => set_gut_names(frm)
});

function fetch_prastav_detail(frm) {
    if (!frm.doc.prastav_id || !frm.doc.gut_number) return;

    frappe.db.get_doc("Prastav", frm.doc.prastav_id).then(prastav => {
        let d = (prastav.prastav_details || []).find(r =>
            String(r.gut_number).trim() === String(frm.doc.gut_number).trim()
        ) || {};

        frm.set_value({
            total_area: d.total_area || 0,
            affected_area: d.affected_area || 0,
            aquisition_type: d.aquisition_type || "",
            landholder: d.landholder || "",
            land_type: d.land_type || "",
            
        });
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