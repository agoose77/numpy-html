from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="numpy-html",
    version="0.0.2",
    packages=["numpy_html"],
    url="https://github.com/agoose77/numpy-html",
    install_requires=["numpy", "ipython"],
    python_requires='>=3.6',
    license="MIT",
    author="Angus Hollands",
    author_email="goosey15@gmail.com",
    description=" A simple table renderer for numpy arrays. Provides a rich display hook for use with Jupyter Lab / Notebok.",
    long_description=long_description,
)
