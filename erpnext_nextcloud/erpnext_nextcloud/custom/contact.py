import datetime
import os
import uuid

import vobject

import frappe
from erpnext_nextcloud.erpnext_nextcloud.vdirsyncer import get_vdirsyncer_address_book_path
from frappe.contacts.doctype.contact.contact import Contact


class SyncedContact(Contact):
    """ Fix bad first_name if Contact is created from Customer. Also Creates vCard """

    def before_insert(self):
        # Fix make_contact() in erpnext/customer.py because sets 'name' as the 'first_name' if created from Customer
        customer_link = self.get_link_for('Customer')

        if customer_link:  # Has a Link for a Customer at creation
            self.set_names(full_name=frappe.get_value('Customer', customer_link, 'customer_name'))

    def on_update(self):
        """ Create/Update vCard """
        # TODO: Update Customer after mobile or email is edited: Eg: https://github.com/frappe/erpnext/pull/26799/files

        if self.phone_nos or self.email_ids:
            create_vcard(self, get_vdirsyncer_address_book_path())  # TODO: Set custom address_book if requested?
            # frappe.msgprint('vCard Created!', alert=True) # TODO: Habilitate this?

    def set_names(self, full_name):
        self.first_name, _, self.last_name = full_name.partition(' ')


def create_vcard(contact, address_book_path: str):
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

    carddav_org_field = frappe.db.get_single_value('Nextcloud Settings', 'carddav_org_field', cache=True)
    if carddav_org_field:
        card.add('org')
        card.org.value = carddav_org_field, ''

    card.add('rev')
    card.rev.value = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + 'Z'

    card.add('uid')
    card.uid.value = contact.nextcloud_contact_id

    # TODO: Pragmatically set a address book, because now only one is working for Contact details
    card_file = open(os.path.join(address_book_path, '{}.vcf'.format(contact.nextcloud_contact_id)), 'w+')
    card_file.write(card.serialize())
    card_file.close()
