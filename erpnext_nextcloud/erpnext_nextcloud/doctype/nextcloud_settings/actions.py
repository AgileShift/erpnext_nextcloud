import shutil

import frappe
from erpnext_nextcloud.erpnext_nextcloud.vdirsyncer import execute_vdirsyncer_in_shell, get_vdirsyncer_address_book_path


@frappe.whitelist()
def sync():
    execute_vdirsyncer_in_shell(cmd='sync')
    return {}


@frappe.whitelist()
def discover():
    execute_vdirsyncer_in_shell(cmd='discover', auto_yes=True)
    return {}


@frappe.whitelist()
def force_delete():
    execute_vdirsyncer_in_shell(cmd='sync --force-delete')
    return {}


@frappe.whitelist()
def create_vcards():
    # contact = frappe.qb.DocType('Contact')
    # contact_phone = frappe.qb.DocType('Contact Phone')
    # contact_email = frappe.qb.DocType('Contact Email')

    # contacts_sql = frappe.qb.from_(contact)\
    #     .select(contact.name, contact.first_name, contact_phone.phone, contact_email.email_id)\
    #     .left_join(contact_phone).on(contact_phone.parent == contact.name)\
    #     .left_join(contact_email).on(contact_email.parent == contact.name)\
    #     .where(contact_phone.phone.isnotnull() | contact_email.email_id.isnotnull())\
    #     .orderby(contact.name)

    # contacts = contacts_sql.run(as_dict=True)

    contacts = frappe.get_all(
        'Contact',
        fields=['name'],
        or_filters=[
            ['Contact Phone', 'phone', 'is', 'set'],
            ['Contact Email', 'email_id', 'is', 'set']
        ], order_by='name', debug=False)

    from erpnext_nextcloud.erpnext_nextcloud.custom.contact import create_vcard

    default_address_book = get_vdirsyncer_address_book_path()
    for contact in contacts:
        frappe_contact = frappe.get_doc('Contact', contact.name)
        create_vcard(frappe_contact, default_address_book)

    frappe.msgprint(msg='Done', alert=True)
    # TODO: WORKING


@frappe.whitelist()
def delete_vcards():  # TODO: make def delete_vcards_in_address_book()
    address_book_folder = get_vdirsyncer_address_book_path()  # TODO: Ask for address_book to delete. Using default

    shutil.rmtree(address_book_folder)                          # Deleting Entire Folder
    frappe.create_folder(address_book_folder, with_init=False)  # Create Folder Again
    return {}


@frappe.whitelist()
def create_config_file():
    doc = frappe.get_cached_doc('Nextcloud Settings')
    doc.create_config_file()

    return
