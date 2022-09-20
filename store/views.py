from django.db.models.aggregates import Count, Min, Max, Avg, Sum
from django.db.models import F, Func, Value
from django.db.models.functions import Concat
from django.http import HttpResponse, HttpResponseServerError, JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from store.models import Product, Customer, Collection, Product, Order, OrderItem

def index(request):
    # queryset = Customer.objects.filter(email__icontains='.com')
    # queryset = Collection.objects.filter(featured_product__isnull=True)
    # queryset = Product.objects.filter(inventory__lt=10)
    # queryset = Order.objects.filter(customer_id=1)
    # queryset = OrderItem.objects.filter(product__collection_id=3)
    # queryset = Product.objects.filter(id__in=OrderItem.objects.values('product_id').distinct()).order_by('title')
    # queryset = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5]
    # orders = Order.objects.aggregate(count=Count('id'))
    # product_1 = OrderItem.objects.filter(product_id=1).aggregate(units_sold=Sum('quantity'))
    # customer_1 = Order.objects.filter(customer_id=1).aggregate(count=Count('id'))
    # price = Product.objects.filter(collection_id=3).aggregate(min=Min('unit_price'), max=Max('unit_price'), average=Avg('unit_price'))
    # queryset = Customer.objects.annotate(is_new=True)
    # queryset = Customer.objects.annotate(
    #     full_name=Func(F('first_name'),Value(' '),F('last_name'),function='CONCAT')
    # )
    # queryset = Customer.objects.annotate(
    #     full_name=Concat('first_name', Value(' '), 'last_name')
    # )
    # customers = Customer.objects.annotate(
    #     last_order_id=Max('order__id')
    # )
    # collections = Collection.objects.annotate(
    #     product_counts=Count('product')
    # )
    # customers = Customer.objects.annotate(
    #     orders_count=Count('order')
    # ).filter(orders_count__gt=5)
    customers = Customer.objects.annotate(
        total_spend=Sum(
            F('order__orderitem__unit_price') *
            F('order__orderitem__quantity') 
        )
    )
    list(customers)
    return render(request, 'index.html', {})

def create_customer(request):
    if request.method == 'POST':
        customer = {
            'first_name': request.POST.get('first_name', None),
            'last_name': request.POST.get('last_name', None),
            'email':request.POST.get('email', None),
            'phone': request.POST.get('phone', None),
            'membership': request.POST.get('membership', None),
            'birth_date': request.POST.get('birth_date', None)
        }
        response_message = None
        try:
            customer = Customer(**customer)
            customer.save()
            response_message = f'Customer {customer.first_name} has been created!'
        except Exception as e:
            return HttpResponseServerError(e)
        return HttpResponse(response_message)

def json(request):
    product_list = list(Product.objects.filter(collection_id=5).values())
    return JsonResponse(product_list, safe=False)

class ExampleTemplateView(TemplateView):
    template_name = 'template-view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'This is a template view'
        return context
