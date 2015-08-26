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
 * General code that should be run on all pages.
 */

(function() {
    'use strict';

    // Enable Semantic UI components
    $('.ui.dropdown,.ui.form select').dropdown();
    $('.ui.dropdown select').each(function() {
        if ($(this).prop('disabled')) {
            $(this).parent().addClass('disabled');
        }
    });
    $('.message .close').on('click', function() {
        $(this).closest('.message').transition('fade');
    });

    // Tablesorter
    window.addEventListener('load', function() {
        if ($().tablesorter) {
            $('table.sortable').tablesorter();
        }
    });
})();

