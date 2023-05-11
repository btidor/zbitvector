from setuptools import Extension, setup

CHECKOUT = "/opt/bitwuzla"

setup(
    ext_modules=[
        Extension(
            "zbitvector.pybitwuzla",
            [
                "pybitwuzla/pybitwuzla.pyx",
                "pybitwuzla/pybitwuzla_enums.pxd",
                "pybitwuzla/pybitwuzla_utils.c",
                "pybitwuzla/pybitwuzla_abort.cpp",
            ],
            include_dirs=[
                f"{CHECKOUT}/src/api/python",
                f"{CHECKOUT}/src/api/c",
                f"{CHECKOUT}/src",
            ],
            libraries=["bitwuzla"],
            extra_compile_args=["-O3"],
            language="c++",
        ),
    ],
)
