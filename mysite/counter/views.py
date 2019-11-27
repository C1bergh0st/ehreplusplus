from django.shortcuts import *
from django.http import HttpResponse, Http404
from .models import *
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from decimal import *

# Create your views here.

@login_required
def issue(request, id):
    if (request.method == "POST"):
        form = IssueCommentForm(request.POST)
        if form.is_valid():
            comment = IssueComment()
            comment.text = form.cleaned_data["text"]
            comment.author = request.user
            comment.save()
            form = IssueCommentForm()
    else:
        form = IssueCommentForm()
    issue = None
    try:
        issue = Issue.objects.get(id=id)
        keepConsistent(issue)
    except Exception as e:
        raise Http404("Issue does not exist")
    return render(request, "issue.html", {"issue":issue, "isOver":issue.isOver(),"form":form})

@login_required
def allIssues(request):
    return render(request, "allIssues.html", {"issues":Issue.objects.all()})

@login_required
def createIssue(request):
    if request.method == "POST":
        form = IssueForm(request.POST)
        if form.is_valid():
            issue = Issue()
            issue.name = form.cleaned_data["name"]
            issue.reason = form.cleaned_data["reason"]
            issue.author = request.user
            issue.target = form.cleaned_data["target"]
            issue.honor_change = form.cleaned_data["honor_change"]
            print(form.cleaned_data["honor_change"])
            issue.save()
            return redirect("/issue/" + str(issue.id))
        return render(request, "issueCreation.html", {"form": form})
    else:
        form = IssueForm()
    return render(request, "issueCreation.html", {"form": form})

@login_required
def rank(request):
    sortedUsers = sorted(User.objects.all(), key=lambda t: t.profile.ehre, reverse=True)
    #sortedUsers = User.objects.all()
    print(sortedUsers)
    return render(request, "rank.html",{"users": sortedUsers})

@login_required
def search(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            search_term = str(form.cleaned_data["search_term"])
            issues_1 = Issue.objects.filter(name__icontains=search_term)
            issues_2 = Issue.objects.filter(reason__icontains=search_term)
            user_1 = User.objects.filter(username__icontains=search_term)
            user_2 = User.objects.filter(first_name__icontains=search_term)
            user_3 = User.objects.filter(last_name__icontains=search_term)
            gangs = Group.objects.filter(name__icontains=search_term)
            issues = issues_1 | issues_2
            users = user_1 | user_2 | user_3
            return render(request, "search.html", {"form":form, "gangs":gangs, "issues":issues, "users":users, "search_term":str(form.cleaned_data["search_term"])})
    else:
        form = SearchForm()
    return render(request, "search.html", {"form": form})

@login_required
def gang(request, id):
    group = get_object_or_404(Group, id=id)
    for user in group.members.all():
        for issue in user.is_targeted_by.all():
            keepConsistent(issue)
    return render(request, "gang.html", {"group":group})

@login_required
def gangSettings(request, id):
    group = get_object_or_404(Group, id=id)
    if (request.user != group.admin):
        return render(request, "denied.html")
    return render(request, "gangSettings.html", {"group":group})


@login_required
def mygangs(request):
    return render(request, "mygangs.html",{"gangs":request.user.ehre_groups.all()})

@login_required
def gangRequest(request, id):
    group = get_object_or_404(Group, id=id)
    user = request.user
    if (user not in group.members.all()) and (user not in group.initiates.all()):
        group.initiates.add(user)
        return redirect("/gang/" + str(group.id))
    else:
        return render(request, "error.html");

@login_required
def gangChange(request, id, uid, approve):
    group = get_object_or_404(Group, id=id)
    user = get_object_or_404(User, id=uid)
    if (request.user != group.admin):
        return render(request, "denied.html")
    approveBool = None
    if(approve == "True"):
        approveBool = True;
    elif (approve == "False"):
        approveBool = False
    else:
        return render(request, "error.html");
    if user not in group.initiates.all():
        return render(request, "error.html");
    if approveBool:
        group.members.add(user)
        group.initiates.remove(user)
    else:
        group.members.remove(user)
        group.initiares.remove(user)
    return redirect("/gang/" + str(group.id) + "/settings")

@login_required
def createGang(request):
    if request.method == "POST":
        form = GroupForm(request.POST)
        if form.is_valid():
            group = Group()
            group.name = form.cleaned_data["name"]
            group.admin = request.user
            group.members.add(request.user)
            group.save()
            return redirect("/gang/" + str(group.id))
        return render(request, "gangCreation.html", {"form": form})
    else:
        form = GroupForm()
    return render(request, "gangCreation.html", {"form": form})


def keepConsistent(issue):
    if(issue.honor_applied or (issue.creation_date + issue.duration).replace(tzinfo=None) > datetime.now()):
        return
    user = issue.target
    profile = user.profile
    print("Ehre davor" + str(profile.ehre));
    if(len(issue.voted_yes.all()) > len(issue.voted_no.all())):
        print("Angenommen");
        if(issue.honor_change):
            profile.ehre += Decimal(1)
        else:
            #profile.ehre -= Decimal(1)
            profile.ehre = Decimal(0);
    print("Ehre danach" + str(profile.ehre));
    issue.honor_applied = True
    issue.save()
    profile.save()
    return


@login_required
def vote(request, issue_id, approve):
    issue = None
    user = None
    approveBool = None

    if(approve == "True"):
        approveBool = True;
    elif (approve == "False"):
        approveBool = False
    else:
        raise HttpResponseBadRequest("");

    issue = get_object_or_404(Issue, id=issue_id)
    keepConsistent(issue)

    if((issue.creation_date + issue.duration).replace(tzinfo=None) < datetime.now()):
        return HttpResponse("The issue has expired")
    try:
        user = request.user
    except Exception as e:
        raise Http404("User does not exist")

    if (approveBool):
        if(user in issue.voted_no.all()):
            issue.voted_no.remove(user)
        issue.voted_yes.add(user)
    else:
        if(user in issue.voted_yes.all()):
            issue.voted_yes.remove(user)
        issue.voted_no.add(user)

    return redirect("/issue/" + str(issue.id))

@login_required
def redirectToUserProfile(request):
    user = request.user;
    return redirect("/profile/" + str(user.id))


@login_required
def profile(request, id):
    profileUser = None
    try:
        profileUser = User.objects.get(id=id)
    except Exception as e:
        raise Http404("User does not exist")
    for iss in profileUser.is_targeted_by.all():
        keepConsistent(iss)
    for iss in profileUser.created_issues.all():
        keepConsistent(iss)

    return render(request, "profile.html", {
        "user":profileUser,
        "issues":profileUser.is_targeted_by.all(),
        "created":profileUser.created_issues.all(),
    })
    return HttpResponse(str(profileUser.username) + "<br>" + str(profileUser.profile.ehre) + "<br>" + response)

def index(request):
    if not request.user.is_authenticated:
        return render(request, "newUserFrontPage.html")
    for iss in Issue.objects.all():
        keepConsistent(iss)
    return render(request, "registration/home.html",{"issues":Issue.objects.all()})
