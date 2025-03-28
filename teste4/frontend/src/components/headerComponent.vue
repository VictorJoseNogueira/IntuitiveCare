<template>
    <div class="Header">
          <!-- Header -->
                        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
                            <div class="container">
                                <a class="navbar-brand" href="#">Minha Página</a>
                            </div>
                        </nav>

    </div>
  </template>
  
  <script>
  export default {
    name: 'HeaderVue',
    props: {
      msg: String
    }
  }
  </script>
  
  <!-- Add "scoped" attribute to limit CSS to this component only -->
