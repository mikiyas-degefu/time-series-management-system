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



  const categoryList = async (id) => {
    let url = `/recent_data_for_topic/${id}`;
    let [loading, response] = await useFetch(url);
    let category_list = response.map((category) => {
      let color = colors[Math.floor(Math.random() * colors.length)];
      return categoryCard(category, color);
    });

    $("#category_list").html(category_list);
  };

  const quarterGraph = (id) => {
    Apex = {
      chart: {
        toolbar: {
          show: false
        }
      },
      tooltip: {
        shared: false
      },
    }

    var optionsYear = {
      chart: {
        id: 'barYear',
        height: 400,
        width: '100%',
        type: 'bar',
      },
      plotOptions: {
        bar: {
          distributed: true,
          horizontal: true,
          endingShape: 'arrow',
          barHeight: '75%',
          dataLabels: {
            position: 'bottom'
          }
        }
      },
      dataLabels: {
        enabled: true,
        textAnchor: 'start',
        style: {
          colors: ['#fff']
        },
        formatter: function(val, opt) {
          return opt.w.globals.labels[opt.dataPointIndex]
        },
        offsetX: 0,
        dropShadow: {
          enabled: true
        }
      },
      colors: colors,
      series: [{
        data: makeData()
      }],
      states: {
        normal: {
          filter: {
            type: 'desaturate'
          }
        },
        active: {
          allowMultipleDataPointsSelection: true,
          filter: {
            type: 'darken',
            value: 1
          }
        }
      },
      tooltip: {
        x: {
          show: false
        },
        y: {
          title: {
            formatter: function(val, opts) {
              return opts.w.globals.labels[opts.dataPointIndex]
            }
          }
        }
      },
      title: {
        text: 'Recent 10 years quarterly performance result',
        offsetX: 15
      },
      subtitle: {
        text: '(Click on year bar to see quarter details)',
        offsetX: 15
      },
      yaxis: {
        labels: {
          show: false
        }
      },
    }
    var yearChart = new ApexCharts(
      document.querySelector("#chart-year"),
      optionsYear
    );
    yearChart.render();
  
    function updateQuarterChart(sourceChart, destChartIDToUpdate) {
      var series = [];
      var seriesIndex = 0;
      var colors = []
      if (sourceChart.w.globals.selectedDataPoints[0]) {
        var selectedPoints = sourceChart.w.globals.selectedDataPoints;
        for (var i = 0; i < selectedPoints[seriesIndex].length; i++) {
          var selectedIndex = selectedPoints[seriesIndex][i];
          var yearSeries = sourceChart.w.config.series[seriesIndex];
          series.push({
            name: yearSeries.data[selectedIndex].x,
            data: yearSeries.data[selectedIndex].quarters
          })
          colors.push(yearSeries.data[selectedIndex].color)
        }
        if (series.length === 0) series = [{
          data: []
        }]
        return ApexCharts.exec(destChartIDToUpdate, 'updateOptions', {
          series: series,
          colors: colors,
          fill: {
            colors: colors
          }
        })
      }
    }
    var optionsQuarters = {
      chart: {
        id: 'barQuarter',
        height: 400,
        width: '100%',
        type: 'bar',
        stacked: true
      },
      plotOptions: {
        bar: {
          columnWidth: '50%',
          horizontal: false
        }
      },
      series: [{
        data: []
      }],
      legend: {
        show: false
      },
      grid: {
        yaxis: {
          lines: {
            show: false,
          }
        },
        xaxis: {
          lines: {
            show: true,
          }
        }
      },
      yaxis: {
        labels: {
          show: false
        }
      },
      title: {
        text: `Quarterly performance results`,
        offsetX: 10
      },
      tooltip: {
        x: {
          formatter: function(val, opts) {
            return opts.w.globals.seriesNames[opts.seriesIndex]
          }
        },
        y: {
          title: {
            formatter: function(val, opts) {
              return opts.w.globals.labels[opts.dataPointIndex]
            }
          }
        }
      }
    }
    var chartQuarters = new ApexCharts(
      document.querySelector("#chart-quarter"),
      optionsQuarters
    )
    chartQuarters.render();
    yearChart.addEventListener('dataPointSelection', function(e, chart, opts) {
      var quarterChartEl = document.querySelector("#chart-quarter");
      var yearChartEl = document.querySelector("#chart-year");
      if (opts.selectedDataPoints[0].length === 1) {
        if (quarterChartEl.classList.contains("active")) {
          updateQuarterChart(chart, 'barQuarter')
        } else {
          yearChartEl.classList.add("chart-quarter-activated")
          quarterChartEl.classList.add("active");
          updateQuarterChart(chart, 'barQuarter')
        }
      } else {
        updateQuarterChart(chart, 'barQuarter')
      }
      if (opts.selectedDataPoints[0].length === 0) {
        yearChartEl.classList.remove("chart-quarter-activated")
        quarterChartEl.classList.remove("active");
      }
    })
    yearChart.addEventListener('updated', function(chart) {
      updateQuarterChart(chart, 'barQuarter')
    })
    document.querySelector("#model").addEventListener("change", function(e) {
      yearChart.updateSeries([{
        data: makeData()
      }])
    })
  }
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
    
     const options = {
        colors: ["#40864b"],
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
    const quarterChartId = `admin_chart_quarter_${category.id}`;
    
    return `
       <h4 class="fw-bold text-${color} text-center">${category.name_ENG}</h4>
        <div class="border border-${color} mt-3 mb-5 rounded shadow">
            <div class="row">
                <div class="col-lg-6">
                    <div id="${yearChartId}"></div>
                </div>
                <div class="col-lg-6">
                    <div id="${quarterChartId}"></div>
                </div>
                
            </div>
            <script>
                var chart_${yearChartId} = new ApexCharts(document.getElementById("${yearChartId}"), ${JSON.stringify(options)});
                chart_${yearChartId}.render();
                var cart_${quarterChartId} = new ApexCharts(document.getElementById("${quarterChartId}"), ${JSON.stringify(options)});
                cart_${quarterChartId}.render();
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
