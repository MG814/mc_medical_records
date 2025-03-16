import factory

from .models import MedicalRecord


class MedicalRecordFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MedicalRecord

    patient_id = factory.Faker('random_int', min=1, max=10)
    doctor_id = factory.Faker('random_int', min=1, max=10)
    title = factory.Faker('text', max_nb_chars=50)
    description = factory.Faker('text', max_nb_chars=250)
