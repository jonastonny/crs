(function(){

    $.ajaxSetup({
    beforeSend: function(xhr) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
    });

    var subscribe = function(){
        $("#unsubscribe").click(function(){
            var _url = $(this).data('url');
            var _parent = $(this).parent()
            $.ajax({
                url: _url + "subscribe/",
                method: "POST"
            }).done(function(data){
                $(_parent).remove();
            })
        });
    };

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    };

    var csrftoken = getCookie('csrftoken');

    subscribe();

})();