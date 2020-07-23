import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "semic_pkg-JasonDrt",
    version = "0.0.2",
    author = "JasonDrt, LesavoureyMael",
    author_email = "lesavoureym@gmail.com",
    description = "Satellite, environmental and meteorologic information collect",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/JasonDrt/semic",
    packages = setuptools.find_packages(),
    package_data = {'semic' : ['code_insee.csv', 'historique_meteo.csv']},
    include_package_data = True,
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)