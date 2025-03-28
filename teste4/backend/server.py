from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from fuzzywuzzy import process, fuzz   # type: ignore  # noqa

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
    """Endpoint de busca com fuzzy matching
      (mínimo 90% de similaridade) e ordenação hierarquizada."""
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
            limit=100,  # Capturar mais candidatos para filtrar
            scorer=fuzz.token_set_ratio,
            score_cutoff=90  # Filtro mínimo direto na busca
        )

        # Aplicar o limite do usuário após filtragem
        matches = raw_matches[:limit]

        # Coletar os resultados
        results = []
        for matched_text, score in matches:
            try:
                index = search_texts.index(matched_text)
                result_dict = df.iloc[index].to_dict()
                result_dict['match_score'] = score
                results.append(result_dict)
            except ValueError:
                app.logger.warning(f'Texto não encontrado: {matched_text}')

        # Determinar se o termo é numérico (int) ou string
        if term.isdigit():
            # Query numérica: priorizar cnpj ou registro ans
            def is_prioritized(result):
                return (term in str(result.get('cnpj', ''))) or (term in str(result.get('registro ans', '')))  # noqa E501
        else:
            term_lower = term.lower()

            def is_prioritized(result):
                return (term_lower in str(result.get('razao social', '')).lower()) or (term_lower in str(result.get('nome fantasia', '')).lower())  # noqa E501

        # Adicionar flag de priorização em cada resultado
        for result in results:
            result['prioritized'] = is_prioritized(result)

        results.sort(key=lambda r: (not r['prioritized'], -r['match_score']))

        return jsonify(results)

    except Exception as e:
        app.logger.error(f'Erro na busca: {str(e)}')
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
