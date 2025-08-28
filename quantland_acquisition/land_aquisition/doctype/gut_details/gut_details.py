# Copyright (c) 2025, Quantbit Tech and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


# class GutDetails(Document):
# 	pass
class GutDetails(Document):
    def validate(self):
        if self.village_id and self.gut_number and self.prastav_id:
            self.gut_name = f"{self.village_id}-{self.gut_number}-{self.prastav_id}"
            
        
