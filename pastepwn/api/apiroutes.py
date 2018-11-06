# -*- coding: utf-8 -*-
from sanic import Sanic
from sanic.response import json


async def default(request):
    return json({"hello": "world"})


async def ignore_404s(request, exception):
    return json({"error": "site not found"}, status=404)


async def get_paste_by_id(request, pasteId):
    return json({"pasteId": pasteId})


async def get_pastes_by_date(request):
    return json({"hello1": "world2"})


async def scrape_paste(request):
    return json({"hello1": "world2"})


async def pastepwn(request):
    return json({"hello1": "world2"})
