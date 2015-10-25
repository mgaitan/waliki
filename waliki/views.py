import json
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.core.urlresolvers import reverse
from .models import Page, Redirect
from .forms import PageForm, MovePageForm, DeleteForm, NewPageForm
from .signals import page_saved, page_preedit, page_moved
from ._markups import get_all_markups
from .acl import permission_required
from . import settings


def home(request):
    return detail(request, slug=settings.WALIKI_INDEX_SLUG)


def compile_breadcrumbs(slug):
    breadcrumbs = [(reverse('waliki_home'), _('Home')),]
    if slug == settings.WALIKI_INDEX_SLUG:
        return breadcrumbs
    slug_parts = slug.split('/')
    url = ''
    # for every string from start until the next slash (or end of string)
    for part in slug_parts:
        # if page exists, find url and title
        # otherwise, grab url and title from slug
        url = url + part
        pages = Page.objects.filter(slug=url)
        url = url + '/'
        if pages:
            title = pages[0].title
        else:
           title = part
        breadcrumbs.append(('/'+url, title))
    return breadcrumbs


@permission_required('view_page')
def detail(request, slug, raw=False):

    slug = slug.strip('/')

    # handle redirects first
    try:
        redirect = Redirect.objects.get(old_slug=slug)      # noqa
        if redirect.status_code == 302:
            return HttpResponseRedirect(redirect.get_absolute_url())
        return HttpResponsePermanentRedirect(redirect.get_absolute_url())
    except Redirect.DoesNotExist:
        pass

    try:
        page = Page.objects.get(slug=slug)
    except Page.DoesNotExist:
        page = None
    if raw and page:
        return HttpResponse(page.raw, content_type='text/plain; charset=utf-8')
    elif raw:
        raise Http404

    context = {'page': page, 'slug': slug}
    if settings.WALIKI_BREADCRUMBS == True:
        context['breadcrumbs'] = compile_breadcrumbs(slug)
    return render(request, 'waliki/detail.html', context)


@permission_required('change_page')
def move(request, slug):
    page = get_object_or_404(Page, slug=slug)
    data = request.POST if request.method == 'POST' else None
    form = MovePageForm(data, instance=page)
    if request.method == 'POST' and form.is_valid():
        new_slug = form.cleaned_data['slug']

        # remove redirections (now there is an actual page)
        Redirect.objects.filter(old_slug=new_slug).delete()
        # squash redirections to new destiny
        Redirect.objects.filter(new_slug=slug).update(new_slug=new_slug)
        # create the new redirection
        Redirect.objects.create(old_slug=slug, new_slug=new_slug)

        if not form.cleaned_data['just_redirect']:
            old_path = page.path
            page.move(new_slug + page.markup_.file_extensions[0])
            page.slug = new_slug
            page.save()
            msg = _("Page moved from %(old_slug)s") % {'old_slug': slug}
            page_moved.send(sender=move,
                            page=page,
                            old_path=old_path,
                            author=request.user,
                            message=msg,
                            )
            url = page.get_absolute_url()
        else:
            msg = _("A redirection from %(old_slug)s to this page was added") % {'old_slug': slug}

        url = reverse('waliki_detail', args=[new_slug])
        messages.success(request, msg)

        if request.is_ajax():
            return HttpResponse(json.dumps({'redirect': url}), content_type="application/json")
        return redirect(url)

    if request.is_ajax():
        data = render_to_string('waliki/generic_form.html', {'page': page, 'form': form},
                                context_instance=RequestContext(request))
        return HttpResponse(json.dumps({'data': data}), content_type="application/json")
    return render(request, 'waliki/generic_form.html', {'page': page, 'form': form})


