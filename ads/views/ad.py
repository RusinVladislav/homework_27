import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView

from ads.models import Ad


def root(request):
    return JsonResponse({"status": "ok"}, status=200)


class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        ad = self.get_object()
        return JsonResponse({"id": ad.pk,
                             "name": ad.name,
                             "author": ad.author,
                             "price": ad.price,
                             "description": ad.description,
                             "address": ad.address,
                             "is_published": ad.is_published
                             })


@method_decorator(csrf_exempt, name='dispatch')
class AdListCreateView(View):
    def get(self, request):
        ad_list = Ad.objects.all()
        return JsonResponse([{"id": ad.pk,
                              "name": ad.name,
                              "author": ad.author,
                              "price": ad.price,
                              "description": ad.description,
                              "address": ad.address,
                              "is_published": ad.is_published
                              } for ad in ad_list], safe=False)

    def post(self, request):
        ad_data = json.loads(request.body)
        new_ad = Ad.objects.create(**ad_data)
        return JsonResponse({"id": new_ad.pk,
                             "name": new_ad.name,
                             "author": new_ad.author,
                             "price": new_ad.price,
                             "description": new_ad.description,
                             "address": new_ad.address,
                             "is_published": new_ad.is_published
                             })
