# Copyright (c) 2025, Quantbit Tech and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        # {"label": "Kalava Number", "fieldname": "kalava_number", "fieldtype": "Data", "width": 150},
        {"label": "Village Name", "fieldname": "village_name", "fieldtype": "Data", "width": 150},
        # {"label": "Sr. No.", "fieldname": "sr_no", "fieldtype": "Int", "width": 80},
        {"label": "Acquisition Type", "fieldname": "aquisition_type", "fieldtype": "Select", "width": 150},
        {"label": "Gut Number", "fieldname": "gut_number", "fieldtype": "Int", "width": 100},
        {"label": "Affected Area", "fieldname": "affected_area", "fieldtype": "Data", "width": 120},
        # {"label": "Amount (in Lakhs)", "fieldname": "amount", "fieldtype": "Currency", "width": 150},
        # {"label": "Payment Approved Ref", "fieldname": "payment_approved_ref", "fieldtype": "Data", "width": 180},
        # {"label": "Notice Date", "fieldname": "notice_date", "fieldtype": "Date", "width": 120},
        # {"label": "Document Number", "fieldname": "document_number", "fieldtype": "Int", "width": 120},
        # {"label": "Doc Submission Date", "fieldname": "doc_submission_date", "fieldtype": "Date", "width": 140},
        {"label": "7/12 Register", "fieldname": "record", "fieldtype": "Select", "options": "Yes\nNo", "width": 120},
        # {"label": "Available 7/12", "fieldname": "available_712", "fieldtype": "Select", "options": "Yes\nNo", "width": 120},
        # {"label": "Remarks", "fieldname": "remarks", "fieldtype": "Data", "width": 200},
    ]


def get_data(filters):
    conditions = ""
    values = {}

    if filters.get("subdivision_id"):
        conditions += " AND gd.subdivision_id = %(subdivision_id)s"
        values["subdivision_id"] = filters["subdivision_id"]

    query = f"""
        SELECT 
            v.village_name,
            gd.aquisition_type,
            gd.gut_number,
            gd.affected_area,
            gd.record
        FROM `tabGut Details` gd
        LEFT JOIN `tabVillage` v
        ON gd.village_id = v.name
        WHERE 1=1 {conditions}
    """

    return frappe.db.sql(query, values, as_dict=True)
