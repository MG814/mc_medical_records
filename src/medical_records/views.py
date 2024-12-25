from rest_framework import status
from rest_framework.mixins import UpdateModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import AllowAny
from .models import MedicalRecord
from .serializers import MedicalRecordSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
import requests


class MedicalRecordViewSet(GenericViewSet, RetrieveModelMixin, UpdateModelMixin):
    serializer_class = MedicalRecordSerializer
    queryset = MedicalRecord.objects.all()
    permission_classes = [AllowAny]

    @action(methods=['GET'], detail=False, url_path='patients/(?P<patient_id>\d+)/medical-records') # patients/<patient_id>/medical-records
    def get_patient_records(self, request, patient_id=None):
        queryset = self.get_queryset().filter(patient_id=patient_id)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        current_user_role = self.request.headers.get('role')
        token = self.request.headers.get('Authorization')
        accounts_service_url = 'http://web-accounts:8100/users/'

        patient_id = self.request.data.get('patient_id')
        patient_url = f'{accounts_service_url}{patient_id}/'

        headers = {
            'Authorization': token
        }

        patient_response = requests.get(patient_url, headers=headers)

        if patient_response.status_code == status.HTTP_404_NOT_FOUND:
            return Response({'message': 'Patient not found.'}, status=status.HTTP_404_NOT_FOUND)

        doctor_id = self.request.data.get('doctor_id')
        doctor_url = f'{accounts_service_url}{doctor_id}/'

        doctor_response = requests.get(doctor_url, headers=headers)

        if doctor_response.status_code == status.HTTP_404_NOT_FOUND:
            return Response({'message': 'Doctor not found.'}, status=status.HTTP_404_NOT_FOUND)

        if current_user_role != 'Doctor':
            return Response({'message': 'Only doctors can create records.'}, status=status.HTTP_403_FORBIDDEN)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
