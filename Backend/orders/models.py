from django.db import models
from store.models import Product
from core.models import User, Customer, Seller

class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    items_in_cart = models.ManyToManyField(Product, through='CartItem')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_items = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Cart ID: {self.cart_id}, Customer: {self.customer.user.first_name}, Total Price: {self.total_amount}, Total Items: {self.total_items}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_quantity = models.PositiveIntegerField()

    def subtotal(self):
        if self.product_quantity is None:
            return 0
        return self.product_quantity * self.product.discountedPrice

    def save(self, *args, **kwargs):
        self.cart.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.cart.total_price -= self.subtotal()
        self.cart.total_items -= self.quantity_buying
        self.cart.save()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"Cart ID: {self.cart_id}, Product: {self.product.name}, Total Quantity: {self.product_quantity}, Subtotal: {self.subtotal()}"



class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    items_in_order = models.ManyToManyField(Product, through='OrderItem')
    transaction_id = models.CharField(max_length=255)
    transaction_amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_status = models.CharField(max_length=255)
    transaction_timestamp = models.DateTimeField()
    payment_gateway_response = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order ID: {self.order_id}, Customer: {self.customer.user.first_name}, Seller ID: {self.seller_id}, Total: {self.total_amount}, Status: {self.transaction_status}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    total_quantity = models.PositiveIntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.total_amount = self.total_quantity * self.product.discountedPrice
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order ID: {self.order_id}, Product: {self.product.name}, Quantity: {self.total_quantity}, Total: {self.total_amount}"

