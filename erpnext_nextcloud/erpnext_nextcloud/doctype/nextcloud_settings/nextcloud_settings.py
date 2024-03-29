from erpnext_nextcloud.erpnext_nextcloud.vdirsyncer import get_vdirsyncer_status_path, get_vdirsyncer_storage_path, get_vdirsyncer_config_file_path
from frappe.model.document import Document


class NextcloudSettings(Document):

    def on_update(self):
        self.create_config_file()

    def create_config_file(self):
        config_file_settings = """
        [general]
        status_path = "{vdirsyncer_status_path}"
        
        [pair frappe_and_nextcloud]
        a = "contacts_in_frappe"
        b = "contacts_in_nextcloud"
        collections = ["from a", "from b"]
        conflict_resolution = "a wins"
        
        [storage contacts_in_frappe]
        type = "filesystem"
        path = "{vdirsyncer_storage_path}"
        fileext = ".vcf"
        
        [storage contacts_in_nextcloud]
        type = "carddav"
        username = "{email}"
        password = "{password}"
        url = "{carddav_url}"
        """.format(
            vdirsyncer_status_path=get_vdirsyncer_status_path(),
            vdirsyncer_storage_path=get_vdirsyncer_storage_path(),
            email=self.email,
            password=self.get_password(),  # TODO: password.fetch = ["prompt", "Password for User"]
            carddav_url=self.carddav_url
        )

        with open(get_vdirsyncer_config_file_path(), 'w') as config_file:
            config_file.write(config_file_settings)
