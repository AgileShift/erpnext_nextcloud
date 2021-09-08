import frappe
from erpnext_nextcloud.erpnext_nextcloud.utils import execute_command_in_shell


@frappe.whitelist()
def sync_all():
    execute_command_in_shell('sync')


@frappe.whitelist()
def discover():
    execute_command_in_shell('discover', auto_yes=True)


@frappe.whitelist()
def create_config_file():
    doc = frappe.get_cached_doc('Nextcloud Settings')
    doc.create_config_file()
    return {}
