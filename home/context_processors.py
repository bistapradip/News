from .models import Category

def category_processor(request):
    return{
        'all_categories': Category.objects.all()
    }
    