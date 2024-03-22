// Create a new Vue instance
const root = Vue.createApp({

    // Data Properties
    data() {
        return {

            // Pretend animal info came from API

            cat_name: "Kitty",
            cat_snack: "Salmon",

            dog_name: "Flash",
            dog_snack: "Beef Jerky"

        }
    }

})

// Add components
root.component("pet-component", {

    // Properties, data properties
    props: ["type", "name", "snack"], 

    template: `
    <h2>
        {{ type }}
    </h2>

    <p>
        Name: {{ name }}
    </p>

    <p>
        Snack: {{ snack }}
    </p>
    `


})

root.mount("#root")