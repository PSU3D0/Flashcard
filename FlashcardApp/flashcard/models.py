from django.db import models
from django.contrib.auth.models import User

from datetime import timedelta

from django.utils import timezone


# Create your models here.

BIN_MAPPING = {
    0: timedelta(seconds=0),
    1: timedelta(seconds=5),
    2: timedelta(seconds=25),
    3: timedelta(minutes=2),
    4: timedelta(minutes=10),
    5: timedelta(hours=1),
    6: timedelta(hours=5),
    7: timedelta(days=1),
    8: timedelta(days=5),
    9: timedelta(days=25),
    10: timedelta(weeks=16),
}






class Flashcard(models.Model):
    WORD_CHOICES = [
    ("N", 'Noun'),
    ("V", 'Verb'),
    ("A", 'Adjective')
    ]

    word = models.CharField(max_length=50)
    definition = models.CharField(max_length=200)
    word_type = models.CharField(choices=WORD_CHOICES,max_length=1)

    active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.word

    def save(self, *args, **kwargs):
        '''
        Overriding save allows admin to create
        and update cards with changes pushed to existing
        users
        '''
        if not self.pk:
            super().save(*args, **kwargs)
            for user in User.objects.all():
                UserFlashcard.objects.create(
                    flashcard=self,
                    user=user
                )
        else:
            for user in User.objects.all():
                #If a definition updates, we reset user metrics
                UserFlashcard.objects.update(
                    flashcard=self,
                    bin_number=0,
                    incorrects=0,
                    showable=timezone.now()
                )
            return super().save(*args, **kwargs)




class UserFlashcard(models.Model):
    flashcard = models.ForeignKey(Flashcard,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='flashcards')

    bin_number = models.SmallIntegerField(default=0)

    last_answered = models.DateTimeField(auto_now_add=True) #Technically unneccesary but good practice
    showable = models.DateTimeField(auto_now_add=True)

    incorrects = models.SmallIntegerField(default=0)
    active = models.BooleanField(default=True)


    def __str__(self) -> str:
        return '{} User: {}'.format(self.flashcard,self.user)

    def update_correct(self):
        self.bin_number +=1
        self.last_answered = timezone.now()

        #If we hit last bin, set inactive and return
        if self.bin_number == 11:
            self.active = False
            self.save()
            return
        
        #This gives us new datetime object
        self.showable = self.last_answered + BIN_MAPPING[self.bin_number]
        self.save()

    def update_incorrect(self):
        self.incorrects +=1
        self.last_answered = timezone.now()

        if self.incorrects == 10:
            self.active = False
            self.save()
            return
        
        self.bin_number = 1
        self.showable = self.last_answered + BIN_MAPPING[self.bin_number]
        print(self.showable,self.bin_number)
        self.save()

