from django.conf.urls import patterns, url
from waliki.settings import WALIKI_SLUG_PATTERN, WALIKI_API_ROOT

from .views import PageListView, PageCreateView, PageEditView, PageDeleteView, PageHistoryView, PageVersionView, PageDiffView, PageRetrieveView, PageMoveView

urlpatterns = patterns('waliki.rest.views',
	url(r'^' + WALIKI_API_ROOT + '/all$', PageListView.as_view() , name='page_list'),
	url(r'^' + WALIKI_API_ROOT + '/new$', PageCreateView.as_view() , name='page_new'),
	url(r'^' + WALIKI_API_ROOT + '/(?P<slug>' + WALIKI_SLUG_PATTERN + ')/edit$',  PageEditView.as_view() , name='page_edit'),
	url(r'^' + WALIKI_API_ROOT + '/(?P<slug>' + WALIKI_SLUG_PATTERN + ')/delete$',  PageDeleteView.as_view() , name='page_delete'),
	url(r'^' + WALIKI_API_ROOT + '/(?P<slug>' + WALIKI_SLUG_PATTERN + ')/move$',  PageMoveView.as_view() , name='page_move'),
	url(r'^' + WALIKI_API_ROOT + '/(?P<slug>' + WALIKI_SLUG_PATTERN + ')/history/(?P<pag>\d+)/$', PageHistoryView.as_view(), name='page_history'),
	url(r'^' + WALIKI_API_ROOT + '/(?P<slug>' + WALIKI_SLUG_PATTERN + ')/history$', PageHistoryView.as_view(), name='page_history'),
	url(r'^' + WALIKI_API_ROOT + '/(?P<slug>' + WALIKI_SLUG_PATTERN + ')/version/(?P<version>[0-9a-f\^]{4,40})/$', PageVersionView.as_view(), name='page_version'),
	url(r'^' + WALIKI_API_ROOT + '/(?P<slug>' + WALIKI_SLUG_PATTERN + ')/diff/(?P<old>[0-9a-f\^]{4,40})\.\.(?P<new>[0-9a-f\^]{4,40})$', PageDiffView.as_view(), name='page_diff'),
	url(r'^' + WALIKI_API_ROOT + '/(?P<slug>' + WALIKI_SLUG_PATTERN + ')$', PageRetrieveView.as_view(), name='page_detail'),
	
)