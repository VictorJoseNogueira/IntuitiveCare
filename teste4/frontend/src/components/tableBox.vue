
<template>
    <div>
        <div class="row">
                            <div class="col-12">
                                <table v-if="hasDatabases" class="table table-striped">
    <thead>
        <tr>
            <th>Registro Ans</th>
            <th>Razão Social</th>
            <th>CNPJ</th>
            <th>Nome Fantasia</th>
            <th>Modalidade</th>
            <th>Logradouro</th>
            <th>Bairro</th>
            <th>Cidade</th>
            <th>CEP</th>
            <th>DDD</th>
            <th>Telefone</th>
            <th>Endereço Eletrônico</th>
            <th>Representante</th>

        </tr>
    </thead>
    <tbody v-for="(database, index) in databases" :key="index">
        <tr>
            <td>{{database.Registro_ANS}}</td>
            <td>{{database.Razao_Social}}</td>
            <td>{{database.CNPJ}}</td>
            <td>{{database.Nome_Fantasia}}</td>
            <td>{{database.Modalidade}}</td>
            <td>{{database.Logradouro}}</td>
            <td>{{database.Bairro}}</td>
            <td>{{database.Cidade}}</td>
            <td>{{database.CEP}}</td>
            <td>{{database.DDD}}</td>
            <td>{{database.Telefone}}</td>
            <td>{{database.Endereco_eletronico}}</td>
            <td>{{database.Representante}}</td>

        </tr>
    </tbody>
</table>

<!-- Mensagem (mostra apenas após busca sem resultados) -->
<div v-if="searchPerformed && !hasDatabases" class="alert alert-info mt-3">
    Nenhum resultado encontrado para sua pesquisa.
</div>
</div>
                            </div>
                        </div>
      </template>
      
      
      <script>
      export default {
        name: 'TableBox',
        props: ['databases'],
        data() {
          return {
            searchPerformed: false,
          }
        },
        computed: {
          hasDatabases() {
            return this.databases && this.databases.length > 0;
          }
        },
        watch: {
          databases(newVal) {
            // Se a busca foi feita (mesmo que retorne um array vazio), marque searchPerformed como true.
            if (newVal !== null) {
              this.searchPerformed = true;
            }
          }
        }
      }
      </script>
      
      
      <!-- Add "scoped" attribute to limit CSS to this component only -->
    <style scoped>

        td {
            text-align: center;
            font-size: 14px;
        }
    </style>
    