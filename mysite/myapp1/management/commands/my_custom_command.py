from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Description of your custom command'

    def handle(self, *args, **options):
        # Your custom code goes here
        self.stdout.write(self.style.SUCCESS('Successfully ran my_custom_command'))