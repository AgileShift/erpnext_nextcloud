import datetime
import os
import uuid

import pexpect
import vobject

import frappe
from frappe.utils import get_bench_path


def get_vdirsyncer_path(*path):
    vdirsyncer_folder_path = get_bench_path() + '/sites/' + frappe.get_site_path('private', 'vdirsyncer', *path)[2:]

    frappe.create_folder(vdirsyncer_folder_path, with_init=False)  # Create Directory (if not exists)

    return vdirsyncer_folder_path


def get_vdirsyncer_status_path():
    return get_vdirsyncer_path('status')


def get_vdirsyncer_storage_path():
    return get_vdirsyncer_path('address_books')


def get_vdirsyncer_config_file_path():
    return os.path.join(get_vdirsyncer_path(), 'vdirsyncer.config')


def create_vcard(contact, storage_path: str, address_book: str):
    # TODO: Add Customer Address details?
    if not contact.nextcloud_contact_id:
        contact.nextcloud_contact_id = str(uuid.uuid4())

        frappe.db.set_value('Contact', contact.name, 'nextcloud_contact_id', contact.nextcloud_contact_id, update_modified=False)

    # New vCard Object
    card = vobject.vCard()
    card.add('n')
    card.n.value = vobject.vcard.Name(given=contact.first_name, family=contact.last_name or '', additional=contact.middle_name or '')

    card.add('fn')
    card.fn.value = "{first_name} {middle_name} {last_name}".format(**contact.as_dict())

    for phone in contact.phone_nos:
        p = card.add('tel')
        p.value = phone.phone

        if phone.is_primary_mobile_no:
            p.type_param = 'mobile'  # IOS Compatible

    for email in contact.email_ids:
        card.add('email').value = email.email_id

    for link in contact.links:
        if link.link_doctype == 'Customer':
            card.add('categories')
            card.categories.value = frappe.get_value('Customer', link.link_name, 'customer_group'), ''
            break

    carddav_org_field = frappe.db.get_single_value('Nextcloud Settings', 'carddav_org_field')
    if carddav_org_field:
        card.add('org')
        card.org.value = carddav_org_field, ''

    card.add('rev')
    card.rev.value = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + 'Z'

    card.add('uid')
    card.uid.value = contact.nextcloud_contact_id

    # TODO: Pragmatically set a address book, because now only one is working: contacts
    card_file = open(os.path.join(storage_path, address_book, '{}.vcf'.format(contact.nextcloud_contact_id)), 'w+')
    card_file.write(card.serialize())
    card_file.close()


def execute_command_in_shell(cmd, auto_yes=False):
    config_file = get_vdirsyncer_path('vdirsyncer.config')

    if auto_yes:
        process = pexpect.run('/bin/bash -c "yes | vdirsyncer -c {} {}"'.format(config_file, cmd), encoding='utf-8')
    else:
        process = pexpect.run('vdirsyncer -c {} {}"'.format(config_file, cmd), encoding='utf-8')

    frappe.msgprint(
        msg="<pre style='background: #36414C; color: white; padding: 9px; border-radius: 5px;'><code>{}</code></pre>".format(process),
        title='Result', is_minimizable=True, wide=True
    )
