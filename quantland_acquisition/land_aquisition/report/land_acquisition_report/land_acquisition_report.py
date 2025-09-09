# Copyright (c) 2025, Quantbit Tech and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": "प्रस्ताव क्रमांक", "fieldname": "prastav_id", "fieldtype": "Link", "options": "Prastav", "width": 150},
        {"label": "गावाचे नाव", "fieldname": "village_name", "fieldtype": "Data", "width": 150},
        {"label": "संपादनाचा प्रकार", "fieldname": "aquisition_type", "fieldtype": "Link","options":"Acquisition Type", "width": 150},
        {"label": "गट क्रमांक", "fieldname": "gut_number", "fieldtype": "Int", "width": 100},
        {"label": "संपदित करवयाचे क्षेत्र", "fieldname": "affected_area", "fieldtype": "Data", "width": 120},
        {"label": "मोबदला रक्कम निवाडा रक्कम", "fieldname": "payment_amount", "fieldtype": "Int", "width": 200},
        {"label": "मोबदला मंजूर संदर्भ", "fieldname": "payment_remarks", "fieldtype": "Data", "width": 180},
        {"label": "मोबदला मंजूर तारीख", "fieldname": "date", "fieldtype": "Date", "width": 120},
        {"label": "लाभधारकला सूचना दिनांकत्र", "fieldname": "purchase_deed", "fieldtype": "Data", "width": 150},
        {"label": "दस्त दिनांक", "fieldname": "purchase_deed_date", "fieldtype": "Date", "width": 150},
        {"label": "७/१२ नोंद झाली होय/नाही", "fieldname": "record", "fieldtype": "Select", "options": "Yes\nNo", "width": 200},
        {"label": "संलग्नक उपलब्ध आहे का", "fieldname": "attachment", "fieldtype": "Attach", "width": 150},
        {"label": "शेरा", "fieldname": "remarks", "fieldtype": "Data", "width": 200},
    ]


def get_data(filters):
    conditions = ""
    values = {}

    if filters.get("village_id"):
        conditions += " AND gd.village_id = %(village_id)s"
        values["village_id"] = filters["village_id"]

    if filters.get("subdivision_id"):
        conditions += " AND gd.subdivision_id = %(subdivision_id)s"
        values["subdivision_id"] = filters["subdivision_id"]

    if filters.get("date"):
        conditions += " AND gd.date = %(date)s"
        values["date"] = filters["date"]


    query = f"""
        SELECT 
            gd.prastav_id,
            v.village_name,
            gd.aquisition_type,
            gd.gut_number,
            gd.affected_area,
            gd.payment_amount,
            gd.payment_remarks,
            gd.date,
            gd.purchase_deed,
            gd.purchase_deed_date,
            gd.record,
            gd.attachment,
            gd.remarks
        FROM `tabGut Details` gd
        LEFT JOIN `tabVillage` v
            ON gd.village_id = v.name
        WHERE 1=1 {conditions}
    """

    return frappe.db.sql(query, values, as_dict=True)
