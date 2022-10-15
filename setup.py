import os

from setuptools import setup


def read(file_name):
    """Read in the supplied file name from the root directory.

    Args:
        file_name (str): the name of the file

    Returns: the content of the file
    """
    this_dir = os.path.dirname(__file__)
    file_path = os.path.join(this_dir, file_name)
    with open(file_path) as f:
        return f.read()


def version_scheme(version):
    """Version scheme hack for setuptools_scm.

    Appears to be necessary to due to the bug documented here: https://github.com/pypa/setuptools_scm/issues/342

    If that issue is resolved, this method can be removed.
    """
    import time

    from setuptools_scm.version import guess_next_version

    if version.exact:
        return version.format_with("{tag}")
    else:
        _super_value = version.format_next_version(guess_next_version)
        now = int(time.time())
        return _super_value + str(now)


def local_version(version):
    """Local version scheme hack for setuptools_scm.

    Appears to be necessary to due to the bug documented here: https://github.com/pypa/setuptools_scm/issues/342

    If that issue is resolved, this method can be removed.
    """
    return ""


setup(
    name="python-open-source-template",  # <--- Your module's name goes here
    description="A template for open-source Python software repositories",  # <--- Your module's description goes here
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="<your name>",
    author_email="<your email>",
    url="http://www.github.com/<your-user-name>/<your-repo-slug>",
    license="MIT",
    packages=("",),  # <--- Your module's directory goes here
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
    ],
    setup_requires=["setuptools_scm"],
    use_scm_version={"version_scheme": version_scheme, "local_scheme": local_version},
    project_urls={
        "Maintainer": "https://github.com/<your-user-name>",
        "Source": "https://github.com/<your-user-name>/<your-repo-slug>",
        "Tracker": "https://github.com/<your-user-name>/<your-repo-slug>/issues",
    },
)
