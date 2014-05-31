var button = $('<button class="btn btn-default" type="button"><span class="glyphicon glyphicon-search"></span></button>');
button.on('click', function () {
    var url = "https://www.googleapis.com/books/v1/volumes?q=isbn:" + $('input[name="isbn"]').val() + "&projection=lite";
    $.ajax(url).success(function (data) {
        $.ajax(data.items[0].selfLink + "?projection=lite").success(function (data) {
            $('input[name="publisher"]').val(data.volumeInfo.publisher);
            $('input[name="title"]').val(data.volumeInfo.title);
            $('input[name="publication_year"]').val(data.volumeInfo.publishedDate.substring(0, 4));
        });
    });
});
$('input[name="isbn"]').wrap('<div class="input-group"></div>').parent().append($('<span class="input-group-btn"/>').append(button));