from .models import Flashcard, UserFlashcard
from django.contrib.auth.models import User



def createNewUserFlashcards(user: User):
    user_flashcards = []

    for flashcard in Flashcard.objects.filter(active=True):
        user_flashcards.append(
            UserFlashcard(
                flashcard=flashcard,
                user=user,
            )
        )
    
    UserFlashcard.objects.bulk_create(user_flashcards)
    