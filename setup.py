import shutil
from pathlib import Path

from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext as _build_ext


class ExternalExtension(Extension):
    """A pre-compiled extension to copy into the wheel."""

    def __init__(self, name: str, source: str):
        self.source = source
        return super().__init__(name, sources=[])


class build_ext(_build_ext):
    def build_extension(self, ext: Extension):
        if not isinstance(ext, ExternalExtension):
            return super().build_extension(ext)  # type: ignore

        # We probably need to create the build directory first...
        destination = Path(self.get_ext_fullpath(ext.name))
        if not destination.parent.exists():
            destination.parent.mkdir(parents=True)

        # Then copy the source file in!
        shutil.copy(ext.source, destination)


setup(
    ext_modules=[
        ExternalExtension(
            "zbitvector.pybitwuzla",
            "/usr/local/lib/pybitwuzla.so",
        )
    ],
    cmdclass={"build_ext": build_ext},
)
