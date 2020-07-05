function get_prediction(text) {
  $.ajax({
    type: "POST",
    contentType: "application/json; charset=utf-8",
    url: "/predict",
    data: JSON.stringify({
      tweet: text,
    }),

    success: function (data) {
      draw(data.response);
      //$("#tweet").val("");
    },
    error: function (e) {
      console.log("jQuery error message = " + e.message);
      //$("#tweet").val("");
    },
  });
}

function draw(resp) {
  var ctx = document.getElementById("myChart").getContext("2d");
  var sentiments = resp.sentiment;
  var labels = [];
  var values = [];
  console.log(sentiments);
  for (var key in sentiments) {
    labels.push(key);
    values.push(sentiments[key]);
  }
  console.log(labels, values);

  var chart = new Chart(ctx, {
    type: "pie",
    data: {
      datasets: [
        {
          data: values,
          backgroundColor: [
            "rgb(214, 69, 65)",
            "rgb(191, 191, 191)",
            "rgb(63, 195, 128)",
          ],
          label: "Sentiment Probability",
        },
      ],
      labels: labels,
    },
    options: {},
  });
}
$(document).ready(() => {
  $("#submit-tweet").attr("disabled", true);
  $("#tweet").keyup(function () {
    if ($(this).val.length != 0) {
      $("#submit-tweet").attr("disabled", false);
    }
  });

  $("#submit-tweet").click(() => {
    let tweet = $("#tweet").val();
    console.log("submitting tweet for " + tweet);

    get_prediction(tweet);
  });
});
