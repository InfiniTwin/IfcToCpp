import setuptools

setuptools.setup(
    name="ifctocpp",
    version="0.1.0",
    author="Besjan Xhika",
    description="A Python package to generate C++ code from IFC JSON definitions",
    packages=["IfcToCpp"],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            # The left side is the command name, 
            # the right side is package.module:function
            "ifctocpp=__main__:main",
        ]
    },
)
