$('.btn-add-book').on('click', function () {
    var tr = $(this).closest($('tr'));
    var existingTr = $('#chosen-books-list').find('tr[data-pk="' + tr.data('pk') + '"]');
    if (existingTr.length > 0) {
        var amountTr = existingTr.find('td[data-type="amount"]');
        var amount = parseInt(amountTr.text());
        amountTr.text(amount + 1);
        $.grep(chosenBooks, function (n, i) {
            return n.pk == tr.data('pk')
        })[0].amount += 1;
    } else {
        var book = new ExistingBook(tr.data('pk'), 1);
        chosenBooks.push(book);
        addExistingBook(tr, book);
    }
});
$('#btn-add-new-book').on('click', function () {
    addNewBook();
});
$('button#btn-next,button#btn-back').on('click', function () {
    $('form').append($('<input type="hidden" name="book_data">').attr('value', JSON.stringify(chosenBooks)))
        .append($('<input type="hidden" name="' + this.id + '">'))
        .submit();
});

function ExistingBook(pk, amount) {
    this.pk = pk;
    this.amount = amount;
}

function NewBook() {
}

function addRetrievedBooks() {
    for (var bookid in chosenBooks) {
        if (chosenBooks[bookid].pk != undefined) {
            addExistingBook($('#bookList').find('table tr[data-pk="' + chosenBooks[bookid].pk + '"]'));
        } else {
            var book = $.extend({}, chosenBooks[bookid]); // Clone the associative array
            if (book.price != "") {
                book.price += currency;
            }
            addBookTr(createNewBookTr(book));
        }
    }
}

function addExistingBook(tr, book) {
    var ctr = tr.clone();
    $('td:last-child', ctr).remove();
    ctr.append($('<td data-type="amount">1</td>'));

    addBookTr(ctr, book);
}

function addNewBook() {
    var ids = ['isbn', 'publisher', 'title', 'publication_year', 'price'];
    var vals = [];

    var book = new NewBook();
    var add = false;
    for (var prid in ids) {
        var input = $('input[name="' + ids[prid] + '"]');
        book[ids[prid]] = input.val();
        if (ids[prid] == 'price' && book[ids[prid]] != '') {
            book[ids[prid]] = parseFloat(book[ids[prid]]).toFixed(2);
            vals.push(book[ids[prid]] + currency);
        } else {
            vals.push(book[ids[prid]]);
        }
        input.val("");

        if (book[ids[prid]] != "") {
            add = true;
        }
    }

    if (add) {
        chosenBooks.push(book);
        var tr = createNewBookTr(vals);
        tr.append($('<td data-type="amount">1</td>'));
        addBookTr(tr, book);
    }
}

function createNewBookTr(vals) {
    var tr = $('<tr/>');

    for (var id in vals) {
        tr = tr.append($('<td/>').text(vals[id]));
    }

    return tr;
}

function addBookTr(tr, book) {
    var button = $('<button class="btn btn-xs btn-link btn-remove-book"><span class="glyphicon glyphicon-remove"></span> ' + gettext("Remove") + '</button>');
    button.on('click', function () {
        removeBook($('#chosen-books-list').find('button.btn-remove-book').index(this))
    });
    tr.append($('<td/>').append(button));

    var chosenTable = $('#chosen-books-list');
    chosenTable.removeClass('hidden');
    $('button#btn-next').removeAttr('disabled');

    chosenTable.append(tr);
}

function removeBook(id) {
    var book = chosenBooks[id];
    var chosenBooksList = $('#chosen-books-list');
    var tr = chosenBooksList.find('tbody tr:eq(' + id + ')');
    if (book.amount > 1) {
        book.amount -= 1;
        tr.find('td[data-type="amount"]').text(book.amount);
    } else {
        tr.remove();
        chosenBooks.splice(id, 1);

        if (chosenBooks.length == 0) {
            chosenBooksList.addClass('hidden');
            $('button#btn-next').attr('disabled', 'disabled');
        }
    }
}

addRetrievedBooks();