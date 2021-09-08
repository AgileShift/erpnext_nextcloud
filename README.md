## ERPNext & Nextcloud

**[ERPNext](https://github.com/frappe/erpnext)** Integration with Nextcloud Contact App
Using 

### Customizations to ERPNext
- **Customer** Doctype is changed to hold Nextcloud Contact ID


### Description

Its Export Contact Doctype to .vcf files
and then push into remote server.

# TODO:
1. Create a Nextcloud settings to allow for a custom config template for each user.
2. Hooks on the customer or contact side to sync each time a new or update occurs
3. Better background job sync
