(function(){

    var clean = function(){
        var answers = $('#answers input.update');
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
            answerDiv.find('input').val('').attr('value', '').focus();
            answerDiv.find('input:hidden').val('None');
            removeAnswer();
            postUpdate();
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

    var postUpdate = function() {
        $('.update').blur(function(data) {
            var _this = $(this);
            $(console.log(data));
            if ($(this).attr('id') == 'id_question_text') {
                var postdata = {question_text: $(this).val()}
            }
            else {
                var postdata = {answer_text: $(this).val(), answer_id: $(this).siblings('#answer_id')[0].value}
            }
            console.log(postdata);
            $.ajax({
                url: $("#update-url").data("url"),
                method: 'POST',
                data: postdata
            }).done(function(data) {
                    //console.log(data);
                _this.parent().find('#answer_id').attr('value', JSON.parse(data)[0].pk);
                console.log(_this.parent());
            });
        });
    };

    postUpdate();
    addAnswer();
    removeAnswer();
    toggleButton();

})();