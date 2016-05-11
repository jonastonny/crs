
var chart = new Chartist.Bar('.ct-chart', {
        labels: [],
        series: []
    }, {
        low: 0,
        axisY: {
            onlyInteger: true
        },
        distributeSeries: true
    }
);

$.ajax({
    url: $('#data-url').val(),
    method: 'POST'
}).done(function(data){
    chart.update(data.data);
});


// Enable pusher logging - don't include this in production
Pusher.log = function(message) {
    if (window.console && window.console.log) {
        window.console.log(message);
    }
};
var pusher = new Pusher('52b285639f1c7195cfac', {
    encrypted: true
});
var channel = pusher.subscribe('crs');
var event = $("#event:hidden").val();
channel.bind(event, function(data) {
    var divs = $(".answer-box");
    divs.each(function(index, value){
        var answerId = parseInt($(value).attr('id'));
        var answer_count = data.data[answerId] ? data.data[answerId].answer_count : 0;
        $(value).text(answer_count);
    });
    $("#response-count").text(data.data.total_responses);
    chart.update(data.data);
});

$("#toggle-answer").click(function(){
    setTimeout(function(){
        chart.update();
    }, 600);
});