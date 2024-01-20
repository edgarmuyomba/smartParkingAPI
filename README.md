# smartParkingAPI
An api used to collect and handle information from smart parking sensors. Designed using [Django](https://www.djangoproject.com/) and [Django Rest Framework](https://www.django-rest-framework.org/). This was designed as part of a smart parking system in part for the completion of my computer science final year project. It serves to provide information for both the [Admin Interface](https://github.com/edgarmuyomba/easypark) and the [Mobile Application]().

## Features
- **CRUD** handling for all models ie ParkingLot, ParkingSession, User, Sensor & Slot
- Information processing and aggregation used by the [Admin Interface](https://github.com/edgarmuyomba/easypark)
- Server side report generation and formatting using [ReportLab]()
- Response pagination
- Token Authentication
- Access restriction using [django-cors-headers](https://pypi.org/project/django-cors-headers/)

## Setting up dev
- Clone the repository
  ```bash
  git clone <url>
  ```
- Navigate into the created directory
  ```bash
  cd smartParkingAPI
  ```
- Create and activate a virtual environment
  ```bash
  python -m venv <env> && .\<env>\Scripts\Activate
  ```
- Install the necessary requirements
  ```bash
  python -m pip install -r requirements.txt
  ```
- Run the server
  ```bash
  python manage.py runserver
  ```
You can now access the server on [localhost:8000](http://localhost:8000)

> [!CAUTION]
> Make sure to make the necessary adjustments to the django-cors-headers settings before access

## Django Cors Headers
The currently allowed domains are `localhost:5173` **(React+Vite)** and `localhost:5500`.
To allow access to your own domain, follow the instructions listed in this [repository](https://github.com/adamchainz/django-cors-headers).

## Technologies Used
- [DjangoRestFramework](https://www.django-rest-framework.org/)
- [Django](https://www.djangoproject.com/)
- [ReportLab](https://docs.djangoproject.com/en/5.0/howto/outputting-pdf/)
- [DjangoCorsHeaders](https://pypi.org/project/django-cors-headers/)
- [Pillow](https://pypi.org/project/pillow/)