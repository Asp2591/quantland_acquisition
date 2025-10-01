# Copyright (c) 2025, Quantbit Tech and contributors
# For license information, please see license.txt
import frappe
from frappe import _
import json

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

@frappe.whitelist()
def get_print_html(filters):
    import json
    from frappe import _

    if isinstance(filters, str):
        filters = frappe._dict(json.loads(filters))
    else:
        filters = frappe._dict(filters)

    columns, data = execute(filters)

    print_columns = [
        {"label": _("जमिनदाराचे नाव"), "fieldname": "landholder"},
        {"label": _("गट क्रमांक"), "fieldname": "gut_number"},
        {"label": _("शेतीसाठी क्षेत्रफळ"), "fieldname": "cultivated_area"},
        {"label": _("पोट खराब"), "fieldname": "waste_area"},
        {"label": _("एकूण क्षेत्रफळ"), "fieldname": "total_area"},
        {"label": _("जमिनीची प्रतवारी"), "fieldname": "land_type"},
        {"label": _("ग्रुप क्रमांक"), "fieldname": "group_number"},
        {"label": _("७/१२ नुसार आकार"), "fieldname": "size_on_paper"},
        {"label": _("हेक्टेअर आकार"), "fieldname": "hectare_size"},
        {"label": _("जिल्हा स्तर समितीद्वारे हेक्टेअर दर"), "fieldname": "per_hectare_rate_by_district_level_committee"},
        {"label": _("संपादन करावयाचे क्षेत्र"), "fieldname": "affected_area"},
        {"label": _("संपादित जमिनीचे मूल्य"), "fieldname": "value_of_acquired_land"},
        {"label": _("गुणक"), "fieldname": "factor"},
        {"label": _("गुणकाद्वारे जमीन किंमत"), "fieldname": "land_price_by_factor"},
        {"label": _("झाडांवरील मूल्यांकन"), "fieldname": "trees"},
        {"label": _("विहीर/पाइपलाइनवरील मूल्यांकन"), "fieldname": "well_pipeline"},
        {"label": _("घरांवरील मूल्यांकन"), "fieldname": "houses"},
        {"label": _("इतर मूल्यांकन"), "fieldname": "others"},
        {"label": _("मालमत्तेचे मूल्यांकन (थेट खरेदी)"), "fieldname": "property_valuation_direct_purchase"},
        {"label": _("एकूण मूल्य (गुणक व थेट खरेदी)"), "fieldname": "factor_purchase_total"},
        {"label": _("१००% सवलत रक्कम"), "fieldname": "relief_amt"},
        {"label": _("एकूण रक्कम"), "fieldname": "grand_total"},
        {"label": _("अतिरिक्त रक्कम (२५% /12%) शासनाद्वारे"), "fieldname": "additional_amount_25_by_govt"},
        {"label": _("एकूण मोबदला रक्कम"), "fieldname": "total_renumeration"},
        {"label": _("वजावट रक्कम"), "fieldname": "deductible_amount"},
        {"label": _("मोबदला देय रक्कम"), "fieldname": "total_amount_of_compensation"},
        {"label": _("शेरा"), "fieldname": "remark"},
    ]
    
    filter_labels = [
        {"fieldname": "village_id", "label": _("गाव")},
        {"fieldname": "tehsil_id", "label": _("तालुका")},
        {"fieldname": "gut_name", "label": _("गट")},
        {"fieldname": "prakalp_id", "label": _("प्रकल्प")},
        {"fieldname": "aquisition_type", "label": _("संपादनाचा प्रकार")},
        {"fieldname": "date", "label": _("तारीख")},
    ]
    

    html = """
<html>
<head>
    <title>कंठी विभाग १ मूल्यांकन अहवाल</title>
    <style>
        @page { margin: 0; }
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; }
        h2 { text-align: center; margin: 10px 0; }
        .sub-header { text-align: center; margin: 5px 0; font-weight: bold; font-size: 12px; }
        table { width: 100%; border-collapse: collapse; font-size: 11px; margin: 0; }
        th, td { border: 1px solid #000; padding: 4px; text-align: center; vertical-align: top; }
        th { background-color: #f0f0f0; white-space: normal; word-wrap: break-word; }
        td { white-space: normal; word-wrap: break-word; }
        .filters-inline { font-size: 13px; display: inline-flex; gap: 40px; flex-wrap: wrap; margin-bottom: 10px;margin-left: 10px; }
        .filters-inline span { white-space: nowrap; }
        .filters-inline strong { margin-right: 5px; }
    </style>
</head>
<body>
<h2>कंठी विभाग १ मूल्यांकन अहवाल</h2>
<div class="sub-header">
मौजे कंठी ता. जत येथिल जमिन खजागी वाटघाटी द्वारे खरेदी करणेकामी निश्चित कर्नेत आलेला मुल्यंकन तक्ता<br>
प्रयोजन जात कळवा की.मी. 35 ते की.मी. 39, मौजे कंठी (भाग-1), मौजे कंठी, ता. जात, जी. सांगली<br>
मोबदला निश्चितीसाठी जिल्हास्तरीय समितीचा बैठकीचा दिनांक
</div>
<div class='filters-inline'>
"""

    for f in filter_labels:
        value = filters.get(f["fieldname"], "")
        if f["fieldname"] in ["village_id", "tehsil_id", "prakalp_id"]:
            if value:
                if f["fieldname"] == "village_id":
                    value = frappe.db.get_value("Village", value, "village_name") or value
                elif f["fieldname"] == "tehsil_id":
                    value = frappe.db.get_value("Tehsil", value, "tehsil_name") or value
                elif f["fieldname"] == "prakalp_id":
                    value = frappe.db.get_value("Prakalp", value, "prakalp_name") or value
        html += f"<span><strong>{f['label']}:</strong> {value}</span>"

    html += "</div>"

    html += "<table><tr>"
    for col in print_columns:
        html += f"<th>{col['label']}</th>"
    html += "</tr>"

    for row in data:
        html += "<tr>"
        for col in print_columns:
            html += f"<td>{row.get(col['fieldname'], '')}</td>"
        html += "</tr>"

    html += """
</table>
<br><br><br>
<div style="display: flex; justify-content: space-between; margin-top: 50px; width: 90%; margin-left:5%">
    <div style="text-align: center;">
        ___________________<br>
        उपविभागीय अभियंता
    </div>
    <div style="text-align: center;">
        ___________________<br>
        कार्यकारी अभियंता
    </div>
    <div style="text-align: center;">
        ___________________<br>
        उपविभागीय अधिकारी
    </div>
</div>
</body>
</html>
"""

    return html



