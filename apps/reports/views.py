#-*- encoding: utf-8 -*-

from django.shortcuts import render
from easy_pdf.views import PDFTemplateView
from django.shortcuts import get_object_or_404
from apps.store.models import PurchaseOrder
from django.http import Http404

class InvoiceView(PDFTemplateView):
    template_name = "reports/invoice.html"

    def get_context_data(self, **kwargs):
        context = super(InvoiceView, self).get_context_data(**kwargs)
        order_id = kwargs['order_id']
        order = get_object_or_404(PurchaseOrder,id=order_id)
        if self.request.user == order.buyer or self.request.user==order.farm.user:
            context['order']=order
            context['title']='Order de Compra N° '
            return context
        else:
            raise Http404
