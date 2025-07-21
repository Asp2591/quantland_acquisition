# Copyright (c) 2025, Frappe Technologies and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Landholder(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.quantland_acquisition.doctype.legal_heirs.legal_heirs import LegalHeirs
		from frappe.types import DF

		address: DF.SmallText | None
		adhaar: DF.Data | None
		amended_from: DF.Link | None
		bank_account_number: DF.Data | None
		bank_name: DF.Data | None
		contact_number: DF.Data | None
		date_of_birth: DF.Date | None
		email_id: DF.Data | None
		gender: DF.Literal["Male", "Female", "Other"]
		ifsc_code: DF.Data | None
		landholder_name: DF.Data | None
		landholder_type: DF.Literal["Individual", "Company", "Trust", "Government Entity"]
		legal_heirs: DF.Table[LegalHeirs]
		linked_land_parcels: DF.Link | None
		pan_number: DF.Data | None
	# end: auto-generated types
	pass
