# Copyright (c) 2025, Frappe Technologies and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class QLAProject(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		actual_expenditure: DF.Currency
		department: DF.Data | None
		description: DF.SmallText | None
		district: DF.Link | None
		end_date: DF.Date | None
		estimated_budget: DF.Currency
		estimated_land_area: DF.Float
		land_area_uom: DF.Literal["Acre", "Hectare", "Sq. Meter"]
		project_code: DF.Data | None
		project_name: DF.Data | None
		project_status: DF.Literal["Planning", "In Progress", "On Hold", "Completed", "Cancelled"]
		remarks: DF.SmallText | None
		start_date: DF.Date | None
		state: DF.Link | None
	# end: auto-generated types
	pass
