from rest_framework.exceptions import ValidationError


def validate_name(attrs):
    detail = None

    if attrs['name'] == attrs['surname']:
        detail = "Name and surname must be different"
    if attrs['name'] == attrs['patronymic']:
        detail = "Name and patronymic must be different"
    if attrs['surname'] == attrs['patronymic']:
        detail = "Surname and patronymic must be different"

    if detail:
        raise ValidationError(
            detail=detail,
            code=400)

    return attrs
