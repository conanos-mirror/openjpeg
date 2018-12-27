from conans import ConanFile, CMake, tools
from conanos.build import config_scheme
import os

class OpenjpegConan(ConanFile):
    name = "openjpeg"
    version = "2.3.0"
    description = "An open-source JPEG 2000 codec written in C language."
    url = "https://github.com/conanos/openjpeg"
    homepage = "https://github.com/uclouvain/openjpeg"
    license = "BSD 2-Clause"
    exports = ["LICENSE"]
    generators = "cmake"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = { 'shared': True, 'fPIC': True }

    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx

        config_scheme(self)

    def source(self):
        url_="https://github.com/uclouvain/openjpeg/archive/v{version}.tar.gz"
        tools.get(url_.format(version=self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def build(self):
        cmake = CMake(self)
        cmake.definitions['BUILD_SHARED_LIBS'] = self.options.shared
        cmake.definitions['BUILD_STATIC_LIBS'] = not self.options.shared
        cmake.definitions['BUILD_PKGCONFIG_FILES'] = True
        cmake.configure(source_folder=self._source_subfolder)
        cmake.build()
        cmake.install()

    def package(self):
        if self.settings.os == 'Windows':
            for dll in ["concrt140.dll","msvcp140.dll","vcruntime140.dll"]:
                os.remove(os.path.join(self.package_folder,"bin", dll))

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

