# Copyright (c) 2025, Quantbit Tech and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Prastav(Document):
    def before_save(self):
        self.create_gut_doc()

    def create_gut_doc(self):
        for row in self.prastav_details:
            gut_number = row.gut_number
            village_name = row.village_name
            village_id = row.village_id

            if not gut_number or not village_id:
                continue

            prastav_name = self.prastav_name
            gut_name = f"{village_name}-{gut_number}-{prastav_name}"

            doc_values = {
                "gut_name": gut_name,
                "gut_number": gut_number,
                "village_name": village_name,
                "village_id": village_id,
                "prastav_name": prastav_name,
                "subdivision_id": self.subdivision_id,
                "division_id": self.divison_id,
                "yojana_id": self.yojana_id,
                "prastav_id": self.prastav_id,
                "total_area": row.total_area or 0,
                "affected_area": row.affected_area or 0,
                "waste_area": row.waste_area or 0,
                "aquisition_type": row.aquisition_type or "",
                "landholder": row.landholder or "",
                "land_type": row.land_type or "",
                "group_number": row.group_number or "",
                "cultivated_area": row.cultivated_area or 0,
                "size_on_paper": row.size_on_paper or 0,
                "hectare_size": row.hectare_size or 0,
                "per_hectare_rate_by_district_level_committee": row.per_hectare_rate_by_district_level_committee or 0,
                "value_of_acquired_land": row.value_of_acquired_land or 0,
                "factor": row.factor or "",
                "land_price_by_factor": row.land_price_by_factor or "",
                "property_valuation_direct_purchase": row.property_valuation_direct_purchase or "",
                "total_value_factor_and_direct_purchase": row.factor_purchase_total or "",
                "relief_amt": row.relief_amt or "",
                "grand_total": row.grand_total or "",
                "additional_amt": row.additional_amount_25_by_govt or "",
                "total_renumeration_amount": row.total_renumeration or "",
                "total_amount_of_compensation": row.total_amount_of_compensation or "",
                "trees": row.trees or "",
                "houses": row.houses or "",
                "others": row.others or "",
                "well_pipeline": row.well_pipeline or "",
                "deductible_amount": row.deductible_amount or ""
            }

            if not frappe.db.exists("Gut Details", gut_name):
                doc = frappe.new_doc("Gut Details")
                doc.update(doc_values)
                doc.insert()
                frappe.msgprint(f"Gut Details created: {gut_name}") 
            else:
                doc = frappe.get_doc("Gut Details", gut_name)
                doc.update(doc_values)
                doc.save()
                frappe.msgprint(f"Gut Details updated: {gut_name}") 
