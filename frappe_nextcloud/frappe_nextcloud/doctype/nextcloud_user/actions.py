import datetime
import json
import uuid
from subprocess import PIPE, STDOUT, run

import frappe
import vobject
from frappe_nextcloud.frappe_nextcloud.utils import get_vdirsyncer_config_file_path, get_vdirsyncer_local_storage_path


def get_nc_user_from_doc(doc):
    """ Get the NC-User from the payload """
    doc = json.loads(doc)
    return frappe.get_doc('Nextcloud User', doc.get('name'))


# TODO: Disable on not enabled.!
# TODO: Improve the way vdirsyncer send us whats next
# TODO: Delete all in both sides: vdirsyncer sync --force-delete my_contacts/contacts

@frappe.whitelist(allow_guest=False)
def discover(doc):
    """ This will discover all address books of the NC-User """
    nc_user = get_nc_user_from_doc(doc)

    command = ['vdirsyncer', '-c', get_vdirsyncer_config_file_path(nc_user.name), 'discover']

    print('Empezando')
    try:
        print('Configurando Credenciales')
        command_credentials = '{0}\n{1}\n{2}\n'.format(nc_user.email, nc_user.get_password(), 'y')

        run(command, stdout=PIPE, stderr=STDOUT, text=True, input=command_credentials)

    except Exception as e:
        print(e)
        frappe.throw('Error Ver logs')
    print('Finalizando')

    frappe.msgprint('Discovering Finished.')


@frappe.whitelist(allow_guest=False)
def sync_all(doc):
    """ For now this will sync all contacts from frappe to nextcloud. """
    nc_user = get_nc_user_from_doc(doc)

    vdirsyncer_local_storage_path = get_vdirsyncer_local_storage_path(nc_user.name)  # TODO: Default address book only.
    command = ['vdirsyncer', '-c', get_vdirsyncer_config_file_path(nc_user.name), 'sync']

    customers_to_sync = frappe.get_all('Customer', fields=[
        'name', 'customer_name', 'customer_group', 'mobile_no', 'email_id', 'nextcloud_contact_id'
    ], filters={'sync_with_nextcloud': True, 'nextcloud_user': nc_user.name})

    for customer in customers_to_sync:

        print(customer)

        if not customer.nextcloud_contact_id:  # Create the Unique UUID
            nextcloud_contact_id = str(uuid.uuid4())
            customer.nextcloud_contact_id = nextcloud_contact_id

            # TODO: Find a Better Way:
            frappe.db.set_value('Customer', customer.name, 'nextcloud_contact_id', nextcloud_contact_id, update_modified=False)

        # New vCard Object
        card = vobject.vCard()
        card.add('n')
        card.add('fn')
        card.add('org')
        card.add('email')
        card.add('tel')
        card.add('categories')
        card.add('rev')
        card.add('uid')
        # TODO: Add Prefix, Add Suffix, Even Image, Multiple phones and emails?

        # TODO: make this a little bit more complex?
        first_name, last_name = customer.customer_name.split(' ', 1)
        card.n.value = vobject.vcard.Name(given=first_name, family=last_name)  # Additional is middle name
        card.fn.value = customer.customer_name

        if nc_user.carddav_org_field:
            card.org.value = 'QuickBox CardDav', ''  # TODO: What about this?

        if customer.email_id:
            card.email.value = customer.email_id
            card.email.type_param = 'Home'  # TODO: Make this work with erpnext

        if customer.mobile_no:
            card.tel.value = customer.mobile_no
            card.tel.type_param = 'Mobile'  # TODO: is primary phone or mobile? - Compatible with Nextcloud default

        # customer group OR Type?
        card.categories.value = customer.customer_group, ''  # This is required by erpnext. so no validation.

        card.rev.value = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + 'Z'
        card.uid.value = customer.nextcloud_contact_id

        # TODO: Pragmatically set a address book, because now only one is working: contacts
        card_file = open(vdirsyncer_local_storage_path + '/contacts/%s.vcf' % customer.nextcloud_contact_id, 'w+')
        card_file.write(card.serialize())
        card_file.close()

    # contacts = frappe.get_all('Contact', fields=['name', 'first_name', 'middle_name', 'last_name', 'google_contacts_id'])
    # contacts_emails = frappe.get_all('Contact Email', fields='parent as name, email_id', as_list=0)
    # contacts_phones = frappe.get_all('Contact Phone', fields=['parent', 'phone', 'is_primary_phone', 'is_primary_mobile_no'])

    # for contact in contacts:
    #     contact_phone = next(contact_phone for contact_phone in contacts_phones if contact_phone['parent'] == contact.name)

    print('Empezando la sincronizacion')
    try:
        print('Configurando Credenciales')
        command_credentials = '{0}\n{1}\n'.format(nc_user.email, nc_user.get_password())

        run(command, stdout=PIPE, stderr=STDOUT, text=True, input=command_credentials)
    except Exception as e:
        print(e)
        frappe.throw('Error Ver logs')

    frappe.msgprint('Synching Finished.')
    print('Finalizando')
