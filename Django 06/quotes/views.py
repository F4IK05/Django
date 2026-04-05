from django.http import HttpResponse
import random
from django.shortcuts import render

def random_quote(request):
    quotes = [
        "Be yourself; everyone else is already taken.",
        "So many books, so little time.",
        "A room without books is like a body without a soul.",
        "You only live once, but if you do it right, once is enough."
    ]

    return HttpResponse(random.choice(quotes))