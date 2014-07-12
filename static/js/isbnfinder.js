var button = $('<button class="btn btn-default" type="button" disabled="disabled"><span class="glyphicon glyphicon-search"></span></button>');

$('input[name="isbn"]').on('keyup', function() {
    var len = $(this).val().replace(/[\D]/g, '').length;
    if (len != 10 && len != 13) {
        button.attr("disabled", "disabled");
    } else {
        button.removeAttr("disabled");
    }
});

button.on('click', function () {
    var isbn = $('input[name="isbn"]').val().replace(/[\D]/g, ''); // remove all non-digit characters

    var url = "https://www.googleapis.com/books/v1/volumes?q=isbn:" + isbn + "&projection=lite";
    $.ajax(url).success(function (data) {
        $.ajax(data.items[0].selfLink + "?projection=lite").success(function (data) {
            $('input[name="publisher"]').val(data.volumeInfo.publisher);
            var title = data.volumeInfo.title;
            if (data.volumeInfo.subtitle != undefined) {
                title += ": " + data.volumeInfo.subtitle;
            }
            $('input[name="title"]').val(title);
            $('input[name="publication_year"]').val(data.volumeInfo.publishedDate.substring(0, 4));
        });
    });
});
$('input[name="isbn"]').wrap('<div class="input-group"></div>').parent().append($('<span class="input-group-btn"/>')
    .append(button));
