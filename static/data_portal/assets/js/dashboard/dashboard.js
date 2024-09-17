$(document).ready(function () {
    const COLORS = ['#264653', '#2a9d8f', '#e9c46a', '#f4a261', '#e76f51', '#606c38', '#283618','#bc6c25']

    const fetchData = async(url) =>{
        const response = await axios.get('/data-portal/api/topic-lists')
        try{
            return response.data
        }catch(error){
            console.error("Error:", error);
        }
    }

    const randomColor = () =>{
        let random = Math.floor(Math.random() * COLORS.length);
        return(COLORS[random])
    }


    const topicListHtml = (topics) =>{
        $("#dashboard-card-list").html('')  //clear inner html
        let topicList = topics.map((topic) => {
            return(`
            <div class="col-md-6 col-xl-3 d-none d-md-block">
                <div class="card social-widget-card " style="background-color: ${randomColor()};">
                    <div class="card-body d-flex justify-content-between align-items-center p-2">
                        <div class="d-flex flex-column">
                            <h3 class="text-white m-0">${topic.category_count}+</h3>
                            <span class="m-t-10">${topic.title_ENG}</span>
                        </div>
                        <i class="fa fa-${topic?.icon?.split(",")[1]}"></i>
                </div>
            </div>
        </div>

                `
            )
        })

        $("#dashboard-card-list").html(topicList)  //assign the cards
    }


    const getWays = async() =>{
        const topics = await fetchData()
        console.log(topics)
        topicListHtml(topics)
    }

    getWays()


  
})