from setuptools import setup, find_packages

setup(
    name="weather_vibes",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.110.0",
        "uvicorn==0.27.0",
        "python-dotenv==1.0.0",
        "jinja2==3.1.2",
        "pydantic",
        "rich>=13.0.0",
        "openai>=1.0.0",
        "requests==2.31.0",
        "google-api-python-client==2.111.0",
    ],
) 