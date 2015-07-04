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

var cache = new Cache(false);

$('input.tokenfield').each(function() {
    $(this).attr("data-val", $(this).val());
    $(this).val('');
});

$('input.tokenfield').tokenfield({
    autocomplete: {
        source: function (request, response) {
            var value = request.term;
            var regex = cache.get(value) ||
                cache.set(value, new RegExp(value.replace(/[^\w]/g, "").split('').join('.*'), 'i'));

            var correctMatches = [];
            users.filter(function(user, key) {
                if(regex.test("#" + key + ": " + user))
                    correctMatches.push({value: key, label: "#" + key + ": " + user});
            });

            correctMatches.sort(compareByLevenshteinDistance(value));
            response(correctMatches);
        },
        delay: 100
    },
    showAutocompleteOnFocus: true,
    delimiter: []
});

$('input.tokenfield').on('tokenfield:createtoken', function(e) {
    var value = e.attrs.value.toString();
    var match = value.match(/^#(\d+)/) || value.match(/^(\d+)/);
    if(match) {
        var index = parseInt(match[1]);
        if(index in users) {
            e.attrs.value = index;
            e.attrs.label = "#" + index + ": " + users[index];
        }
        else
            return false;
    }
    else
        return false;
});


$('input.tokenfield').each(function() {
    var values = $(this).attr("data-val").split(',');
    for(var i = 0; i < values.length; ++i)
        $(this).tokenfield('createToken', { value: values[i]});
});

$('div.tokenfield.form-control').each(function() {
    if($(this).children('input.tokenfield.form-control').hasClass('has-error')) {
        $(this).css("border-color", "#a94442");
        $(this).css("-webkit-box-shadow", "inset 0 1px 1px rgba(0,0,0,.075)");
        $(this).css("box-shadow", "inset 0 1px 1px rgba(0,0,0,.075)");
    }
});

$(document.forms[0]).on('submit', function() {
    $('input.tokenfield.form-control').each(function() {
        var tokens = $(this).tokenfield('getTokens');
        var values = new Array();
        for(var i = 0; i < tokens.length; ++i) {
            values.push(tokens[i].value.toString());
        }
        $(this).val(values.join(','));
    });
});

function levenshteinDistance(text1, text2) {
    var distance = new Array(text1.length+1);
    var i;
    for(i = 0; i <= text1.length; ++i)
        distance[i] = new Array(text2.length+1);

    for(i = 0; i <= text1.length; ++i)
        distance[i][0] = i;

    for(i = 0; i <= text2.length; ++i)
        distance[0][i] = i;

    for(i = 1; i <= text1.length; ++i)
        for(var j = 1; j <= text2.length; ++j) {
            if (text1[i] == text2[j])
                distance[i][j] = distance[i-1][j-1];
            else
                distance[i][j] = Math.min(distance[i-1][j], distance[i][j-1], distance[i-1][j-1])+1;
        }

    return distance[text1.length][text2.length];
}

function compareByLevenshteinDistance(original) {
    return function(a, b) {
        return levenshteinDistance(original, a.label) - levenshteinDistance(original, b.label);
    }
}