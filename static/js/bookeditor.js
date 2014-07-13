if (!/Android|webOS|iPhone|iPad|iPod|BlackBerry/i.test(navigator.userAgent)) {
    $('select#id_categories').selectpicker({
        countSelectedText: gettext('{0} of {1} selected'),
        noneSelectedText: gettext('Nothing selected'),
        selectedTextFormat: 'count > 4'
    });
}