from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    joined = models.DateTimeField(auto_now_add=True)
    initial_balance = models.IntegerField(default=15000, null=True)
    current_balance = models.IntegerField(default=15000, null=True)
    CATS = [('U', 'USER'), ('B', 'BROKER')]
    category = models.CharField(max_length=2, choices=CATS, default='U')

    def serialize(self):
        stocks = self.stocks.all()
        dps = self.dataPoints.all()
        return {
            'username': self.username,
            'joined': self.joined.strftime("%b %-d %Y, %-I:%M %p"),
            'stocks': [stock.serialize() for stock in stocks],
            'current_balance': self.current_balance,
            'initial_balance': self.initial_balance,
            'dataPoints': [dp.serialize() for dp in dps],
        }

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Stock(models.Model):
    symbol = models.CharField(max_length=5)
    buy_date = models.DateTimeField(auto_now_add=True)
    buy_price = models.DecimalField(max_digits=10, decimal_places=5)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='stocks'
    )

    def serialize(self):
        return {
            'id': self.id,

            'symbol': self.symbol.upper(),
            'buy_date': self.buy_date.strftime("%b %-d %Y, %-I:%M %p"),
            'owner': self.owner.username,
            'buy_price': self.buy_price,
        }

    def __str__(self):
        return f"{self.symbol} Куплена {self.buy_date} за {self.buy_price}"

    class Meta:
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'


class DataPoint(models.Model):
    x = models.DateTimeField(auto_now_add=True)
    y = models.DecimalField(max_digits=10, decimal_places=5)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='dataPoints'
    )

    def serialize(self):
        return {
            'date': self.x.strftime("%b %-d %Y, %-I:%M %p"),
            'owner': self.owner.username,
            'balance': self.y,
        }


class Company(models.Model):
    name = models.CharField(
        max_length=64,
        verbose_name='Название'
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Company'
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'
        ordering = ['name']


class Service(models.Model):
    name = models.CharField(
        max_length=64,
        verbose_name='Название'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена'
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name='Компания'
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Service'
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
        ordering = ['name']


class Request(models.Model):
    username = models.CharField(
        max_length=64,
        verbose_name='Пользователь'
    )
    company = models.CharField(
        max_length=64,
        verbose_name='Компания'
    )
    type = models.CharField(
        max_length=64,
        verbose_name='Тип'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена'
    )

    def __str__(self):
        return f'{self.username}, {self.company}'

    class Meta:
        db_table = 'Request'
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['username']
