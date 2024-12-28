from setuptools import setup, find_packages

setup(
    name="ospdf",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "chardet==5.2.0",
        "lxml==5.3.0",
        "numpy==2.2.1",
        "opencv-python==4.10.0.84",
        "pillow==11.0.0",
        "PyMuPDF==1.25.1",
        "python-docx==1.1.2",
        "RapidFuzz==3.11.0",
        "reportlab==4.2.5",
        "thefuzz==0.22.1",
        "typing_extensions==4.12.2",
    ],  # List of dependencies
    entry_points={
        "console_scripts": [
            "ospdf=ospdf.main:main",  # This should remain the same as long as `main.py` is in the root directory
        ],
    },

    classifiers=[  # Classifiers can help categorize your package
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Specify your supported Python versions
)