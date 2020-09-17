import markdown2
import secrets

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import forms
from django.urls import reverse

from . import util
from markdown2 import Markdown

# class CreateForm(forms.Form):
#     titulo = forms.CharField(label="Entry Title", widget=forms.TextInput())
#     contenido = forms.CharField(label="Content", widget=forms.Textarea())
class CreateForm(forms.Form):
    title = forms.CharField(label="Entry title", widget=forms.TextInput())
    content = forms.CharField(widget=forms.Textarea())
    edit = forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request,entry):
    markdowner = Markdown()
    entryMD = util.get_entry(entry)
    if entryMD is None:
        return render(request, "encyclopedia/entryError.html", {
            "entryTitle": entry,
            "error": "Warning!!!"
        })
    else:
         return render(request, "encyclopedia/entry.html", {
             "entry": markdowner.convert(entryMD),
             "entryTitle": entry
         })   

def newPage(request):
    #Return method POST
    if request.method == "POST":
        #Form with its values
       form = CreateForm(request.POST)
       #Boolean
       if form.is_valid():
           #value: conten and title
           title = form.cleaned_data["title"]
           content = form.cleaned_data["content"]
           if util.get_entry(title) is None or form.cleaned_data["edit"] is True:
               util.save_entry(title, content)
               return HttpResponseRedirect(reverse('entry', kwargs={'entry': title}))
           else:
               return render(request, "encyclopedia/entryError.html")    
       else:
           return render(request, "encyclopedia/newPage.html")    
    else:
    #not a POST method    
        return render(request, "encyclopedia/newPage.html",{
            "form": CreateForm()
        })   

def edit(request, entry):
    newEntry = util.get_entry(entry) 
    if newEntry is None:
        return render(request, "encyclopedia/entryError.html",{
            "entryTitle": entry
        })       
    else:
        form = CreateForm()    
        form.fields["title"].initial = entry
        form.fields["title"].widget = forms.HiddenInput()
        form.fields["content"].initial = newEntry
        form.fields["edit"].initial = True
        return render(request, "encyclopedia/newPage.html",{
            "form": form,
            "entryTitle": form.fields["title"].initial,
            "edit": form.fields["edit"].initial
        })

def random(request):
    random = util.list_entries()
    randomList = secrets.choice(random)
    return HttpResponseRedirect(reverse('entry', kwargs={'entry': randomList}))

def search(request):
    value = request.GET.get('q', '')
    if util.get_entry(value) is not None:
        return HttpResponseRedirect(reverse('entry', kwargs={'entry': value}))   
    else:
        return render(request, "encyclopedia/index.html",{
            "value": value,
            "state": True
        })    