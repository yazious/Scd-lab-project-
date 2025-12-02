# models/category.py
from .product import Product

# Abstract Factory
class CategoryFactory:
    def create_product(self, name, price, stock):
        raise NotImplementedError


class ElectronicsFactory(CategoryFactory):
    def create_product(self, name, price, stock):
        return Product("Electronics", name, price, stock)


class ClothingFactory(CategoryFactory):
    def create_product(self, name, price, stock):
        return Product("Clothing", name, price, stock)


class HomeAppliancesFactory(CategoryFactory):
    def create_product(self, name, price, stock):
        return Product("Home Appliances", name, price, stock)
