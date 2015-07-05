$("#class_filter").on("change", function () {
    var student_class = $(this).val();
    $("table > tbody > tr").each(function () {
        if($(this).attr("data-class") !== student_class && student_class !== "0") {
            $(this).attr("style", "display: none");
        }
        else {
            $(this).attr("style", "display: table-row");
        }
    });
});
