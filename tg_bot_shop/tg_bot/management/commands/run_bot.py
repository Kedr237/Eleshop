from django.core.management.base import BaseCommand
import subprocess
import sys
import os

class Command(BaseCommand):
  help = 'Запуск бота'

  def handle(self, *args, **options):
    path_to_bot = os.path.join('tg_bot', 'bot.py')
    path_to_python = sys.executable
    subprocess.run([path_to_python, path_to_bot])