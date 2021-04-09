import factory
from django.template.defaultfilters import slugify
from . import models


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Category

    #name = 'Coffee'
    name = factory.Faker("name")
    slug = factory.LazyAttribute(lambda a: slugify(a.name))


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Product

    #name = 'Cappucino'
    name = factory.Faker("name")
    slug = factory.LazyAttribute(lambda a: slugify(a.name))
    description = "some very good description"
    category = factory.SubFactory(CategoryFactory)
    price = 25.00
