import frappe
from frappe import _
from frappe.utils import parse_val

from workboard.utils import _context, _create_task_from_rule


def create_task_for_event(doc, method):
	try:
		if (
			(frappe.flags.in_import and frappe.flags.mute_emails)
			or frappe.flags.in_patch
			or frappe.flags.in_install
		):
			return
		event = _map_method_to_based_on(doc, method)
		if not event:
			return
		rules = frappe.get_all(
			"WB Task Rule",
			filters={
				"enabled": 1,
				"event": 1,
				"based_on": event,
				"reference_doctype": doc.doctype,
			},
			fields=["*"],
		)
		if not rules:
			return
		ctx = _context(doc)
		for r in rules:
			if event == "Value Change":
				if not r.value_changed or not frappe.db.has_column(doc.doctype, r.value_changed):
					continue
				doc_before_save = doc.get_doc_before_save()
				field_value_before_save = doc_before_save.get(r.value_changed) if doc_before_save else None
				field_value_before_save = parse_val(field_value_before_save)
				if doc.get(r.value_changed) == field_value_before_save:
					continue
			if r.condition and not frappe.safe_eval(r.condition, None, ctx):
				continue
			_create_task_from_rule(r, context=ctx)
	except Exception:
		frappe.log_error(title=_("WorkBoard Error"), message=frappe.get_traceback())


def _map_method_to_based_on(doc, method):
	m = {"after_insert": "New", "after_save": "Save", "on_submit": "Submit", "on_cancel": "Cancel"}
	if not doc.flags.in_insert:
		m["on_change"] = "Value Change"
	return m.get(method)
