import frappe
from frappe import _
from frappe.utils import getdate, nowdate, add_days, cint
from frappe.utils.safe_exec import get_safe_globals

def _create_th_task_from_rule(rule, context=None):
	title = rule.title or _("Task")
	description = frappe.render_template(rule.description, context) if (rule.description and context) else (rule.description or "")
	doc = frappe.get_doc({
		"doctype": "TH Task",
		"title": title,
		"description": description,
		"priority": rule.priority,
		"assign_from": rule.assign_from,
		"assign_to": rule.assign_to,
		"due_date": add_days(nowdate(), cint(rule.due_days or 0)),
		"status": "Open",
		"task_type": "Auto",
		"has_checklist": cint(rule.has_checklist or 0),
		"checklist_template": rule.checklist_template,
	})
	doc.fetch_checklist()
	doc.save(ignore_permissions=True)
	return doc

def _context(doc):
	return {"doc": doc, "nowdate": nowdate, "frappe": frappe._dict(utils=get_safe_globals().get("frappe").get("utils"))}
