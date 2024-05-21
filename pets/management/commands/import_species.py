from django.core.management.base import BaseCommand, CommandError
from pets.models import Pet_encyclopedia
import json


class Command(BaseCommand):
    help = 'Imports species data from a JSON file into the database'

    def handle(self, *args, **options):
        try:
            with open('pets/management/commands/species_cn.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.stdout.write("Starting the import process...")

                # 清空当前数据表（慎用！）
                Pet_encyclopedia.objects.all().delete()

                # 导入猫的数据
                for cat in data['cats']:
                    Pet_encyclopedia.objects.create(
                        species_id=cat['species_id'],
                        species_name=cat['species_name'],
                        species_name_cn=cat['species_name_cn'],
                        pet_type=0  # 假设0代表猫
                    )

                # 导入狗的数据
                for dog in data['dogs']:
                    Pet_encyclopedia.objects.create(
                        species_id=dog['species_id'],
                        species_name=dog['species_name'],
                        species_name_cn=dog['species_name_cn'],
                        pet_type=1  # 假设1代表狗
                    )

                self.stdout.write(self.style.SUCCESS('Successfully imported all species data.'))
        except Exception as e:
            raise CommandError(f"Error importing species data: {str(e)}")
