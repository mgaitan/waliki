# -*- coding: utf-8 -*-
import json
import imghdr
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.utils.six import text_type
from django.http import HttpResponse
from sendfile import sendfile
from waliki.models import Page
from waliki.acl import permission_required
from .models import Attachment


@permission_required('change_page')
def attachments(request, slug):
    last_attached = None
    page = get_object_or_404(Page, slug=slug)
    if request.method == 'POST' and 'attach' in request.FILES:
        last_attached = request.FILES['attach']
        Attachment.objects.create(file=last_attached, page=page)
        messages.success(request, '"%s" was attached succesfully to /%s' % (last_attached.name, page.slug))
    return render(request, 'waliki/attachments.html', {'page': page})


@permission_required('delete_page')
def delete_attachment(request, slug, attachment_id_or_filename):
    if attachment_id_or_filename.isnumeric():
        attachment = get_object_or_404(Attachment, id=attachment_id_or_filename, page__slug=slug)
    else:
        attachment = get_object_or_404(Attachment, file__endswith=attachment_id_or_filename, page__slug=slug)
    name = text_type(attachment)
    if request.is_ajax() and request.method in ('POST', 'DELETE'):
        attachment.delete()
        return HttpResponse(json.dumps({'removed': name}), content_type="application/json")
    return HttpResponse(json.dumps({'removed': None}), content_type="application/json")


@permission_required('view_page', raise_exception=True)
def get_file(request, slug, attachment_id=None, filename=None):
    attachment = get_object_or_404(Attachment, file__endswith=filename, page__slug=slug)
    as_attachment = ((not imghdr.what(attachment.file.path) and 'embed' not in request.GET)
                      or 'as_attachment' in request.GET)
    # ref https://github.com/johnsensible/django-sendfile
    return sendfile(request, attachment.file.path,
                    attachment=as_attachment, attachment_filename=text_type(attachment))
