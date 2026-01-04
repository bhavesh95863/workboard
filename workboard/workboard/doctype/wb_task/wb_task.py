# Copyright (c) 2025, Nesscale Solutions Pvt Ltd and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import get_datetime, getdate, now_datetime, nowdate

from workboard.utils import get_workboard_settings


class WBTask(Document):
	def validate(self):
		if self.status not in ("Open", "Done", "Completed", "Overdue"):
			frappe.throw(_("Invalid Status"))
		self.validate_overdue()
		self.enforce_checklist()
		self.stamp_completion()

	def validate_overdue(self):
		if not self.due_date or self.status in ("Done", "Completed"):
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
		rows = self.get("wb_task_checklist_details") or []
		if not rows:
			frappe.throw(_("Checklist is required"))
		all_done = all(bool(getattr(r, "completed", 0)) for r in rows)
		if self.status in ("Done", "Completed") and not all_done:
			frappe.throw(_("Complete all checklist items before marking as Done or Completed"))
		if all_done and self.status in ("Open", "In Progress", "Overdue"):
			self.status = "Done" if self.task_type == "Manual" else "Completed"

	def stamp_completion(self):
		if self.status == "Completed":
			if not self.date_of_completion:
				self.date_of_completion = nowdate()

			# Calculate timeliness based on whether task is time-based or not
			if int(self.depends_on_time or 0) and self.end_datetime:
				# For time-based tasks, compare completion datetime with end_datetime
				completion_datetime = (
					now_datetime() if not self.date_of_completion else get_datetime(self.date_of_completion)
				)
				end_dt = get_datetime(self.end_datetime)
				self.timeliness = "Ontime" if completion_datetime <= end_dt else "Late"
			elif self.due_date and self.date_of_completion:
				# For date-based tasks, compare completion date with due_date
				self.timeliness = (
					"Ontime" if getdate(self.date_of_completion) <= getdate(self.due_date) else "Late"
				)
		else:
			self.timeliness = None

	@frappe.whitelist()
	def mark_done(self):
		"""Mark task as Done by the assignee (task doer)"""
		if self.status not in ("Open", "Overdue"):
			frappe.throw(_("Only Open or Overdue tasks can be marked Done"))

		# Check if user has admin role
		settings = get_workboard_settings()
		admin_role = settings.get("workboard_admin_role")
		has_admin_role = admin_role and admin_role in frappe.get_roles(frappe.session.user)

		# Only assignee or admin role can mark done
		if (
			frappe.session.user != self.assign_to
			and frappe.session.user != "Administrator"
			and not has_admin_role
		):
			frappe.throw(_("Only the assigned user can mark this task as Done"))

		self.enforce_checklist()
		self.status = "Done"
		self.save(ignore_permissions=True)

	@frappe.whitelist()
	def mark_completed(self):
		"""Mark task as Completed - controlled by settings for Manual tasks"""
		# For Manual tasks, check settings to determine completion permissions
		if self.task_type == "Manual":
			if self.status != "Done":
				frappe.throw(_("Manual tasks must be marked as Done first before completion"))

			# Check WorkBoard Settings
			settings = get_workboard_settings()
			only_assignee_can_complete = settings.get("only_assignee_can_complete", 0)
			admin_role = settings.get("workboard_admin_role")

			current_user = frappe.session.user
			is_assignee = current_user == self.assign_to
			is_assigner = current_user == self.assign_from
			is_admin = current_user == "Administrator"
			has_admin_role = admin_role and admin_role in frappe.get_roles(current_user)

			if only_assignee_can_complete:
				# Only assignee or admin role can mark complete
				if not is_assignee and not is_admin and not has_admin_role:
					frappe.throw(_("Only the assigned user can mark this task as Completed"))
			else:
				# Only assigner or admin role can mark complete (approval workflow)
				if not is_assigner and not is_admin and not has_admin_role:
					frappe.throw(_("Only the task assigner can mark this task as Completed"))
		else:
			# For Auto tasks, allow direct completion
			if self.status not in ("Open", "Overdue"):
				frappe.throw(_("Only Open or Overdue tasks can be marked Completed"))

		self.status = "Completed"
		self.save(ignore_permissions=True)

	@frappe.whitelist()
	def fetch_checklist(self):
		self.wb_task_checklist_details = []
		if not self.checklist_template:
			return
		checklist_doc = frappe.get_doc("WB Task Checklist Template", self.checklist_template)
		for row in checklist_doc.wb_task_checklist_template_details:
			self.append("wb_task_checklist_details", {"checklist_item": row.checklist_item})
