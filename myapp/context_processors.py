from .models import Product
from django.db.models import Q


def searchFunction(request):
    search_context = {}
    if "search-box" in request.GET:
        query = request.GET.get("q")
        search_box = request.GET.get("search-box")
        if search_box:
            # Search for brand
            brands_results = Q(brand__name__icontains=query)
            # Search for item name
            item_results = Q(item__icontains=query)
            # Search for description
            description_results = Q(description__icontains=query)
            # Search for type
            type_results = Q(type__name__icontains=query)

            results = Product.objects.filter(
                brands_results | item_results | description_results | type_results).distinct()
        else:
            results = []

        num_results = results.count()

        search_context = {
            "results": results,
            "query": query,
            "num_results": num_results,
        }

    return search_context
