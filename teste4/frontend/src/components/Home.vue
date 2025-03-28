<template>
  <div class="Home">
    <SearchBox @search="handleSearch"></SearchBox>
    <TableBox :databases="databases"></TableBox>
  </div>
</template>


<script>
import SearchBox from './searchBox.vue'
import TableBox from './tableBox.vue'
export default {
  name: 'HomeVue',
  props: {
    msg: String
  },
  components: {
    SearchBox,
    TableBox
  },
  data() {
    return {
      databases: null
    }
    
  },
  methods: {
      handleSearch(results) {
        this.databases = results;
      }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
