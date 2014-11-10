import json
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.utils.six import text_type
from django.http import HttpResponse
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


@permission_required('change_page')
def delete_attachment(request, slug, attachment_id):
	attachment = get_object_or_404(Attachment, id=attachment_id, page__slug=slug)
	name = text_type(attachment)
	if request.is_ajax() and request.method in ('POST', 'DELETE'):
		attachment.delete()
		return HttpResponse(json.dumps({'removed': name}), content_type="application/json")
	return HttpResponse(json.dumps({'removed': None}), content_type="application/json")