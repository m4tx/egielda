/*
 * This file is part of e-Giełda.
 * Copyright (C) 2014-2015  Mateusz Maćkowski and Tomasz Zieliński
 *
 * e-Giełda is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with e-Giełda.  If not, see <http://www.gnu.org/licenses/>.
 */

/**
 * ISBN finder which retrieves information about the book when ISBN is entered.
 */

var egielda = egielda || {};

egielda.isbnFinder = function() {
    'use strict';

    var INVALID_ISBN = gettext('This ISBN is invalid.'),
        BOOK_NOT_FOUND =
            gettext('The book wasn\'t found. Please check the ISBN or fill out the form manually.');
    var get = egielda.jQ.get;

    function getInputByName(name) {
        return get('input[name="' + name + '"]');
    }

    var searchIsbnButton = get('<button class="ui icon button" disabled="disabled">' +
        '<i class="icon search"></i></button>');
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

    function setSearchIsbnIcon(icon) {
        searchIsbnButton.children('i').removeClass().addClass('icon').addClass(icon);
    }

    function setSearchIsbnStatus(success, text, clearFields) {
        searchIsbnButton.removeClass('loading');

        if (success) {
            setSearchIsbnIcon('checkmark');
            searchIsbnButton.disable();
        } else {
            setSearchIsbnIcon('cancel');
            // 'is visible' returns either true or element, so we have to compare it to true
            if (searchIsbnButton.popup('is visible') !== true) {
                searchIsbnButton.popup({
                    content: text,
                    position: 'top right',
                    onHidden: function() {
                        searchIsbnButton.popup('destroy');
                    }
                });

                searchIsbnButton.popup('show');
            }

            if (clearFields) {
                $.each(['title', 'publication_year', 'publisher'], function() {
                    getInputByName(this).setText('');
                });
            }
        }
    }

    function clearSearchIsbnStatus() {
        setSearchIsbnIcon('search');
        searchIsbnButton.popup('hide');
    }

    searchIsbnButton.on('click', function(e) {
        e.preventDefault();

        // remove all chars which are not allowed
        var isbn = isbnInput.getText().toUpperCase().replace(/[^\dX]/g, '');
        if (!isIsbnValid(isbn)) {
            setSearchIsbnStatus(false, INVALID_ISBN, true);
            return;
        }

        searchIsbnButton.addClass('loading');
        var url = 'https://www.googleapis.com/books/v1/volumes?q=isbn:' + isbn +
            '&fields=items(selfLink)';
        $.ajax(url)
            .success(function(data) {
                var link;
                try {
                    link = data.items[0].selfLink;
                } catch (err) {
                    setSearchIsbnStatus(false, BOOK_NOT_FOUND, true);
                    return;
                }

                $.ajax(link + '?fields=volumeInfo(title,subtitle,publisher,publishedDate)')
                    .success(function(data) {
                        setSearchIsbnStatus(true);

                        var title = data.volumeInfo.title || '';
                        if (data.volumeInfo.subtitle != undefined) {
                            title += ': ' + data.volumeInfo.subtitle;
                        }
                        var publisher = data.volumeInfo.publisher || '';
                        var publicationYear = data.volumeInfo.publishedDate || '';

                        getInputByName('publisher').setText(publisher.substring(0, 150));
                        getInputByName('title').setText(title.substring(0, 250));
                        getInputByName('publication_year')
                            .setText(publicationYear.substring(0, 4));
                    })
                    .fail(function() {
                        setSearchIsbnStatus(false, BOOK_NOT_FOUND, true);
                    });
            })
            .fail(function() {
                setSearchIsbnStatus(false, BOOK_NOT_FOUND, true);
            });
    });

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
    isbnInput.wrap('<div class="ui action input"/>').parent().append(searchIsbnButton);

    // Add some util functions to egielda namespace
    egielda.isbnFinderUtils = {
        isIsbnValid: isIsbnValid,
        setSearchIsbnStatus: setSearchIsbnStatus
    };
};
