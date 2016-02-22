(function(){

    var clean = function(){
        var corrects = $('#answers input.correct');
        corrects.each(function (index, correct) {
            $(correct).attr('id', 'id_' + index + '-correct');
            $(correct).attr('name', index + '-correct');
        });
        var answers = $('#answers textarea.answer');
        answers.each(function(index, answer){
            $(answer).attr('id', 'id_' + index + '-answer_text');
            $(answer).attr('name', index + '-answer_text');


            if(~(window.location.pathname).indexOf('edit')){
                var answerId = $(answer).parent().find('#answer_id').val();
                var deleteUrl = $(answer).parent().find('#delete-url').val();
                var array = deleteUrl.split("/");
                array[9] = answerId;
                $(answer).parent().find("#delete-url").val(array.join("/"));
            }
        });
        toggleButton();
    };

    var addAnswer = function(){
        $('#add-answer').on('click', function(){
            var answerDiv = $('#answer-div').clone();
            $('#answers').append(answerDiv);
            answerDiv.find('textarea.answer').val('').attr('value', '').focus();
            answerDiv.find('input:hidden#answer_id').val('None');
            removeAnswer();
            postUpdate();
            clean();
        });
    };

    var removeAnswer = function(){
        $('.remove-answer').on('click', function(){
            clean();
            var _this = $(this);
            if($('.remove-answer').length > 1){
                _this.parent().remove();
                if(~(window.location.pathname).indexOf('edit')){ // we are editing and deleting
                    if($(_this).parent().find("#answer_id").val() != "None"){
                        $.ajax({
                           method: 'POST',
                           url : _this.parent().find('#delete-url').val()
                        });
                    }
                }
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
            if (_this.val()){
                if ($(this).attr('id') == 'id_question_text') {
                    var postdata = {
                        question_text: $(this).val()
                    }
                }
                else {
                    var postdata = {
                        answer_text: $(this).val(),
                        answer_id: $(this).siblings('#answer_id')[0].value
                    }
                }
                $.ajax({
                    url: $("#update-url").data("url"),
                    method: 'POST',
                    data: postdata
                }).done(function(data) {
                    _this.parent().find('#answer_id').attr('value', JSON.parse(data)[0].pk);
                });
            }
        });
    };

    addAnswer();
    postUpdate();
    removeAnswer();
    toggleButton();

})();