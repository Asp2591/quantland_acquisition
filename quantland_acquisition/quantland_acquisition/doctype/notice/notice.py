# Copyright (c) 2025, Frappe Technologies and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Notice(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		delivery_method: DF.Literal["Post", "Hand Delivery", "Email"]
		description: DF.Text | None
		due_date: DF.Date | None
		issue_date: DF.Date | None
		land_parcel: DF.Link | None
		landholder: DF.Link | None
		linked_documents: DF.Attach | None
		naming_series: DF.Literal["NID-"]
		notice_type: DF.Literal["Section 4", "Section 6", "Award", "Possession"]
		project: DF.Link | None
		remarks: DF.SmallText | None
		status: DF.Literal["Issued", "Delivered", "Response Received", "Closed"]
	# end: auto-generated types
	pass
