# ---Drf---
from rest_framework.exceptions import ValidationError


def parse_int(data, field):

    try:
        if isinstance(data, bool) or not isinstance(data, (str, int)):
            raise ValidationError(f"{field} এর ডাটাটি 'str' অথবা 'পূর্ণসংখ্যা' পাঠান।")

        else:
            data = int(data)
            return data

    except ValueError:
        raise ValidationError(
            f"{field} অবশ্যই একটি বৈধ সংখ্যা হতে হবে। আপনি পাঠিয়েছেন: '{data}'"
        )
