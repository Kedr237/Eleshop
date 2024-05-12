import django
import sys
import os
def setup_core_dir():
  core_dir  = os.path.dirname(os.path.dirname(__file__))
  sys.path.append(core_dir)
setup_core_dir()
django.setup()

from telegram import InputMediaPhoto
from django.db.models import Model
from django.conf import settings
from asgiref.sync import sync_to_async
from typing import List
from typing import Dict
from config import *


# Interaction with django
def get_objs_all(model: Model) -> List[Model]:
  return sync_to_async(list)(model.objects.all())

def get_objs_by_filter(model: Model, filters: Dict[str, any]) -> List[Model]:
  return sync_to_async(list)(model.objects.filter(**filters))

def get_obj_by_id(model: Model, id: int) -> Model:
  return sync_to_async(model.objects.get)(id=id)

def get_abs_img_path(image_path: str) -> str:
  return os.path.join(settings.BASE_DIR, image_path.lstrip('/'))

async def get_media_photos(model: Model, parent: str, obj: Model) -> List[InputMediaPhoto]:
  images: List[model] = await get_objs_by_filter(model, {parent: obj})
  img_paths: List[str] = [img.image.url for img in images]
  media: List[InputMediaPhoto] = [InputMediaPhoto(open(get_abs_img_path(img_path), 'rb')) for img_path in img_paths]
  return media