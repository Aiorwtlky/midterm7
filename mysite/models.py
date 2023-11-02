from django.db import models
from django.utils.translation import gettext as _

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=50)
    write = models.CharField(max_length=50, default="不詳")
    slug = models.CharField(max_length=200)
    body = models.TextField()
    isBorrow = models.BooleanField(_("外借中"), default=False)
    pub_date = models.DateTimeField(auto_now_add=True)

    @property
    def formatted_is_borrow(self):
        if self.isBorrow:
            return '<span style="color: white; background-color: green; padding: 3px; border-radius: 3px;">外借中</span>'
        else:
            return '<span style="color: black; background-color: white; border: 1px solid black; padding: 3px; border-radius: 3px;">未外借</span>'

    formatted_is_borrow.fget.short_description = "外借狀態"
    
    class Meta:
        ordering = ("-pub_date",) 
    def __str__(self):
        return self.title
    
class Product(models.Model):
    SIZES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    )
    sku = models.CharField(max_length=5)
    name = models.CharField(max_length=20)
    price = models.PositiveIntegerField()
    size = models.CharField(max_length=1, choices=SIZES)

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0002_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='size',
            field=models.CharField(choices=[('S', 'Small'), ('M', 'Medium'), ('L', 'Large')], max_length=1),
        ),
    ]

    