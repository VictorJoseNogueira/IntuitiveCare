<template>
    <div class="Footer">
          <!-- Header -->
            <div class="container">
                <p class="mb-0">© 2023 Minha Página. Todos os direitos reservados.</p>
            </div>
      
    </div>
  </template>
  
  <script>
  export default {
    name: 'FooterVue',
    props: {
      msg: String
    }
  }
  </script>
  
  <!-- Add "scoped" attribute to limit CSS to this component only -->
  <style scoped>
  .site-footer {
    width: 100%;
    /* O footer terá altura automática baseada no conteúdo */
  }
  
  </style>
  