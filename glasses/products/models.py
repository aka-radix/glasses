from django.db import models


class Currency(models.TextChoices):
    USD = "USD", "USD"
    EUR = "EUR", "EUR"
    GBP = "GBR", "GBR"
    JPY = "JOD", "JOD"
    CNY = "JPY", "JPY"


class BaseProduct(models.Model):
    """Base abstract product holding shared fields between Frame and Lens."""

    description = models.TextField()
    stock = models.PositiveIntegerField(default=0)
    price = models.FloatField()
    currency = models.CharField(
        choices=Currency.choices,
        max_length=3,
        default=Currency.USD,
    )

    class Meta:
        abstract = True

    def check_currency_match(self, user) -> bool:
        return self.currency == user.currency

    def decrement_stock(self) -> None:
        self.stock -= 1
        self.save()


class Frame(BaseProduct):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"

    name = models.CharField(max_length=100)
    status = models.CharField(
        choices=Status.choices,
        default=Status.ACTIVE,
        max_length=8,
    )

    class Meta(BaseProduct.Meta):
        unique_together = ("price", "currency")

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        if not self.stock:
            self.status = self.Status.INACTIVE

        super().save(*args, **kwargs)

    @property
    def available(self) -> bool:
        return self.status == self.Status.ACTIVE and self.stock > 0


class Lens(BaseProduct):
    class PrescriptionType(models.TextChoices):
        FASHION = "fashion", "Fashion"
        SINGLE_VISION = "single_vision", "Single Vision"
        VARIFOCAL = "varifocal", "Varifocal"

    class LensType(models.TextChoices):
        CLASSIC = "classic", "Classic"
        BLUE_LIGHT = "blue_light", "Blue Light"
        TRANSITION = "transition", "Transition"

    colour = models.CharField(max_length=32)
    prescription_type = models.CharField(
        choices=PrescriptionType.choices,
        max_length=13,
    )
    lens_type = models.CharField(choices=LensType.choices, max_length=10)

    class Meta(BaseProduct.Meta):
        unique_together = ("price", "currency")

    def __str__(self) -> str:
        return f"{self.colour} {self.prescription_type} {self.lens_type}"

    @property
    def available(self) -> bool:
        return self.stock > 0
