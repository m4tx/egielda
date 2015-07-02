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

function Cache(useLocalStorage) {
    this._cache = {};

    if(!useLocalStorage) {
        this.localStorageEnabled = false;
    }
    else {
        try {
            this.localStorageEnabled = ('localStorage' in window) && window['localStorage'] !== null;
        }
        catch(e) {
            this.localStorageEnabled = false;
        }
    }
}

Cache.prototype = {
    get: function(key, isObject) {
        if(this.localStorageEnabled) {
            var value = localStorage.getItem(key) || undefined;
            if(value && isObject)
                value = JSON.parse(value);

            return value;
        }

        return this._cache[key] || undefined;
    },

    set: function(key, value, isObject) {
        if(this.localStorageEnabled) {
            if(isObject)
                value = JSON.stringify(value);

            try {
                localStorage.setItem(key, value);
            }
            catch(e) {
                if(e.name == 'QUOTA_EXCEEDED_ERR')
                    localStorage.clear();
            }
        }
        else {
            this._cache[key] = value;
        }

        return value;
    }
};