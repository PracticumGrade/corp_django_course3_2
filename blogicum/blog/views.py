from datetime import datetime
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse_lazy

from .models import Post, Category, Location


def get_now_datetime():
    return datetime.now()


class PostMixin:
    model = Post

    def get_queryset(self):
        return self.model.objects.filter(
            pub_date__lte=get_now_datetime(),
            is_published=True,
            category__is_published=True
        )


class PostListView(PostMixin, ListView):
    template_name = "blog/index.html"
    ordering = 'created_at'
    paginate_by = 10


class PostDetailView(PostMixin, DetailView):
    template_name = "blog/detail.html"
    context_object_name = "post"
    pk_url_kwarg = "id"


class CategoryDetailView(SingleObjectMixin, ListView):
    """ Пример из документации - https://docs.djangoproject.com/en/3.2/topics/class-based-views/mixins/#using-singleobjectmixin-with-listview"""
    template_name = "blog/category.html"
    slug_url_kwarg = "category_slug"
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Category.objects.filter(is_published=True))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.object
        return context

    def get_queryset(self):
        return self.object.post_set.filter(
            is_published=True,
            pub_date__lte=get_now_datetime()
        )


class LocationListView(ListView):
    paginate_by = 10
    queryset = Location.objects.filter(is_published=True)


class LocationMixin:
    model = Location


class LocationFormMixin:
    fields = ('name',)


class LocationDetailView(LocationMixin,  DetailView):
    ...


class LocationCreateView(LocationMixin, LocationFormMixin, CreateView):
    ...


class LocationUpdateView(LocationMixin, LocationFormMixin, UpdateView):
    ...


class LocationDeleteView(LocationMixin, DeleteView):
    success_url = reverse_lazy("blog:location_list")
