# Copyright (c) 2022, Frappe and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class CourseInstructor(Document):
	pass


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def instructor_query(
	doctype: str,
	txt: str,
	searchfield: str,
	start: int,
	page_len: int,
	filters: dict | None,
):
	"""Limit the instructor picker to enabled users holding the LMS Trainer role."""
	Users = frappe.qb.DocType("User")
	HasRole = frappe.qb.DocType("Has Role")
	return (
		frappe.qb.from_(Users)
		.inner_join(HasRole)
		.on(HasRole.parent == Users.name)
		.where((HasRole.role == "LMS Trainer") & (Users.enabled == 1) & (Users.name.like(f"%{txt}%")))
		.select(Users.name, Users.full_name)
		.distinct()
		.orderby(Users.full_name)
		.limit(page_len)
		.offset(start)
	).run()
