from django.urls import path, include

from . import views


urlpatterns = [
    path('',views.index,name="home"),
    path('accounts/register/',views.signup,name="register"),
    path('accounts/', include('django.contrib.auth.urls')),

    path('ajax/updateFlashCard/',views.updateFlashCard,name="update-flashcard"),
    path('ajax/getLatestFlashCards/',views.getLatestFlashCards,name="latest-flashcard")
]