from collections import Counter


def books_by_types(books):
    """
    Groups provided books by their book types and adds information about amount of books in each book type.
    :param books: list of Books
    :return: dictionary containing BookType -> Book pairs, where Book is the last Book from its BookType in books list
    """
    amounts = Counter([book.book_type for book in books])
    d = {}
    for book in books:
        book.book_type.amount = amounts[book.book_type]
        d[book.book_type] = book
    return d
