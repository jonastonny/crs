(function(){
    var subscribe = function(){
        $(".toggle_subscription").click(function(){
            var _url = $(this).data('url');
            var _parent = $(this).parent()
            var _this = $(this)
            $.ajax({
                url: _url,
                method: "POST"
            }).done(function(data){
                if($(_this).attr("id") != "room_detail"){
                    $(_parent).remove();
                }
            })
        });
    };

    var toggle = function(){
            $(".toggle_question").click(function(){
                var _url = $(this).data('url');
                $.ajax({
                    url: _url,
                    method: "POST"
                }).done(function(){
                })
            });
        };

    subscribe();
    toggle();

})();