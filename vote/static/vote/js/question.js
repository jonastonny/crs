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


//    <div class="form-group has-feedback" id="answer-div">
//	<label>Answer:</label>
//	<input class="correct" id="id_0-correct" name="0-correct" type="checkbox"> - mark this answer as correct?
//	<textarea class="form-control answer" cols="40" id="id_0-answer_text" name="0-answer_text" rows="1"></textarea>
//
//
//	<button type="button" class="btn btn-primary btn-block remove-answer" style="display: none;">Remove</button>
//</div>
//
//    var div = $('<div></div>');
//    var label = $('<label></label>');
//    var input = $('<input type="checkbox">');
//    var textarea = $('textarea');



    var addAnswer = function(){
        $('#add-answer').on('click', function(){
            var answerDiv = copyMe.clone();
            $('#answers').append(answerDiv);
            answerDiv.find('textarea.answer').val('').attr('value', '').focus();
            answerDiv.find('input:hidden#answer_id').val('None');
            answerDiv.find('input.correct').removeAttr('checked');
            removeAnswer();
            postUpdate();
            clean();
            //autosize($('textarea'));

            var id = answerDiv.find('textarea').attr('id');
            //tinyMCE.execCommand('mceRemoveEditor', false, id);
            tinyMCE.execCommand('mceAddEditor', false, id);

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
        var val = $('.remove-answer');
        if(val.length == 1){
            val.each(function(){
               $(this).hide();
            });
        }
        else{
            val.each(function(){
               $(this).show();
            });
        }
    };

    var updateAnswer = function() {
        $('.update-answer').blur(function(data) {
            updateAnswerHelper(this);
        });
        $('.correct').change(function(data){
            updateAnswerHelper(this);
        });
    };


    function updateAnswerHelper(_that){
        var _this = $(_that).parent();
        console.log(_this);

        //console.log($(_this).siblings('.correct')[0].checked);
        var postdata = {
            answer_text: _this.children('.update-answer')[0].value,
            answer_id: _this.children('#answer_id')[0].value,
            correct: _this.children('.correct')[0].checked
        };
        console.log(postdata);
        $.ajax({
            url: $("#update-url").data("url"),
            method: 'POST',
            data: postdata
        }).done(function(data) {
            _this.find('#answer_id').attr('value', JSON.parse(data)[0].pk);
        });
    }

    var updateQuestion = function(){
        $('.update-question').blur(function(){
            var _this = $(this);
            if (_this.val()){
                var postdata = {
                    question_text: $(_this).val(),
                }
                $.ajax({
                    url: $("#update-url").data("url"),
                    method: 'POST',
                    data: postdata
                }).done(function(data) {
                    console.log("Question updated...");
                });
            }
        });
    };

    tinyMCE.init({
        toolbar: [
            'undo redo | styleselect | bold italic | link | alignleft aligncenter alignright'
          ]
	});


    var copyMe =  $('#answer-div').clone();
    var a_id = $('#answer-div').find('textarea').attr('id');
    var q_id = $('#id_question_text').attr('id');
    tinyMCE.execCommand('mceAddEditor', false, a_id);
    tinyMCE.execCommand('mceAddEditor', false, q_id);


    var postUpdate = function(){
        updateAnswer();
        updateQuestion();
    };

    postUpdate();
    addAnswer();
    removeAnswer();
    toggleButton();

})();