## ERPNext & Nextcloud

This app lets you Sync Contacts To a Nextcloud Account.

**[ERPNext](https://github.com/frappe/erpnext)** Integration with Nextcloud Contact App


### App Includes:
- Nextcloud Settings Doctype


### Customizations to Frappe and ERPNext
- Custom Class for **Contact** and **Customer**.
- **Contact** Doctype is changed to hold Nextcloud Contact ID.


### Description

Create a .vcf file for each **Contact** Doc if it has email or phone, then uses **vdirsyncer** to syncs with remote nextcloud server.

* **Contact** first_name and last_name are always updated if a linked **Customer** is updated.


The following configuration is set in **Nextcloud Settings** Single Doctype:
- Nextcloud URL
- Email Account
- App password(Can be account password) 

# WORK IN PROGRESS

# TODO:
3. Better background job sync
