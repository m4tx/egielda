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
var choosingIncorrect = 'off',
    fields = ['username', 'first_name', 'last_name', 'year', 'class_letter', 'phone_number', 'email'];

// Animations
$.fn.fadeOutKeepSpace = function(duration, complete) {
    this.fadeTo(duration, 0, 'swing', function() {
        $(this).css('visibility', 'hidden');
        if ($.isFunction(complete)) {
            complete.call(this);
        }
    });
    return this;
};
$.fn.fadeInKeepSpace = function(duration, complete) {
    this.css('visibility', 'visible');
    this.fadeTo(duration, 1, 'swing', complete);
    return this;
};

// Create the checkboxes
$('.responsive-form > div').each(function (i) {
    var div = $('<div class="ui checkbox"/>')
            .css('visibility', 'hidden')
            .css('opacity', 0),
        input = $('<input type="checkbox" class="to-correct">')
            .prop('id', 'to_correct_' + fields[i]);
    div.append(input).append($('<label/>'));
    $(this).prepend(div);
});

// "Cancel" button on-click
$('#cancel').click(function (e) {
    if (choosingIncorrect === 'on') {
        e.preventDefault();
        choosingIncorrect = 'switching';

        $('#to-correct-info').slideUp();
        $('#to-correct-not-selected').slideUp();
        $('#verify').prop('disabled', false);
        $('.to-correct').parent().fadeOutKeepSpace(400, function () {
            $(this).children('input').prop('checked', false);
            choosingIncorrect = 'off';
        });
    }
});

// "Needs correction" button on-click
$('#needs-correction').click(function (e) {
    e.preventDefault();
    if (choosingIncorrect === 'switching') {
        // Clicking needs correction when checkboxes are already fading out should do nothing
        return;
    }

    if (choosingIncorrect == 'off') {
        // Not yet in "Needs correction" mode
        $('#to-correct-info').slideDown();
        $('.to-correct').parent().fadeInKeepSpace(400);
        $('#verify').prop('disabled', true);
        choosingIncorrect = 'on';
    } else if ($('.to-correct:checked').length == 0) {
        // No checkboxes were selected
        $('#to-correct-not-selected').slideDown();
        window.setTimeout(function () {
            $('#to-correct-not-selected').slideUp();
        }, 3000);
    } else {
        // Send selected checkboxes
        var toCorrect = new Array();
        $('.to-correct:checked').each(function () {
            toCorrect.push($(this).prop('id').substr('to_correct_'.length));
        });
        var form = $(document.forms[0]);

        form.append(
            $('<input type="hidden" name="incorrect_fields">').prop('value', toCorrect.join(','))
        );
        form.attr('action', form.data('action-needscorrection'));
        form.submit();
    }
});
