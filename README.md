[![codecov](https://codecov.io/gh/MG814/mc_medical_records/graph/badge.svg?token=0SWUPVLU9C)](https://codecov.io/gh/MG814/mc_medical_records)

# Medical Records Microservice

A microservice for managing patient medical documentation within a healthcare system.

## Description

**Medical Records** is a microservice responsible for storing, updating, and managing patients' medical records. It allows doctors to add medical entries, attach documents, and manage the patient’s medical history.

## 🛠 Technologies

- **python 3.13**
- **django 5.1**
- **djangorestframework 3.15.2**
- **psycopg2-binary 2.9.10**
- **drf-spectacular 0.28.0**

## Installation

### System Requirements

- Python 3.13+
- PostgreSQL
- Poetry

### Setup

#### 1. Clone the repository

```bash
git clone https://github.com/MG814/mc_medical_records.git
cd mc_medical_records
```
#### 2. Running the entire application:

```bash
docker-compose up --build
```

#### 3. Migrations (in a separate terminal):

```bash
docker-compose exec web-medical-records python src/manage.py migrate
```

