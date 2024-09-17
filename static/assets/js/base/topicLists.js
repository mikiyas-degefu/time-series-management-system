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

  // const annualTable = (indicatorValue) =>{
  //     $("#annualTable").html('')
  //     console.log(indicatorValue)
  //     let table = `
  //     <div class="p-5 rounded bg-white">
  //         <p>Annual Table</p>

  //         ${indicatorValue.categories.map((category) =>{
  //             let filterIndicator = indicatorValue.indicators.filter((indicator) => indicator.for_category.includes(category.id));
  //             let years = indicatorValue.years.map((year) => ` <th style="width:100px;  scope="col">${year.year_EC}</th>` ).join("")
  //             let indicatorLists = filterIndicator.map((indicator) => {

  //                 let value = indicatorValue.years.map((year) =>{
  //                     let getValue = indicatorValue.annualData.find((data) => data.for_datapoint == year.id && data.indicator == indicator.id)
  //                     return ` <td class="text-danger text-center">${getValue ? getValue.performance : ' - '}</td>`
  //                 }).join("")

  //                 return `
  //                 <tr>
  //                     <td class="text-success fw-bold text-start">${indicator.title_ENG} <a href="/indicator_detail_view/${indicator.id}"><i class="fa fa-eye float-end "></i></a> </td>
  //                     <td class="text-success fw-bold text-start">${indicator.title_AMH}</td>
  //                     ${value}
  //                  </tr>
  //                 `

  //             }).join("")
  //             return `
  //             <div class="table-responsive m-3">
  //                 <button
  //                   id="btnDownloadExcel"
  //                   onclick="tableToExcel('yearData${category.id}', 'yearData${category.id}', 'yearData${category.id}.xls');"
  //                   type="button"
  //                   class="btn btn-success mb-2 float-end">
  //                   <i class="bi bi-download"></i>
  //                 </button>

  //                 <table id="yearData${category.id}" class="m-0 p-0 table table-bordered table-hover"  style="table-layout: fixed;" >
  //                     <thead  name="tableHead">

  //                           <tr style="background-color: #40864b;" >
  //                               <th style="width:500px;"  class="text-light" scope="col" >${category.name_ENG}</th>
  //                               <th style="width:500px;"  scope="col"></th>
  //                               ${indicatorValue.years.map((year) => ` <th style="width:100px;  scope="col"></th>` ).join("")}
  //                           </tr>

  //                         <tr style="background-color: #9fdfa9;" >
  //                           <th  scope="col">Indicator (English)</th>
  //                           <th  scope="col">Indicator (Amharic)</th>
  //                           ${years}
  //                         </tr>
  //                     </thead >
  //                     <tbody name="tableBody">
  //                       ${indicatorLists ? indicatorLists : `<tr><td colspan="${indicatorValue.years.length + 2}" class="text-danger text-center" >No data.</td></tr>`}
  //                     </tbody>
  //                  </table>
  //             </div>
  //             `
  //         }).join('')}
  //     </div>
  //     `

  //     $("#annualTable").html(table)
  // }

  // const multiSelectForm = (htmlId) =>{
  //     //multi select
  //     new MultiSelectTag(htmlId, {
  //         rounded: false, // default true
  //         placeholder: "Search Category", // default Search...
  //         onChange: function (values) {
  //           console.log(values);
  //         },
  //       });
  // }

  // const columnChart = (item) =>{
  //     $("#chart").html('')
  //     var options = {
  //         series: [{
  //         name: 'Indicators',
  //         data: item.map((value) => value.indicator_count)
  //       }],

  //       colors:['#40864b',],
  //       chart: {
  //         height: 350,
  //         type: 'bar',
  //         toolbar: { show: false },
  //       },
  //       plotOptions: {
  //         bar: {
  //           borderRadius: 10,
  //           columnWidth: '50%',
  //         }
  //       },
  //       dataLabels: {
  //         enabled: false
  //       },
  //       stroke: {
  //         width: 0
  //       },
  //       xaxis: {
  //         labels: {
  //           rotate: -45
  //         },
  //         categories: item.map((name) => name.name_ENG),
  //         tickPlacement: 'on'
  //       },
  //       yaxis: {
  //         title: {
  //           text: 'Number of Indicators',
  //         },
  //       },
  //       fill: {
  //         type: 'gradient',
  //         gradient: {
  //           shade: 'light',
  //           type: "horizontal",
  //           shadeIntensity: 0.25,
  //           gradientToColors: undefined,
  //           inverseColors: true,
  //           opacityFrom: 0.85,
  //           opacityTo: 0.85,
  //           stops: [50, 0, 100]
  //         },
  //       }
  //       };

  //       var chart = new ApexCharts(document.querySelector("#chart"), options);
  //       chart.render();
  // }

  // const categoryFilter = (items) =>{
  //     $("#filter_category").html('')
  //     let catFilterHtml = `
  //         <hr>
  //         <div class="p-5 mb-5 rounded bg-white">
  //           <p>Filter Category</p>
  //           <form id="filterCategoryForm" style="padding-bottom: 100px;">
  //             <div class="d-flex">
  //                 <select required id="id_for_category" class="form-select me-2" multiple aria-label="multiple select example">
  //                 ${items.map((item) => `<option value="${item.id}">${item.name_ENG}</option>` )}
  //                 </select>
  //                 <button class="btn btn-outline-success ms-3" type="submit">Filter</button>
  //             </div>
  //           </form>
  //         </div>
  //     `
  //     $("#filter_category").html(catFilterHtml)

  //     $("#filterCategoryForm").on('submit', async function(e) {
  //         e.preventDefault()

  //         let values = $("#id_for_category").val().join(" ,");

  //         let [indicatorLoading,indicatorValue] = await useFetch(`/filter_by_category_with_value/?category=${values}`);
  //         annualTable(indicatorValue, values.split(" ,"))

  //     })
  // }

  const yearGraph = (id) => {
    axios
      .get(`/indicator_graph/${id}`)
      .then((response) => {
        const data = response.data;
        const annualData = data.annual_data_value.map((item) => ({
          year: item.for_datapoint__year_EC,
          performance: item.performance,
        }));

        // Update the chart with the fetched data
        const options = {
          colors: ["#40864b"],
          series: [
            {
              name: "Performance",
              data: annualData.map((item) => item.performance),
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
            categories: annualData.map((item) => item.year),
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

        const chart = new ApexCharts(document.querySelector("#admin-chart-year"), options);
        chart.render();

        const monthData = data.month_data_value.map((item) => ({
          month: item.for_month__number,
          year: item.for_datapoint__year_EC,
          performance: item.performance,
        }));
        console.log(data);

        // Create month-year combinations for x-axis categories
        const categories = monthData.map(
          (item) => `${item.month}/2/${item.year}`
        );
        console.log(categories);

        const optionsMonth = {
          colors: ["#40864b"],
          series: [
            {
              name: "Performance",
              data: monthData.map((item) => item.performance),
            },
          ],
          chart: {
            height: 350,
            type: "line",
          },
          forecastDataPoints: {
            count: 10,
          },
          stroke: {
            width: 5,
            curve: "smooth",
          },
          xaxis: {
            type: "datetime",
            categories: categories,
            tickAmount: 10,
            labels: {
              formatter: function (value, timestamp, opts) {
                return opts.dateFormatter(new Date(timestamp), "dd MMM");
              },
            },
          },
          title: {
            text: "Recent year month performance",
            align: "left",
            style: {
              fontSize: "16px",
              color: "#666",
            },
          },
          fill: {
            type: "gradient",
            gradient: {
              shade: "dark",
              gradientToColors: ["#FDD835"],
              shadeIntensity: 1,
              type: "horizontal",
              opacityFrom: 1,
              opacityTo: 1,
              stops: [0, 100, 100, 100],
            },
          },
        };

        var chartMonth = new ApexCharts(
          document.querySelector("#admin-chart-month"),
          optionsMonth
        );
        chartMonth.render();
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  };

  const quarterGraph = (id) => {
    async function fetchData(id) {
      try {
          const response = await axios.get(`/indicator_graph/${id}`, {
              headers: {
                  'Content-Type': 'application/json'
              }
          });
  
          return response.data;
      } catch (error) {
          console.error('Error:', error);
      }
  }

  fetchData(id)
      .then((data) => {

          function makeData() {
              // Group quarter data by year
              var yearData = data.quarter_data_value.reduce((acc, curr) => {
                  var year = curr.for_datapoint__year_EC;
                  if (!acc[year]) {
                      acc[year] = [];
                  }
                  acc[year].push(curr);
                  return acc;
              }, {});
          
              
          
              // Map grouped data to the final structure
              var dataYearSeries = Object.keys(yearData).map(year => {
                  var yearPerformance = yearData[year].reduce((sum, item) => sum + item.performance, 0);
          
                  var quarters = yearData[year].map(item => ({
                      x: `Q${item.for_quarter__number}`,
                      y: item.performance
                  }));
          
                  return {
                      x: year,
                      y: yearPerformance,
                      color: getRandomColor(colors),
                      quarters: quarters
                  };
              });
          
              return dataYearSeries;
          }
          
         var colors = ['#FF5733', '#33FF57', '#3357FF', '#FF3357', '#57FF33', '#5733FF'];
          function getRandomColor(colors) {
              return colors[Math.floor(Math.random() * colors.length)];
          }

          
         
          var result = makeData();
         
          

          

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

      })
      .catch((error) => {
          console.error('Error:', error);
      });
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
      yearGraph(199); // year and month chart
      quarterGraph(199); // quarter chart
    });
  };

  fetchTopicLists();
});
