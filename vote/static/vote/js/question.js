(function(){

    var clean = function(){
        var answers = $('#answers input');
        answers.each(function(index, answer){
            $(answer).attr('id', 'id_' + index + '-answer_text');
            $(answer).attr('name', index + '-answer_text');
        });
    };

    var addAnswer = function(){
        $('#add-answer').click(function(){
           var answerDiv = $('#answer-div').clone();
           $('#answers').append(answerDiv);
           answerDiv.find('input').val('').focus();
           removeAnswer();
           clean();
           toggleButton();
        });
    };

    var removeAnswer = function(){
        $('.remove-answer').click(function(){
            if($('.remove-answer').length > 1){
                $(this).parent().remove();
            }
            toggleButton();
        });
    };

    var toggleButton = function(){
        console.log($('.remove-answer').length);
        if($('.remove-answer').length == 1){
            $('.remove-answer').each(function(){
               $(this).hide();
            });
        }
        else{
            $('.remove-answer').each(function(){
               $(this).show();
            });
        }
    };

    //removeAnswer();
    addAnswer();
    toggleButton();

})();