# Copyright (c) 2025, Nesscale Solutions Pvt Ltd and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate, nowdate

class THTask(Document):
	def validate(self):
		if self.status not in ("Open", "In Progress", "Completed", "Overdue"):
			frappe.throw(_("Invalid Status"))
		self.validate_overdue()
		self.enforce_checklist()
		self.stamp_completion()

	def validate_overdue(self):
		if not self.due_date or self.status == "Completed":
			return
		today = getdate(nowdate())
		due = getdate(self.due_date)
		if self.status in ("Open", "In Progress") and due < today:
			self.status = "Overdue"
		if self.status == "Overdue" and due >= today:
			self.status = "Open"

	def enforce_checklist(self):
		if not int(self.has_checklist or 0):
			return
		rows = self.get("th_task_checklist_details") or []
		if not rows:
			frappe.throw(_("Checklist is required"))
		all_done = all(bool(getattr(r, "completed", 0)) for r in rows)
		if self.status == "Completed" and not all_done:
			frappe.throw(_("Complete all checklist items before marking as Completed"))
		if all_done and self.status in ("Open", "In Progress", "Overdue"):
			self.status = "Completed"

	def stamp_completion(self):
		if self.status == "Completed":
			if not self.date_of_completion:
				self.date_of_completion = nowdate()
			if self.due_date and self.date_of_completion:
				self.timeliness = "Ontime" if getdate(self.date_of_completion) <= getdate(self.due_date) else "Late"
		else:
			self.timeliness = None

	@frappe.whitelist()
	def mark_completed(self):
		if self.status not in ("Open", "In Progress", "Overdue"):
			frappe.throw(_("Only Open, In Progress or Overdue tasks can be marked Completed"))
		self.enforce_checklist()
		self.status = "Completed"
		self.save(ignore_permissions=True)
	
	@frappe.whitelist()
	def fetch_checklist(self):
		self.th_task_checklist_details = []
		if not self.checklist_template:
			return
		checklist_doc = frappe.get_doc("TH Task Checklist Template", self.checklist_template)
		for row in checklist_doc.th_task_checklist_template_details:
			self.append("th_task_checklist_details", {
				"checklist_item": row.checklist_item
			})
