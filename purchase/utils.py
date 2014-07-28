from django.db.models import Q
from django.utils import timezone
from books.models import Book


def get_available_books():
    return Book.objects.prefetch_related('book_type').filter(accepted=True, sold=False).filter(
        Q(reserved_until__lte=timezone.now()) | Q(reserved_until__isnull=True))