from django.shortcuts import render,redirect
from django.http import HttpResponse, Http404
from .models import *
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from decimal import *

# Create your views here.

@login_required
def createFeedback(request):
    if request.method == "POST":
        form = FeedBackForm(request.POST)
        if form.is_valid():
            feedback = FeedBack()
            feedback.betreff = form.cleaned_data["betreff"]
            feedback.text = form.cleaned_data["text"]
            feedback.save()
            return redirect("/")
        return render(request, "feedBackCreation.html", {"form": form})
    else:
        form = FeedBackForm()
    return render(request, "feedBackCreation.html", {"form": form})


@login_required
def feedBack(request):
    return render(request, "feedBack.html", {"feedbacks": FeedBack.objects.all()})
