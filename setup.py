from setuptools import Extension, setup  # type: ignore

CHECKOUT = "/opt/bitwuzla"

setup(
    ext_modules=[
        Extension(
            "zbitvector.pybitwuzla",
            sources=[
                "zbitvector/pybitwuzla/pybitwuzla.pyx",
                "zbitvector/pybitwuzla/pybitwuzla_abort.cpp",
            ],
            libraries=["bitwuzla"],
            extra_compile_args=["-O3"],
            language="c++",
        ),
    ],
)
