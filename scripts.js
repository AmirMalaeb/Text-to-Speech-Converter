var API_ENDPOINT = "your API endpoint URL goes here";

$(document).ready(function() {
    $("#sayButton").click(function() {
        var inputData = {
            "voice": $('#voiceSelected').val(),
            "text": $('#postText').val()
        };

        $.ajax({
            url: API_ENDPOINT,
            type: 'POST',
            data: JSON.stringify(inputData),
            contentType: 'application/json; charset=utf-8',
            success: function(response) {
                console.log('Response:', response);
                $("#postIDText").text("Post ID: " + response);
                $("#postIDreturned").css("visibility", "visible");
            },
            error: function() {
                alert("Error in posting data");
            }
        });
    });

    $("#searchButton").click(function() {
        var postId = $('#postId').val();

        $.ajax({
            url: API_ENDPOINT + '?postId=' + postId,
            type: 'GET',
            success: function(response) {
                console.log('Search response:', response);
                $('#posts tbody').empty();

                $.each(response, function(i, data) {
                    var player = data['url'] ? "<audio controls><source src='" + data['url'] + "' type='audio/mpeg'></audio>" : "";
                    $("#posts tbody").append("<tr> \
                        <td>" + data['id'] + "</td> \
                        <td>" + data['voice'] + "</td> \
                        <td>" + data['text'] + "</td> \
                        <td>" + player + "</td> \
                    </tr>");
                });
            },
            error: function() {
                alert("Error in fetching data");
            }
        });
    });

    $("#postText").on('input', function() {
        var length = $(this).val().length;
        $("#charCounter").text("Characters: " + length);
    });

    $("#copyButton").click(function() {
        var postIDText = $("#postIDText").text().replace("Post ID: ", "");
        var tempInput = $("<input>");
        $("body").append(tempInput);
        tempInput.val(postIDText).select();
        document.execCommand("copy");
        tempInput.remove();
        alert("Post ID copied to clipboard");
    });
});