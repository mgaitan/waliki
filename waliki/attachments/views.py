from django.shortcuts import render, get_object_or_404
from django.contrib import messages
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

