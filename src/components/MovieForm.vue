<template>
    <form id="movieForm" action="" method="post" @submit.prevent="saveMovie">
        <div class="form-group mb-3">
            <label for="title" class="form-label">Movie Title</label>
            <input type="text" name="title" class="form-control" />
        </div>
        <div class="form-group mb-3">
            <label for="description" class="form-label">Description</label>
            <textarea id="description" name="description" class="form-control" > </textarea>
        </div>
        <div class="form-group mb-3">
            <label for="poster" class="form-label">Poster</label>
            <input type="file" id="poster" name="poster" class="form-control" />
        </div>
        <button type="submit" name="submit" id="submit" class="btn btn-primary "> Add </button>
        <div>

        </div>
    </form>
</template>

<script setup>
import { ref, onMounted } from 'vue';
let csrf_token = ref("");

function getCsrftoken(){
    fetch('/api/v1/csrf-token')
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
            csrf_token.value = data.csrf_token;
    })

}



onMounted(() => {
    getCsrftoken();
});

function saveMovie() {
    console.log("Saving movie");
    
    let movieForm = document.getElementById("movieForm");
    let form_data = new FormData(movieForm);

    fetch("/api/v1/movies", {
        
        method: 'POST',
        body: form_data,
        headers: {
            'X-CSRFToken': csrf_token.value
            }
        })

            .then(function (response) {
            return response.json();
            })
            .then(function (data) {
            
            console.log(data);
            })
            .catch(function (error) {
            
            console.log(error);
            });

}
</script>
<style></style>