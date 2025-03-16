from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from .models import MedicalRecord
from .serializers import MedicalRecordSerializer
from .factory_models import MedicalRecordFactory
from core.settings import HTTP_URL

from responses import activate, add


class TestMedicalRecordsView(APITestCase):
    def setUp(self) -> None:
        self.medical_record = MedicalRecordFactory()
        self.medical_records_url = reverse('medical-records-create-list')
        self.medical_records_detail_url = reverse('medical-records-create-detail', kwargs={'pk': self.medical_record.id})
        self.medical_records_get_url = reverse('medical-records-create-get-patient-records', kwargs={'patient_id': 11})

        self.medical_record_data = {
            "patient_id": 11,
            "doctor_id": 2,
            "title": "Wizyta kontrolna",
            "description": "Test",
        }

    def test_get_medical_record_details(self):
        response = self.client.get(self.medical_records_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, MedicalRecordSerializer(self.medical_record).data)

    def test_get_patient_medical_records(self):
        MedicalRecordFactory(patient_id=1, doctor_id=2)

        response = self.client.get(reverse('medical-records-create-get-patient-records', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(MedicalRecord.objects.filter(patient_id=1).count(), len(response.data))

    @activate
    def test_create_medical_record(self):
        add(
            method='GET',
            url=f"{HTTP_URL}/users/11/",
            json={"id": 11, "role": "Patient"},
            status=200
        )
        add(
            method='GET',
            url=f"{HTTP_URL}/users/2/",
            json={"id": 2, "role": "Doctor"},
            status=200
        )
        response = self.client.post(self.medical_records_url, data=self.medical_record_data,
                                    HTTP_AUTHORIZATION='Bearer mocktoken',
                                    HTTP_ROLE='Doctor')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["patient_id"], 11)
        self.assertEqual(MedicalRecord.objects.filter(patient_id=11).count(), 1)

    @activate
    def test_create_doctor_not_found(self):
        add(
            method='GET',
            url=f"{HTTP_URL}/users/11/",
            json={"id": 11, "role": "Patient"},
            status=200
        )
        add(
            method='GET',
            url=f"{HTTP_URL}/users/2/",
            status=404
        )
        response = self.client.post(self.medical_records_url, data=self.medical_record_data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('Doctor not found.', response.data["message"])

    @activate
    def test_create_patient_not_found(self):
        add(
            method='GET',
            url=f"{HTTP_URL}/users/11/",
            status=404
        )
        add(
            method='GET',
            url=f"{HTTP_URL}/users/2/",
            json={"id": 2, "role": "Doctor"},
            status=200
        )
        response = self.client.post(self.medical_records_url, data=self.medical_record_data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('Patient not found.', response.data["message"])

    @activate
    def test_create_medical_record_by_patient(self):
        add(
            method='GET',
            url=f"{HTTP_URL}/users/11/",
            json={"id": 11, "role": "Patient"},
            status=200
        )
        add(
            method='GET',
            url=f"{HTTP_URL}/users/2/",
            json={"id": 2, "role": "Doctor"},
            status=200
        )
        response = self.client.post(self.medical_records_url, data=self.medical_record_data,
                                    HTTP_AUTHORIZATION='Bearer mocktoken',
                                    HTTP_ROLE='Patient')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('Only doctors can create records.', response.data["message"])

    def test_medical_record_update(self):
        updated_data = {
            "title": "Updated title",
            "description": "Updated Test",
        }
        response = self.client.patch(self.medical_records_detail_url, data=updated_data)
        self.medical_record.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.medical_record.title, "Updated title")
        self.assertEqual(self.medical_record.description, "Updated Test")
