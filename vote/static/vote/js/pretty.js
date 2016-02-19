(function() {
    var addPrettyfi = function() {
        var pre = $('pre');
        pre.each(function() {
            $(pre).addClass('prettyprint linenums');
        });
        var code = $('code');
        code.each(function() {
           $(code).addClass('prettyprint linenums');
        });
    };
    addPrettyfi();
})();
