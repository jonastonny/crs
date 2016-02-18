/**
 * Created by jtn on 18/02/16.
 */
(function() {
    var addPrettyfi = function() {
        var pre = $('pre');
        pre.each(function() {
            $(pre).addClass('prettyprint');
        });
        var code = $('code');
        code.each(function() {
           $(code).addClass('prettyprint');
        });
    };
    addPrettyfi();
})();

