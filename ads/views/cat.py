import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from ads.models import Category


def root(request):
    return JsonResponse({
        "status": "ok"
    })


class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        cat = self.get_object()

        return JsonResponse({"id": cat.id, "name": cat.name, })


class CategoryListView(ListView):
    model = Category
    queryset = Category.objects.order_by("name").all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        return JsonResponse([{"id": cat.id, "name": cat.name} for cat in self.object_list], safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    fields = "__all__"

    def post(self, request, **kwargs):
        data = json.loads(request.body)
        new_cat = Category.objects.create(name=data["name"], )
        return JsonResponse({"id": new_cat.id, "name": new_cat.name}, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Category
    fields = "__all__"

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)
        self.object.name = data["name"]
        self.object.save()
        return JsonResponse({"id": self.object.id, "name": self.object.name}, safe=False)

    def put(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)
        self.object.name = data["name"]
        self.object.save()
        return JsonResponse({"id": self.object.id, "name": self.object.name}, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        cat = self.get_object()
        cat_id = cat.id
        super().delete(request, *args, **kwargs)
        return JsonResponse({"id": cat_id}, safe=False)