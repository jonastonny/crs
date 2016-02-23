(function () {
    var toggleQuestion = function() {
        $(".toggleQuestion").click(function () {
            $(this).toggleClass("btn-warning btn-success");
            if($(this).text() == "Close Question") {
                $(this).text("Open Question");
            } else {
                $(this).text("Close Question");
            };
        });
    };

    var toggleQuestionGroup = function() {
        $(".toggleQuestionGroup").click(function () {
            $(this).toggleClass("btn-warning btn-success");
            if($(this).text() == "Close Group") {
                $(this).text("Open Group");
            } else {
                $(this).text("Close Group");
            };
        });
    };
    toggleQuestion();
    toggleQuestionGroup();
})();