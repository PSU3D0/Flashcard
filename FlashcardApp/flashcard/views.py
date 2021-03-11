from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import JsonResponse
from django.utils import timezone

from django.views.decorators.csrf import csrf_exempt

from datetime import datetime



from .models import Flashcard, UserFlashcard
from .utils import createNewUserFlashcards



'''
User Views
'''

@login_required
def index(request):
    return render(request, 'flashcard/index.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)

            createNewUserFlashcards(user) #UserFlashcard added here

            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/sign_up.html', {'form': form})



'''
AJAX views
'''

@csrf_exempt
def updateFlashCard(request):
    if request.is_ajax() and request.user.is_authenticated and request.method == "POST":
        user_flashcard_id = request.POST.get('flashcard_id')
        user = request.user
        correct = request.POST.get('correct')


        flashcard = UserFlashcard.objects.get(user=user,pk=user_flashcard_id)
        
        if correct:
            flashcard.update_correct()
        else:
            flashcard.update_incorrect()
        
        return JsonResponse({})


'''
Why not grab the latest n cards?

A more up-to-date card (higher bin number) may become
valid while the user is solving the current cards in the 
queue. To ensure this doesn't happen, we only get the first.

If serving cards in perfect order is not a strict requirement,
we can save on database calls by passing the entire (or a portion)
of the valid queryset to the frontend
'''

def getLatestFlashCards(request):
    if request.is_ajax() and request.user.is_authenticated:
        user = request.user

        #Base check. If no more active flashcards, we are done for good
        flashcards = UserFlashcard.objects.filter(user=user, active=True)
        if not flashcards:
            return JsonResponse(
                {
                    "empty": True,
                    "Message": "You have no more words to review; you are permanently done!"
                }
            )

        '''
        This queryset naturally fulfills requirements.
        Flashcards are added to the stack in descending order by bin_number,
        meaning that after higher bin numbers are exhausted, we move onto
        bin-0 items
        '''
        flashcard = flashcards.filter(showable__lt=timezone.now())\
            .order_by("-bin_number").first()

        #If all words have positive timers, and no words in bin-0...
        if not flashcard:
            return JsonResponse(
                {
                    "empty": True,
                    "Message": "You are temporarily done; please come back later to review more words."
                }
            )

        '''
        If returning n cards, we will switch to using rest_framework
        for concise and fast serialization. For one item, we can
        manually do it with python dictionary
        '''

        res = {
            'id': flashcard.pk,
            'word': flashcard.flashcard.word,
            'definition': flashcard.flashcard.definition
        }

        
        return JsonResponse(
            {
                "empty": False,
                "data": res
            }
        )






