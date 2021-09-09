import shutil

import frappe
from erpnext_nextcloud.erpnext_nextcloud.vdirsyncer import execute_command_in_shell, get_vdirsyncer_address_book_path


@frappe.whitelist()
def sync_all():
    execute_command_in_shell('sync')
    return {}


@frappe.whitelist()
def discover():
    execute_command_in_shell('discover', auto_yes=True)
    return {}


@frappe.whitelist()
def create_config_file():
    doc = frappe.get_cached_doc('Nextcloud Settings')
    doc.create_config_file()
    return {}


@frappe.whitelist()
def delete_local_vcards():
    # TODO: Delete all in both sides: vdirsyncer sync --force-delete my_contacts/contacts
    shutil.rmtree(get_vdirsyncer_address_book_path())  # TODO: Ask for address_book to delete. Default is contacts
    return {}


@frappe.whitelist()
def create_vcards():
    contact = frappe.qb.DocType('Contact')
    contact_phone = frappe.qb.DocType('Contact Phone')
    contact_email = frappe.qb.DocType('Contact Email')

    contacts = frappe.qb.from_(contact)\
        .select(contact.name, contact_phone.phone, contact_email.email_id)\
        .left_join(contact_phone).on(contact_phone.parent == contact.name)\
        .left_join(contact_email).on(contact_email.parent == contact.name)\
        .where(contact_phone.phone.isnotnull() | contact.email_id.isnotnull())

    print(contacts)
    # print(contacts.run(as_dict=True))

    # frappe.utils.groupby_metric()


"""
select `tabContact`.name, `tabContact Phone`.phone
from `tabContact`
left join `tabContact Phone` on (`tabContact Phone`.parent = `tabContact`.name)
WHERE `tabContact Phone`.phone != ''
order by `tabContact`.`modified` ASC
"""
