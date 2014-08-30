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

var button = $('<button class="btn btn-default" type="button" disabled="disabled">' +
    '<span class="glyphicon glyphicon-search"></span></button>');
var isbnInput = $('input[name="isbn"]');

function checkIsbnLength() {
    $(this).parent().removeClass('has-error');
    $(this).next().removeClass('glyphicon-warning-sign glyphicon-ok').attr('title', '').attr('data-original-title', '');
    var len = $(this).val().replace(/[^0-9X]/g, '').length;
    if (len != 10 && len != 13) {
        button.attr("disabled", "disabled");
    } else {
        button.removeAttr("disabled");
    }
}

function setSuccess() {
    isbnInput.parent().removeClass('has-error');
    isbnInput.next().removeClass('glyphicon-warning-sign').addClass('glyphicon-ok').attr('title', '')
        .attr('data-original-title', '');
}

function setFail(text) {
    isbnInput.parent().addClass('has-error has-feedback');
    isbnInput.next().removeClass('glyphicon-ok').addClass('glyphicon-warning-sign').attr('title',
        text).tooltip('fixTitle');
    $('input[name="title"]').val('');
    $('input[name="publication_year"]').val('');
    $('input[name="publisher"]').val('');
}

button.on('click', function () {
    var isbn = isbnInput.val().replace(/[^0-9X]/g, ''); // remove all non-digit characters
    if (!isIsbnValid(isbn)) {
        setFail(gettext("This ISBN is invalid."));
        return;
    }

    var url = "https://www.googleapis.com/books/v1/volumes?q=isbn:" + isbn + "&projection=lite";
    $.ajax(url)
        .success(function (data) {
            if (data.totalItems == 0) {
                setFail(gettext("The book wasn't found. Please check the ISBN or fill out the form manually."));
                return;
            }

            $.ajax(data.items[0].selfLink + "?projection=lite")
                .success(function (data) {
                    setSuccess();
                    $('input[name="publisher"]').val(data.volumeInfo.publisher.substring(0, 150));
                    var title = data.volumeInfo.title;
                    if (data.volumeInfo.subtitle != undefined) {
                        title += ": " + data.volumeInfo.subtitle;
                    }
                    $('input[name="title"]').val(title.substring(0, 250));
                    $('input[name="publication_year"]').val(data.volumeInfo.publishedDate.substring(0, 4));
                })
                .fail(function () {
                    setFail(gettext("The book wasn't found. Please check the ISBN or fill out the form manually."));
                });
        })
        .fail(function () {
            setFail(gettext("The book wasn't found. Please check the ISBN or fill out the form manually."));
        });
});

checkIsbnLength.call(isbnInput);
isbnInput.on('input', checkIsbnLength);
isbnInput.wrap('<div class="input-group has-feedback"/>').parent().append($('<span class="input-group-btn"/>')
    .append(button));
isbnInput.after('<span class="glyphicon form-control-feedback"></span>');
isbnInput.next().tooltip();
