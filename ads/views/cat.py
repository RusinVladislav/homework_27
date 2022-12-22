import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, DeleteView, UpdateView

from ads.models import Category


def root(request):
    return JsonResponse({"status": "ok"}, status=200)


class CategoryListView(ListView):
    model = Category
    queryset = Category.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object_list = self.object_list.order_by('name')
        return JsonResponse(data=[{"id": category.pk, "name": category.name} for category in self.object_list],
                            safe=False)


class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        category = self.get_object()
        return JsonResponse({"id": category.pk, "name": category.name})


@method_decorator(csrf_exempt, name='dispatch')
class CategoryCreatelView(CreateView):
    model = Category
    fields = "__all__"

    def post(self, request, *args, **kwargs):
        category_data = json.loads(request.body)
        new_category = Category.objects.create(**category_data)
        return JsonResponse({"id": new_category.pk, "name": new_category.name})


@method_decorator(csrf_exempt, name='dispatch')
class CategoryUpdatelView(UpdateView):
    model = Category
    fields = "__all__"

    def patch(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        category_data = json.loads(request.body)
        self.object.name = category_data["name"]
        self.object.save()

        return JsonResponse({"id": self.object.pk, "name": self.object.name})


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDeletelView(DeleteView):
    model = Category
    success_url = "/"

    def patch(self, request, *args, **kwargs):
        cat_pk = self.get_object().pk
        super().delete(request, *args, **kwargs)

        return JsonResponse({"id": cat_pk})
