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

$("#class_filter").on("change", function () {
    var studentClass = $(this).val();
    $("table > tbody > tr").each(function () {
        if($(this).attr("data-class") !== studentClass && studentClass !== "0") {
            $(this).attr("style", "display: none");
        }
        else {
            $(this).attr("style", "display: table-row");
        }
    });
});
