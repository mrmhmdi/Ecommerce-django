from django.views import View
from django.shortcuts import render, redirect, get_object_or_404

from .models import Product, Comment
from .forms import CommentForm
# Create your views here.


class ProductDetailView(View):

    def get(self, request, slug):
        form = CommentForm()
        product = get_object_or_404(Product, slug=slug)
        comment = product.comments.all()
        context = {'product': product, 'comments': comment}
        return render(request, 'products/product_detail.html', context)

    def post(self, request, slug):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.product = get_object_or_404(Product, slug=slug)
            comment.save()

        return redirect('product-detail', slug)
