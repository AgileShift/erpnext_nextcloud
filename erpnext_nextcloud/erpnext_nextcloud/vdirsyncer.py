import os
import sys

import pexpect

import frappe


def get_vdirsyncer_path(*path, is_folder=True):
    folder_path = frappe.utils.get_bench_path() + '/sites/' + frappe.get_site_path('private', 'vdirsyncer', *path)[2:]

    if is_folder:
        frappe.create_folder(folder_path, with_init=False)  # Create Directory (if not exists)

    return folder_path


def get_vdirsyncer_status_path():
    return get_vdirsyncer_path('status', is_folder=True)


def get_vdirsyncer_storage_path(*path):
    return get_vdirsyncer_path('address_books', *path, is_folder=True)


def get_vdirsyncer_address_book_path(address_book='contacts'):
    return get_vdirsyncer_storage_path(address_book)


def get_vdirsyncer_config_file_path():
    return get_vdirsyncer_path('vdirsyncer.config', is_folder=False)


def execute_command_in_shell(cmd, auto_yes=False):
    # TODO: Rename this def, and make more human workable
    config_file = get_vdirsyncer_config_file_path()
    vdirsyncer_exec = os.path.join(sys.exec_prefix, 'bin', 'vdirsyncer')

    if auto_yes:
        process = pexpect.run('/bin/bash -c "yes | {} -c {} {}"'.format(vdirsyncer_exec, config_file, cmd), encoding='utf-8')
    else:
        process = pexpect.run('{} -c {} {}"'.format(vdirsyncer_exec, config_file, cmd), encoding='utf-8')

    print(process)

    frappe.msgprint(
        msg="<pre style='background: #36414C; color: white; padding: 9px; border-radius: 5px;'><code>{}</code></pre>".format(process),
        title='Result', is_minimizable=True, wide=True
    )
