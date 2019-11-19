from django.db import models
from django import forms
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import *
from math import floor

# Create your models here.

class Issue(models.Model):
    name = models.CharField(max_length=256, default="Issue", help_text="Der Titel für diesen Antrag")
    reason = models.TextField(help_text="Der Grund für diesen Antrag")
    author = models.ForeignKey(User, default=1, on_delete=models.PROTECT, related_name='created_issues')
    target = models.ForeignKey(User, on_delete=models.PROTECT, related_name='is_targeted_by')
    honor_change = models.BooleanField(default="True", help_text="Ehre geben")
    creation_date = models.DateTimeField(default=datetime.now, help_text="Erstellt am")
    duration = models.DurationField(default=timedelta(1), help_text="Dauer")
    voted_yes = models.ManyToManyField(User, editable=True, related_name='voted_yes', blank=True)
    voted_no = models.ManyToManyField(User, editable=True, related_name='voted_no', blank=True)
    honor_applied = models.BooleanField(default="False", editable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.creation_date =  timezone.now()

    def isOver(self):
        return (self.creation_date + self.duration).replace(tzinfo=None) < datetime.now()

    def remaining(self):
        remainder = (self.creation_date + self.duration).replace(tzinfo=None) - datetime.now()
        days = str(remainder.days)
        hours = str(floor(remainder.seconds / (60 * 60)))
        minutes = str(floor((remainder.seconds / 60) % 60))
        sec = str(remainder.seconds % 60)
        return days + " Tagen " + hours + " Stunden " + minutes + " Minuten " + sec + " Sekunden"

    def wasAccepted(self):
        return len(self.voted_yes.all()) > len(self.voted_no.all())


YES_NO_OPTION = [("True","Ehrenmann"),("False","Ehre genommen")]
class IssueForm(forms.Form):
    name = forms.CharField(max_length=256, label="Titel", initial="Antrag", required=True)
    reason = forms.CharField(widget=forms.Textarea, label="Grund", initial="Ist ein Ehrenmann", required=True)
    target = forms.ModelChoiceField(empty_label=None, label="Ziel", queryset = None, required=True)
    honor_change = forms.ChoiceField(
        required=True,
        widget=forms.RadioSelect,
        choices=YES_NO_OPTION,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['target'].queryset = User.objects.all()

class SearchForm(forms.Form):
    search_term = forms.CharField(max_length=256, label="Titel", initial="")



class UserValues(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    ehre = models.IntegerField(default='0')

    def ref(self):
        return '/profile/' + str(self.user.id)




#make sure every user has UserValues
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserValues.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    #try:
    instance.profile.save()
    # if the profile does not exist, kwargs is modified and the call redirected to create_user_profile
    #except Exception:
    #    kwargs.update({'created': True})
    #    create_user_profile(sender, instance, **kwargs)
