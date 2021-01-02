# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "frappe_nextcloud"
app_title = "Frappe Nextcloud"
app_publisher = "Agile Shift"
app_description = "Frappe & ERPNext Integrations: NextCloud CardDav"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "contacto@gruporeal.org"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/frappe_nextcloud/css/frappe_nextcloud.css"
# app_include_js = "/assets/frappe_nextcloud/js/frappe_nextcloud.js"

# include js, css files in header of web template
# web_include_css = "/assets/frappe_nextcloud/css/frappe_nextcloud.css"
# web_include_js = "/assets/frappe_nextcloud/js/frappe_nextcloud.js"

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

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "frappe_nextcloud.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "frappe_nextcloud.install.before_install"
# after_install = "frappe_nextcloud.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "frappe_nextcloud.notifications.get_notification_config"

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

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"frappe_nextcloud.tasks.all"
# 	],
# 	"daily": [
# 		"frappe_nextcloud.tasks.daily"
# 	],
# 	"hourly": [
# 		"frappe_nextcloud.tasks.hourly"
# 	],
# 	"weekly": [
# 		"frappe_nextcloud.tasks.weekly"
# 	]
# 	"monthly": [
# 		"frappe_nextcloud.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "frappe_nextcloud.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "frappe_nextcloud.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "frappe_nextcloud.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

