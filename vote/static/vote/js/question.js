(function(){

    var clean = function(){
        var answers = $('#answers input');
        answers.each(function(index, answer){
            $(answer).attr('id', 'id_' + index + '-answer_text');
            $(answer).attr('name', index + '-answer_text');
        });
        toggleButton();
    };

    var addAnswer = function(){
        $('#add-answer').on('click', function(){
           var answerDiv = $('#answer-div').clone();
           $('#answers').append(answerDiv);
           answerDiv.find('input').val('').focus();
           removeAnswer();
           clean();
        });
    };

    var removeAnswer = function(){
        $('.remove-answer').on('click', function(){
            if($('.remove-answer').length > 1){
                $(this).parent().remove();
            }
            clean();
        });
    };

    var toggleButton = function(){
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

    addAnswer();
    removeAnswer();
    toggleButton();

})();