def get_columns():
    return [
        {"label": _("प्रस्ताव आयडी"), "fieldname": "parent_docname", "fieldtype": "Link", "options": "Prastav"},
        {"label": _("गावाचे नाव"), "fieldname": "village_name", "fieldtype": "Data"},
        {"label": _("तहसीलचे नाव"), "fieldname": "tehsil_name", "fieldtype": "Data"},
        {"label": _("जिल्ह्याचे नाव"), "fieldname": "district_name", "fieldtype": "Data"},
        {"label": _("जमिनदाराचे नाव"), "fieldname": "landholder", "fieldtype": "Data"},
        {"label": _("गट क्रमांक"), "fieldname": "gut_number", "fieldtype": "Int"},
        {"label": _("गट नाव"), "fieldname": "gut_name", "fieldtype": "Link","options":"Gut Details"},
        {"label": _("ग्रुप क्रमांक"), "fieldname": "group_number", "fieldtype": "Data"},
        {"label": _("७/१२ नोंद"), "fieldname": "record", "fieldtype": "Data"},
        {"label": _("संपादनाचा प्रकार"), "fieldname": "aquisition_type", "fieldtype": "Data"},
        {"label": _("एकूण क्षेत्रफळ"), "fieldname": "total_area", "fieldtype": "Int"},
        {"label": _("शेतीसाठी क्षेत्रफळ"), "fieldname": "cultivated_area", "fieldtype": "Int"},
        {"label": _("पोट खराब"), "fieldname": "waste_area", "fieldtype": "Int"},
        {"label": _("संपादन करावयाचे क्षेत्र"), "fieldname": "affected_area", "fieldtype": "Int"},
        {"label": _("७/१२ नुसार आकार"), "fieldname": "size_on_paper", "fieldtype": "Data"},
        {"label": _("हेक्टेअर आकार"), "fieldname": "hectare_size", "fieldtype": "Int"},
        {"label": _("जमिनीची प्रतवारी"), "fieldname": "land_type", "fieldtype": "Data"},
        {"label": _("जिल्हा स्तर समितीद्वारे हेक्टेअर दर"), "fieldname": "per_hectare_rate_by_district_level_committee", "fieldtype": "Int"},
        {"label": _("संपादित जमिनीचे मूल्य"), "fieldname": "value_of_acquired_land", "fieldtype": "Int"},
        {"label": _("गुणक"), "fieldname": "factor", "fieldtype": "Int"},
        {"label": _("गुणकाद्वारे जमीन किंमत"), "fieldname": "land_price_by_factor", "fieldtype": "Int"},
        {"label": _("झाडांवरील मूल्यांकन"), "fieldname": "trees", "fieldtype": "Int"},
        {"label": _("विहीर/पाइपलाइनवरील मूल्यांकन"), "fieldname": "well_pipeline", "fieldtype": "Int"},
        {"label": _("घरांवरील मूल्यांकन"), "fieldname": "houses", "fieldtype": "Int"},
        {"label": _("इतर मूल्यांकन"), "fieldname": "others", "fieldtype": "Int"},
        {"label": _("मालमत्तेचे मूल्यांकन (थेट खरेदी)"), "fieldname": "property_valuation_direct_purchase", "fieldtype": "Int"},
        {"label": _("एकूण मूल्य (गुणक व थेट खरेदी)"), "fieldname": "factor_purchase_total", "fieldtype": "Int"},
        {"label": _("१००% सवलत रक्कम"), "fieldname": "relief_amt", "fieldtype": "Int"},
        {"label": _("एकूण रक्कम"), "fieldname": "grand_total", "fieldtype": "Int"},
        {"label": _("अतिरिक्त रक्कम (२५% / 12%) शासनाद्वारे"), "fieldname": "additional_amount_25_by_govt", "fieldtype": "Int"},
        {"label": _("एकूण मोबदला रक्कम"), "fieldname": "total_renumeration", "fieldtype": "Int"},
        {"label": _("वजावट रक्कम"), "fieldname": "deductible_amount", "fieldtype": "Int"},
        {"label": _("मोबदला देय रक्कम"), "fieldname": "total_amount_of_compensation", "fieldtype": "Int"},
        {"label": _("तारीख"), "fieldname": "date", "fieldtype": "Date"},
        {"label": _("शेरा"), "fieldname": "remark", "fieldtype": "Text"},
    ]

