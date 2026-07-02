import frappe
from frappe import _


def employee_doctype_exists() -> bool:
	"""The Employee doctype ships with HRMS/ERPNext and may be absent on a pure-LMS bench."""
	return bool(frappe.db.exists("DocType", "Employee"))


def require_employee_doctype() -> None:
	if not employee_doctype_exists():
		frappe.throw(_("This feature requires the Employee doctype. Install HRMS to enable it."))
