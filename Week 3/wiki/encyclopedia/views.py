from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.urls import reverse

from random import randint

from django import forms

from . import util, form_classes, regex

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    title = title.capitalize()
    if util.get_entry(title):
        entry = util.get_entry(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": regex.mdconverter(entry)
        })
    else: 
        return render(request, "encyclopedia/error.html", {
            "title": title
        })

def search(request):
    if request.method == 'POST':
        query = request.POST['q']
        lowered_list = util.list_entries()
        for i in range(len(lowered_list)):
            lowered_list[i] = lowered_list[i].lower()
            if query.lower() == lowered_list[i]:
                return HttpResponseRedirect(util.list_entries()[i])
        entries = []
        for entry in util.list_entries():
            if query.lower() in entry.lower():
                entries.append(entry)
        if len(entries) != 0:
            return render(request, "encyclopedia/list.html", {
                "query": query,
                "entries": entries
            })
        else:
            return render(request, "encyclopedia/error.html", {
            "title": query
        })

def new(request):
    if request.method == 'POST':
        form = form_classes.NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            text = form.cleaned_data['text']
            lowered_list = util.list_entries()
            for i in range(len(lowered_list)):
                lowered_list[i] = lowered_list[i].lower()
            if title.lower() in lowered_list:
                form.add_error("text", forms.ValidationError("There is an article with this title already"))
                return render(request, "encyclopedia/newpage.html", {
                    "form": form
                })
            else:
                file = default_storage.open(f"entries/{title}.md", "w")
                file.write(text)
                file.close()
                return HttpResponseRedirect(title)
        else:
            return render(request, "encyclopedia/newpage.html", {
                "form": form
            })
    else:
        return render(request, "encyclopedia/newpage.html", {
            "form": form_classes.NewPageForm()
        })

def edit(request, title):
    if request.method == 'POST':
        form = form_classes.EditPageForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            file = default_storage.open(f"entries/{title}.md", "w")
            file.write(text)
            file.close()
            entry = util.get_entry(title)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "entry": regex.mdconverter(entry)
            })
    else:
        return render(request, "encyclopedia/editpage.html", {
            "form": form_classes.EditPageForm(),
            "title": title
        })

def random(request):
    list = util.list_entries()
    entry = list[randint(0, len(list) - 1)]
    return HttpResponseRedirect(entry)
