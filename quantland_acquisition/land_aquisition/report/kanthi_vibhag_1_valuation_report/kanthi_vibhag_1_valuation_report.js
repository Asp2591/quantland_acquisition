frappe.query_reports["Kanthi Vibhag 1 Valuation Report"] = {
    "filters": [
        { "fieldname": "village_id", "label": __("गाव"), "fieldtype": "Link", "options": "Village" },
        { "fieldname": "tehsil_id", "label": __("तालुका"), "fieldtype": "Link", "options": "Tehsil" },
        { "fieldname": "gut_number", "label": __("गट क्रमांक"), "fieldtype": "Link", "options": "Gut Details" },
        { "fieldname": "aquisition_type", "label": __("संपादनाचा प्रकार"), "fieldtype": "Link","options":"Acquisition Type" },
        { "fieldname": "date", "label": __("तारीख"), "fieldtype": "Date" }
    ],

    onload: function(report) {
        report.page.add_inner_button(__('Print Report'), async function() {
            let filters = report.get_values();

            let r = await frappe.call({
                method: "quantland_acquisition.land_aquisition.report.kanthi_vibhag_1_valuation_report.kanthi_vibhag_1_valuation_report.get_print_html",
                args: { filters: filters }
            });

            if(r.message) {
                let printWindow = window.open('', '_blank');
                printWindow.document.write(r.message);
                printWindow.document.close();
                printWindow.focus();
                printWindow.print();
            }
        });
    }
};
