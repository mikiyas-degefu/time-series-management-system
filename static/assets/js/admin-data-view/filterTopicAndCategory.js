$(document).ready(function () {
    let URL = "/filter_topic_and_category";
    let indicatorId = [];  //selected indicator ids
    const LOADING_HTML = `
    <div class="d-flex justify-content-center">
        <div class="spinner-border" role="status">
           <span class="visually-hidden">Loading...</span>
        </div>
    </div>
    `

    //request indicator Annual values
    $('#applyFilterButton').on('click', function(){
        $("#tableBody").html(
            `
            <tr>
                <td colspan="7"></td>
            </tr>
            `
        )
        fetchTableData()
    })

    const fetchTableData = async () => {
        const params = new URLSearchParams();
        params.set('indicator_ids', indicatorId.join(','));
        const url = '/filter_indicator_annual_value/?' + params.toString();

        $("#tableLoader").html(LOADING_HTML)

        let response = await axios.get(url)
        try{
            contractAnnualTable(response.data)
        }catch(error){
            console.error("Error:", error);
        }
        $("#tableLoader").html("")
    }


    const handleButton = (state) => {
        $('#applyFilterButton').attr("disabled", state);
        state ? $('#applyFilterButton').html(`Select indicator`) : $('#applyFilterButton').html(`Apply`)
    }

    const handleIndicator = async (catId) => {
        $("#indicatorListParent").html(LOADING_HTML)
        let [loading,response] = await useFetch(`/filter_indicator_by_category/${catId}`);
        let indicators = response.indicators

        const selectAllHtml = `
         <div>
            <input type="checkbox"  name="selectAllIndicator" id="selectAllIndicator">
            <label for="selectAllIndicator" class="ms-2">Select All</label>
            <hr />
        </div>
        
        `

        const indicatorLists = indicators.map((item) =>{
            return`
            <div class="col-1"> 
               <input type="checkbox" value="${item.id}" name="indicator_lists" id="indicator_list${item.id}">
            </div>
             <div class="col-11">
                 <label for="indicator_list${item.id}" style="font-size: small;" class="mb-0">${item.title_ENG} - ${item.title_AMH}</label>
             </div>           
        `
        })

        $("#indicatorListParent").html(indicatorLists.length > 0 ? selectAllHtml + indicatorLists.join("") : `<p class="text-danger text-center">No indicator found!</p>`)
         //handle indicator on change
         $("#indicatorListParent").on('change', function(){
            indicatorId = []
            $(this).find('input[name="indicator_lists"]:checked').each(function(){
                indicatorId.push($(this).val())
                $("#selectAllIndicator").attr('checked', false)
            });

            //select all if select all button clicked
            if($("#selectAllIndicator").is(':checked')){
                indicatorId = []
                $(this).find('input[name="indicator_lists"]').prop('checked', true)
                $(this).find('input[name="indicator_lists"]:checked').each(function(){
                    indicatorId.push($(this).val())
                    $("#selectAllIndicator").attr('checked', false)
                });
                handleButton(false, indicatorId)
            }
            //handle button
            handleButton(false, indicatorId)
        })
    }

    const handleTopic = (topics) =>{
        const topicLists = topics.map((item) =>{
            return`
            <div class="col-1"> 
                <input type="radio" value="${item.id}" name="topic_lists" id="topic_list${item.id}">
            </div>
            <div class="col-11">
                <label for="topic_list${item.id}" style="font-size: small;" class="mb-0">${item.title_ENG} - ${item.title_AMH}</label>
            </div>           
            `
        })
        $("#topicListParent").html(topicLists)
    }

    const handleCategory = (category, topic_id) => {
        const filterCategory = category.filter((item) => item.topic__id === Number(topic_id))
        const categoryLists = filterCategory.map((item) =>{
            return`
            <div class="col-1"> 
               <input type="radio" value="${item.id}" name="category_lists" id="category_list${item.id}">
            </div>
             <div class="col-11">
                 <label for="category_list${item.id}" style="font-size: small;" class="mb-0">${item.name_ENG} - ${item.name_AMH}</label>
             </div>           
        `
        })

        $("#categoryListParent").html(categoryLists.length > 0 ? categoryLists : `<p class="text-danger text-center">No category found!</p>`)
        
        //handle topic on change
        $("#categoryListParent").on('change', function(){
            let categoryId = $(this).find('input[name="category_lists"]:checked').val();
            handleIndicator(categoryId)
            handleButton(true)
        })


    }


    const handleAccordion = (data) => {
        handleTopic(data.topics)
        //handle topic on change
        $("#topicListParent").on('change', function(){
            //handle topic on change and clear indicator
            $("#indicatorListParent").html(`<p class="text-danger text-center">Please Select Category</p>`)
            let topic_id = $(this).find('input[name="topic_lists"]:checked').val();
            handleButton(true)
            handleCategory(data.categories, topic_id)
        })
    }

    const fetchTopicAndCategory = async() => {

        $("#topicListParent").html(LOADING_HTML)
        let [loading,response] = await useFetch(URL);
        loadingTopic = loading
        handleAccordion(response)

    }

    fetchTopicAndCategory()




    /// Table
    const contractAnnualTable = (data) => {
        $("#tableHead").html(
            `<th scope="col" style="width:400px;">Name</th>
            <th scope="col" style="width:400px;">ስም</th>
            ` +
            data.year.map((year) =>{
            return `
            <th scope="col" style="width:100px;">${year.for_datapoint__year_EC} E.C </th>
            `
        }))


        let tableData = indicatorId.map((indicator_id) =>{
            let filterIndicator = data.annual_data_value.filter((item) => item.indicator__id === Number(indicator_id))
            
            //parent indicator
            let row = data.year.map((year) =>{
                let getIndicatorValue = filterIndicator.find((item) => item.for_datapoint__year_EC == year.for_datapoint__year_EC)
                if (getIndicatorValue){
                    return `
                    <td>${getIndicatorValue.performance}</td>
                    `
                }else{
                    return `<td> - </td>`
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
                        let getIndicatorValue = filterChildOfChildIndicator.find((item) => item.for_datapoint__year_EC == year.for_datapoint__year_EC)
                        if (getIndicatorValue){
                            return `
                            <td>${getIndicatorValue.performance}</td>
                            `
                        }else{
                            return `<td> - </td>`
                        }
                    })
    
                    return  `
                <tr>
                   <td class="">${space}  ${filterChildOfIndicator[0].indicator__title_ENG}</td> 
                   <td class="">${space}  ${filterChildOfIndicator[0].indicator__title_AMH}</td> 
                   ${childRow}
                </tr>
                ${space += String("&nbsp;&nbsp;&nbsp;&nbsp")}
                ${childDataFn(filterChildOfChildIndicator[0].indicator__id)}
                `
                })
            }

            let childData = uniqueChildId.map((child_id) =>{
                let filterChildIndicator = data.annual_data_value.filter((item) => item.indicator__id === Number(child_id))
                let childRow = data.year.map((year) =>{
                    let getIndicatorValue = filterChildIndicator.find((item) => item.for_datapoint__year_EC == year.for_datapoint__year_EC)
                    if (getIndicatorValue){
                        return `
                        <td>${getIndicatorValue.performance}</td>
                        `
                    }else{
                        return `<td> - </td>`
                    }
                })

                return  `
            <tr>
               <td class="">&nbsp;&nbsp;&nbsp;&nbsp ${filterChildIndicator[0].indicator__title_ENG}</td> 
               <td class="">&nbsp;&nbsp;&nbsp;&nbsp ${filterChildIndicator[0].indicator__title_AMH}</td> 
               ${childRow}
            </tr>
            ${childDataFn(filterChildIndicator[0].indicator__id)}
            `
            })

            

            return  `
            <tr>
               <td class="fw-bold"> <a href="/user-admin/data_view_indicator_detail/${filterIndicator[0].indicator__id}/">${filterIndicator[0].indicator__title_ENG}</a></td> 
               <td class="fw-bold"> <a href="/user-admin/data_view_indicator_detail/${filterIndicator[0].indicator__id}/">${filterIndicator[0].indicator__title_AMH}</a></td> 
               ${row}
            </tr>
            ${childData}
            `
           
        })

        $("#tableBody").html(tableData)

    }


})