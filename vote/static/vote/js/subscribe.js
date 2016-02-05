(function(){
    var subscribe = function(){
        $("#unsubscribe").click(function(){
            var _url = $(this).data('url');
            var _parent = $(this).parent()
            $.ajax({
                url: _url,
                method: "POST"
            }).done(function(data){
                $(_parent).remove();
            })
        });
    };

    subscribe();

})();