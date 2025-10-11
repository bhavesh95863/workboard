# Copyright (c) 2025, Nesscale Solutions Pvt Ltd and contributors
# For license information, please see license.txt

from datetime import date, timedelta

import frappe
from frappe import _


def execute(filters=None):
	filters = filters or {}
	days = int(filters.get("days") or 7)

	cols = [
		{"label": _("Date"), "fieldname": "date", "fieldtype": "Date", "width": 110},
		{"label": _("Created"), "fieldname": "created", "fieldtype": "Int", "width": 100},
		{"label": _("Completed"), "fieldname": "completed", "fieldtype": "Int", "width": 110},
	]

	end = date.today()
	start = end - timedelta(days=days - 1)

	data = []
	for i in range(days):
		d = start + timedelta(days=i)
		d_start = f"{d} 00:00:00"
		d_end = f"{d} 23:59:59"

		created = frappe.db.count(
			"WB Task", filters=[["WB Task", "creation", ">=", d_start], ["WB Task", "creation", "<=", d_end]]
		)

		completed = frappe.db.count(
			"WB Task",
			filters=[
				["WB Task", "status", "=", "Completed"],
				["WB Task", "date_of_completion", ">=", d.strftime("%Y-%m-%d")],
				["WB Task", "date_of_completion", "<=", d.strftime("%Y-%m-%d")],
			],
		)

		data.append({"date": d, "created": created, "completed": completed})

	chart = {
		"data": {
			"labels": [str(r["date"]) for r in data],
			"datasets": [
				{"name": "Created", "values": [r["created"] for r in data]},
				{"name": "Completed", "values": [r["completed"] for r in data]},
			],
		},
		"type": "line",
		"height": 220,
	}

	return cols, data, None, chart
