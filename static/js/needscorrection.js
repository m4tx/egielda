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

// 'on', 'off' or 'switching'
var choosingIncorrect = 'off';

$('#cancel').click(function (e) {
    if (choosingIncorrect === 'on') {
        e.preventDefault();
        choosingIncorrect = 'switching';

        $('#to-correct-info').slideUp();
        $('#to-correct-not-selected').slideUp();
        $('#verify').prop('disabled', false);
        $('.to-correct').fadeOut(function() {
            $(this).remove();
            choosingIncorrect = 'off';
        });
    }
});

$('#needs-correction').click(function (e) {
    e.preventDefault();
    if (choosingIncorrect === 'switching') {
        // Clicking needs correction when checkboxes are already fading out should do nothing
        return;
    }
    choosingIncorrect = 'on';

    $('#to-correct-info').slideDown();
    $('#verify').prop('disabled', true);

    if ($('.to-correct').length == 0) {
        $('.form-group').each(function () {
            $(this).children().first().prepend(
                $('<input type="checkbox" class="to-correct" style="margin-top: 11px;">').fadeIn()
            );
        });
    } else if ($('.to-correct:checked').length == 0) {
        $('#to-correct-not-selected').slideDown();
        window.setTimeout(function () {
            $('#to-correct-not-selected').slideUp();
        }, 3000);
    } else {
        var toCorrect = new Array();
        $('.to-correct:checked').each(function () {
            toCorrect.push($(this).parent().attr('id').substr('to-correct-'.length));
        });
        var form = $(document.forms[0]);

        form.append(
            $('<input type="hidden" name="incorrect_fields">').prop('value', toCorrect.join(','))
        );
        form.attr('action', form.data('action-needscorrection'));
        form.submit();
    }
});
