# coding: utf-8

from django.conf.urls import url

from .views import SitesView, SiteInfoView, SummaryView, SummaryAverageView

urlpatterns = []
urlpatterns += (
    url(r'^$', SitesView.as_view(), name=u'sites'),
    url(r'^sites/$', SitesView.as_view(), name=u'sites'),
    url(r'sites/(?P<id>[0-9]+)/$', SiteInfoView.as_view(), name=u'site_info'),
    url(r'summary/$', SummaryView.as_view(), name='summary'),
    url(r'summary-average/$', SummaryAverageView.as_view(), name='summary-average')
    # url(r'get_pdf/(?P<guid>[0-9a-f-]+)/$', login_required(GetPDFResultsView.as_view()), name=u'get_pdf'),
)
