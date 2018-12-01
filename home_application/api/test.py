# -*- coding: utf-8 -*-
from common.mymako import render_json


def test(request):
    return render_json({"result": True, "message": "success", "data": request.user.username})
