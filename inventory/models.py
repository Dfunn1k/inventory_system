from django.db import models
from uuid import uuid4
from django.contrib.auth.models import User


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')

    class Meta:
        abstract = True


class Category(BaseModel):
    name = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    code = models.CharField(max_length=10, unique=True, verbose_name='Código')
    description = models.TextField(blank=True, null=True, verbose_name='Descripción')

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

    def __str__(self):
        return self.name


class Product(BaseModel):
    name = models.CharField(max_length=200, verbose_name='Nombre')
    description = models.TextField(blank=True, null=True, verbose_name='Descripción')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio')
    stock_min = models.PositiveIntegerField(default=0, verbose_name='Stock mínimo')
    stock_max = models.PositiveIntegerField(default=100, verbose_name='Stock máximo')
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name='Imagen')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Categoría')

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return self.name

    @property
    def stock(self):
        return Stock.objects.filter(product=self).aggregate(models.Sum('quantity'))['quantity__sum'] or 0


class Stock(BaseModel):
    quantity = models.PositiveIntegerField(verbose_name='Cantidad')
    warehouse_location = models.CharField(max_length=100, blank=True, null=True, verbose_name='Ubicación en almacén')
    notes = models.TextField(blank=True, null=True, verbose_name='Notas')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Producto')

    class Meta:
        verbose_name = 'Stock'
        verbose_name_plural = 'Stock'


# class Supplier(BaseModel):
#     name = models.CharField(max_length=200, verbose_name='Nombre')
#     address = models.CharField(max_length=200, blank=True, null=True, verbose_name='Dirección')
#     phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Teléfono')
#     email = models.EmailField(blank=True, null=True, verbose_name='Correo electrónico')
#     country = models.CharField(max_length=50, blank=True, null=True, verbose_name='País')
#     city = models.CharField(max_length=50, blank=True, null=True, verbose_name='Ciudad')
#     ruc = models.CharField(max_length=12, blank=True, null=True, unique=True, verbose_name='RUC')
#     notes = models.TextField(blank=True, null=True, verbose_name='Notas')
#
#     class Meta:
#         verbose_name = 'Proveedor'
#         verbose_name_plural = 'Proveedores'
#
#     def __str__(self):
#         return self.name


class Costumer(BaseModel):
    IDENTIFICATION_TYPE = (
        ('DNI', 'DNI'),
        ('RUC', 'RUC'),
        ('CE', 'Carnet de Extranjería')
    )

    name = models.CharField(max_length=200, verbose_name='Nombre')
    identification_type = models.CharField(max_length=3, choices=IDENTIFICATION_TYPE, verbose_name='Tipo de identificación')
    vat = models.CharField(max_length=12, blank=True, null=True, unique=True, verbose_name='Número de identificación')
    address = models.CharField(max_length=200, blank=True, null=True, verbose_name='Dirección')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Teléfono')
    email = models.EmailField(blank=True, null=True, verbose_name='Correo electrónico')
    country = models.CharField(max_length=50, blank=True, null=True, verbose_name='País')
    city = models.CharField(max_length=50, blank=True, null=True, verbose_name='Ciudad')
    is_occasional = models.BooleanField(default=False, verbose_name='Es ocasional')

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return f'{self.name} - {self.identification_type}: {self.vat}'


# class ProductSupplier(BaseModel):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Producto')
#     supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name='Proveedor')
#     number_invoicing = models.CharField(max_length=20, blank=True, null=True, verbose_name='Número de factura')
#     purchase_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio de compra')
#     quantity = models.PositiveIntegerField(verbose_name='Cantidad')
#     total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Total')
#     datetime = models.DateTimeField(auto_now_add=True, verbose_name='Fecha y hora')
#
#     class Meta:
#         verbose_name = 'Compra de Producto'
#         verbose_name_plural = 'Compras de Productos'
#
#     def __str__(self):
#         return f'{self.product} - {self.supplier} - {self.purchase_price}'
#
#     def save(self, *args, **kwargs):
#         is_new = self._state.adding
#         super(ProductSupplier, self).save(*args, **kwargs)
#         if is_new:
#             StockMove.objects.create(
#                 product=self.product,
#                 type='In',
#                 quantity=self.quantity,
#                 supplier=self.supplier,
#                 notes=f'Compra de {self.product} a {self.supplier}'
#             )
#             Stock.objects.create(
#                 product=self.product,
#                 quantity=self.quantity,
#                 notes=f'Compra de {self.product} a {self.supplier}'
#             )


class ProductCostumer(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Producto')
    costumer = models.ForeignKey(Costumer, on_delete=models.CASCADE, verbose_name='Cliente', blank=True, null=True)
    quantity = models.PositiveIntegerField(verbose_name='Cantidad')
    # total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Total')
    # sale_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio de venta')
    datetime = models.DateTimeField(auto_now_add=True, verbose_name='Fecha y hora')

    class Meta:
        verbose_name = 'Venta de Producto'
        verbose_name_plural = 'Ventas de Productos'

    def __str__(self):
        return f'{self.product} - {self.costumer}'

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super(ProductCostumer, self).save(*args, **kwargs)
        if is_new:
            StockMove.objects.create(
                product=self.product,
                type='Out',
                quantity=self.quantity,
                notes=f'Venta de {self.product} a {self.costumer}'
            )
            stock_entry, created = Stock.objects.get_or_create(product=self.product)
            stock_entry.quantity -= self.quantity
            stock_entry.save()


class StockMove(BaseModel):
    type_moves = (
        ('In', 'Ingreso'),
        ('Out', 'Salida')
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Producto')
    type = models.CharField(max_length=3, choices=type_moves, verbose_name='Tipo')
    quantity = models.PositiveIntegerField(verbose_name='Cantidad')
    datetime = models.DateTimeField(auto_now_add=True, verbose_name='Fecha y hora')
    notes = models.TextField(blank=True, null=True, verbose_name='Notas')

    class Meta:
        verbose_name = 'Movimiento de Stock'
        verbose_name_plural = 'Movimientos de Stock'

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super(StockMove, self).save(*args, **kwargs)
        if is_new:
            stock_entry, created = Stock.objects.get_or_create(product=self.product, quantity=0)
            if self.type == 'In':
                stock_entry.quantity += self.quantity
            elif self.type == 'Out':
                stock_entry.quantity -= self.quantity
            stock_entry.save()
