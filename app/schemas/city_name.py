from dataclasses import dataclass 
import string

from marshmallow import Schema, fields, post_load, validates, ValidationError


@dataclass
class CityNameModel:
    name: str


class CityNameSchema(Schema):
    """Схема для валидации названия города"""
    name = fields.String(
        required=True, 
        validate=lambda x: 0 < len(x) < 256,
        metadata={"description": "Название города (1-255 символов). Не может быть пустым или содержать только пробелы."}
    )

    @validates("name")
    def validate_name(self, value):
        """Дополнительная проверка, чтобы строка не содержала только пробелы"""
        if value.strip() == "":
            raise ValidationError("Название города не может быть пустым или состоять только из пробелов.")

    @post_load
    def make_city(self, data, **kwargs):
        data["name"] = string.capwords(data["name"].strip())
        return CityNameModel(**data)