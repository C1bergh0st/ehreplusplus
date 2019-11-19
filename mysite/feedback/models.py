from django.db import models
from django import forms

# Create your models here.

class FeedBack(models.Model):
    betreff = models.CharField(max_length=256, default=str(), help_text="Betreff")
    text = models.TextField(help_text="Was gibt's?")
    creation_date = models.DateTimeField(auto_now=True, help_text="Erstellt am")

class FeedBackForm(forms.Form):
    betreff = forms.CharField(max_length=256, label="Betreff", initial="", required=True)
    text = forms.CharField(widget=forms.Textarea, label="Was gibt's?", initial="", required=True)
