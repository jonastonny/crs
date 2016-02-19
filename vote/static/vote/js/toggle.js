(function () {
    var toggleQuestion = function() {
        $(".toggleQuestion").click(function () {
            $(this).toggleClass("btn-warning btn-success");
            if($(this).text() == "Question is open") {
                $(this).text("Question is closed");
            } else {
                $(this).text("Question is open");
            };
        });
    };

    var toggleQuestionGroup = function() {
        $(".toggleQuestionGroup").click(function () {
            $(this).toggleClass("btn-warning btn-success");
            if($(this).text() == "Questiongroup is open") {
                $(this).text("Questiongroup is closed");
            } else {
                $(this).text("Questiongroup is open");
            };
        });
    };
    toggleQuestion();
    toggleQuestionGroup();
})();