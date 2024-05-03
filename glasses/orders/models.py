from django.db import models

from glasses.products.models import Currency, Frame, Lens


class Basket(models.Model):
    """A temporary container for selected products."""

    # a user can only have one basket
    user = models.OneToOneField(
        "users.User",
        related_name="basket",
        on_delete=models.CASCADE,
    )
    currency = models.CharField(
        choices=Currency.choices,
        max_length=3,
        default=Currency.USD,
    )
    total = models.PositiveIntegerField(default=0)

    frame = models.ForeignKey(
        Frame,
        related_name="basket",
        on_delete=models.SET_NULL,
        null=True,
    )

    lens = models.ForeignKey(
        Lens,
        related_name="basket",
        on_delete=models.SET_NULL,
        null=True,
    )

    def __str__(self) -> str:
        total_str = str(self.total)
        email = self.user.email if self.user else "No User"
        return f"{email} {total_str} {self.currency}"

    def save(self, *args, **kwargs) -> None:
        self.currency = self.user.currency
        self.calculate_total()
        super().save(*args, **kwargs)

    def calculate_total(self) -> None:
        """Calculate the total price of the basket."""

        total = 0
        if self.frame:
            total += self.frame.price
        if self.lens:
            total += self.lens.price
        self.total = total

    def flush(self) -> None:
        """Empty the basket and decrement product stock."""

        if self.frame:
            self.frame.decrement_stock()
            self.frame = None
        if self.lens:
            self.lens.decrement_stock()
            self.lens = None
        self.save()

    def add_products(self, products) -> "Basket":
        """Add products to the basket."""

        self.frame = products.get("frame", self.frame)
        self.lens = products.get("lens", self.lens)
        self.save()
        return self


class Order(models.Model):
    user = models.ForeignKey(
        "users.User",
        related_name="orders",
        related_query_name="orders",
        on_delete=models.SET_NULL,
        null=True,
    )
    currency = models.CharField(
        choices=Currency.choices,
        max_length=3,
        default=Currency.USD,
    )

    total = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        total_str = str(self.total)
        email = self.user.email if self.user else "No User"
        return f"{email} {total_str} {self.currency}"

    def save(self, *args, **kwargs) -> None:
        if not self.pk:
            super().save(*args, **kwargs)
            return
        self.currency = self.user.currency if self.user else Currency.USD
        self.calculate_total()
        super().save(*args, **kwargs)

    def calculate_total(self, *args, **kwargs) -> None:
        """Calculate the total price of the basket."""

        self.total = self.purchase.frame["price"] + self.purchase.lens["price"]


class Purchase(models.Model):
    """A purchase is a snapshot of a product at the time of purchaseing."""

    frame = models.JSONField("frame", default=dict)
    lens = models.JSONField("lens", default=dict)
    order = models.OneToOneField(
        Order,
        related_name="purchase",
        related_query_name="purchase",
        on_delete=models.SET_NULL,
        null=True,
    )

    def __str__(self) -> str:
        return self.pk
