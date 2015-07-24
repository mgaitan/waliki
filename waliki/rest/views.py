from django.contrib import messages
from waliki import settings
from django.http import HttpResponse,  HttpResponseRedirect

from waliki.models import Page
from waliki import views
from waliki.git import Git
from waliki.git.views import version, diff, history as git_history

from rest_framework import generics, permissions, mixins, status
from rest_framework.response import Response

from .serializers import PageListRetrieveSerializer, PageCreateSerializer, PageEditSerializer, PageDeleteSerializer, PageRetrieveSerializer, PageMoveSerializer
from .permissions import WalikiPermission_AddPage, WalikiPermission_ViewPage, WalikiPermission_ChangePage

class PageRetrieveView(
    mixins.RetrieveModelMixin,
    generics.GenericAPIView):
    """
    A simple View to retrieve a Page.
    """
    lookup_field = 'slug'
    serializer_class = PageRetrieveSerializer
    permission_classes = (WalikiPermission_ViewPage, )

    def get_queryset(self):
        return Page.objects.filter(slug=self.kwargs['slug'])

    def get(self, request, *args, **kwargs):
        response = views.detail(request._request, raw=True, *args, **kwargs)
        
        if 302 ==response.status_code:
            return HttpResponseRedirect(request.path.rstrip('/'+kwargs['slug'])+response.url)
        
        return self.retrieve(request, *args, **kwargs)



class PageListView(generics.ListAPIView):
    """
    A simple View to list all Pages.
    """
    queryset = Page.objects.all()
    serializer_class = PageListRetrieveSerializer
    permission_classes = (WalikiPermission_ViewPage, )


class PageCreateView(generics.CreateAPIView):
    """
    A simple View to create a new Page.
    """
    serializer_class = PageCreateSerializer
    permission_classes = (WalikiPermission_AddPage, )


class PageEditView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    generics.GenericAPIView):
    """
    A View to edit a Page.
    """
    lookup_field = 'slug'
    serializer_class = PageEditSerializer
    permission_classes = (WalikiPermission_ChangePage, )

    def get_queryset(self):
        return Page.objects.filter(slug=self.kwargs['slug'])

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
       

class PageDeleteView(generics.GenericAPIView):
    """
    A no much simple View to delete a Page or namespace.
    """
    lookup_field = 'slug'
    serializer_class = PageDeleteSerializer
    permission_classes = (WalikiPermission_ChangePage, )

    def get_queryset(self):
        return Page.objects.filter(slug=self.kwargs['slug'])

    def post(self, request, *args, **kwargs):
        #call waliki.view.delete
        response = views.delete(request._request,*args, **kwargs)

        django_messages = []

        for message in messages.get_messages(request):
            django_messages.append({
                "level": message.level,
                "message": message.message,
                "extra_tags": message.tags,
            })
        return Response(django_messages, status=status.HTTP_200_OK)


class PageHistoryView(
    mixins.RetrieveModelMixin,
    generics.GenericAPIView):
    """
    A complex and c+p View to get history of one Page.
    """
    lookup_field = 'slug'
    serializer_class = PageListRetrieveSerializer
    permission_classes = (WalikiPermission_ViewPage, )

    def get_queryset(self):
        return Page.objects.filter(slug=self.kwargs['slug'])[0]

    def get(self, request, *args, **kwargs):
        pag = kwargs.get('pag', 1)
        page = self.get_queryset()

        #same code of waliki.git.views.history
        pag = int(pag or 1)
        skip = (pag - 1) * settings.WALIKI_PAGINATE_BY
        max_count = settings.WALIKI_PAGINATE_BY
        
        history = Git().history(page)
        max_changes = max([(v['insertion'] + v['deletion']) for v in history])
        data = {'page': self.get_serializer(page, many=False).data,
        'history': history[skip:(skip+max_count)],
        'max_changes': max_changes,
        'prev': pag - 1 if pag > 1 else None,
        'next': pag + 1 if skip + max_count < len(history) else None}
        return Response(data)


class PageVersionView(
    mixins.RetrieveModelMixin,
    generics.GenericAPIView):
    """
    A View to retrieve a version of a Page.
    """
    lookup_field = 'slug'
    serializer_class = PageListRetrieveSerializer
    permission_classes = (WalikiPermission_ViewPage, )

    def get_queryset(self):
        return Page.objects.filter(slug=self.kwargs['slug'])[0]

    def get(self, request, *args, **kwargs):
        page = self.get_queryset()

        #call waliki.git version
        response = version(request, raw=True,  *args, **kwargs)

        data = self.get_serializer(page, many=False).data
        data['raw'] = response.content.decode("utf8")
        data['version'] = kwargs['version']

        return Response(data)

class PageDiffView(
    mixins.RetrieveModelMixin,
    generics.GenericAPIView):
    """
    to view diff between versions.
    """
    lookup_field = 'slug'
    serializer_class = PageListRetrieveSerializer
    permission_classes = (WalikiPermission_ViewPage, )

    def get_queryset(self):
        return Page.objects.filter(slug=self.kwargs['slug'])[0]

    def get(self, request, *args, **kwargs):
        page = self.get_queryset()

        #call waliki.git diff
        response = diff(request, raw=True,  *args, **kwargs)

        data = self.get_serializer(page, many=False).data
        data['new'] = kwargs['new']
        data['old'] = kwargs['old']
        data['raw'] = response.content.decode("utf8")

        return Response(data)



class PageMoveView(generics.GenericAPIView):
    """
    View to move a Page.
    """
    lookup_field = 'slug'
    serializer_class = PageMoveSerializer
    permission_classes = (WalikiPermission_ChangePage, )

    def get_queryset(self):
        return Page.objects.filter(slug=self.kwargs['slug'])

    def post(self, request, *args, **kwargs):
        #call waliki.view.delete
        response = views.move(request._request,*args, **kwargs)

        django_messages = []

        for message in messages.get_messages(request):
            django_messages.append({
                "level": message.level,
                "message": message.message,
                "extra_tags": message.tags,
            })
        return Response(django_messages, status=status.HTTP_200_OK)