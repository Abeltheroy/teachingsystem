from django.test import TestCase
from app.models import *
# Create your tests here.

if __name__ == '__main__':
    c1 = Course.objects.filter(price=19.99).all()
    print(c1)