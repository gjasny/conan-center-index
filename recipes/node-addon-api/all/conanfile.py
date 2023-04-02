from conan import ConanFile
from conan.tools.build import check_min_cppstd
from conan.tools.files import get, copy
from conan.tools.layout import basic_layout
import os


required_conan_version = ">=1.52.0"


class PackageConan(ConanFile):
    name = "node-addon-api"
    description = "C++ Node-API wrapper"
    license = "MIT"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://github.com/nodejs/node-addon-api"
    topics = ("addon", "node", "api")
    package_type = "header-library"
    settings = "os", "arch", "compiler", "build_type"
    no_copy_source = True

    @property
    def _min_cppstd(self):
        return 11

    def layout(self):
        basic_layout(self, src_folder="src")

    def requirements(self):
        self.requires("nodejs/16.3.0", transitive_headers=True)

    def package_id(self):
        self.info.clear()

    def validate(self):
        if self.settings.compiler.get_safe("cppstd"):
            check_min_cppstd(self, self._min_cppstd)

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def build(self):
        pass

    # Copy all files to the package folder
    def package(self):
        copy(self, pattern="LICENSE.md", dst=os.path.join(self.package_folder, "licenses"), src=self.source_folder)
        copy(
            self,
            pattern="napi*.h",
            dst=os.path.join(self.package_folder, "include"),
            src=self.source_folder,
        )

    def package_info(self):
        self.cpp_info.bindirs = []
        self.cpp_info.libdirs = []

        # TODO: to remove in conan v2 once cmake_find_package_* generators removed
        self.cpp_info.filenames["cmake_find_package"] = "NodeAddonAPI"
        self.cpp_info.filenames["cmake_find_package_multi"] = "node-addon-api"
        self.cpp_info.names["cmake_find_package"] = "NodeAddonAPI"
        self.cpp_info.names["cmake_find_package_multi"] = "node-addon-api"
