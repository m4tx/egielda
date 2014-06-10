$('.btn-add-book').on('click', function() {
    var tr = $(this).closest($('tr'));
    var book = new ExistingBook(tr.data('pk'));
    chosenBooks.push(book);
    addExistingBook(tr, book);
});
$('#btn-add-new-book').on('click', function () {
    addNewBook();
});
$('button#btn-next,button#btn-back').on('click', function() {
    $('form').append($('<input type="hidden" name="book_data">').attr('value', JSON.stringify(chosenBooks)))
        .append($('<input type="hidden" name="' + this.id + '">'))
        .submit();
});

function ExistingBook(pk) {
    this.pk = pk;
}

function NewBook() {
}

function addRetrievedBooks() {
    for (var book in chosenBooks) {
        if (chosenBooks[book].pk != undefined) {
            addExistingBook($('#bookList').find('table tr[data-pk="' + chosenBooks[book].pk + '"]'));
        } else {
            addBookTr(createNewBookTr(chosenBooks[book]));
        }
    }
}

function addExistingBook(tr, book) {
    var ctr = tr.clone();
    tr.addClass('hidden');
    $('td:last-child', ctr).remove();

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
        }
        input.val("");

        if (book[ids[prid]] != "") {
            add = true;
        }
        vals.push(book[ids[prid]]);
    }

    if (add) {
        chosenBooks.push(book);
        addBookTr(createNewBookTr(vals), book);
    }
}

function createNewBookTr(vals) {
    var tr = $('<tr/>');

    for (var id in vals) {
        if (id == 'price' && vals[id] != '') {
            tr = tr.append($('<td/>').text(vals[id] + currency));
        } else {
            tr = tr.append($('<td/>').text(vals[id]));
        }
    }

    return tr;
}

function addBookTr(tr, book) {
    var button = $('<button class="btn btn-xs btn-link btn-remove-book"><span class="glyphicon glyphicon-remove"></span> ' + gettext("Remove") + '</button>');
    button.on('click', function() {
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
    if (book.pk != undefined) {
        $('#bookList').find('table tr[data-pk="' + book.pk + '"]').removeClass('hidden');
    }

    var chosenBooksList = $('#chosen-books-list');
    chosenBooks.splice(id, 1);
    chosenBooksList.find('tbody tr:eq(' + id + ')').remove();

    if (chosenBooks.length == 0) {
        chosenBooksList.addClass('hidden');
        $('button#btn-next').attr('disabled', 'disabled');
    }
}

addRetrievedBooks();