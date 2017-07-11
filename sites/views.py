from django.shortcuts import render
from django.views.generic import ListView
# Create your views here.

from .models import Site


class SitesView(ListView):
    template_name = u'site/sites.html'

    def get_context_data(self, **kwargs):
        context = super(SitesView, self).get_context_data(**kwargs)
        context['site'] = Site.objects.all()
        return context