def get_data(filters):
    data = []

    status_filter = filters.get("status") or "Active"  
    conditions = "c.parentfield = 'prastav_details' AND p.status = %(status)s"
    values = {"status": status_filter}

    computed_gut_name = "CONCAT(IFNULL(v.village_name, ''), '-', IFNULL(c.gut_number, ''), '-', IFNULL(p.prastav_name, ''))"

    if filters.get("village_id"):
        conditions += " AND c.village_id = %(village_id)s"
        values["village_id"] = filters["village_id"]
    if filters.get("prakalp_id"):
        conditions += " AND p.prakalp_id = %(prakalp_id)s"
        values["prakalp_id"] = filters["prakalp_id"]
    if filters.get("tehsil_id"):
        conditions += " AND t.name = %(tehsil_id)s"
        values["tehsil_id"] = filters["tehsil_id"]
    if filters.get("gut_number"):
        conditions += " AND c.gut_number LIKE %(gut_number)s"
        values["gut_number"] = "%" + filters["gut_number"] + "%"
    if filters.get("aquisition_type"):
        conditions += " AND c.aquisition_type LIKE %(aquisition_type)s"
        values["aquisition_type"] = "%" + filters["aquisition_type"] + "%"
    if filters.get("gut_name"):
        conditions += f" AND {computed_gut_name} LIKE %(gut_name)s"
        values["gut_name"] = "%" + filters["gut_name"] + "%"
    if filters.get("date"):
        conditions += " AND p.date = %(date)s"
        values["date"] = filters["date"]

    rows = frappe.db.sql(f"""
        SELECT
            p.name AS parent_docname,
            p.prastav_name AS prastav_name,
            p.prakalp_id AS prakalp_id,
            v.village_name,
            t.tehsil_name,
            d.district_name,
            c.landholder,
            c.gut_number,
            c.group_number,
            c.record,
            c.aquisition_type,
            c.total_area,
            c.cultivated_area,
            c.waste_area,
            c.affected_area,
            c.size_on_paper,
            c.hectare_size,
            c.land_type,
            c.per_hectare_rate_by_district_level_committee,
            c.value_of_acquired_land,
            c.factor,
            c.land_price_by_factor,
            c.trees,
            c.well_pipeline,
            c.houses,
            c.others,
            c.property_valuation_direct_purchase,
            c.factor_purchase_total,
            c.relief_amt,
            c.grand_total,
            c.additional_amount_25_by_govt,
            c.total_renumeration,
            c.deductible_amount,
            c.total_amount_of_compensation,
            p.date,
            c.remark
        FROM `tabPrastav Details` c
        JOIN `tabPrastav` p ON c.parent = p.name
        LEFT JOIN `tabVillage` v ON c.village_id = v.name
        LEFT JOIN `tabTehsil` t ON v.tehsil_id = t.name
        LEFT JOIN `tabDistrict` d ON v.district_id = d.name
        WHERE {conditions}
        ORDER BY p.name, c.idx
    """, values=values, as_dict=True)

    for r in rows:
        data.append({
            "parent_docname": r.parent_docname,
            "prastav_name": r.prastav_name,
            "prakalp_name": r.prakalp_name,
            "village_name": r.village_name,
            "tehsil_name": r.tehsil_name,
            "district_name": r.district_name,
            "landholder": r.landholder,
            "gut_number": r.gut_number,
            "gut_name": f"{r.village_name or ''}-{r.gut_number or ''}-{r.prastav_name or ''}",
            "group_number": r.group_number,
            "record": r.record,
            "aquisition_type": r.aquisition_type,
            "total_area": r.total_area,
            "cultivated_area": r.cultivated_area,
            "waste_area": r.waste_area,
            "affected_area": r.affected_area,
            "size_on_paper": r.size_on_paper,
            "hectare_size": r.hectare_size,
            "land_type": r.land_type,
            "per_hectare_rate_by_district_level_committee": r.per_hectare_rate_by_district_level_committee,
            "value_of_acquired_land": r.value_of_acquired_land,
            "factor": r.factor,
            "land_price_by_factor": r.land_price_by_factor,
            "trees": r.trees,
            "well_pipeline": r.well_pipeline,
            "houses": r.houses,
            "others": r.others,
            "property_valuation_direct_purchase": r.property_valuation_direct_purchase,
            "factor_purchase_total": r.factor_purchase_total,
            "relief_amt": r.relief_amt,
            "grand_total": r.grand_total,
            "additional_amount_25_by_govt": r.additional_amount_25_by_govt,
            "total_renumeration": r.total_renumeration,
            "deductible_amount": r.deductible_amount,
            "total_amount_of_compensation": r.total_amount_of_compensation,
            "date": r.date,
            "remark": r.remark
        })

    return data