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
 * Master ("Select all")-children checkboxes, used in some tables.
 */

var egielda = egielda || {};

egielda.checkboxTable = function() {
    'use strict';

    window.addEventListener('load', function() {
        $('.ui.checkbox').checkbox('set enabled');
        $('.table .master.checkbox').checkbox({
            onChecked: function() {
                var $childCheckbox = $(this).closest('.table').find('.checkbox');
                $childCheckbox.checkbox('check');
            },
            onUnchecked: function() {
                var $childCheckbox = $(this).closest('.table').find('.checkbox');
                $childCheckbox.checkbox('uncheck');
            }
        });

        $('.table .child.checkbox').checkbox({
            fireOnInit: true,
            onChange: function() {
                var $listGroup = $(this).closest('.table'),
                    $parentCheckbox = $listGroup.find('th .master.checkbox'),
                    $checkbox = $listGroup.find('.checkbox').not('.master'),
                    allChecked = true,
                    allUnchecked = true;

                $checkbox.each(function() {
                    if ($(this).checkbox('is checked')) {
                        allUnchecked = false;
                    } else {
                        allChecked = false;
                    }
                });
                if (allChecked) {
                    $parentCheckbox.checkbox('set checked');
                } else if (allUnchecked) {
                    $parentCheckbox.checkbox('set unchecked');
                } else {
                    $parentCheckbox.checkbox('set indeterminate');
                }
            }
        });
    });
};
