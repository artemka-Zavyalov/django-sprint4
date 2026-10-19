from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .models import Category, Post


def get_published_posts():
    """
    Возвращает список объектов отфильтрованных публикаций.

    Критерии отбора публикаций:
        1. Дата публикации — не позже текущего времени.
        2. Флаг публикации самого поста равен True.
        3. Флаг публикации категории равен True.
    """
    return (
        Post.objects
        .select_related('author', 'category', 'location')
        .filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True
        )
    )


def index(request):
    """Главная страница: 5 последних публикаций."""
    post_list = get_published_posts()[:5]
    context = {'post_list': post_list}
    return render(request, 'blog/index.html', context)


def category_posts(request, category_slug):
    """Страница категории."""
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    post_list = get_published_posts().filter(category=category)
    context = {
        'category': category,
        'post_list': post_list,
    }
    return render(request, 'blog/category.html', context)


def post_detail(request, post_id):
    """Страница отдельной публикации."""
    post = get_object_or_404(get_published_posts(), pk=post_id)
    context = {'post': post}
    return render(request, 'blog/detail.html', context)


class RegistrationView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/registration_form.html'
    success_url = reverse_lazy('login')
