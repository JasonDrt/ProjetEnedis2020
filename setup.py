import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "semic",
    version = "0.0.1",
    author = "JasonDrt, LesavoureyMael",
    author_email = "lesavoureym@gmail.com",
    description = "Satellite, environmental and meteorologic information collect",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/JasonDrt/semic",
    packages = setuptools.find_packages(),
    include_package_data = True,
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL-3.0 License",
        "Operating System :: OS Independent",
    ],
)