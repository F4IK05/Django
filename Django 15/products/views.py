from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template.context_processors import request

from products.forms import ReviewForm
from products.models import Product, Review


# Create your views here.
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product/product_list.html', {'products': products})


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    form = ReviewForm()

    return render(request, 'product/product_detail.html', {
        'product': product,
        'form': form,
        'reviews': Review.objects.filter(product=product)
    })

@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()

    return redirect('product_detail', product_id=product_id)

@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id)

    if review.user != request.user:
        return redirect('product_list')

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('product_detail', product_id=review.product.pk)
    else:
        form = ReviewForm(instance=review)

    return render(request, 'review/edit_review.html', {'form': form})

@login_required
def delete_review(request, pk):
    review = get_object_or_404(Review, pk=pk)

    if review.user == request.user:
        product_pk = review.product.pk
        review.delete()
        return redirect('product_detail', product_id=product_pk)

    return redirect('product_list')
