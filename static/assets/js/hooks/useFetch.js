const useFetch = async (url) =>{
    let response = await axios.get(url)
    try{
        return response.data
    }catch(error){
        return error
    }
}