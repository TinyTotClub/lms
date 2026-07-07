import json

import frappe


def filter_importable_doctypes(user):
	"""Filter DocTypes in the Data Import dropdown to LMS, Employee, and User doctypes."""
	lms_doctypes = frappe.get_all("DocType", filters={"module": "LMS"}, pluck="name")
	allowed_doctypes = ["User", "Employee"] + lms_doctypes

	return f"`tabDocType`.name in ({', '.join(repr(dt) for dt in allowed_doctypes)})"


@frappe.whitelist()
def search_link_override(
	doctype: str,
	txt: str,
	query: str | None = None,
	filters: str | dict | list | None = None,
	page_length: int = 10,
	searchfield: str | None = None,
	reference_doctype: str | None = None,
	ignore_user_permissions: bool = False,
	*,
	link_fieldname: str | None = None,
):
	"""Override search_link so the DocType picker in Data Import only offers allowed doctypes."""
	parsed_filters = filters
	if isinstance(filters, str):
		try:
			parsed_filters = json.loads(filters)
		except Exception:
			parsed_filters = {}

	if (
		doctype == "DocType"
		and parsed_filters
		and isinstance(parsed_filters, dict)
		and parsed_filters.get("allow_import") == 1
	):
		lms_doctypes = frappe.get_all("DocType", filters={"module": "LMS"}, pluck="name")
		allowed_doctypes = ["User", "Employee"] + lms_doctypes

		parsed_filters["name"] = ["in", allowed_doctypes]
		filters = json.dumps(parsed_filters)

	from frappe.desk.search import search_link as original_search_link

	return original_search_link(
		doctype=doctype,
		txt=txt,
		query=query,
		filters=filters,
		page_length=page_length,
		searchfield=searchfield,
		reference_doctype=reference_doctype,
		ignore_user_permissions=ignore_user_permissions,
		link_fieldname=link_fieldname,
	)
