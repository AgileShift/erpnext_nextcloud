""" Utils for frappe nextcloud module """
import frappe
from frappe.utils import get_site_path, get_bench_path


def get_vdirsyncer_path(*path):
    """ Return absolute folder path unique for each site and NC-User. """
    # https://discuss.erpnext.com/t/getting-the-full-path-of-uploaded-files/25517/3
    vdirsyncer_folder_path = get_bench_path() + '/sites/' + get_site_path('private', 'vdirsyncer', *path)[2:]

    # Create Directory (if not exists)
    frappe.create_folder(vdirsyncer_folder_path, with_init=False)

    return vdirsyncer_folder_path


def get_vdirsyncer_config_file_path(*path):
    """ Get vdirsyncer config file path. Note: Is not an absolute url. """
    return get_site_path('private', 'vdirsyncer', *path, 'vdirsyncer.config')


def get_vdirsyncer_local_storage_path(*path):
    """ Get absolute vdirsyncer storage path for the NC-User """
    return get_vdirsyncer_path(*path, 'address_books')


def get_vdirsyncer_config_template_file_path():
    """ Get absolute vdirsyncer config template file. This is to create configurations for each account """
    return frappe.get_app_path('Frappe Nextcloud', 'vdirsyncer.config_template')
