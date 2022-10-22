from setuptools import setup
from setuptools.command.build import build


# Override build command
class BuildCommand(build):
    def initialize_options(self):
        build.initialize_options(self)
        self.build_base = "/tmp"


setup(
    name="cb_firebase_basic_chat",
    version="0.1",
    packages=["firebase_basic_chat"],
    install_requires=["firebase-admin"],
    cmdclass={"build": BuildCommand},
)