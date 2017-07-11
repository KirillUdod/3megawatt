from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.

import psycopg2.pool
import psycopg2.extras

from .models import Site, SiteData



class SitesView(TemplateView):
    template_name = u'site/sites.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['sites'] = Site.objects.all()
        return data


class SiteInfoView(TemplateView):
    template_name = u'site/site-info.html'

    def get_context_data(self, id, **kwargs):
        data = super().get_context_data(**kwargs)
        try:
            data['site'] = Site.objects.get(id=id)
            if data['site']:
                data['data'] = SiteData.objects.filter(site=data['site'])
        finally:
            return data


class SummaryView(TemplateView):
    template_name = u'site/summary.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['data'] = []
        for site in Site.objects.all():
            con = {}
            con['name'] = site.name
            temp = SiteData.objects.filter(site=site)
            con['a_val'] = sum(t.a_value for t in temp)
            con['b_val'] = sum(t.b_value for t in temp)
            data['data'].append(con)
        return data


class SummaryAverageView(TemplateView):
    template_name = u'site/summary.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['data'] = []
        data['data'] = get_data()
        return data


def get_data():
    psycopg2.extensions.register_adapter(dict, psycopg2.extras.Json)

    pool = psycopg2.pool.ThreadedConnectionPool(1, 100, database='mw', host='localhost', port='5432', user='mw',
                                            password='mw2017')
    conn = pool.getconn()
    curs = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    data = []
    try:
        curs.execute("SELECT * FROM sites_site")
        sites = curs.fetchall()
        for site in sites:
            data1 = {}
            data1['name'] = site['name']
            curs.execute("SELECT * FROM sites_sitedata WHERE site_id={id}". format(id=site['id']))
            mytest = curs.fetchall()

            temp_arr_a = []
            temp_arr_b = []
            for l in mytest:
                temp_arr_a.append(l['a_value'])
                temp_arr_b.append(l['b_value'])
            data1['a_val'] = sum(temp_arr_a) / float(len(temp_arr_a))
            data1['b_val'] = sum(temp_arr_b) / float(len(temp_arr_b))
            #
            # data1['a_val'] = list(sum(l) / float(len(l)) for l in [arr['a_value'] for arr in mytest])
            # data1['b_val'] = list(sum(l) / float(len(l)) for l in [arr['b_value'] for arr in mytest])
            # print(data1)

            # data1['a_val'] = []
            # data1['b_val'] = []
            # print(list((sum(l['b_value']) / float(len(l['b_value'])) for l in mytest)))
            # print(list(sum(l['b_value']) / float(len(l['b_value'])) for l in mytest))
            data.append(data1)
        return data

    except psycopg2.Error as e:
        conn.rollback()
        print('error %s %s' % (e.pgcode, e.pgerror))
    except Exception as ex:
        conn.rollback()
        print('error %s' % ex)
    finally:
        curs.close()
        conn.close()
        pool.putconn(conn)
