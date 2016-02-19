(function () {
    var open = function() {
        $("#toggle").click(function () {
            $(this).toggleClass("toggle_open toggle_closed btn-warning btn-success");
            if($(this).text() == "Question is open") {
                $(this).text("Question is closed");
            } else {
                $(this).text("Question is open");
            };
        });
    };

    open();
})();