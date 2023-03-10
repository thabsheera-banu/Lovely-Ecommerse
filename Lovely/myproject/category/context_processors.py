from .models import Category

def menu_links(request):
    links = Category.objects.all()
    foundation=Category.objects.filter(category_name='Foundation')
    lipstick=Category.objects.filter(category_name='Lipstick')
    facewash=Category.objects.filter(category_name='Facewash')
    # mascara=Category.objects.filter(category_name='')

    return dict(links=links,foundation=foundation,lipstick=lipstick,facewash=facewash)