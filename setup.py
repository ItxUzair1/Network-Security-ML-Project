import sys
from setuptools import setup,find_packages
from src.exception.exception import CustomException

list=[]

def get_requirements(file_name):
    try:
        with open(file_name,"r") as file:
            dependenices=file.readline()


            for dependiency in dependenices:
                list.append(dependiency.strip())


                if dependiency == "-e .":
                    list.remove("-e .")

            
            return list
    except Exception as e:
        raise CustomException(e,sys) # type: ignore




setup(
    name="Network Security",
    version="0.1",
    author="Muhammad Uzair",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=get_requirements("requirements.txt"),
)