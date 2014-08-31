/*
 * This file is part of e-Giełda.
 * Copyright (C) 2014  Mateusz Maćkowski and Tomasz Zieliński
 *
 * e-Giełda is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with e-Giełda.  If not, see <http://www.gnu.org/licenses/>.
 */

$('.btn-add-book').on('click', function () {
    var tr = $(this).closest($('tr'));
    var inStockTd = $('td.in-stock', tr);
    inStockTd.text(parseInt(inStockTd.text()) - 1);
    checkInStock(tr);

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
    var isbn = $('input[name="isbn"]').val().toUpperCase().replace(/[^\dX]/g, ''); // remove all chars which are not
                                                                                   // allowed in ISBN
    if (!isIsbnValid(isbn)) {
        setFail(gettext("This ISBN is invalid."), false);
        return;
    }

    var title = $.trim($('input[name="title"]').val());

    var existingTr = $('#chosen-book-list tr td:first-child').filter(function () {
        return $(this).text() == isbn
    });
    existingTr = existingTr.parent();

    if (existingTr.length > 0) {
        var amountTr = existingTr.find('td[data-type="amount"]');
        var amount = parseInt(amountTr.text());
        amountTr.text(amount + 1);
        $.grep(chosenBooks, function (n, i) {
            return n.isbn == isbn
        })[0].amount += 1;
    } else {
        addNewBook(1);
    }
});
$('button[name="btn-next"],button[name="btn-back"]').on('click', function () {
    $('form').append($('<input type="hidden" name="book_data">').attr('value', JSON.stringify(chosenBooks)))
        .submit();
});

function checkInStock(tr) {
    var inStock = $('td.in-stock', tr);
    var inStockVal = parseInt(inStock.text());
    var addBookBtn = $('button.btn-add-book', tr);

    // Reset
    $(tr).removeClass('bg-warning bg-danger text-muted');
    addBookBtn.removeAttr('disabled');

    // Check the In stock value
    if (inStockVal == 0) {
        $(tr).addClass('bg-danger text-muted');
        $('button.btn-add-book', tr).attr('disabled', 'disabled');
    } else if (inStockVal <= 5) {
        $(tr).addClass('bg-warning');
    }
}

function ExistingBook(pk, amount) {
    this.pk = pk;
    this.amount = amount;
}

function NewBook() {
}

function addRetrievedBooks() {
    for (var bookid in chosenBooks) {
        if (chosenBooks[bookid].pk != undefined) {
            var tr = $('#bookList').find('table tr[data-pk="' + chosenBooks[bookid].pk + '"]');
            var inStock = $('td.in-stock', tr);
            inStock.text(parseInt(inStock.text()) - chosenBooks[bookid].amount);
            addExistingBook(tr.attr("data-id", bookid), chosenBooks[bookid].amount);
        } else {
            var book = $.extend({}, chosenBooks[bookid]); // Clone the associative array
            book.price = "N/A";
            addBookTr(createNewBookTr(book));
        }
    }
}

function addExistingBook(tr, amount) {
    var ctr = tr.clone();
    ctr.removeClass();
    $('td:last-child', ctr).remove();
    $('td.in-stock', ctr).remove();
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

        if (ids[prid] === 'isbn')
            book[ids[prid]] = book[ids[prid]].toUpperCase().replace(/[^\dX]/g, '');

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
        if (id === 'amount') {
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
    $('button[name=btn-next]').removeAttr('disabled');

    chosenTable.append(tr);
}

function removeBook(id) {
    var book = chosenBooks[id];
    if (book.hasOwnProperty('pk')) {
        var listTr = '#bookList tr[data-pk="' + book['pk'] + '"]';
        var inStock = $('td.in-stock', listTr);
        inStock.text(parseInt(inStock.text()) + 1);
        checkInStock(listTr)
    }

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
            $('button[name="btn-next"]').attr('disabled', 'disabled');
        }
    }
}

addRetrievedBooks();
$('table tbody tr', '#bookList').each(function (index, value) {
    checkInStock(value);
});

function sortTable() {
    var rows = $('#bookList tbody tr');
    rows.detach();

    rows.sort(function (a, b) {
        var aAmount = 0;
        if (typeof $(a).attr("data-id") != 'undefined') {
            aAmount = chosenBooks[parseInt($(a).attr("data-id"))].amount;
        }

        var bAmount = 0;
        if (typeof $(b).attr("data-id") != 'undefined') {
            bAmount = chosenBooks[parseInt($(b).attr("data-id"))].amount;
        }

        a = parseInt($(a).find('.in-stock').text()) + aAmount;
        b = parseInt($(b).find('.in-stock').text()) + bAmount;

        if (a < b) {
            return 1;
        }

        if (a > b) {
            return -1;
        }

        return 0;
    });

    $.each(rows, function (index, row) {
        $('#bookList tbody').append(row);
    });
}
sortTable();

$("#category_filter").on("change", function () {
    var category = parseInt($(this).val());
    $("#bookList table > tbody > tr").each(function () {
        var bookCategories = $(this).attr("data-categories").split(",");
        var visible = false;

        for (var categoryID in bookCategories) {
            if (parseInt(bookCategories[categoryID]) === category || category === 0) {
                $(this).attr("style", "display: table-row");
                visible = true;
                break;
            }
        }

        if (!visible) {
            $(this).attr("style", "display: none");
        }
    });
})

function showMessage(text) {
    alert(text);
}
