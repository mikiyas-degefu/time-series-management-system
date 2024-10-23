const size = {
  '50%': 'col-md-6',
  '33%': 'col-md-4',
  '25%': 'col-md-3',
  '100%': 'col-md-12'
}

const bar_horizontal_stacked = () => {

  new ApexCharts(document.querySelector("#bar-chart-4"), {
    chart: { height: 350, type: "bar", stacked: !0, stackType: "100%" },
    plotOptions: { bar: { horizontal: !0 } },
    colors: ["#4680FF", "#13c2c2", "#2CA87F", "#E58A00", "#DC2626"],
    stroke: { width: 1, colors: ["#fff"] },
    series: [
      { name: "Marine Sprite", data: [44, 55, 41, 37, 22, 43, 21] },
      { name: "Striking Calf", data: [53, 32, 33, 52, 13, 43, 32] },
      { name: "Tank Picture", data: [12, 17, 11, 9, 15, 11, 20] },
      { name: "Bucket Slope", data: [9, 7, 5, 8, 6, 9, 4] },
      { name: "Reborn Kid", data: [25, 12, 19, 32, 25, 24, 10] },
    ],
    xaxis: { categories: [2008, 2009, 2010, 2011, 2012, 2013, 2014] },
    tooltip: {
      y: {
        formatter: function (e) {
          return e + "K";
        },
      },
    },
    fill: { opacity: 1 },
    legend: { position: "top", horizontalAlign: "left", offsetX: 40 },
  }).render()
};

const bar_horizontal = (id, component) => {

  const newComponent = component

  newComponent.annual_value.sort((a, b) => {
    if (a.for_datapoint < b.for_datapoint) return -1
    return 1
  })

  const years = Array.from(new Set(newComponent?.annual_value?.map((item) => item.for_datapoint)))
  const data = newComponent.indicator.map((indicator) => {
    let annual = newComponent.annual_value.filter((item) => item.indicator === indicator.id).map((item) => item.performance)
    return {
      name: indicator.title_ENG,
      data: annual
    }
  }
  )
  var options = {
    series: data,
    chart: {
      type: 'bar',
      height: 430
    },
    title: {
      text: newComponent.title
    },
    plotOptions: {
      bar: {
        horizontal: true,
        dataLabels: {
          position: 'top',
        },
      }
    },
    dataLabels: {
      enabled: true,
      offsetX: -6,
      style: {
        fontSize: '12px',
        colors: ['#fff']
      }
    },
    stroke: {
      show: true,
      width: 1,
      colors: ['#fff']
    },
    tooltip: {
      shared: true,
      intersect: false
    },
    xaxis: {
      categories: years,
    },
  };

  var chart = new ApexCharts(document.querySelector(`#${id}`), options);
  chart.render();

};

const bar_stacked = () => {
  // Function logic for bar_stacked
};

const bar = (id, component) => {
  const newComponent = component

  newComponent.annual_value.sort((a, b) => {
    if (a.for_datapoint < b.for_datapoint) return -1
    return 1
  })

  const years = Array.from(new Set(newComponent?.annual_value?.map((item) => item.for_datapoint)))
  const data = newComponent.indicator.map((indicator) => {
    let annual = newComponent.annual_value.filter((item) => item.indicator === indicator.id).map((item) => item.performance)
    return {
      name: indicator.title_ENG,
      data: annual
    }
  })



  new ApexCharts(document.querySelector(`#${id}`), {
    chart: { height: 350, type: "bar" },
    plotOptions: {
      bar: { horizontal: !1, columnWidth: "55%", endingShape: "rounded" },
    },
    dataLabels: { enabled: !1 },
    colors: ["#2CA87F", "#4680FF", "#13c2c2"],
    stroke: { show: !0, width: 2, colors: ["transparent"] },
    series: data,
    title: {
      text: newComponent.title
    },
    xaxis: {
      categories: years,
    },
    fill: { opacity: 1 },
    tooltip: {
      y: {
        formatter: function (e) {
          return "$ " + e + " thousands";
        },
      },
    },
  }).render()
};

const basic_line = () => {
  // Function logic for basic_line
};

const different_line_area = () => {
  // Function logic for different_line_area
};

const mixed_area_line_bar = () => {
  // Function logic for mixed_area_line_bar
};

const mixed_line_bar = () => {
  // Function logic for mixed_line_bar
};

const pie_donut = () => {
  // Function logic for pie_donut
};

const radial_bar_custom_angle = () => {
  // Function logic for radial_bar_custom_angle
};

const radial_bar = () => {
  // Function logic for radial_bar
};

const pie = () => {
  // Function logic for pie
};

const different_line = () => {
  // Function logic for different_line
};

const banner = (id, component) => {
  $(`#${id}`).html(`
      <div class="card welcome-banner bg-blue-900">
          <div class="card-body">
              <div class="row">
                  <div class="col-sm-6">
                      <div class="p-4">
                          <h2 class="text-white">${component?.title}</h2>
                          <p class="text-white">${component?.description}</p>
                      </div>
                  </div>
              </div>
          </div>
      </div>`
)
};

const list_with_category = () => {
  // Function logic for list_with_category
};

const progress_card = () => {
  // Function logic for progress_card
};

const rate_card = () => {
  // Function logic for rate_card
};

const simple_card = () => {
  // Function logic for simple_card
};

const top_list = () => {
  // Function logic for top_list
};


const fetchData = async () => {
  let url = '/dashboard/components/1';
  try {
    const res = await axios.get(url);
    let pc_content = $('#pc-content');
    const rows = res.data.rows.forEach((row) => {
      let col = row.cols.map((component) => {
        return (`<div id="graph-${component.id}" class="${size[component.width]}"></div>`);
      }).join('');

      pc_content.append(`
                <div class="row">
                    ${col}
                </div>`
      );


      row.cols.forEach((component) => {

      let id = `graph-${component.id}`;
      new Function('arg1', 'arg2', component.component + '(arg1 , arg2)')(id, component);


      });

    });
  } catch (error) {
    console.log(error);
  }
}



fetchData();  