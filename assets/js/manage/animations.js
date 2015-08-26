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
 * jQuery plugin adding some animations.
 */

(function() {
    'use strict';

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
})();

