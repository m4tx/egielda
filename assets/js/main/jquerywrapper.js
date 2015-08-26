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
 * Wrapper for some commonly used jQuery functions.
 */

var egielda = egielda || {};

egielda.jQ = (function() {
    'use strict';

    function Button(predecessor) {
        // extends jQuery's button object
        for (var property in predecessor) {
            this[property] = predecessor[property];
        }

        this.enable = function() {
            predecessor.removeAttr('disabled');
        };

        this.disable = function() {
            predecessor.attr('disabled', 'disabled');
        };
    }

    function Edit(predecessor) {
        // extends jQuery's text input object
        for (var property in predecessor) {
            this[property] = predecessor[property];
        }

        this.setText = function(text) {
            predecessor.val(text);
        };

        this.getText = function() {
            return predecessor.val();
        };
    }

    var get = function(expr) {
        var element = $(expr);
        if (element.is('input[type=button],button')) {
            return new Button(element);
        }
        if (element.is('input[type=text],input[type=number]')) {
            return new Edit(element);
        }
    };

    return {
        get: get
    };
})();
