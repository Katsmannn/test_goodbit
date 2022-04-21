import os.path
import json

from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .utils import create_promocode, search_promocode


@api_view(['POST'])
def generate_promocode(request):
    group = request.data.get('group')
    amount = request.data.get('amount')
    if group is None or amount is None:
        return Response("Отсутствуют обязательные параметры group и amount")
    promocode = create_promocode()
    while search_promocode(promocode):
        promocode = create_promocode()
    if os.path.exists(settings.FILE_PATH):
        with open(settings.FILE_PATH, 'r') as f:
            coupons = json.load(f)
    else:
        coupons = []
    group_index = [
        i for i in range(len(coupons)) if coupons[i]['group_name'] == group
    ]
    if group_index == []:
        coupons.append(
            {
                'group_name': group,
                'promocodes': [{'code': promocode, 'amount': amount}]
            }
        )
    else:
        coupons[group_index[0]]['promocodes'].append(
            {'code': promocode, 'amount': amount}
        )
    with open(settings.FILE_PATH, 'w') as f:
        json.dump(coupons, f)
    return Response({"code": promocode})


@api_view(['POST'])
def check_promocode(request):
    promocode = request.data.get('code')
    if promocode is None:
        return Response("Отсутствует обязательный параметр code")
    group = search_promocode(promocode)
    if group:
        return Response(f"Код существует. Группа - {group}.")
    return Response("Код не существует.")
