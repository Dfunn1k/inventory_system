from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from .models import Product, Inventory
from .forms import ProductForm, InventoryForm


def list_products(request):
    products = Product.objects.all()
    return render(request, 'inventory/list_products.html', {'productos': products})


def add_products(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            Inventory.objects.create(product=product, quantity=0)
            return redirect('list_products')
    else:
        form = ProductForm()
    return render(request, 'inventory/add_products.html', {'form': form})


def edit_products(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('list_products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'inventory/edit_products.html', {'form': form})


def delete_products(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('list_products')
    return render(request, 'inventory/delete_products.html', {'producto': product})
