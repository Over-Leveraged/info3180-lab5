<template>
  <main>
    <h1>Movies</h1>
    <div class="movie-list">
      <div class="movie-card" v-for="movie in movies" :key="movie.title">
        <div class="movie-image">
          <img :src="'/api/v1/posters/' + movie.poster" alt="Movie Poster" />
        </div>
        <div class="movie-details">
          <h3>{{ movie.title }}</h3>
          <p>{{ movie.description }}</p>
        </div>
      </div>
    </div>
  </main>
</template>

<style>
  .movie-list {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
  }

  .movie-card {
    border-radius: 0.5rem;
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
    display: flex;
    flex-direction: column;
    overflow: hidden;
    width: 300px;
  }

  .movie-image img {
    display: block;
    height: auto;
    max-width: 100%;
  }

  .movie-details {
    background-color: #f9f9f9;
    padding: 1rem;
  }

  .movie-details h3 {
    margin-top: 0;
  }

  .movie-details p {
    margin-bottom: 0;
  }
</style>

<script setup>
    import { ref, onMounted } from "vue";
    let movies = ref([]);

    function fetchMovies() {
    fetch("/api/v1/movies",
        {
            method: "GET" //,
            //headers: {
            //    "Content-Type": "application/json",
            //},
        })
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
            movies.value = data.movies;
        })
        .catch((error) => {
            console.log(error);
        });
}

onMounted(() => {
    fetchMovies();
});

</script>

