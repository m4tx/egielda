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

var INVALID_ISBN = gettext("This ISBN is invalid.");
var BOOK_NOT_FOUND = gettext("The book wasn't found. Please check the ISBN or fill out the form manually.");

function getInputByName(name) {
    return get('input[name="' + name + '"]');
}

var searchIsbnButton = get('<button class="btn btn-default" type="button" disabled="disabled">' +
    '<span class="glyphicon glyphicon-search"></span></button>');
var isbnInput = getInputByName('isbn');

// Ported from utils/isbn.py
function isIsbnValid(isbn) {
    function isbnToDigitArray(isbn) {
        var arr = [];
        for (var i = 0; i < isbn.length; ++i) {
            arr.push(isbn[i] == 'X' ? 'X' : parseInt(isbn[i]));
        }
        return arr;
    }

    function calcIsbn10CheckDigit(isbn) {
        isbn = isbnToDigitArray(isbn);

        var tmp = 0;
        for (var i = 0; i < 9; ++i) {
            tmp += (i + 1) * isbn[i];
        }
        tmp %= 11;
        return tmp == 10 ? 'X' : tmp;
    }

    function calcIsbn13CheckDigit(isbn) {
        isbn = isbnToDigitArray(isbn);

        var tmp = 0;
        for (var i = 0; i < 12; i += 2) {
            tmp += isbn[i];
        }
        for (i = 1; i < 12; i += 2) {
            tmp += 3 * isbn[i];
        }
        return (10 - tmp % 10) % 10;
    }

    if (isbn.length == 10) {
        for (var i = 0; i < isbn.length - 1; ++i) {
            if (isbn[i] < '0' || isbn[i] > '9') {
                return false;
            }
        }
        if (isbn[isbn.length - 1] != 'X' &&
            (isbn[isbn.length - 1] < '0' || isbn[isbn.length - 1] > '9')) {
            return false;
        }
        if (isbn[isbn.length - 1] != calcIsbn10CheckDigit(isbn)) {
            return false;
        }
    } else if (isbn.length == 13) {
        if (isbn[isbn.length - 1] != calcIsbn13CheckDigit(isbn)) {
            return false;
        }
    } else {
        return false;
    }
    return true;
}

function setSearchIsbnStatus(success, text, clearFields) {
    if(success) {
        isbnInput.parent().removeClass('has-error');
        isbnInput.next().removeClass('glyphicon-warning-sign').addClass('glyphicon-ok').attr('title', '')
            .attr('data-original-title', '');
    }
    else {
        isbnInput.parent().addClass('has-error has-feedback');
        isbnInput.next().removeClass('glyphicon-ok').addClass('glyphicon-warning-sign').attr('title', text)
            .tooltip('fixTitle');

        if (clearFields) {
            $.each(['title', 'publication_year', 'publisher'], function(){
                getInputByName(this).setText('');
            });
        }
    }
}

searchIsbnButton.on('click', function () {
    var isbn = isbnInput.getText().toUpperCase().replace(/[^\dX]/g, ''); // remove all chars which are not allowed
    if (!isIsbnValid(isbn)) {
        setSearchIsbnStatus(false, INVALID_ISBN, true);
        return;
    }

    var url = "https://www.googleapis.com/books/v1/volumes?q=isbn:" + isbn + "&fields=items(selfLink)";
    $.ajax(url)
        .success(function (data) {
            if (data.totalItems == 0) {
                setSearchIsbnStatus(false, BOOK_NOT_FOUND, true);
                return;
            }

            $.ajax(data.items[0].selfLink + "?fields=volumeInfo(title,subtitle,publisher,publishedDate)")
                .success(function (data) {
                    setSearchIsbnStatus(true);

                    var title = data.volumeInfo.title || "";
                    if (data.volumeInfo.subtitle != undefined) {
                        title += ": " + data.volumeInfo.subtitle;
                    }
                    var publisher = data.volumeInfo.publisher || "";
                    var publication_year = data.volumeInfo.publishedDate || "";

                    getInputByName('publisher').setText(publisher.substring(0, 150));
                    getInputByName('title').setText(title.substring(0, 250));
                    getInputByName('publication_year').setText(publication_year.substring(0, 4));
                })
                .fail(function () {
                    setSearchIsbnStatus(false, BOOK_NOT_FOUND, true);
                });
        })
        .fail(function () {
            setSearchIsbnStatus(false, BOOK_NOT_FOUND, true);
        });
});

function clearSearchIsbnStatus() {
    isbnInput.parent().removeClass('has-error');
    isbnInput.next().removeClass('glyphicon-warning-sign glyphicon-ok').attr('title', '')
        .attr('data-original-title', '');
}

function checkSearchAvailability() {
    var isbn = isbnInput.getText();
    isbn = isbn.toUpperCase().replace(/[^\dX]/g, ''); // remove all chars which are not allowed

    if (isbn.length != 10 && isbn.length != 13) {
        searchIsbnButton.disable();
    } else {
        searchIsbnButton.enable();
    }
}

// track user input to disable or enable search's button when applicable
checkSearchAvailability.call(isbnInput);
isbnInput.on('input', function() {
    clearSearchIsbnStatus();
    checkSearchAvailability();
});

// append controls to document
isbnInput.wrap('<div class="input-group has-feedback"/>').parent().append($('<span class="input-group-btn"/>')
    .append(searchIsbnButton));
isbnInput.after('<span class="glyphicon form-control-feedback"></span>');
isbnInput.next().tooltip();