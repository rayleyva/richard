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

import bleach


from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
import jingo


from richard import utils
from videos import models


def category_list(request):
    category_kinds = models.CategoryKind.objects.all()

    ret = jingo.render(
        request, 'videos/category_list.html',
        {'title': utils.title(u'Categories'),
         'kinds': category_kinds})
    return ret


def category(request, category_id, slug):
    obj = get_object_or_404(models.Category, pk=category_id)

    ret = jingo.render(
        request, 'videos/category.html',
        {'title': utils.title(obj.title),
         'category': obj})
    return ret


def speaker_list(request):
    # TODO: Should cache this--no need to look it up every time.
    qs = models.Speaker.objects.values_list('name', flat=True)
    chars = list(set(sname[0].lower() for sname in qs))
    chars.sort()

    c = request.GET.get('character', 'a')
    try:
        if len(c) != 1 or c not in chars:
            c = chars[0]
    except TypeError:
        c = chars[0]

    speakers = models.Speaker.objects.filter(name__istartswith=c)

    ret = jingo.render(
        request, 'videos/speaker_list.html',
        {'title': utils.title(u'Speakers'),
         'chars': chars,
         'active_char': c,
         'speakers': speakers})
    return ret


def speaker(request, speaker_id, slug=None):
    obj = get_object_or_404(models.Speaker, pk=speaker_id)

    ret = jingo.render(
        request, 'videos/speaker.html',
        {'title': utils.title(obj.name),
         'speaker': obj})
    return ret


def video(request, video_id, slug):
    obj = get_object_or_404(models.Video, pk=video_id)

    meta = [
        ('keywords', ",".join([t.tag for t in obj.tags.all()]))
        ]
    if obj.summary:
        meta.append(('description', 
                     bleach.clean(obj.summary, tags=[], strip=True)))

    ret = jingo.render(
        request, 'videos/video.html',
        {'title': utils.title(obj.title),
         'meta': meta,
         'v': obj})
    return ret


# TODO: Move this elsewhere

class JSONResponse(HttpResponse):
     def __init__(self, content):
         super(JSONResponse, self).__init__(
             content, mimetype='application/json')


def apiurlforsource(request):
    host_url = request.GET.get('host_url')
    if not host_url:
        raise Http404

    obj = get_object_or_404(models.Video, source_url=host_url)
    return JSONResponse('{"source_url": "http://pyvideo.org%s"}' % obj.get_absolute_url())
