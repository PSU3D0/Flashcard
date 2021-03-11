from django.core.management.base import BaseCommand
import csv
from ...models import Flashcard


class Command(BaseCommand):
    help = "Loads words into the database"

    def handle(self, *args, **kwargs):
        with open("words.csv", "r") as f:
            reader = csv.reader(f)
            for row in reader:
                word, t, definition = row
                t = t.upper()
                word = word.title()
                definition = definition.strip()
                Flashcard.objects.create(
                    word=word,
                    word_type=t,
                    definition=definition
                    
                )
        print("Successfully created database")


