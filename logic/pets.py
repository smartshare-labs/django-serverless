
import logging

from sls_django.pets.models import Pet
from sls_django.pets.serializers import PetSerializer


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def _set_or_default(new, old):
    return new if new is not None else old

def create_pet(*, name):
  new_pet = Pet.objects.create(name=name)
  
  return new_pet

def update_pet(*, pet_id, name):
  pet = Pet.objects.get(external_id=pet_id)
  pet.name = _set_or_default(name, pet.name)

  pet.save()
  return pet

def delete_pet(*, pet_id):
    pet = Pet.objects.get(external_id=pet_id)

    pet.delete()
    return pet

def get_pet(*, pet_id):
    pet = Pet.objects.get(external_id=pet_id)
    
    return pet

def list_pets():
    return list(Pet.objects.all())
