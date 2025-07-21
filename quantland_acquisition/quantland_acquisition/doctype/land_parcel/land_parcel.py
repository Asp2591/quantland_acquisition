# Copyright (c) 2025, Frappe Technologies and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class LandParcel(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		acquisition_status: DF.Literal["Identified", "Surveyed", "Valuated", "Notice Issued", "Objections Received", "Award Declared", "Compensation Paid", "Handed Over", "Cancelled"]
		current_owner: DF.Data | None
		date_of_survey: DF.Date | None
		date_of_valuation: DF.Date | None
		district: DF.Link | None
		encumbrances: DF.SmallText | None
		estimated_value: DF.Data | None
		final_award_amount: DF.Data | None
		land_area: DF.Float
		land_area_uom: DF.Float
		land_type: DF.Literal["Agricultural", "Residential", "Commercial", "Barren", "Forest", "Government Land"]
		linked_documents: DF.Attach | None
		naming_series: DF.Literal["Pl-"]
		plot_no: DF.Data | None
		project: DF.Link | None
		remarks: DF.SmallText | None
		state: DF.Link | None
		sub_district_taluka: DF.Data | None
		survey_number: DF.Data | None
		village_mouza: DF.Data | None
	# end: auto-generated types
	pass
