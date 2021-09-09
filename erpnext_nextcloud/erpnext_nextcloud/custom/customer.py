import frappe
from erpnext.selling.doctype.customer.customer import Customer


class SyncedCustomer(Customer):
    """ Whenever a Customer is Created/Updated it syncs the name with a Primary Contact. """

    def create_primary_contact(self):
        if not self.customer_primary_contact:
            super(SyncedCustomer, self).create_primary_contact()  # Try to create a Primary Contact from core def
        else:
            contact = frappe.get_cached_doc('Contact', self.customer_primary_contact)
            contact.set_names(full_name=self.customer_name)
            contact.flags.ignore_mandatory = True
            contact.save(ignore_permissions=True, ignore_version=True)  # Calls on_update and creates vCard
