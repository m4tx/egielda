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

function checkIsbnLength() {
    var len = $(this).val().replace(/[\D]/g, '').length;
    if (len != 10 && len != 13) {
        button.attr("disabled", "disabled");
    } else {
        button.removeAttr("disabled");
    }
}

button.on('click', function () {
    var isbn = $('input[name="isbn"]').val().replace(/[\D]/g, ''); // remove all non-digit characters

    var url = "https://www.googleapis.com/books/v1/volumes?q=isbn:" + isbn + "&projection=lite";
    $.ajax(url)
        .success(function (data) {
            if(data.totalItems == 0) {
                $('input[name="isbn"]').parent().addClass('has-error has-feedback');
                $('input[name="isbn"]').next().removeClass('glyphicon-ok').addClass("glyphicon-warning-sign")
                    .attr("title", gettext("Please enter valid ISBN number."));
                $('input[name="title"]').val('');
                $('input[name="publication_year"]').val('');
                $('input[name="publisher"]').val('');
                return;
            }

            $.ajax(data.items[0].selfLink + "?projection=lite")
                .success(function (data) {
                    $('input[name="isbn"]').parent().removeClass('has-error');
                    $('input[name="isbn"]').next().removeClass('glyphicon-warning-sign').addClass("glyphicon-ok")
                        .attr("title", "");
                    $('input[name="publisher"]').val(data.volumeInfo.publisher);
                    var title = data.volumeInfo.title;
                    if (data.volumeInfo.subtitle != undefined) {
                        title += ": " + data.volumeInfo.subtitle;
                    }
                    $('input[name="title"]').val(title);
                    $('input[name="publication_year"]').val(data.volumeInfo.publishedDate.substring(0, 4));
                })

                .fail(function() {
                    $('input[name="isbn"]').parent().addClass('has-error has-feedback');
                    $('input[name="isbn"]').next().removeClass('glyphicon-ok').addClass("glyphicon-warning-sign")
                        .attr("title", gettext("Please enter valid ISBN number."));
                    $('input[name="title"]').val('');
                    $('input[name="publication_year"]').val('');
                    $('input[name="publisher"]').val('');
                });

        })

        .fail(function() {
            $('input[name="isbn"]').parent().addClass('has-error has-feedback');
            $('input[name="isbn"]').next().removeClass('glyphicon-ok').addClass("glyphicon-warning-sign")
                .attr("title", gettext("Please enter valid ISBN number."));
            $('input[name="title"]').val('');
            $('input[name="publication_year"]').val('');
            $('input[name="publisher"]').val('');
        });
});

var isbnInput = $('input[name="isbn"]');
checkIsbnLength.call(isbnInput);
isbnInput.on('input', checkIsbnLength);
isbnInput.wrap('<div class="input-group has-feedback"/>').parent().append($('<span class="input-group-btn"/>')
    .append(button));
isbnInput.after('<span class="glyphicon form-control-feedback"></span>');
