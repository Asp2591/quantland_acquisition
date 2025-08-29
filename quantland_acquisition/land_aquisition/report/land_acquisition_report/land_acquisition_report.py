# Copyright (c) 2025, Quantbit Tech and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": "Prastav ID", "fieldname": "prastav_id", "fieldtype": "Link", "options": "Prastav", "width": 150},
        {"label": "Village Name", "fieldname": "village_name", "fieldtype": "Data", "width": 150},
        {"label": "Acquisition Type", "fieldname": "aquisition_type", "fieldtype": "Select", "width": 150},
        {"label": "Gut Number", "fieldname": "gut_number", "fieldtype": "Int", "width": 100},
        {"label": "Affected Area", "fieldname": "affected_area", "fieldtype": "Data", "width": 120},
        {"label": "Payment Amount", "fieldname": "payment_amount", "fieldtype": "Currency", "width": 150},
        {"label": "Payment Remarks", "fieldname": "payment_remarks", "fieldtype": "Data", "width": 180},
        {"label": "Date", "fieldname": "date", "fieldtype": "Date", "width": 120},
        {"label": "Purchase Deed", "fieldname": "purchase_deed", "fieldtype": "Data", "width": 150},
        {"label": "Purchase Deed Date", "fieldname": "purchase_deed_date", "fieldtype": "Date", "width": 150},
        {"label": "7/12 Record", "fieldname": "record", "fieldtype": "Select", "options": "Yes\nNo", "width": 120},
        {"label": "Attachment", "fieldname": "attachment", "fieldtype": "Attach", "width": 150},
        {"label": "Remarks", "fieldname": "remarks", "fieldtype": "Data", "width": 200},
    ]

def get_data(filters):
    conditions = ""
    values = {}

    if filters.get("village_id"):
        conditions += " AND gd.village_id = %(village_id)s"
        values["village_id"] = filters["village_id"]


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
