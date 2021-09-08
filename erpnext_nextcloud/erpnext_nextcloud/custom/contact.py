import frappe
from erpnext_nextcloud.erpnext_nextcloud.utils import get_vdirsyncer_path, create_vcard
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
        storage_path = get_vdirsyncer_path('address_books')
        create_vcard(self, storage_path, address_book='contacts')

    def set_names(self, full_name):
        self.first_name, _, self.last_name = full_name.partition(' ')
