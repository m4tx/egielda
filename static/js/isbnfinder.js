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

var button = $('<button class="btn btn-default" type="button" disabled="disabled">' +
    '<span class="glyphicon glyphicon-search"></span></button>');
var isbnInput = $('input[name="isbn"]');

function checkIsbn() {
    $(this).parent().removeClass('has-error');
    $(this).next().removeClass('glyphicon-warning-sign glyphicon-ok')
    var len = $(this).val().replace(/[\D]/g, '').length;
    if (len != 10 && len != 13) {
        button.attr("disabled", "disabled");
    } else {
        button.removeAttr("disabled");
    }
}

button.on('click', function () {
    var isbn = isbnInput.val().replace(/[\D]/g, ''); // remove all non-digit characters

    var url = "https://www.googleapis.com/books/v1/volumes?q=isbn:" + isbn + "&projection=lite";
    $.ajax(url)
        .success(function (data) {
            if (data.totalItems == 0) {
                isbnInput.parent().addClass('has-error has-feedback');
                isbnInput.next().removeClass('glyphicon-ok').addClass("glyphicon-warning-sign").attr("title",
                    gettext("The book wasn't found. Please check the ISBN or fill out the form manually."))
                    .tooltip('fixTitle');
                $('input[name="title"]').val('');
                $('input[name="publication_year"]').val('');
                $('input[name="publisher"]').val('');
                return;
            }

            $.ajax(data.items[0].selfLink + "?projection=lite")
                .success(function (data) {
                    isbnInput.parent().removeClass('has-error');
                    isbnInput.next().removeClass('glyphicon-warning-sign').addClass("glyphicon-ok").attr("title", "")
                        .attr("data-original-title", "");
                    $('input[name="publisher"]').val(data.volumeInfo.publisher);
                    var title = data.volumeInfo.title;
                    if (data.volumeInfo.subtitle != undefined) {
                        title += ": " + data.volumeInfo.subtitle;
                    }
                    $('input[name="title"]').val(title);
                    $('input[name="publication_year"]').val(data.volumeInfo.publishedDate.substring(0, 4));
                })

                .fail(function () {
                    isbnInput.parent().addClass('has-error has-feedback');
                    isbnInput.next().removeClass('glyphicon-ok').addClass("glyphicon-warning-sign").attr("title",
                        gettext("The book wasn't found. Please check the ISBN or fill out the form manually."))
                        .tooltip('fixTitle');
                    $('input[name="title"]').val('');
                    $('input[name="publication_year"]').val('');
                    $('input[name="publisher"]').val('');
                });

        })

        .fail(function () {
            isbnInput.parent().addClass('has-error has-feedback');
            isbnInput.next().removeClass('glyphicon-ok').addClass("glyphicon-warning-sign").attr("title",
                gettext("The book wasn't found. Please check the ISBN or fill out the form manually."))
                .tooltip('fixTitle');
            $('input[name="title"]').val('');
            $('input[name="publication_year"]').val('');
            $('input[name="publisher"]').val('');
        });
});

checkIsbn.call(isbnInput);
isbnInput.on('input', checkIsbn);
isbnInput.wrap('<div class="input-group has-feedback"/>').parent().append($('<span class="input-group-btn"/>')
    .append(button));
isbnInput.after('<span class="glyphicon form-control-feedback"></span>');
isbnInput.next().tooltip();
