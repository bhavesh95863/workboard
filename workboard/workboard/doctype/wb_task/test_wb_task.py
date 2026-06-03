# Copyright (c) 2025, Nesscale Solutions Pvt Ltd and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase
from frappe.utils import add_days, nowdate


class TestWBTask(IntegrationTestCase):
	def make_task(self, **overrides):
		values = {
			"doctype": "WB Task",
			"title": "Test Task",
			"priority": "Medium",
			"status": "Open",
			"due_date": add_days(nowdate(), 1),
			"description": "<p>Test</p>",
			"assign_from": "Administrator",
			"assign_to": "Administrator",
			"task_type": "Manual",
		}
		values.update(overrides)
		return frappe.get_doc(values)

	def make_checklist_template(self):
		name = "Test Checklist"
		if frappe.db.exists("WB Task Checklist Template", name):
			return frappe.get_doc("WB Task Checklist Template", name)
		template = frappe.get_doc(
			{
				"doctype": "WB Task Checklist Template",
				"checklist_name": name,
				"wb_task_checklist_template_details": [{"checklist_item": "Step 1"}],
			}
		)
		template.insert()
		return template

	def test_invalid_status_is_rejected(self):
		task = self.make_task(status="Pending")
		self.assertRaises(frappe.ValidationError, task.insert)

	def test_open_task_becomes_overdue_when_past_due(self):
		task = self.make_task(due_date=add_days(nowdate(), -1))
		task.insert()
		self.assertEqual(task.status, "Overdue")

	def test_overdue_task_reverts_to_open_when_due_in_future(self):
		task = self.make_task(status="Overdue", due_date=add_days(nowdate(), 2))
		task.insert()
		self.assertEqual(task.status, "Open")

	def test_checklist_required_when_enabled(self):
		template = self.make_checklist_template()
		task = self.make_task(has_checklist=1, checklist_template=template.name)
		self.assertRaises(frappe.ValidationError, task.insert)

	def test_completed_checklist_auto_marks_manual_task_done(self):
		template = self.make_checklist_template()
		task = self.make_task(has_checklist=1, checklist_template=template.name)
		task.append("wb_task_checklist_details", {"checklist_item": "Step 1", "completed": 1})
		task.insert()
		self.assertEqual(task.status, "Done")

	def test_completion_stamps_date_and_ontime(self):
		task = self.make_task()
		task.insert()
		task.status = "Completed"
		task.save()
		self.assertEqual(task.date_of_completion, nowdate())
		self.assertEqual(task.timeliness, "Ontime")

	def test_completion_marked_late_when_past_due(self):
		task = self.make_task(status="Completed", due_date=add_days(nowdate(), -2))
		task.insert()
		self.assertEqual(task.timeliness, "Late")

	def test_mark_done_then_completed_flow(self):
		task = self.make_task()
		task.insert()
		task.mark_done()
		self.assertEqual(task.status, "Done")
		task.mark_completed()
		self.assertEqual(task.status, "Completed")
