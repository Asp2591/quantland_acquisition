# Copyright (c) 2025, Frappe Technologies and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class CompensationRecord(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		amount_paid: DF.Currency
		balance_amount: DF.Currency
		land_parcel: DF.Link | None
		land_value_per_unit: DF.Currency
		landholder: DF.Link | None
		linked_documents: DF.Attach | None
		naming_series: DF.Literal["CID.####"]
		other_compensation_details: DF.Data | None
		payment_date: DF.Date | None
		payment_method: DF.Literal["Bank Transfer", "Cheque"]
		payment_status: DF.Literal["Pending", "Partially Paid", "Fully Paid", "On Hold)"]
		project: DF.Data | None
		r_r_package_amount: DF.Currency
		remarks: DF.SmallText | None
		solatium_amount: DF.Currency
		total_compensation_amount: DF.Currency
		total_land_value: DF.Currency
		transaction_id: DF.Data | None
		valuation_date: DF.Date | None
	# end: auto-generated types
	pass
