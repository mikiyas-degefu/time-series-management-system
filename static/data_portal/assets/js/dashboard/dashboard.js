$(document).ready(function () {
    const COLORS = ['#264653', '#2a9d8f', '#e9c46a', '#f4a261', '#e76f51', '#606c38', '#283618','#bc6c25']

    const fetchData = async(url) =>{
        const response = await axios.get(url)
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

    const handleTopicSkeleton = (show=true) =>{
        const skeleton = `
                        <div class="col-md-6 col-xl-3 col-6 container loading-skeleton ">
                            <div class="card social-widget-card">
                                <div class="card-body d-flex justify-content-between align-items-center p-2">
                                    <div class="bg-body text-center text-primary p-3 mt-3 rounded" style="width: 100%;">
                                        <div class="spinner-grow" role="status">
                                            <span class="visually-hidden">Loading...</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        `
        $("#dashboard-card-list").html(show ? skeleton.repeat(8) : '')
    }


    const handleCardSkeleton = (show=true) =>{
        const skeleton = `
                        <div class="col-md-6 col-xl-4 d-md-block container loading-skeleton ">
                            <div class="card social-widget-card">
                                <div class="card-body d-flex justify-content-between align-items-center p-2">
                                    <div class="bg-body  d-flex flex-column justify-content-center align-items-center text-primary p-3 mt-3 rounded" style="height:160px; width: 100%;">
                                        <div class="spinner-grow" role="status">
                                            <span class="visually-hidden">Loading...</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
            `
        $("#category-card-list").html(show ? skeleton.repeat(6) : '')
    }


    const topicListHtml = (topics) =>{
        $("#dashboard-card-list").html('')  //clear inner html
        let topicList = topics.map((topic) => {
            return(`
            <div class="col-6 col-md-3" data-id="${topic.id}" data-topic-name="${topic.title_ENG}" name="topic-card" >
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

    const categoryHtml = (data) => {
    }


    const getWays = async() =>{


        handleTopicSkeleton(true) // show loading before fetching data
        const topics = await fetchData('/data-portal/api/topic-lists')
        handleTopicSkeleton(false)  // hide loading
        
        
        topicListHtml(topics) //contract the topic cards


         //handle on topic clicked
        $("[name='topic-card']").click(async function () {
            let cardData = $(this).data();
            $("#topic-title").html(cardData.topicName)

            handleCardSkeleton(true)
            const categories = await fetchData(`/data-portal/api/category-with-indicator/${cardData.id}`)
            handleCardSkeleton(false)

            categoryHtml(categories)
        })



    }

    getWays()

   


  
})