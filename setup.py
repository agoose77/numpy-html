from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="numpy-html",
    version="0.0.4",
    packages=["numpy_html"],
    url="https://github.com/agoose77/numpy-html",
    install_requires=["numpy", "ipython"],
    python_requires=">=3.6",
    license="MIT",
    author="Angus Hollands",
    author_email="goosey15@gmail.com",
    description=" A simple table renderer for numpy arrays. Provides a rich display hook for use with Jupyter Lab / Notebook.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Framework :: Jupyter",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
