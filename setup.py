from setuptools import setup, find_packages

setup(
    name="techbazar",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "flask==3.1.0",
        "flask-sqlalchemy==3.1.1",
        "flask-login==0.6.3",
        "flask-bcrypt==1.0.1",
        "python-dotenv==1.1.0",
        "mysqlclient==2.2.7",
    ],
)
