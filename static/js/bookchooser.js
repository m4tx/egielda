$('.btn-add-book').on('click', function () {
    var tr = $(this).closest($('tr'));
    var existingTr = $('#chosen-book-list').find('tr[data-pk="' + tr.data('pk') + '"]');
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
        addExistingBook(tr, book.amount);
    }
});

$('#btn-add-new-book').on('click', function () {
    var isbn = $.trim($('input[name="isbn"]').val())
    var title = $.trim($('input[name="title"]').val())

    var existingTr = $('#chosen-book-list tr td:first-child').filter(function() {
        return $(this).text() == isbn && $(this).next().next().text() == title
    });
    existingTr = existingTr.parent();

    if (existingTr.length > 0) {
        var amountTr = existingTr.find('td[data-type="amount"]');
        var amount = parseInt(amountTr.text());
        amountTr.text(amount + 1);
        $.grep(chosenBooks, function (n, i) {
            return n.isbn == isbn && n.title == title;
        })[0].amount += 1;
    } else {
        var len = $('input[name="isbn"]').val().replace(/[\D]/g, '').length;
        if(len != 13 && len != 10) {
            return showMessage(gettext("Please enter valid ISBN number."));
        }

        addNewBook(1);
    }
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
            addExistingBook($('#bookList').find('table tr[data-pk="' + chosenBooks[bookid].pk + '"]'), chosenBooks[bookid].amount);
        } else {
            var book = $.extend({}, chosenBooks[bookid]); // Clone the associative array
            book.price = "N/A";
            addBookTr(createNewBookTr(book));
        }
    }
}

function addExistingBook(tr, amount) {
    var ctr = tr.clone();
    $('td:last-child', ctr).remove();
    ctr.append($('<td data-type="amount">' + amount + '</td>'));

    addBookTr(ctr);
}

function addNewBook(amount) {
    var ids = ['isbn', 'publisher', 'title', 'publication_year'];
    var vals = [];

    var book = new NewBook();
    var add = false;
    for (var prid in ids) {
        var input = $('input[name="' + ids[prid] + '"]');
        book[ids[prid]] = $.trim(input.val());
        vals.push(book[ids[prid]]);

        if (book[ids[prid]] != "") {
            add = true;
        }
    }
    vals.push("N/A");
    book.price = 0;
    book.amount = amount;

    if (add) {
        chosenBooks.push(book);
        var tr = createNewBookTr(vals);
        tr.append($('<td data-type="amount">' + book.amount + '</td>'))
        addBookTr(tr);
    }
}

function createNewBookTr(vals) {
    var tr = $('<tr/>');

    for (var id in vals) {
        if(id === 'amount') {
            tr = tr.append($('<td data-type="amount"/>').text(vals[id]));
        } else {
            tr = tr.append($('<td/>').text(vals[id]));
        }
    }

    return tr;
}

function addBookTr(tr) {
    var button = $('<button class="btn btn-xs btn-link btn-remove-book"><span class="glyphicon glyphicon-remove"></span> ' + gettext("Remove") + '</button>');
    button.on('click', function () {
        removeBook($('#chosen-book-list').find('button.btn-remove-book').index(this))
    });
    tr.append($('<td/>').append(button));

    $('#chosen-book-list-div').removeClass('hidden');
    var chosenTable = $('#chosen-book-list');
    $('button#btn-next').removeAttr('disabled');

    chosenTable.append(tr);
}

function removeBook(id) {
    var book = chosenBooks[id];
    var chosenBooksList = $('#chosen-book-list');
    var tr = chosenBooksList.find('tbody tr:eq(' + id + ')');
    if (book.amount > 1) {
        book.amount -= 1;
        tr.find('td[data-type="amount"]').text(book.amount);
    } else {
        tr.remove();
        chosenBooks.splice(id, 1);

        if (chosenBooks.length == 0) {
            $('#chosen-book-list-div').addClass('hidden');
            $('button#btn-next').attr('disabled', 'disabled');
        }
    }
}

addRetrievedBooks();

$("#category_filter").on("change", function(){
    var category = parseInt($(this).val());
    $("#bookList table > tbody > tr").each(function(){
        var bookCategories = $(this).attr("data-categories").split(",");
        var visible = false;

        for(var categoryID in bookCategories) {
            if(parseInt(bookCategories[categoryID]) === category || category === 0) {
                $(this).attr("style", "display: table-row");
                visible = true;
                break;
            }
        }

        if(!visible) {
            $(this).attr("style", "display: none");
        }
    });
})

function showMessage(text) {
    alert(text);
}
