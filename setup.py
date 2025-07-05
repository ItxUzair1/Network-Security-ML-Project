from setuptools import setup,find_packages


setup(
    name="Network Security",
    version="0.1",
    author="Muhammad Uzair",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pandas",
        "numpy",
        "scikit-learn",
        "matplotlib",
        "seaborn",
        "flask",
        "joblib",
        "scipy",
        "pymongo",
    ],
)