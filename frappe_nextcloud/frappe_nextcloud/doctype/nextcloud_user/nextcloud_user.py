# -*- coding: utf-8 -*-
# Copyright (c) 2020, Agile Shift I/O and contributors
# For license information, please see license.txt
from frappe.model.document import Document
from frappe_nextcloud.frappe_nextcloud.utils import get_vdirsyncer_config_file_path, get_vdirsyncer_path, \
    get_vdirsyncer_config_template_file_path, get_vdirsyncer_local_storage_path


class NextcloudUser(Document):
    """
    Nextcloud User Doctype.
    Configures where contacts will be sync: Config files and vdirsyncer options.
    """

    def on_update(self):
        """ After update doctype reload the vdirsyncer config file for the NC-User(site-wise) """
        vdirsyncer_user_path = get_vdirsyncer_path(self.name)
        vdirsyncer_user_local_storage_path = get_vdirsyncer_local_storage_path(self.name)
        vdirsyncer_user_config_file = get_vdirsyncer_config_file_path(self.name)
        vdirsyncer_config_template_file = get_vdirsyncer_config_template_file_path()

        # Custom Data for each NC-User
        config_file_status_path = 'status_path = "' + vdirsyncer_user_path + '/status/"'
        config_file_local_storage_path = 'path = "' + vdirsyncer_user_local_storage_path + '/"'
        config_file_remote_storage_url = 'url = "' + self.carddav_url + '"'

        # Setting up template
        with open(vdirsyncer_config_template_file, 'r') as config_template_file:
            template_data = config_template_file.read()  # Reading template

            # TODO: Find a better approach ;)
            template_data = template_data.replace('status_path = ""', config_file_status_path)
            template_data = template_data.replace('path = ""', config_file_local_storage_path)
            template_data = template_data.replace('url = ""', config_file_remote_storage_url)

        # Creating config file in the right path
        with open(vdirsyncer_user_config_file, 'w') as config_file:
            config_file.write(template_data)
