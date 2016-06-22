from django.contrib.sitemaps import Sitemap
from apps.farm.models import Farm
from apps.product.models import Product
from apps.account.models import User
from apps.groups.models import Group

class FarmSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Farm.objects.filter(is_active=True)

    def name(self, obj):
        return obj.name

class ProductSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Product.objects.all()

class UserSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return User.objects.all()

class GroupSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Group.objects.all()
