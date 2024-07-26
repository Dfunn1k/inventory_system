from django.contrib import admin
from .models import Category, Product, Stock, StockMove, ProductCostumer, Costumer
from django.contrib.admin import SimpleListFilter


class PriceFilter(SimpleListFilter):
    title = 'Precio'
    parameter_name = 'precio'

    def lookups(self, request, model_admin):
        return (
            ('>80', 'Más de 80'),
            ('>200', 'Más de 200'),
        )

    def queryset(self, request, queryset):
        if self.value() == '>80':
            return queryset.filter(price__gt=80)
        if self.value() == '>200':
            return queryset.filter(price__gt=200)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')
    readonly_fields = ('id', 'created_at', 'updated_at')
    fieldsets = (
        (
            'Atributos', {
                'fields': (
                    'id', 'name', 'code', 'description',
                )
            }
        ),
        (
            'Auditoría', {
                'fields': (
                    'created_at', 'updated_at',
                )
            }
        )

    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    def stock(self, obj):
        return obj.stock

    list_display = ('name', 'price', 'category', 'stock', 'stock_min', 'stock_max')
    search_fields = ('name', 'category__name')
    list_filter = ('category', PriceFilter)
    readonly_fields = ('id', 'created_at', 'updated_at')
    fieldsets = (
        (
            'Parámetros', {
                'fields': (
                    'id', 'name', 'description', 'price', 'image', 'category', 'stock_min', 'stock_max',
                )
            }
        ),
        (
            'Auditoría', {
                'fields': (
                    'created_at', 'updated_at',
                )
            }
        )
    )


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'warehouse_location')
    list_filter = ('product', 'warehouse_location')
    search_fields = ('product__name', 'warehouse_location')
    readonly_fields = ('id', 'created_at', 'updated_at')
    fieldsets = (
        (
            'Parámetros', {
                'fields': (
                    'id', 'product', 'quantity', 'warehouse_location', 'notes',
                )
            }
        ),
        (
            'Auditoría', {
                'fields': (
                    'created_at', 'updated_at',
                )
            }
        )
    )


# @admin.register(Supplier)
# class SupplierAdmin(admin.ModelAdmin):
#     list_display = ('name', 'phone', 'email', 'ruc')
#     search_fields = ('name', 'ruc', 'email')
#     readonly_fields = ('id', 'created_at', 'updated_at')
#     fieldsets = (
#         (
#             'Atributos', {
#                 'fields': (
#                     'id', 'name', 'address', 'phone', 'email', 'country', 'city', 'ruc', 'notes'
#                 )
#             }
#         ),
#         (
#             'Auditoría', {
#                 'fields': (
#                     'created_at', 'updated_at',
#                 )
#             }
#         )
#
#     )


# @admin.register(ProductSupplier)
# class ProductSupplierAdmin(admin.ModelAdmin):
#     list_display = ('number_invoicing', 'datetime', 'product', 'supplier')
#     search_fields = ('product__name', 'supplier__name', 'number_invoicing', 'datetime')
#     list_filter = ('product', 'supplier', 'datetime')
#     readonly_fields = ('id', 'created_at', 'updated_at', 'datetime')
#     fieldsets = (
#         (
#             'Parámetros', {
#                 'fields': (
#                     'id', 'number_invoicing', 'product', 'supplier', 'purchase_price', 'quantity', 'total', 'datetime',
#                 )
#             }
#         ),
#         (
#             'Auditoría', {
#                 'fields': (
#                     'created_at', 'updated_at',
#                 )
#             }
#         )
#     )


@admin.register(StockMove)
class StockMoveAdmin(admin.ModelAdmin):
    list_display = ('type', 'product', 'quantity', 'datetime')
    search_fields = ('product__name', 'datetime')
    list_filter = ('type', 'product', 'datetime')
    readonly_fields = ('id', 'created_at', 'updated_at', 'datetime')
    fieldsets = (
        (
            'Parámetros', {
                'fields': (
                    'id', 'type', 'product', 'quantity', 'datetime', 'notes',
                )
            }
        ),
        (
            'Auditoría', {
                'fields': (
                    'created_at', 'updated_at',
                )
            }
        )
    )

#
# @admin.register(Costumer)
# class CostumerAdmin(admin.ModelAdmin):
#     list_display = ('name', 'identification_type', 'vat', 'phone', 'email')
#     search_fields = ('name', 'identification_type', 'email', 'vat')
#     readonly_fields = ('id', 'created_at', 'updated_at')
#     fieldsets = (
#         (
#             'Atributos', {
#                 'fields': (
#                     'id', 'name', 'identification_type', 'vat', 'address', 'phone', 'email', 'country', 'city', 'is_occasional'
#                 )
#             }
#         ),
#         (
#             'Auditoría', {
#                 'fields': (
#                     'created_at', 'updated_at',
#                 )
#             }
#         )
#
#     )
