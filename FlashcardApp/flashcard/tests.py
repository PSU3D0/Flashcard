from datetime import timedelta
from django.test import TestCase
from django.utils import timezone

from .models import Flashcard, UserFlashcard, BIN_MAPPING
from .utils import createNewUserFlashcards

from django.contrib.auth.models import User


class FlashcardTestCase(TestCase):
    def setUp(self):
        #Create Flashcard(s)
        Flashcard.objects.create(word='word',definition="this is a word")
        user = User.objects.create_user('user1','','password1')
        self.now = timezone.now()
        createNewUserFlashcards(user)

    def test_user_card_correct(self):
        flashcard = User.objects.first().flashcards.first()

        #Check if updated showables are valid
        for i in range(10):
            flashcard.update_correct()
            self.assertTrue(abs(self.now+BIN_MAPPING[i+1]-flashcard.showable) < timedelta(seconds=5))
            self.assertEqual(flashcard.bin_number,i+1)
            self.now = timezone.now()

        flashcard.update_correct()
        self.assertEqual(flashcard.active,False) #Check if we mark inactive

    def test_new_user_flashcard_creation(self):
        flashcard = Flashcard.objects.first()
        user = User.objects.first()
        self.assertEqual(user.flashcards.first().flashcard,flashcard)

    def test_admin_added_flashcard(self):
        flashcard = Flashcard.objects.create(word='word1',definition="this is a word1")
        user = User.objects.first()

        self.assertEqual(user.flashcards.last().flashcard, flashcard)
    

