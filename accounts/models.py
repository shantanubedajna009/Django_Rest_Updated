from django.db import models
from django.db.models import Q, Min

# Create your models here.



class Author(models.Model):
    author_name = models.CharField(
        verbose_name='Author', primary_key=True, max_length=250)

    country = models.CharField(verbose_name='Country', 
                                null=False, blank=False,
                                max_length=250)

    def __str__(self):
        return self.author_name


class Publisher(models.Model):
    publisher_name = models.CharField(
        verbose_name='Publisher', primary_key=True, max_length=250)

    pub_add = models.TextField(verbose_name='Address', blank=False, null=False)

    def __str__(self):
        return self.publisher_name




class BooksModelManager(models.Manager):

    def get_books_2004(self):

        qs_initial = self.get_queryset().filter(pub_year=2004).aggregate(
            Min('unit_price'))

        lowest_price_book = qs_initial['unit_price__min']
        
        qs = self.get_queryset().filter(unit_price__gt=lowest_price_book)

        return qs




class Book(models.Model):
    isbn        = models.IntegerField(verbose_name='ISBN', 
                                    primary_key=True)

    title       = models.CharField(verbose_name='Title',
                                    unique=True,
                                    blank=False,
                                    null=False,
                                    max_length=250)

    pub_year    = models.IntegerField(verbose_name='Publish Year',
                                    blank=False, 
                                    null=False)

    unit_price  = models.IntegerField(verbose_name='Unit Price', 
                                    blank=False, 
                                    null=False)
    
    authors      = models.ForeignKey(Author,
                                    verbose_name='Author of book',
                                    on_delete=models.DO_NOTHING, blank=True, null=True)

    publishers   = models.ForeignKey(Publisher, 
                                    verbose_name='Publisher of book', 
                                    on_delete=models.DO_NOTHING, blank=True, null=True)

    objects  = BooksModelManager()



    def __str__(self):
        return self.title + ' ' + str(self.unit_price) 