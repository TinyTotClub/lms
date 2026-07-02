def extend_bootinfo(bootinfo):
	"""Only surface the LMS app on the desk apps screen."""
	if "apps" in bootinfo:
		bootinfo["apps"] = [app for app in bootinfo["apps"] if app.get("name") == "frappe_lms"]
