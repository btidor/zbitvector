from setuptools import Extension, setup

CHECKOUT = "/opt/bitwuzla"

setup(
    ext_modules=[
        Extension(
            "zbitvector.pybitwuzla",
            sources=[
                "pybitwuzla/pybitwuzla.pyx",
                "pybitwuzla/pybitwuzla_abort.cpp",
            ],
            libraries=["bitwuzla"],
            extra_compile_args=["-O3"],
            language="c++",
        ),
    ],
)
