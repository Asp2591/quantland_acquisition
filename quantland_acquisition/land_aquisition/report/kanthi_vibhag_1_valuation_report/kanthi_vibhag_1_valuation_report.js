// Copyright (c) 2025, Quantbit Tech and contributors
// For license information, please see license.txt

frappe.query_reports["Kanthi Vibhag 1 Valuation Report"] = {
    "filters": [
        {
            "fieldname": "subdivision_id",      
            "label": __("Subdivision"),         
            "fieldtype": "Link",                
            "options": "Subdivision"            
        },
        {
            "fieldname": "village_id",
            "label": __("Village ID"),
            "fieldtype": "Link",
            "options": "Village"
        },
         {
            "fieldname": "date",
            "label": __("Date"),
            "fieldtype": "Date",
            
        }
    ]
};

