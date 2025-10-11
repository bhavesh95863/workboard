app_name = "workboard"
app_title = "WorkBoard"
app_publisher = "Nesscale Solutions Pvt Ltd"
app_description = "WorkBoard is a modern Work Management System that centralizes all your tasks — from one-off actions to recurring and event-triggered work — so your team can stay organized, productive, and on track."
app_email = "bhavesh@nesscale.com"
app_license = "agpl-3.0"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "workboard",
# 		"logo": "/assets/workboard/logo.png",
# 		"title": "WorkBoard",
# 		"route": "/workboard",
# 		"has_permission": "workboard.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/workboard/css/workboard.css"
# app_include_js = "/assets/workboard/js/workboard.js"

# include js, css files in header of web template
# web_include_css = "/assets/workboard/css/workboard.css"
# web_include_js = "/assets/workboard/js/workboard.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "workboard/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "workboard/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "workboard.utils.jinja_methods",
# 	"filters": "workboard.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "workboard.install.before_install"
# after_install = "workboard.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "workboard.uninstall.before_uninstall"
# after_uninstall = "workboard.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "workboard.utils.before_app_install"
# after_app_install = "workboard.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "workboard.utils.before_app_uninstall"
# after_app_uninstall = "workboard.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "workboard.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"*": {
		"after_insert": "workboard.events.handlers.create_task_for_event",
		"after_save": "workboard.events.handlers.create_task_for_event",
		"on_submit": "workboard.events.handlers.create_task_for_event",
		"on_cancel": "workboard.events.handlers.create_task_for_event",
		"on_change": "workboard.events.handlers.create_task_for_event",
	}
}

# Scheduled Tasks
# ---------------

scheduler_events = {
	"daily": ["workboard.background_jobs.trigger_daily_rules", "workboard.background_jobs.update_task_status"]
}

# scheduler_events = {
# 	"all": [
# 		"workboard.tasks.all"
# 	],
# 	"daily": [
# 		"workboard.tasks.daily"
# 	],
# 	"hourly": [
# 		"workboard.tasks.hourly"
# 	],
# 	"weekly": [
# 		"workboard.tasks.weekly"
# 	],
# 	"monthly": [
# 		"workboard.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "workboard.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "workboard.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "workboard.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["workboard.utils.before_request"]
# after_request = ["workboard.utils.after_request"]

# Job Events
# ----------
# before_job = ["workboard.utils.before_job"]
# after_job = ["workboard.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"workboard.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }
