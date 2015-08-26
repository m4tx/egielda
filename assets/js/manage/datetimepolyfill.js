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
 * "Polyfill" for datetime-local for browsers that do not support it (Firefox).
 */

var egielda = egielda || {};

egielda.datetimePolyfill = function(lang) {
    'use strict';

    window.addEventListener('load', function() {
        var input = document.createElement('input');
        input.setAttribute('type', 'datetime-local');

        if (input.type !== 'datetime-local') {
            // datetime-local not supported

            $('input[type="datetime-local"]').each(function() {
                $(this).datetimepicker({
                    format: 'Y-m-d H:i',
                    lang: lang
                });

                $(this).attr('placeholder', gettext('YYYY-MM-DD HH:MM'));
                if ($(this).is('[value]')) {
                    $(this).attr('value', $(this).attr('value').replace('T', ' '));
                }
            });
        }
    });
};
