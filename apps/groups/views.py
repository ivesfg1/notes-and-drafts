from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from ..notes.forms import NoteForm  # ou from apps.notes.forms import NoteForm

from .models import Group
from .forms import GroupForm

from django.http import HttpResponse


@login_required
def group_list(request):

    logged_user = request.user
    context = {"groups": Group.objects.filter(owner=logged_user)}

    form = GroupForm(request.POST or None)

    if request.method == "POST":

        if form.is_valid():
            group = form.save(commit=False)
            group.owner = request.user
            group.save()
            return redirect(request.path)

    context["form"] = form

    return render(request, "group/list.html", context)


@login_required
def group_detail(request, pk=None):

    context = {}

    try:
        group = Group.objects.get(id=pk)

    except Group.DoesNotExist:
        return redirect("group-list")

    if group.owner != request.user:
        return HttpResponse("Você não tem permissão para realizar essa ação")

    form = NoteForm(request.POST or None)

    if request.method == "POST":

        if form.is_valid():

            note = form.save(commit=False)
            note.group = group
            note.owner = group.owner

            note.save()
            return redirect(request.path)

    context["group"] = group
    context["notes"] = group.get_notes()
    context["form"] = form

    return render(request, "group/detail.html", context)


@login_required
def group_edit(request, pk=None):

    context = {}

    try:
        group = Group.objects.get(id=pk)

    except Group.DoesNotExist:
        return redirect("group-list")

    if group.owner != request.user:
        return HttpResponse("Você não tem permissão para realizar essa ação")

    form = GroupForm(request.POST or None, instance=group)

    if request.method == "POST":

        if form.is_valid():
            form.save()
            # return redirect("group-detail", pk=group.pk)
            return redirect(
                request.GET.get("next") or "group-detail", pk=group.pk
            )  # TODO: ainda nao entendi mt bem, ver dps se mesmo quando tem o "next" ele ainda passa o pk=group.pk

    context["form"] = form

    return render(request, "group/edit.html", context)


@login_required
def group_delete(request, pk=None):

    try:
        group = Group.objects.get(id=pk)

    except Group.DoesNotExist:
        return redirect("group-list")

    if group.owner != request.user:
        return HttpResponse("Você não tem permissão para realizar essa ação")

    group.delete()
    return redirect("group-list")  # TODO: Fazer pagina pra confirmar deleção
