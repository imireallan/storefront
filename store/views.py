from django.shortcuts import render
from django.db.models.aggregates import Count, Min, Max, Avg, Sum
from django.db.models import F
from store.models import Product, Customer, Collection, Product, Order, OrderItem

def index(request):
    query_set = Product.objects.prefetch_related('promotions')
    # customers_queryset = Customer.objects.filter(email__icontains='.com')
    # collections_queryset = Collection.objects.filter(featured_product__isNull=True)
    # products_queryset = Product.objects.filter(inventory__lt=10)
    # orders_queryset = Order.objects.filter(customer=1)
    # orders_queryset = OrderItem.objects.select_related('product').filter(product__collection__id=3
    # ordered_products = Product.objects.filter(id__in=OrderItem.objects.values('product_id')).order_by('title').distinct()
    # orders = Order.objects.select_related('customer').order_by('-placed_at')[:5]
    # orders = Product.objects.aggregate(count=Count('id'), max_price=Max('unit_price'), min_price=Min('unit_price'))
    # orders = Order.objects.aggregate(count=Count('id'))
    # orders = OrderItem.objects.filter(product_id=1).aggregate(count=Count('id'))
    # orders = Order.objects.filter(customer_id=1).aggregate(count=Count('id'))
    orders = Product.objects.filter(collection_id=3).aggregate(min=Min('unit_price'), max=Max('unit_price'), avg=Avg('unit_price'))
    # customers = Customer.objects.annotate(last_order_id=Max('order__id'))
    # collections = Collection.objects.annotate(product_count=Count('product'))
    # customers = Customer.objects.annotate(orders_count=Count('order')).filter(orders_count__gt=5)
    customers = Product.objects.annotate(
        total_sales=Sum(
            F('orderitem__unit_price') * F('orderitem__quantity')
        )).order_by('-total_sales')[:5]
    print(customers)
    return render(request, 'index.html', {'orders': orders })
