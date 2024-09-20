$(document).ready(function () {
  const colors = [
    "primary",
    "secondary",
    "success",
    "danger",
    "warning",
    "info",
    "dark",
  ];



  const getColorHex = (colorClass) => {
    switch (colorClass) {
        case 'primary':
            return '#007bff'; // Example primary color
        case 'secondary':
            return '#6c757d'; // Example secondary color
        case 'success':
            return '#28a745'; // Example success color
        case 'danger':
            return '#dc3545'; // Example danger color
        case 'warning':
            return '#ffc107'; // Example warning color
        case 'info':
            return '#17a2b8'; // Example info color
        case 'dark':
            return '#343a40'; // Example dark color
        default:
            return '#000000'; // Default color (black) or handle unknown cases
    }
};



  const categoryList = async (id) => {
    let url = `/recent_data_for_topic/${id}`;
    let [loading, response] = await useFetch(url);
    let category_list = response.map((category) => {
      let color = colors[Math.floor(Math.random() * colors.length)];
      return categoryCard(category, color);
    });

    $("#category_list").html(category_list);
  };

 

  const topicCard = (topic, color) => {
    return `
    <style>
      .card {
        transition: box-shadow 0.3s;
      }
      
      .card:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 12px rgba(0, 0, 0, 0.3);
        background-color: gray;
        text : white;
      }
    </style>
    <div data-id="${topic.id}" name="topic-card" class="col-md-3 col-sm-6">
      <div style="border-radius: 16px;" class="card border-0 shadow-sm p-3">
        <h4 class="fw-bold">${topic.category_count}+</h4>
        <p>${topic.title_ENG}</p>
        <div class="row justify-content-between d-flex align-items-center">
          <div class="col-6">
            <div style="width: 60px; height: 60px;" class="bg-${color} d-flex flex-column justify-content-center rounded-circle text-center">
              <i class="fa fa-${topic?.icon?.split(",")[1]} h3"></i>
            </div>
          </div>
          <div class="col-6 text-center">
            <i style="font-size: 40px;" class="bi text-${color} align-text-bottom bi-bar-chart-line-fill"></i>
          </div>
        </div>
      </div>
    </div>
    `;
  };


  const categoryCard = (category, color ) => {


     const hexColor = getColorHex(color);
     const options = {
        colors: [hexColor],
        series: [
            {
                name: "Performance",
                data: category.indicators.map((item) => item.annual_data[0].performance),
            },
        ],
        chart: {
            height: 350,
            type: "bar",
            toolbar: {
                show: false,
                offsetX: 0,
                offsetY: 0,
            },
        },
        plotOptions: {
            bar: {
                borderRadius: 10,
                columnWidth: "50%",
            },
        },
        dataLabels: {
            enabled: false,
        },
        stroke: {
            width: 0,
        },
        grid: {
            row: {
                colors: ["#fff", "#f2f2f2"],
            },
        },
        xaxis: {
            labels: {
                rotate: -45,
            },
            categories: category.indicators.map((item) => item.title_ENG),
            tickPlacement: "on",
        },
        yaxis: {
            title: {
                text: "Last 10 Years Performance",
            },
        },
        fill: {
            type: "gradient",
            gradient: {
                shade: "light",
                type: "horizontal",
                shadeIntensity: 0.25,
                gradientToColors: undefined,
                inverseColors: true,
                opacityFrom: 0.85,
                opacityTo: 0.85,
                stops: [50, 0, 100],
            },
        },
    };
    
    const yearChartId = `admin_chart_year_${category.id}`;

    
    return `
       <h4 class="fw-bold text-${color} text-center">${category.name_ENG}</h4>
        <div class="border border-${color} mt-3 mb-5 rounded shadow">
            <div class="row">
                <div class="col-lg-6">
                    <div id="${yearChartId}"></div>
                </div>

               
              
                
            </div>
            <script>
                var chart_${yearChartId} = new ApexCharts(document.getElementById("${yearChartId}"), ${JSON.stringify(options)});
                chart_${yearChartId}.render();
                
            </script>
        </div>
    `;
    };


  const fetchTopicLists = async () => {
    let url = "/topic_list/";
    let [loading, response] = await useFetch(url);

    let topicLists = response.map((topic) => {
      let color = colors[Math.floor(Math.random() * colors.length)];
      return topicCard(topic, color);
    });

    $("#topic_list").html(topicLists);

    $("[name='topic-card']").click(async function () {
      let id = $(this).data("id");
      categoryList(id);
    });
  };

  fetchTopicLists();
});
