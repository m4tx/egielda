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
 * Simple key-value store.
 */

var egielda = egielda || {};

egielda.Cache = (function() {
    function Cache() {
        this._cache = {};
    }

    Cache.prototype = {
        get: function(key) {
            return this._cache[key] || undefined;
        },

        set: function(key, value) {
            this._cache[key] = value;
            return value;
        }
    };

    return Cache;
})();

