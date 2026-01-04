import frappe
from frappe import _
from frappe.utils import add_days, add_to_date, cint, getdate, nowdate, today

from workboard.utils import _context, _create_task_from_rule


def trigger_daily_rules():
	try:
		_run_recurring_rules()
		_run_offset_rules()
	except Exception:
		frappe.log_error(title=_("WorkBoard Error"), message=frappe.get_traceback())


def _run_recurring_rules():
	rules = frappe.get_all("WB Task Rule", filters={"enabled": 1, "recurring": 1}, fields=["*"])
	if not rules:
		return
	today_dt = getdate(today())
	selected = []
	for r in rules:
		if r.frequency == "Daily":
			selected.append(r)
		elif r.frequency == "Weekly" and today_dt.strftime("%A") == r.day_of_week:
			selected.append(r)
		elif r.frequency == "Fortnightly" and today_dt.strftime("%A") == r.day_of_week:
			# Check if it's a fortnightly occurrence (every 14 days)
			# We use a simple check: if the day number is in the first or third week of the month
			day_of_month = today_dt.day
			if (day_of_month <= 7) or (15 <= day_of_month <= 21):
				selected.append(r)
		elif r.frequency == "Monthly" and cint(today_dt.day) == cint(r.date_of_month):
			selected.append(r)
		elif r.frequency == "Quarterly" and cint(today_dt.day) == cint(r.date_of_month):
			# Quarterly: every 3 months (January, April, July, October)
			if today_dt.month in [1, 4, 7, 10]:
				selected.append(r)
		elif (
			r.frequency == "Yearly"
			and cint(today_dt.day) == cint(r.date_of_month)
			and cint(today_dt.month) == cint(r.month_of_year)
		):
			selected.append(r)
	for r in selected:
		try:
			_create_task_from_rule(r)
			frappe.db.commit()
		except Exception:
			frappe.log_error(title=_("WorkBoard Error"), message=frappe.get_traceback())


def _run_offset_rules():
	rules = frappe.get_all(
		"WB Task Rule",
		filters={
			"enabled": 1,
			"event": 1,
			"based_on": ["in", ["Days Before", "Days After"]],
		},
		fields=["*"],
	)
	for r in rules:
		for ref_doc in _docs_matching_offset_window(r):
			try:
				ctx = _context(ref_doc)
				if r.condition and not frappe.safe_eval(r.condition, None, ctx):
					continue
				_create_task_from_rule(r, context=ctx)
			except Exception:
				frappe.log_error(title=_("WorkBoard Error"), message=frappe.get_traceback())


def _docs_matching_offset_window(rule):
	out = []
	if not rule.reference_doctype or not rule.reference_date:
		return out
	if not frappe.db.has_column(rule.reference_doctype, rule.reference_date):
		return out
	diff = cint(rule.days_before_or_after or 0)
	if rule.based_on == "Days After":
		diff = -diff
	ref_date = add_to_date(nowdate(), days=diff)
	start = f"{ref_date} 00:00:00.000000"
	end = f"{ref_date} 23:59:59.000000"
	names = frappe.get_all(
		rule.reference_doctype,
		fields=["name"],
		filters=[
			[rule.reference_doctype, rule.reference_date, ">=", start],
			[rule.reference_doctype, rule.reference_date, "<=", end],
		],
	)
	for n in names:
		out.append(frappe.get_doc(rule.reference_doctype, n.name))
	return out


def update_task_status():
	names = frappe.get_all("WB Task", filters={"status": ["not in", ["Completed"]]}, pluck="name")
	for name in names:
		try:
			d = frappe.get_doc("WB Task", name)
			prev = d.status
			d.validate()
			if d.status != prev:
				d.save(ignore_permissions=True)
		except Exception:
			frappe.log_error(title=_("WorkBoard Status update error"), message=frappe.get_traceback())
