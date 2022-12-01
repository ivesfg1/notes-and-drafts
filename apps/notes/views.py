from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from ..groups.models import Group  # ou entao from apps.groups.models import Group

from .models import Note
from .forms import NoteForm

# TODO: Adicionar nas views de detail e delete para permitir ação apenas se o
# usuario logado atualmente for dono do objeto em questao


@login_required
def draft_list(request):

    logged_user = request.user
    context = {"drafts": Note.objects.global_notes().filter(owner=logged_user)}

    form = NoteForm(request.POST or None)

    if request.method == "POST":

        if form.is_valid():
            note = form.save(commit=False)
            note.owner = logged_user
            note.save()
            return redirect(request.path)

    context["form"] = form
    return render(request, "draft/list.html", context)


@login_required
def note_delete(request, pk=None):

    try:
        note = Note.objects.get(id=pk)

    except Group.DoesNotExist:
        return redirect("note-list")

    note_group = note.group
    note.delete()

    if note_group:  # pra checar se era uma anotação global ou não
        return redirect("group-detail", pk=note_group.pk)  # tem que ser pk aqui
    # TODO: Fazer pagina pra confirmar deleção

    return redirect("draft-list")
