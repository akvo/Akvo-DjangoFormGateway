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
python manage.py fake_gateway_data_seeder -r 100
```

### Arguments

| Short | Long     | Description                           |
| ----- | -------- | ------------------------------------- |
| -r    | --repeat | Number of fake datapoints             |
| -t    | --test   | Optional argument for testing purpose |

## Geolocation converters

This command is required when you are migrating from a disabled to an enabled Google Maps API.

```bash
python manage.py gateway_geo_converter
```

## Router

To get the new endpoint provided by AkvoDjangoFormGateway, Add the corresponding route to your Django project's `urls.py` file.

> Assuming the prefix is `api/gateway`

```python

urlpatterns = [
    ..., # other url patterns
    path(
        r"api/gateway/",
        include("AkvoDjangoFormGateway.urls"),
        name="gateway",
    ),
]
```

Test the endpoint by running the following command

> Assuming Django is running on port 8000

```curl
curl -X 'GET' \
  'http://localhost:8000/api/gateway/check/' \
  -H 'accept: */*'
```

# Properties

To create a JSON form using AkvoDjangoFormGateway, you need to provide a JSON object that defines the form and its questions. Below are the properties you can use:

## Form's fields description

| Field       | Type               | Description                        |
| ----------- | ------------------ | ---------------------------------- |
| id          | Integer            | Unique key to identifying the form |
| form        | String             | Form name                          |
| description | String             | Form description                   |
| questions   | Array of questions | List of questions on the form      |

## Question's fields description

| Field    | Type                          | Description                                                      |
| -------- | ----------------------------- | ---------------------------------------------------------------- |
| id       | Integer                       | Unique key to identifying the question                           |
| question | String                        | question text                                                    |
| order    | Integer                       | Unique number for sorting questions                              |
| required | Boolean                       | Set the questions that must be answered. True = Yes, False = No. |
| type     | Enumeration of question types | Set the question type based on the expected answer               |

## Question types

| Type            | Description                                                   |
| --------------- | ------------------------------------------------------------- |
| geo             | Type of question for geolocation answers                      |
| text            | Type of question for free text answers                        |
| number          | Type of question for numeric answers                          |
| option          | Type of question for single option answers                    |
| multiple_option | Type of question for multiple options answers                 |
| photo           | Type of question for image answers                            |
| date            | Type of question for date answers with the format: DD-MM-YYYY |

# Example

## Creating a complaint from

To create a complaint form using AkvoDjangoFormGateway, you can follow the JSON form guidelines outlined in the previous section.

```json
[
  {
    "id": 1,
    "form": "Form Complaint",
    "description": "Collect complaint data from customers",
    "questions": [
      {
        "id": 1,
        "question": "Details of the complaint",
        "order": 1,
        "required": true,
        "type": "text"
      },
      {
        "id": 2,
        "question": "Upload a photo",
        "order": 2,
        "required": true,
        "type": "photo"
      },
      {
        "id": 3,
        "question": "Your location",
        "order": 3,
        "required": true,
        "type": "geo"
      }
    ]
  }
]
```

# Development

## Run Dev Containers

The dev environment contains two containers: Django backend and PostgreSQL db, to run:

```bash
docker compose up -d
```

Before go to the next step, wait until the service started at [http://localhost:8000](http://localhost:8000).

## Seed Necessary Data

In order to debug the data itself. We need to seed the example form and fake datapoints

### Seed the example form

```bash
docker compose exec backend python manage.py gateway_form_seeder -f ./backend/source/forms/1.json
```

### Seed fake datapoints

```bash
docker compose exec backend python manage.py fake_gateway_data_seeder -r 100
```

## Teardown

To properly shut down the container and clean up the resources, use the following command:

```bash
docker compose down -v
```
