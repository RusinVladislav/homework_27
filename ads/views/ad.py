import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, DeleteView, UpdateView

from ads.models import Ad, Category
from users.models import User

ADS_ON_PAGE = 4


def root(request):
    return JsonResponse({"status": "ok"}, status=200)


class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        ad = self.get_object()
        return JsonResponse({"id": ad.pk,
                             "name": ad.name,
                             "author": ad.author.username,
                             "price": ad.price,
                             "description": ad.description,
                             "address": [loc.name for loc in ad.author.locations.all()],
                             "is_published": ad.is_published,
                             "image": ad.image.url if ad.image else None
                             })


class AdListView(ListView):
    model = Ad
    queryset = Ad.objects.order_by("-price")

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        paginator = Paginator(self.object_list, ADS_ON_PAGE)
        page_num = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_num)

        ads = [{"id": ad.pk,
                "name": ad.name,
                "author": ad.author.username,
                "price": ad.price,
                "description": ad.description,
                "address": [loc.name for loc in ad.author.locations.all()],
                "is_published": ad.is_published,
                "image": ad.image.url if ad.image else None} for ad in page_obj]
        result = {"items": ads,
                  "num_pages": paginator.num_pages,
                  "total": paginator.count
                  }

        return JsonResponse(result, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class AdCreatelView(CreateView):
    model = Ad
    fields = "__all__"

    def post(self, request, *args, **kwargs):
        ad_data = json.loads(request.body)
        author = get_object_or_404(User, pk=ad_data["author_id"])
        category = get_object_or_404(Category, pk=ad_data["category_id"])
        new_ad = Ad.objects.create(name=ad_data["name"],
                                   price=ad_data["price"],
                                   author=author,
                                   category=category,
                                   description=ad_data.get("description"),
                                   is_published=ad_data.get("is_published", False)
                                   )
        return JsonResponse({"id": new_ad.pk,
                             "name": new_ad.author.username,
                             "author": new_ad.author,
                             "price": new_ad.price,
                             "description": new_ad.description,
                             "address": [loc.name for loc in new_ad.author.locations.all()],
                             "is_published": new_ad.is_published,
                             "image": new_ad.image.url if new_ad.image else None
                             })


@method_decorator(csrf_exempt, name='dispatch')
class AdUploadImage(UpdateView):
    model = Ad
    fields = "__all__"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.image = request.FIELS.get('image')
        self.object.save()
        return JsonResponse({"id": self.object.pk,
                             "name": self.object.author.username,
                             "image": self.object.image.url
                             })


@method_decorator(csrf_exempt, name='dispatch')
class AdUpdatelView(UpdateView):
    model = Ad
    fields = "__all__"

    def patch(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        ad_data = json.loads(request.body)

        if "name" in ad_data:
            self.object.name = ad_data["name"]
        if "price" in ad_data:
            self.object.price = ad_data["price"]
        if "description" in ad_data:
            self.object.description = ad_data["description"]
        if "author_id" in ad_data:
            self.object.author_id = ad_data["author_id"]

        self.object.save()

        return JsonResponse({"id": self.object.pk,
                             "name": self.object.author.username,
                             "author": self.object.author,
                             "price": self.object.price,
                             "description": self.object.description
                             })


@method_decorator(csrf_exempt, name='dispatch')
class AdDeletelView(DeleteView):
    model = Ad
    success_url = "/"

    def patch(self, request, *args, **kwargs):
        ad_pk = self.get_object().pk
        super().delete(request, *args, **kwargs)

        return JsonResponse({"id": ad_pk})
