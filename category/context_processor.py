from .models import Category


def main_links(request):
    links = Category.objects.all()
    return dict(links= links)
