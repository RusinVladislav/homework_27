import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView

from ads.models import Categorie


def root(request):
    return JsonResponse({"status": "ok"}, status=200)


class CategorieDetailView(DetailView):
    model = Categorie

    def get(self, request, *args, **kwargs):
        category = self.get_object()
        return JsonResponse({"id": category.pk, "name": category.name})


@method_decorator(csrf_exempt, name='dispatch')
class CategorieListCreateView(View):
    def get(self, request):
        cat_list = Categorie.objects.all()
        return JsonResponse([{"id": cat.pk,
                              "name": cat.name
                              } for cat in cat_list], safe=False)

    def post(self, request):
        ad_data = json.loads(request.body)
        new_cat = Categorie.objects.create(**ad_data)
        return JsonResponse({"id": new_cat.pk,
                             "name": new_cat.name
                             })
