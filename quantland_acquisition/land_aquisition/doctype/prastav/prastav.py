# Copyright (c) 2025, Quantbit Tech and contributors
# For license information, please see license.txt
import frappe
from frappe.model.document import Document

class Prastav(Document):
    def before_save(self):
        self.create_gut_doc()

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
            prastav_name = self.prastav_name
            subdivision_id=self.subdivision_id
            division_id=self.divison_id
            yojana_id=self.yojana_id
            prastav_id=self.prastav_id

            gut_name = f"{village_name}-{gut_number}-{prastav_name}"

            if not gut_number or not village_id:
                continue

            if not frappe.db.exists("Gut Details", gut_name):
                doc = frappe.new_doc("Gut Details")
                
                doc.name = str(gut_number)
                doc.gut_number = gut_number
                doc.village_name = village_name
                doc.prastav_name = prastav_name
                doc.gut_name = gut_name
                doc.subdivision_id=subdivision_id
                doc.yojana_id=self.yojana_id
                doc.division_id=division_id
                doc.prastav_id=self.prastav_id
                doc.total_area = row.total_area or 0
                doc.affected_area = row.affected_area or 0
                doc.waste_area = row.waste_area or 0
                doc.aquisition_type = row.aquisition_type or ""
                doc.landholder = row.landholder or ""
                doc.land_type = row.land_type or ""
                doc.group_number = row.group_number or ""
                doc.cultivated_area = row.cultivated_area or 0
                doc.size_on_paper = row.size_on_paper or 0
                doc.hectare_size = row.hectare_size or 0
                doc.per_hectare_rate_by_district_level_committee = row.per_hectare_rate_by_district_level_committee or 0
                doc.value_of_acquired_land = row.value_of_acquired_land or 0
                doc.factor = row.factor or ""
                doc.land_price_by_factor = row.land_price_by_factor or ""
                # doc.private_acquisition_area = row.private_acquisition_area or ""
                doc.property_valuation_direct_purchase = row.property_valuation_direct_purchase or ""
                doc.total_value_factor_and_direct_purchase = row.factor_purchase_total or ""
                doc.relief_amt = row.relief_amt or ""
                doc.grand_total = row.grand_total or ""
                doc.additional_amt = row.additional_amount_25_by_govt or ""
                doc.total_renumeration_amount = row.total_renumeration or ""
                doc.total_amount_of_compensation = row.total_amount_of_compensation or ""
                doc.trees = row.trees or ""
                doc.houses = row.houses or ""
                doc.others = row.others or ""
                doc.well_pipeline = row.well_pipeline or ""
                doc.deductible_amount = row.deductible_amount or ""
                doc.village_id = village_id

                # Insert the document into the database
                doc.insert(ignore_permissions=True)
                frappe.db.commit()

                frappe.msgprint(f"Gut Details created: {gut_name}")
            else:
                frappe.msgprint(f"Gut Details already exists: {gut_name}")


                doc.insert()
                
