from product.models import Product
from django.db.models import Max,Min
def get_filters(request):
	colors=Product.objects.distinct().values('color__title','color__id')
	sizes=Product.objects.distinct().values('size__title','size__id')
	minMaxPrice =Product.objects.aggregate(Min('price'),Max('price'))
	data={
		'colors':colors,
		'sizes':sizes,
		'minMaxPrice':minMaxPrice
	}
	return data