$(document).ready(function () {

    const colors = ['primary', 'secondary', 'success', 'danger', 'warning', 'info', 'dark'];

    const annualTable = (indicatorValue) =>{
        $("#annualTable").html('')
        console.log(indicatorValue)
        let table = `
        <div class="p-5 rounded bg-white">
            <p>Annual Table</p>
            
            ${indicatorValue.categories.map((category) =>{
                let filterIndicator = indicatorValue.indicators.filter((indicator) => indicator.for_category.includes(category.id));
                let years = indicatorValue.years.map((year) => ` <th style="width:100px;  scope="col">${year.year_EC}</th>` ).join("")
                let indicatorLists = filterIndicator.map((indicator) => {

                    let value = indicatorValue.years.map((year) =>{
                        let getValue = indicatorValue.annualData.find((data) => data.for_datapoint == year.id && data.indicator == indicator.id)
                        return ` <td class="text-danger text-center">${getValue ? getValue.performance : ' - '}</td>`
                    }).join("")

                    return `
                    <tr>
                        <td class="text-success fw-bold text-start">${indicator.title_ENG} <a href="#"><i class="fa fa-eye float-end "></i></a> </td>
                        <td class="text-success fw-bold text-start">${indicator.title_AMH}</td>
                        ${value}
                     </tr>
                    `
                    
                    
                }).join("")
                return `
                <div class="table-responsive m-3">
                    <button 
                      id="btnDownloadExcel"
                      onclick="tableToExcel('yearData${category.id}', 'yearData${category.id}', 'yearData${category.id}.xls');" 
                      type="button" 
                      class="btn btn-success mb-2 float-end">
                      <i class="bi bi-download"></i>
                    </button>
                    <table id="yearData${category.id}" class="m-0 p-0 table table-bordered table-hover"  style="table-layout: fixed;" >
                        <thead  name="tableHead">

                             <tr style="background-color: #40864b;" >
                                  <th style="width:500px;"  class="text-light" scope="col" >Yearly</th>
                                  <th style="width:500px;"  scope="col"></th>
                                  ${indicatorValue.years.map((year) => ` <th style="width:100px;  scope="col"></th>` ).join("")}
                            </tr>
                           
                            <tr style="background-color: #9fdfa9;" >
                              <th  scope="col">Indicator (English)</th>
                              <th  scope="col">Indicator (Amharic)</th>
                              ${years}
                            </tr>
                        </thead >
                        <tbody name="tableBody">
                          ${indicatorLists ? indicatorLists : `<tr><td colspan="${indicatorValue.years.length + 2}" class="text-danger text-center" >No data.</td></tr>`}
                        </tbody>
                     </table>
                </div>
                `
            }).join('')}
        </div>
        `

        $("#annualTable").html(table)
    }

    const multiSelectForm = (htmlId) =>{
        //multi select
        new MultiSelectTag(htmlId, {
            rounded: false, // default true
            placeholder: "Search Category", // default Search...
            onChange: function (values) {
              console.log(values);
            },
          });
    }

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

    const categoryFilter = (items) =>{
        $("#filter_category").html('')
        let catFilterHtml = `
            <hr>
            <div class="p-5 rounded bg-white">
              <p>Filter Category</p>
              <form id="filterCategoryForm">
                <div class="d-flex">
                    <select required id="id_for_category" class="form-select me-2" multiple aria-label="multiple select example">
                    ${items.map((item) => `<option value="${item.id}">${item.name_ENG}</option>` )}
                    </select>
                    <button class="btn btn-outline-success ms-3" type="submit">Filter</button>
                </div>
              </form>
            </div>
        `
        $("#filter_category").html(catFilterHtml)

        $("#filterCategoryForm").on('submit', async function(e) {
            e.preventDefault()

            let values = $("#id_for_category").val().join(" ,");

            let [indicatorLoading,indicatorValue] = await useFetch(`/filter_by_category_with_value/?category=${values}`);
            annualTable(indicatorValue, values.split(" ,"))

           
        })
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
            columnChart(category_count_indicator) // column chart
            categoryFilter(category_count_indicator) //filter category 
            multiSelectForm('id_for_category') //activate multi select style
        })   
        
        
        
    
    }


   

    fetchTopicLists()

   

   
})