from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import User

# Create your models here.
class BorrowingRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=20)  # '借閱', '歸還', '預約', '取消預約'

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.user.username} - {self.action} - {self.timestamp}'

class Post(models.Model):
    title = models.CharField(max_length=50)
    write = models.CharField(max_length=50, default="不詳")
    slug = models.CharField(max_length=200)
    bookstype=[("一般書籍","一般書籍"),("教學用書","教學用書")]
    category = models.CharField(max_length=20, choices=bookstype, default="一般書籍")
    intro = models.TextField(default="", blank=True)
    photolink = models.TextField(default="", blank=True)
    body = models.TextField()
    borrower = models.CharField(max_length=150, blank=True, null=True)
    isBorrow = models.BooleanField(_("外借中"), default=False)
    pub_date = models.DateTimeField(auto_now_add=True)
    reservations = models.ManyToManyField(User, related_name='reserved_books', blank=True)
    borrowing_records = models.ManyToManyField(BorrowingRecord, related_name='borrowed_books', blank=True)
    

    @property
    def formatted_is_borrow(self):
        if self.isBorrow:
            try:
                user = User.objects.get(username=self.borrower)
                return f'<span style="color: white; background-color: red; border: 1px solid white; padding: 3px; border-radius: 3px;">已出借給{user.username}</span>'
            except User.DoesNotExist:
                return f'<span style="color: white; background-color: red; border: 1px solid white; padding: 3px; border-radius: 3px;">已出借給 {self.borrower}</span>'
        elif self.is_reserved:
            reservations = self.reservations.all()
            if reservations and self.borrower != reservations[0].username:
                return '<span style="color: white; background-color: gold; border: 1px solid white; padding: 3px; border-radius: 3px;">尚有預約者</span>'
        else:
            return '<span style="color: white; background-color: green; border: 1px solid white; padding: 3px; border-radius: 3px;">可立即借閱</span>'

    formatted_is_borrow.fget.short_description = "外借狀態"

    
    @property
    def is_reserved(self):
        return self.reservations.exists()
    
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