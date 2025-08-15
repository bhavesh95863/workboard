# Copyright (c) 2025, Nesscale Solutions Pvt Ltd and contributors
# For license information, please see license.txt

import frappe
from datetime import date, timedelta

def execute(filters=None):
    filters = filters or {}
    days = int(filters.get("days") or 7)

    cols = [
        {"label": "Date", "fieldname": "date", "fieldtype": "Date", "width": 110},
        {"label": "Created", "fieldname": "created", "fieldtype": "Int", "width": 100},
        {"label": "Completed", "fieldname": "completed", "fieldtype": "Int", "width": 110},
    ]

    end = date.today()
    start = end - timedelta(days=days-1)

    data = []
    for i in range(days):
        d = start + timedelta(days=i)
        d_start = f"{d} 00:00:00"
        d_end = f"{d} 23:59:59"

        created = frappe.db.count(
            "TH Task",
            filters=[["TH Task", "creation", ">=", d_start], ["TH Task", "creation", "<=", d_end]]
        )

        completed = frappe.db.count(
            "TH Task",
            filters=[["TH Task", "status", "=", "Completed"],
                     ["TH Task", "date_of_completion", ">=", d.strftime("%Y-%m-%d")],
                     ["TH Task", "date_of_completion", "<=", d.strftime("%Y-%m-%d")]]
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
        "height": 220
    }

    return cols, data, None, chart

