# richard -- video index system
# Copyright (C) 2012 richard contributors.  See AUTHORS.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.conf.urls.defaults import patterns, url
from haystack.views import SearchView, search_view_factory
from haystack.forms import ModelSearchForm
from richard import utils


class TitledSearchView(SearchView):
    def extra_context(self):
        # TODO: Not sure why .extra_context() kicks up an
        # AttributeError here, but SearchView.extra_context() returns
        # an empty dict anyhow, so I'll use that for now.
        # 
        # extra = super(SearchView, self).extra_context()
        if self.query:
            title = u'Search: ' + self.query
        else:
            title = u'Search'
        return {'title': utils.title(title)}


urlpatterns = patterns(
    'videos.views',

    # categories
    url(r'category/?$',
        'category_list', name='videos-category-list'),
    url(r'category/(?P<category_id>[0-9]+)/(?P<slug>[\w-]*)/?$',
        'category', name='videos-category'),

    # speakers
    url(r'speaker/$',
        'speaker_list', name='videos-speaker-list'),
    url(r'speaker/(?P<speaker_id>[0-9]+)/?$',
        'speaker', name='videos-speaker-noslug'),
    url(r'speaker/(?P<speaker_id>[0-9]+)/(?P<slug>[\w-]*)/?$',
        'speaker', name='videos-speaker'),

    # videos
    url(r'video/(?P<video_id>[0-9]+)/(?P<slug>[\w-]*)/?$',
        'video', name='videos-video'),

    # search
    url(r'^search/?$',
        search_view_factory(
            view_class=TitledSearchView,
            template='videos/search.html',
            form_class=ModelSearchForm),
        name='haystack-search'),

    # faux api for carl
    url(r'^api/1.0/videos/urlforsource$',
        'apiurlforsource', name='videos-api-urlforsource'),
)