@permission_required('change_page')
def edit(request, slug):
    slug = slug.strip('/')
    just_created = False
    try:
        page = Page.objects.get(slug=slug)
    except Page.DoesNotExist:
        if request.method == 'POST':
            page = Page.objects.create(slug=slug)
            page.raw = ""
            page_saved.send(sender=edit,
                            page=page,
                            author=request.user,
                            message=_("Page created"),
                            form_extra_data={})
            just_created = True
        else:
            return redirect('waliki_detail', slug)

    original_markup = page.markup
    data = request.POST if request.method == 'POST' and not just_created else None
    form_extra_data = {}
    receivers_responses = page_preedit.send(sender=edit, page=page)
    for r in receivers_responses:
        if isinstance(r[1], dict) and 'form_extra_data' in r[1]:
            form_extra_data.update(r[1]['form_extra_data'])

    form = PageForm(
        data, instance=page, initial={'extra_data': json.dumps(form_extra_data)})
    if form.is_valid():
        page = form.save(commit=False)
        if page.markup != original_markup:
            old_path = page.path
            page.update_extension()
            msg = _("The markup was changed from {original} to {new}").format(original=original_markup,
                                                                              new=page.markup)
            page_moved.send(sender=edit,
                            page=page,
                            old_path=old_path,
                            author=request.user,
                            message=msg,
                            commit=False
                            )
            was_moved = True
            messages.warning(request, msg)
        else:
            was_moved = False
        page.raw = form.cleaned_data['raw']
        page.save()
        try:
            receivers_responses = page_saved.send(sender=edit,
                                                  page=page,
                                                  author=request.user,
                                                  message=form.cleaned_data[
                                                      "message"],
                                                  form_extra_data=json.loads(form.cleaned_data["extra_data"] or "{}"),
                                                  was_moved=was_moved)
        except Page.EditionConflict as e:
            messages.warning(request, e)
            return redirect('waliki_edit', slug=page.slug)

        for r in receivers_responses:
            if isinstance(r[1], dict) and 'messages' in r[1]:
                for key, value in r[1]['messages'].items():
                    getattr(messages, key)(request, value)

        if 'next' in request.GET:
            return redirect(request.GET['next'])
        return redirect('waliki_detail', slug=page.slug)
    cm_modes = [(m.name, m.codemirror_mode_name) for m in get_all_markups()]

    cm_settings = settings.WALIKI_CODEMIRROR_SETTINGS
    cm_settings.update({'mode': dict(cm_modes)[page.markup]})
    return render(request, 'waliki/edit.html', {'page': page,
                                                'form': form,
                                                'slug': slug,
                                                'cm_modes': cm_modes,
                                                'cm_settings': json.dumps(cm_settings)})


def preview(request):
    data = {}
    if request.is_ajax() and request.method == "POST":
        data['html'] = Page.preview(
            request.POST['markup'], request.POST['text'])
        return HttpResponse(json.dumps(data), content_type="application/json")


@permission_required('delete_page')
def delete(request, slug):
    page = get_object_or_404(Page, slug=slug)
    data = request.POST if request.method == 'POST' else None
    form = DeleteForm(data)
    if form.is_valid():
        if form.cleaned_data['what'] == 'this':
            msg = _("The page %(slug)s was deleted") % {'slug': slug}
            page.delete()
        else:
            Page.objects.filter(slug__startswith=slug).delete()
            msg = _("The page %(slug)s and all its namespace was deleted") % {
                'slug': slug}

        messages.warning(request, msg)
        if request.is_ajax():
            return HttpResponse(json.dumps({'redirect': reverse('waliki_home')}), content_type="application/json")
        return redirect('waliki_home')

    if request.is_ajax():
        data = render_to_string('waliki/delete.html', {'page': page, 'form': form},
                                context_instance=RequestContext(request))
        return HttpResponse(json.dumps({'data': data}), content_type="application/json")
    return render(request, 'waliki/delete.html', {'page': page, 'form': form})


def new(request):
    data = request.POST if request.method == 'POST' else None
    form = NewPageForm(data, user=request.user)
    if request.method == 'POST' and form.is_valid():
        page = form.save()
        page.raw = ""
        page_saved.send(sender=new,
                        page=page,
                        author=request.user,
                        message=_("Page created"),
                        form_extra_data={})
        if request.is_ajax():
            return HttpResponse(json.dumps({'redirect': page.get_edit_url()}), content_type="application/json")
        return redirect(page.get_edit_url())

    if request.is_ajax():
        data = render_to_string('waliki/generic_form.html', {'form': form},
                                context_instance=RequestContext(request))
        return HttpResponse(json.dumps({'data': data}), content_type="application/json")
    return render(request, 'waliki/generic_form.html', {'form': form})


def get_slug(request):
    slug = settings.get_slug(request.GET.get('title', ''))
    return HttpResponse(json.dumps({'slug': slug}), content_type="application/json")
