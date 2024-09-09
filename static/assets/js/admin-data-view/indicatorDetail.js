$(document).ready(function () {
    let urlPath = window.location.pathname;
    let pathID = urlPath.replace("/user-admin/data_view_indicator_detail/", "").replace("/", "");
    let URL = `/filter_indicator_detail_annual_value/${pathID}`

    const indicatorId = [pathID]


    const contractTable = (data) =>{
        AnnualTable(data)
    }

    const AnnualTable = (data) =>{

        //table header
        $("#tableHead").html(
            `<th scope="col" style="width:450px;">Name</th>
            <th scope="col" style="width:400px;">ስም</th>
            ` +
            data.year.map((year) =>{
            return `
            <th scope="col" style="width:100px;">${year.year_EC} E.C </th>
            `
        }))


         let tableData = indicatorId.map((indicator_id) =>{
            let filterIndicator = data.annual_data_value.filter((item) => item.indicator__id === Number(indicator_id))
            
            //parent indicator
            let row = data.year.map((year) =>{
                let getIndicatorValue = filterIndicator.find((item) => item.for_datapoint__year_EC == year.year_EC)
                if (getIndicatorValue){
                    return `
                    <td>
                        <button 
                            id="${indicator_id}-${year.year_EC}"
                            data-indicator-id="${indicator_id}" 
                            data-value="${getIndicatorValue.performance}" 
                            data-year="${year.year_EC}"
                            data-bs-toggle="modal" 
                            name="btnIndicator" 
                            data-bs-target="#indicatorEditValue" 
                            class="btn btn-block btn-outline-secondary border-0 fw-bold text-dark">
                            ${getIndicatorValue.performance}
                        </button>
                    </td>
                    `
                }else{
                    return `
                    <td>
                        <button 
                            id="${indicator_id}-${year.year_EC}"
                            data-indicator-id="${indicator_id}"
                            data-year="${year.year_EC}" 
                            data-value="" 
                            data-bs-toggle="modal" 
                            name="btnIndicator" 
                            data-bs-target="#indicatorEditValue" 
                            class="btn btn-block btn-outline-secondary border-0 fw-bold text-dark">
                             - 
                        </button>
                    </td>`
                }
            })

            //child indicator
            let filterChildIndicator = data.annual_data_value.filter(item => item.indicator__parent_id === Number(indicator_id))
            let uniqueChildId = []
            filterChildIndicator.map((item) =>{
                if (!uniqueChildId.includes(item.indicator__id)){
                    uniqueChildId.push(item.indicator__id)
                }
            })

            let childDataFn = (parent, space="&nbsp;&nbsp;&nbsp;&nbsp&nbsp;&nbsp;&nbsp;&nbsp") =>{

                //child of child indicator
                let filterChildOfIndicator = data.annual_data_value.filter(item => item.indicator__parent_id === Number(parent))
                let uniqueChildOfChildId = []
                filterChildOfIndicator.map((item) =>{
                    if (!uniqueChildOfChildId.includes(item.indicator__id)){
                        uniqueChildOfChildId.push(item.indicator__id)
                    }
                })

                return uniqueChildOfChildId.map((child_id) =>{
                    let filterChildOfChildIndicator = data.annual_data_value.filter((item) => item.indicator__id === Number(child_id))
                    let childRow = data.year.map((year) =>{
                        let getIndicatorValue = filterChildOfChildIndicator.find((item) => item.for_datapoint__year_EC == year.year_EC)
                        if (getIndicatorValue){
                            return `
                            
                            <td>
                                <button
                                    id="${child_id}-${year.year_EC}" 
                                    data-indicator-id="${child_id}" 
                                    data-value="${getIndicatorValue.performance}" 
                                    data-year="${year.year_EC}"
                                    data-bs-toggle="modal" 
                                    name="btnIndicator" 
                                    data-bs-target="#indicatorEditValue" 
                                    class="btn btn-block btn-outline-secondary border-0 fw-bold text-dark">
                                    ${getIndicatorValue.performance}
                                </button>
                            </td>
                            `
                        }else{
                            return `
                            <td>
                                <button 
                                    id="${child_id}-${year.year_EC}" 
                                    data-indicator-id="${child_id}" 
                                    data-year="${year.year_EC}"
                                    data-value="" 
                                    data-bs-toggle="modal" 
                                    name="btnIndicator" 
                                    data-bs-target="#indicatorEditValue" 
                                    class="btn btn-block btn-outline-secondary border-0 fw-bold text-dark">
                                    -
                                </button>
                            </td>`
                        }
                    })
    
                    return  `
                    <tr>
                        <td>
                           <div class="row">
                                <div class="col-10">&nbsp;&nbsp;&nbsp;&nbsp ${space}  ${filterChildOfIndicator[0].indicator__title_ENG}</div>
                                   <div class="col-1">
                                     <button 
                                         type="button" 
                                         name="btnAddIndicator" 
                                         data-indicator-id="${child_id}" 
                                         data-bs-toggle="modal" 
                                         data-bs-target="#modalAddNewIndicator" 
                                         class="btn btn-outline-primary border-0  pt-1 pb-1" 
                                         data-bs-placement="bottom" 
                                         title="Add new Sub-Indicator">+</button> 
                                   </div>
                                   <div class="col-1">
                                     <button 
                                         type="button" 
                                         name="btnDeleteIndicator" 
                                         data-indicator-id="${child_id}"
                                         data-indicator-name="${filterChildOfIndicator[0].indicator__title_ENG}" 
                                         data-bs-toggle="modal" 
                                         data-bs-target="#modalRemoveIndicator" 
                                         class="btn btn-outline-danger border-0  pt-1 pb-1" 
                                         data-bs-placement="bottom" 
                                         title="Remove Indicator">-</button> 
                                   </div>
                                </div>
                         </td>
                       <td class="">${space}  ${filterChildOfIndicator[0].indicator__title_AMH}</td> 
                       ${childRow}
                    </tr>
                ${space += String("&nbsp;&nbsp;&nbsp;&nbsp")}
                ${childDataFn(filterChildOfChildIndicator[0].indicator__id, space)}
                `
                })
            }

            let childData = uniqueChildId.map((child_id) =>{
                let filterChildIndicator = data.annual_data_value.filter((item) => item.indicator__id === Number(child_id))
                let childRow = data.year.map((year) =>{
                    let getIndicatorValue = filterChildIndicator.find((item) => item.for_datapoint__year_EC == year.year_EC)
                    if (getIndicatorValue){
                        return `
                        <td>
                            <button
                                id="${child_id}-${year.year_EC}"  
                                data-indicator-id="${child_id}" 
                                data-value="${getIndicatorValue.performance}" 
                                data-year="${year.year_EC}"
                                data-bs-toggle="modal" 
                                name="btnIndicator" 
                                data-bs-target="#indicatorEditValue" 
                                class="btn btn-block btn-outline-secondary border-0 fw-bold text-dark">
                                ${getIndicatorValue.performance}
                            </button>
                        </td>
                        `
                    }else{
                        return `
                        <td> 
                            <button
                                id="${child_id}-${year.year_EC}"  
                                data-indicator-id="${child_id}" 
                                data-year="${year.year_EC}"
                                data-value="" 
                                data-bs-toggle="modal" 
                                name="btnIndicator" 
                                data-bs-target="#indicatorEditValue" 
                                class="btn btn-block btn-outline-secondary border-0 fw-bold text-dark">
                                - 
                            </button>
                        </td>`
                    }
                })

                return  `
                <tr>
                    <td class="">
                        <div class="row">
                         <div class="col-10">&nbsp;&nbsp;&nbsp;&nbsp ${filterChildIndicator[0].indicator__title_ENG}</div>
                            <div class="col-1">
                              <button 
                                  type="button" 
                                  name="btnAddIndicator" 
                                  data-indicator-id="${child_id}"
                                  data-bs-toggle="modal" 
                                  data-bs-target="#modalAddNewIndicator" 
                                  class="btn btn-outline-primary border-0  pt-1 pb-1" 
                                  data-bs-placement="bottom" 
                                  title="Add new Sub-Indicator">+</button> 
                            </div>
                            <div class="col-1">
                              <button 
                                  type="button" 
                                  name="btnDeleteIndicator" 
                                  data-indicator-id="${child_id}"
                                  data-indicator-name="${filterChildIndicator[0].indicator__title_ENG}"
                                  data-bs-toggle="modal" 
                                  data-bs-target="#modalRemoveIndicator" 
                                  class="btn btn-outline-danger border-0  pt-1 pb-1" 
                                  data-bs-placement="bottom" 
                                  title="Remove Indicator">-</button> 
                            </div>
                         </div>
                    </td>
               <td class="">&nbsp;&nbsp;&nbsp;&nbsp ${filterChildIndicator[0].indicator__title_AMH}</td> 
               ${childRow}
            </tr>
            ${childDataFn(filterChildIndicator[0].indicator__id)}
            `
            })

            

            return  `
            <tr>
                <td class="fw-bold">
                     <div class="row">
                      <div class="col-10">${filterIndicator[0].indicator__title_ENG}</div>
                      <div class="col-1">
                        <button 
                            type="button" 
                            name="btnAddIndicator" 
                            data-indicator-id="${indicatorId}"
                            data-bs-toggle="modal" 
                            data-bs-target="#modalAddNewIndicator" 
                            class="btn btn-outline-primary border-0  pt-1 pb-1" 
                            data-bs-placement="bottom" 
                            title="Add new Sub-Indicator">+</button> 
                      </div>
                      <div class="col-1">
                        <button 
                            type="button" 
                            name="btnDeleteIndicator" 
                            data-indicator-id="${indicatorId}"
                            data-indicator-name="${filterIndicator[0].indicator__title_ENG}"
                            data-bs-toggle="modal" 
                            data-bs-target="#modalRemoveIndicator" 
                            class="btn btn-outline-danger border-0  pt-1 pb-1" 
                            data-bs-placement="bottom" 
                            title="Remove Indicator">-</button> 
                      </div>
                    </div>
                </td>
               <td class="fw-bold">${filterIndicator[0].indicator__title_AMH}</td> 
               ${row}
            </tr>
            ${childData}
            `
           
        })

        $("#tableBody").html(tableData)
    }

    const fetchTableData = async() =>{
        let [loading, response] = await useFetch(URL)
        contractTable(response)
    }


    //handle value button clicked
    $("#tableBody").on("click","button[name='btnIndicator']",function(){
        const buttonData = $(this).data()
        $("#IndicatorFormValue").val(buttonData.value)
        $("#form_indicator_id").val(buttonData.indicatorId)
        $("#form_year_id").val(buttonData.year)
    })

    //handle add indicator button clicked
    $("#tableBody").on("click","button[name='btnAddIndicator']",function(){
        const buttonData = $(this).data()
        $("#form_indicator_add_id").val(buttonData.indicatorId)
    })

    fetchTableData()

})