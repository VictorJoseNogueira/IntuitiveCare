<template>
  <div>
    <main class="container my-5">
      <!-- Seção de Busca -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="input-group">
            <input v-model="searchText" type="text" class="form-control" placeholder="Buscar..." @keyup.enter="searchByText">
            <button @click="searchByText" class="btn btn-primary" type="button">Buscar</button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: 'SearchBox',
  data() {
    return {
      searchText: ''
    }
  },
  methods: {
    async searchByText() {
      if (!this.searchText.trim()) {
        console.warn('O texto de busca está vazio');
        return;
      }

      try {
        const response = await fetch('http://localhost:5000/api/search', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            query: this.searchText
          })
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const responseData = await response.json();
        
        console.log('Resposta do servidor:', responseData);
        
        // Emitir evento para o componente pai com os resultados
        this.$emit("search", responseData);
        
      } catch (error) {
        console.error('Erro ao enviar dados:', error);
        // Você pode adicionar aqui um feedback visual para o usuário
      }
    }
  }
}
</script>