import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS
from fuzzywuzzy import fuzz, process  # type: ignore  # noqa

app = Flask(__name__)
CORS(app)

CSV_PATH = 'teste3/data/Relatorio_cadop.csv'


def load_data():
    """Carrega os dados do arquivo CSV."""
    df = pd.read_csv(CSV_PATH, sep=';', decimal=',', encoding='utf-8')
    df = df.fillna('')
    df.columns = df.columns.str.strip()
    return df


df = load_data()


@app.route('/api/search', methods=['GET', 'POST'])
def search():
    """Endpoint de busca com fuzzy matching (mínimo 90% de similaridade)."""
    try:
        # Obter o termo de busca
        if request.method == 'POST':
            data = request.get_json()
            term = data.get('query', '').strip()
        else:
            term = request.args.get('q', '').strip()
        limit = min(int(request.args.get('limit', 10)), 20)

        if not term:
            return jsonify({'error': 'Termo de busca obrigatório'}), 400

        # Criar a lista de textos para busca
        search_texts = df.apply(
            lambda row: ' '.join(f'{col}:{val}' for col, val in row.items()),
            axis=1
        ).tolist()
        # Buscar com limite maior para depois filtrar
        raw_matches = process.extractBests(
            term,
            search_texts,
            limit=limit,  # Usar diretamente o limite do usuário
            scorer=fuzz.token_set_ratio,
            score_cutoff=90  # Filtro mínimo direto na busca
        )

        # Coletar os resultados
        results = []
        for matched_text, score in raw_matches:
            try:
                index = search_texts.index(matched_text)
                result_dict = df.iloc[index].to_dict()
                result_dict['match_score'] = score
                results.append(result_dict)
            except ValueError:
                app.logger.warning(f'Texto não encontrado: {matched_text}')
        organize_inveted_list = []
        for result in results:
            try:
                if term.isalpha():
                    term_lower = term.lower()
                    razao = str(result.get('Razao_Social', '')).lower()
                    fantasia = str(result.get('Nome_Fantasia', '')).lower()

                    if term_lower in razao or term_lower in fantasia:
                        organize_inveted_list.append(result)
                        print(f"\33[32m {result['Razao_Social']} {result['Nome_Fantasia']}")  # noqa E501
                    else:
                        organize_inveted_list.insert(0, result)
                        print(f"\33[31m {result['Razao_Social']} {result['Nome_Fantasia']}")  # noqa E501

                elif term.isnumeric():
                    cnpj = str(result.get('CNPJ', ''))
                    ans = str(result.get('Registro_ANS', ''))

                    if term in cnpj or term in ans:
                        organize_inveted_list.append(result)
                        print(f"\33[32m {result['CNPJ']} {result['Registro_ANS']}")  # noqa E501
                    else:
                        organize_inveted_list.insert(0, result)
                        print(f"\33[31m {result['CNPJ']} {result['Registro_ANS']}")  # noqa E501

                else:
                    organize_inveted_list.append(result)
                    print(f"\33[35m {result}")  # noqa E501

            except Exception as e:
                print(f"Erro ao processar resultado: {e}")
                print(term_lower)
        results.sort(key=lambda r: -r['match_score'])
        inverted_results = list(reversed(organize_inveted_list))
        print("Resultados antes da organização:", results)
        print("Lista organizada antes de inverter:", organize_inveted_list)

        return jsonify(inverted_results)

    except Exception as e:
        app.logger.error(f'Erro na busca: {str(e)}')
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
