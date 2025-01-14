# Copyright 2023 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import os

from click.testing import CliRunner

from odoo_tools.utils import pkg as pkg_utils

from .common import make_fake_project_root, mock_pypi_version_cache


def test_pkg_class():
    addon_name = "edi_oca"
    mock_pypi_version_cache(f"odoo-addon-{addon_name}", "1.9.0")
    runner = CliRunner()
    with runner.isolated_filesystem():
        make_fake_project_root()
        pkg = pkg_utils.Package(addon_name)
    assert pkg.odoo
    assert pkg.name == addon_name
    assert pkg.pypi_name == f"odoo-addon-{addon_name}"
    assert pkg.latest_version == "1.9.0"
    assert pkg.pinned_version is None
    old_req = f"{pkg.pypi_name} @ git+https://github.com/OCA/repo@refs/pull/3/head#subdirectory=setup/{pkg.name}"
    with runner.isolated_filesystem():
        make_fake_project_root()
        with open("./requirements.txt", "w") as fd:
            fd.write(old_req)
        req_path = os.getcwd() + "/requirements.txt"
        pkg = pkg_utils.Package(addon_name, req_filepath=req_path)
    assert pkg.has_pending_merge()
