from rest_framework import serializers
from .models import Review, Category, Rate

class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for the Review model.

    This serializer maps all the fields of the Review model ('__all__') to JSON format for the Django REST framework.
    It can be used for handling HTTP requests and responses involving Review objects.

    Inherits from:
    serializers.ModelSerializer: This is a shortcut for creating serializer classes. 
    A ModelSerializer class is just a regular Serializer class, that includes simple 
    implementations of .create() and .update().

    Class variables:
    Meta: This inner class contains metadata for the serializer. It has two attributes:
        - model: Specifies the model class to be serialized.
        - fields: Specifies which fields of the model should be included in the serialized representation.
    """
    class Meta:
        model = Review
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model.

    This serializer maps all the fields of the Category model ('__all__') to JSON format for the Django REST framework.
    It can be used for handling HTTP requests and responses involving Category objects.

    Inherits from:
    serializers.ModelSerializer: This is a shortcut for creating serializer classes.

    Class variables:
    Meta: This inner class contains metadata for the serializer. It has two attributes:
        - model: Specifies the model class to be serialized.
        - fields: Specifies which fields of the model should be included in the serialized representation.
    """
    class Meta:
        model = Category
        fields = '__all__'

class RateSerializer(serializers.ModelSerializer):
    """
    Serializer for the Rate model.

    This serializer maps all the fields of the Rate model ('__all__') to JSON format for the Django REST framework.
    It can be used for handling HTTP requests and responses involving Rate objects.

    Inherits from:
    serializers.ModelSerializer: This is a shortcut for creating serializer classes.

    Class variables:
    Meta: This inner class contains metadata for the serializer. It has two attributes:
        - model: Specifies the model class to be serialized.
        - fields: Specifies which fields of the model should be included in the serialized representation.
    """
    class Meta:
        model = Rate
        fields = '__all__'