from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .models import Group, Note
from .forms import GroupForm, NoteForm


def draft_list(request):

    context = {"drafts": Note.objects.global_notes()}

    if request.method == "POST":

        form = NoteForm(request.POST)

        if form.is_valid():
            note = form.save(commit=False)
            note.owner = request.user
            note.save()
            return redirect(request.path)

    form = NoteForm()
    context["form"] = form
    return render(request, "draft/list.html", context)


def group_list(request):

    context = {"groups": Group.objects.all()}

    if request.method == "POST":
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.owner = request.user
            group.save()
            return redirect(request.path)

    form = GroupForm()
    context["form"] = form

    return render(request, "group/list.html", context)


def group_detail(request, pk=None):

    context = {}

    try:
        group = Group.objects.get(id=pk)

    except Group.DoesNotExist:
        return redirect("group-list")

    if request.method == "POST":

        form = NoteForm(request.POST)

        if form.is_valid():

            note = form.save(commit=False)
            note.group = group
            note.owner = group.owner

            note.save()
            return redirect(request.path)

    form = NoteForm()

    context["group"] = group
    context["notes"] = group.get_notes()
    context["form"] = form

    return render(request, "group/detail.html", context)


def group_edit(request, pk=None):

    context = {}

    try:
        group = Group.objects.get(id=pk)

    except Group.DoesNotExist:
        return redirect("group-list")

    if request.method == "POST":

        form = NoteForm(request.POST)

        if form.is_valid():

            note = form.save(commit=False)
            note.group = group
            note.owner = group.owner

            note.save()
            return redirect(request.path)

    form = NoteForm()

    context["group"] = group
    context["notes"] = group.get_notes()
    context["form"] = form

    return render(request, "group/detail.html", context)


def group_delete(request, pk=None):

    try:
        group = Group.objects.get(id=pk)

    except Group.DoesNotExist:
        return redirect("group-list")

    group.delete()
    return redirect("group-list")  # TODO: Fazer pagina pra confirmar deleção


def note_delete(request, pk=None):

    try:
        note = Note.objects.get(id=pk)

    except Group.DoesNotExist:
        return redirect("note-list")

    note_group = note.group
    note.delete()

    if note_group:  # pra checar se era uma anotação global ou não
        return redirect("group-detail", pk=note_group.pk)  # tem que ser pk aqui

    return redirect("draft-list")
