$(document).ready(function () {

    const colors = ['primary', 'secondary', 'success', 'danger', 'warning', 'info', 'dark'];

    const columnChart = (item) =>{
        $("#chart").html('')
        var options = {
            series: [{
            name: 'Indicators',
            data: item.map((value) => value.indicator_count)
          }],
         
          colors:['#40864b',],
          chart: {
            height: 350,
            type: 'bar',
            toolbar: { show: false },
          },
          plotOptions: {
            bar: {
              borderRadius: 10,
              columnWidth: '50%',
            }
          },
          dataLabels: {
            enabled: false
          },
          stroke: {
            width: 0
          },
          xaxis: {
            labels: {
              rotate: -45
            },
            categories: item.map((name) => name.name_ENG),
            tickPlacement: 'on'
          },
          yaxis: {
            title: {
              text: 'Number of Indicators',
            },
          },
          fill: {
            type: 'gradient',
            gradient: {
              shade: 'light',
              type: "horizontal",
              shadeIntensity: 0.25,
              gradientToColors: undefined,
              inverseColors: true,
              opacityFrom: 0.85,
              opacityTo: 0.85,
              stops: [50, 0, 100]
            },
          }
          };

          var chart = new ApexCharts(document.querySelector("#chart"), options);
          chart.render();
    }
    const topicCard = (topic,color) =>{
        return `
        <div data-id="${topic.id}" name="topic-card" class="col-md-3 col-sm-6">
          <div style="border-radius: 16px;" class="card border-0 shadow-sm p-3">
            <h4 class="fw-bold">${topic.category_count}+</h4>
                <p>${topic.title_ENG}</p>
               <div class="row justify-content-between d-flex align-items-center">

                <div class="col-6">
                  <div style="width: 60px; height: 60px;" class="bg-${color} d-flex flex-column justify-content-center rounded-circle text-center">
                    <i  class="fa fa-${topic?.icon?.split(",")[1]}  h3"></i>
                  </div>
                </div>
                <div class="col-6 text-center">
                  <i style="font-size: 40px;" class="bi text-${color} align-text-bottom bi-bar-chart-line-fill"></i>
                </div>

               </div>
          </div>
        </div>
        `
    }
    const fetchTopicLists = async() =>{
        let url = "/topic_list/";
        let [loading,response] = await useFetch(url);

        let topicLists = response.map((topic) =>{
            let color = colors[Math.floor(Math.random() * colors.length)];
            return topicCard(topic, color)
        })

        $("#topic_list").html(topicLists)

        $("[name='topic-card']").click(async function () {
            let id = $(this).data("id");
            let [loading,category_count_indicator] = await useFetch(`/count_indicator_by_category/${id}/`);
            columnChart(category_count_indicator)
        })
        
    }

    fetchTopicLists()
})