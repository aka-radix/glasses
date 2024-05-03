from typing import Union

from rest_framework.validators import ValidationError

from glasses.products.models import Frame, Lens
from glasses.users.models import User


def validate_object_exist(
    obj: Union[Frame, Lens],
    user: User,
):
    validation_error_message = (
        "Selected product/s is/are unavailable or out of stock"
    )
    if not obj:
        raise ValidationError(validation_error_message)

    model_class = obj._meta.model

    try:
        if not obj.available or not obj.check_currency_match(user):
            raise model_class.DoesNotExist
    except model_class.DoesNotExist:
        validation_error_message = f"Selected {model_class.__name__.lower()} is unavailable or out of stock"  # noqa: E501
        raise ValidationError(validation_error_message)  # noqa: B904

    return obj
