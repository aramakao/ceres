from django.contrib import admin
from .models import *

admin.site.register(ProductComments)
#admin.site.register(ShoppingCart)
admin.site.register(Payment)
admin.site.register(ShippingOption)
admin.site.register(ShippingAddress)
admin.site.register(PurchaseOrder)
#admin.site.register(ProductOrder)
admin.site.register(PurchaseRecord)
admin.site.register(FeedbackProduct)
admin.site.register(FeedbackSeller)
admin.site.register(Mailbox)
