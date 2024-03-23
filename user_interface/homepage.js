// Create a new Vue instance
const root = Vue.createApp({

    // Data Properties
    data() {
        return {

            events: ""

        }
    },
    methods: {
        get_all_events() {

            // call API endpoint

            let api_endpoint_url = "http://localhost:8000/api/v1/event/1"

            axios.get(api_endpoint_url)
                .then(response => {
                    console.log(response.data) // Array

                    this.events = response.data // Array
                })

                .catch(error => {
                    console.log(error.message)
                })

            console.log("=== [END] get_all_posts() ===")
        }
    },
    
    // This will run when the webpage loads for the first time 
    created() { 
        console.log("===[START] created() ===") 
 
            // call API endpoint 
            let api_endpoint_url = "http://localhost:8000/api/v1/event/1"

            // Don't do risky stuff here first
            axios.get(api_endpoint_url)
                .then(response => {
                    console.log(response.data) // Array

                    this.events = response.data // Array
                })

                .catch(error => {
                    console.log(error.message)
                })

            console.log("=== [END] get_all_posts() ===")
 
    }

})
root.mount("#root")
