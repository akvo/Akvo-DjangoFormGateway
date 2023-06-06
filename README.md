# Akvo-DjangoFormGateway

[![Build Status](https://github.com/akvo/Akvo-DjangoFormGateway/actions/workflows/test.yml/badge.svg)](https://github.com/akvo/Akvo-DjangoFormGateway/actions) [![Repo Size](https://img.shields.io/github/repo-size/akvo/Akvo-DjangoFormGateway)](https://img.shields.io/github/repo-size/akvo/Akvo-DjangoFormGateway) [![Coverage Status](https://coveralls.io/repos/github/akvo/Akvo-DjangoFormGateway/badge.svg?branch=main)](https://coveralls.io/github/akvo/Akvo-DjangoFormGateway?branch=main) [![Languages](https://img.shields.io/github/languages/count/akvo/Akvo-DjangoFormGateway)](https://img.shields.io/github/languages/count/akvo/Akvo-DjangoFormGateway) [![Issues](https://img.shields.io/github/issues/akvo/Akvo-DjangoFormGateway)](https://img.shields.io/github/issues/akvo/Akvo-DjangoFormGateway) [![Last Commit](https://img.shields.io/github/last-commit/akvo/Akvo-DjangoFormGateway/main)](https://img.shields.io/github/last-commit/akvo/Akvo-DjangoFormGateway/main) [![GitHub license](https://img.shields.io/github/license/akvo/Akvo-DjangoFormGateway.svg)](https://github.com/akvo/Akvo-DjangoFormGateway/blob/main/LICENSE)

**Akvo-DjangoFormGateway** is a Django library that enables seamless integration of messenger services such as WhatsApp, SMS, and SSID for collecting form data. It provides an easy-to-use gateway to receive and process form submissions from various messaging platforms, empowering developers to build interactive and conversational form experiences within their Django applications.

Please note that you can further customize and expand upon this description to provide more specific details about the features, functionality, and benefits of your library.

# Requirements

This section outlines the requirements for using the
AkvoDjangoFormGateway package. Make sure your environment meets the following prerequisites:

- Python 3.7 or higher
- setuptools>=36.2
- twilio>=8.2.0
- djangorestframework>=3.12.4
- requests==2.26.0

# Installation

To install AkvoDjangoFormGateway in your Django project, use the following command:

```bash
pip install AkvoDjangoFormGateway
```

# Configuration

## Environment file

Create an environment file (`.env`) in your project directory

```bash
touch .env
```

and include the following required variables:

```bash
TWILIO_ACCOUNT_SID="YOUR TWILIO_ACCOUNT_SID"
TWILIO_AUTH_TOKEN="YOUR TWILIO_AUTH_TOKEN"
TWILIO_PHONE_NUMBER="YOUR TWILIO_PHONE_NUMBER"
```

You can also include an optional variable:

```
GOOGLE_MAPS_API_KEY="YOUR GOOGLE_MAPS_API_KEY"
```

## Docker

It should be noted, if your django project is located in a docker container then it is highly recommended to add the environment variable to `docker-compose.yml`.

```docker
---
version: "3.9"
services:
  container-name:
    ... # other configuration
    environment: # add it to the environment section
      - TWILIO_ACCOUNT_SID
      - TWILIO_AUTH_TOKEN
      - TWILIO_PHONE_NUMBER
      - GOOGLE_MAPS_API_KEY
      - ... # other environment variables
```

## Django Settings

Add the following configurations to your Django project's `settings.py` file:

```python
API_APPS = [
    ..., # other apps
    "AkvoDjangoFormGateway",
]
# Load environment variables
TWILIO_ACCOUNT_SID = environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = environ.get("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = environ.get("TWILIO_PHONE_NUMBER")
GOOGLE_MAPS_API_KEY = environ.get("GOOGLE_MAPS_API_KEY")
```

# Usage

## Form Seeder

To seed forms into the gateway, use the following command:

```bash
python manage.py gateway_form_seeder -f ./your/source/json/form.json
```

### Arguments

| Short | Long   | Description                              |
| ----- | ------ | ---------------------------------------- |
| -f    | --file | The path location for the JSON form file |
| -t    | --test | Optional argument for testing purpose    |

## Dummy data seeder (optional)

To generate dummy data for the gateway forms, you can use the following command:

```bash
python manage.py fake_gateway_form_seeder -r 100
```

### Arguments

| Short | Long     | Description                           |
| ----- | -------- | ------------------------------------- |
| -r    | --repeat | Number of populated fake datapoints   |
| -t    | --test   | Optional argument for testing purpose |

## Geolocation converters

This command is required when you are migrating from a disabled to an enabled Google Maps API.

```bash
python manage.py gateway_geo_converter
```

