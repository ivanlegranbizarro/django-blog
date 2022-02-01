from .models import Category


def access_to_all_categories(request):
    categories = Category.objects.all()
    return {'categories': categories}
