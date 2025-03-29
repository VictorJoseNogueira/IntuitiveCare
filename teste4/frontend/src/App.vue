<template>
  <div id="app">
    <div class="main-layout">
      <header class="header-container">
        <HeaderVue></HeaderVue>
      </header>

      <main class="content">
        <HomeVue/>
      </main>

      <footer class="bg-dark text-white text-center py-3 footer-container">
        <FooterVue></FooterVue>
      </footer>
    </div>
  </div>
</template>

<script>
import 'bootstrap/dist/css/bootstrap.min.css'
import HomeVue from './components/Home.vue'
import HeaderVue from './components/headerComponent.vue'
import FooterVue from './components/FooterComponent.vue'
export default {
  name: 'App',
  components: {
    HomeVue,
    HeaderVue,
    FooterVue
  }
}
</script>

<style>
.content{
  margin: 0 auto;
  max-width: 1440px;
  min-width: 1000px;
}
.header-container{
  min-width: 1440px;

}
.footer-container{
  min-width: 1440px;

}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

html, body {
  height: 100%;
  margin: 0;
  padding: 0;
}

.main-layout {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.content {
  flex: 1;
  padding-bottom: 60px; /* Espaço extra se necessário */
}

footer {
  margin-top: auto; /* Força o footer para baixo */
  width: 100%;
}
</style>