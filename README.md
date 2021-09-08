## ERPNext & Nextcloud

**[ERPNext](https://github.com/frappe/erpnext)** Integration with Nextcloud Contact App

### Customizations to ERPNext
- Custom Class for **Contact** and **Customer**.
- **Contact** Doctype is changed to hold Nextcloud Contact ID


### Description

Its Export Contact Doc to .vcf file and then push into remote server.

# TODO:
1. Create a Nextcloud settings to allow for a custom config template for each user.
2. Hooks on the customer or contact side to sync each time a new or update occurs
3. Better background job sync
