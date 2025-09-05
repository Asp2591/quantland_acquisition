# Copyright (c) 2025, Quantbit Tech and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    """Return columns for the report."""
    return [
        {"label": _("Prastav ID"), "fieldname": "parent_docname", "fieldtype": "Link", "options": "Prastav"},
        {"label": _("Village Name"), "fieldname": "village_name", "fieldtype": "Data"},
        {"label": _("Tehsil Name"), "fieldname": "tehsil_name", "fieldtype": "Data"},
        {"label": _("District Name"), "fieldname": "district_name", "fieldtype": "Data"},
        {"label": _("Landholder"), "fieldname": "landholder", "fieldtype": "Data"},
        {"label": _("Gut Number"), "fieldname": "gut_number", "fieldtype": "Int"},
        {"label": _("7/12 Record"), "fieldname": "record", "fieldtype": "Data"},
        {"label": _("Acquisition Type"), "fieldname": "aquisition_type", "fieldtype": "Data"},
        {"label": _("Cultivated Area"), "fieldname": "cultivated_area", "fieldtype": "Float"},
        {"label": _("Affected Area"), "fieldname": "affected_area", "fieldtype": "Float"},
        {"label": _("Size on 7/12"), "fieldname": "size_on_paper", "fieldtype": "Data"},
        {"label": _("Group Number"), "fieldname": "group_number", "fieldtype": "Data"},
        {"label": _("Hectare Size"), "fieldname": "hectare_size", "fieldtype": "Float"},
        {"label": _("Land Type"), "fieldname": "land_type", "fieldtype": "Data"},
        {"label": _("Total Area"), "fieldname": "total_area", "fieldtype": "Float"},
        {"label": _("Land Size"), "fieldname": "land_size", "fieldtype": "Float"},
        {"label": _("Per Hectare Rate by District Level Committee"), "fieldname": "per_hectare_rate_by_district_level_committee", "fieldtype": "Currency"},
        {"label": _("Valuation on Trees"), "fieldname": "trees", "fieldtype": "Data"},
        {"label": _("Valuation on Well/pipeline"), "fieldname": "well_pipeline", "fieldtype": "Data"},
        {"label": _("Valuation on Houses"), "fieldname": "houses", "fieldtype": "Data"},
        {"label": _("Valuation on Others"), "fieldname": "others", "fieldtype": "Data"},

        {"label": _("Grand Total"), "fieldname": "grand_total", "fieldtype": "Data"},
        {"label": _("Value of Acquired Land"), "fieldname": "value_of_acquired_land", "fieldtype": "Currency"},
        {"label": _("Property Valuation (Direct Purchase)"), "fieldname": "property_valuation_direct_purchase", "fieldtype": "Float"},
        {"label": _("Additional Amount (25%) by Govt"), "fieldname": "additional_amount_25_by_govt", "fieldtype": "Data"},
        {"label": _("Factor"), "fieldname": "factor", "fieldtype": "Int"},
        {"label": _("Total Value (Factor and Direct Purchase)"), "fieldname": "factor_purchase_total", "fieldtype": "Data"},
        {"label": _("Total Renumeration Amount"), "fieldname": "total_renumeration", "fieldtype": "Data"},
        {"label": _("Land Price by Factor"), "fieldname": "land_price_by_factor", "fieldtype": "Currency"},
        {"label": _("100% Relief Amount"), "fieldname": "relief_amt", "fieldtype": "Data"},
        {"label": _("Total Amount of Compensation Payable"), "fieldname": "total_amount_of_compensation", "fieldtype": "Data"},
        {"label": _("Remarks"), "fieldname": "remark", "fieldtype": "Text"},
    ]


def get_data(filters):
    """Return data for the report from child table with Village → Tehsil → District names."""
    data = []
    conditions = ""
    values = {}

    if filters and filters.get("village_id"):
        conditions += " AND c.village_id = %(village_id)s"
        values["village_id"] = filters["village_id"]
        
    if filters and filters.get("subdivision_id"):
        conditions += " AND subdivision_id = %(subdivision_id)s"
        values["subdivision_id"] = filters["subdivision_id"]

    if filters and filters.get("date"):
        conditions += " AND p.date = %(date)s"
        values["date"] = filters["date"]

    rows = frappe.db.sql(f"""
        SELECT
            p.name AS parent_docname,
            v.village_name,
            t.tehsil_name,
            d.district_name,
            c.landholder,
            c.gut_number,
            c.record ,
            c.aquisition_type,
            c.cultivated_area,
            c.affected_area,
            c.size_on_paper,
            c.group_number,
            c.hectare_size,
            c.land_type,
            c.total_area,
            c.land_size,
            c.per_hectare_rate_by_district_level_committee,
            c.trees,
            c.well_pipeline,
            c.houses,
            c.others,
            c.grand_total,
            c.value_of_acquired_land,
            c.property_valuation_direct_purchase,
            c.additional_amount_25_by_govt,
            c.factor,
            c.factor_purchase_total ,
            c.total_renumeration,
            c.land_price_by_factor,
            c.relief_amt,
            c.total_amount_of_compensation,
            c.remark
        FROM `tabPrastav Details` c
        JOIN `tabPrastav` p ON c.parent = p.name
        LEFT JOIN `tabVillage` v ON c.village_id = v.name
        LEFT JOIN `tabTehsil` t ON v.tehsil_id = t.name
        LEFT JOIN `tabDistrict` d ON v.district_id = d.name
        WHERE c.parentfield = 'prastav_details' {conditions}
        ORDER BY p.name, c.idx
    """, values=values, as_dict=True)

    for r in rows:
        data.append([
            r.parent_docname,
            r.village_name,
            r.tehsil_name,
            r.district_name,
            r.landholder,
            r.gut_number,
            r.record,
            r.aquisition_type,
            r.cultivated_area,
            r.affected_area,
            r.size_on_paper,
            r.group_number,
            r.hectare_size,
            r.land_type,
            r.total_area,
            r.land_size,
            r.per_hectare_rate_by_district_level_committee,
            r.trees,
            r.well_pipeline,
            r.houses,
            r.others,
            r.grand_total,
            r.value_of_acquired_land,
            r.property_valuation_direct_purchase,
            r.additional_amount_25_by_govt,
            r.factor,
            r.factor_purchase_total,
            r.total_renumeration,
            r.land_price_by_factor,
            r.relief_amt,
            r.total_amount_of_compensation,
            r.remark
        ])
    
    return data
