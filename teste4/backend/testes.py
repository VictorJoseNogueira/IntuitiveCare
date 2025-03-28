from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from fuzzywuzzy import process, fuzz  # type: ignore  # noqa

app = Flask(__name__)
CORS(app)

CSV_PATH = 'teste3/data/Relatorio_cadop.csv'


# Funções Boyer-Moore
def boyer_moore_preprocess(pattern):
    """Pré-processamento para as regras de Bad Character e Good Suffix."""
    bad_char = {}
    for i in range(len(pattern)):
        bad_char[pattern[i]] = i

    good_suffix = [0] * (len(pattern) + 1)
    i = len(pattern)
    j = i + 1
    good_suffix[i] = j

    while i > 0:
        while j <= len(pattern) and pattern[i-1] != pattern[j-1]:
            if good_suffix[j] == 0:
                good_suffix[j] = j - i
            j = good_suffix[j]
        i -= 1
        j -= 1
        good_suffix[i] = j

    return bad_char, good_suffix


def boyer_moore_search(text, pattern):
    """Executa a busca Boyer-Moore no texto."""
    bad_char, good_suffix = boyer_moore_preprocess(pattern)
    m = len(pattern)
    n = len(text)
    i = 0

    while i <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[i + j]:
            j -= 1
        if j < 0:
            return i
        else:
            bc_shift = j - bad_char.get(text[i + j], -1)
            gs_shift = good_suffix[j + 1]
            i += max(bc_shift, gs_shift)
    return -1


# Carregamento de dados
def load_data():
    """Carrega os dados do arquivo CSV."""
    df = pd.read_csv(CSV_PATH, sep=';', decimal=',', encoding='utf-8')
    df = df.fillna('')
    df.columns = df.columns.str.strip()
    return df


df = load_data()


@app.route('/api/search', methods=['GET', 'POST'])
def search():
    """Endpoint de busca combinando Fuzzy Matching e Boyer-Moore."""
    try:
        # Obter termo de busca
        if request.method == 'POST':
            data = request.get_json()
            term = data.get('query', '').strip().lower()
        else:
            term = request.args.get('q', '').strip().lower()

        limit = min(int(request.args.get('limit', 10)), 20)

        if not term:
            return jsonify({'error': 'Termo de busca obrigatório'}), 400

        # Parte 1: Busca Fuzzy
        search_texts = df.apply(
            lambda row: ' '.join(f'{col}:{val}' for col, val in row.items()),
            axis=1
        ).tolist()

        raw_fuzzy = process.extractBests(
            term,
            search_texts,
            limit=100,
            scorer=fuzz.token_set_ratio,
            score_cutoff=100
        )

        # Processar resultados fuzzy
        fuzzy_indices = {}
        for match in raw_fuzzy[:limit]:
            text, score = match
            try:
                idx = search_texts.index(text)
                fuzzy_indices[idx] = score
            except ValueError:
                continue

        # Parte 2: Busca Boyer-Moore
        bm_indices = set()
        for idx, row in df.iterrows():
            for col, val in row.items():
                if boyer_moore_search(str(val).lower(), term) != -1:
                    bm_indices.add(idx)
                    break

        # Combinar resultados
        combined = []

        # Adicionar resultados Boyer-Moore primeiro (score 100)
        for idx in bm_indices:
            result = df.iloc[idx].to_dict()
            result['match_score'] = 100
            combined.append((idx, result))

        # Adicionar resultados fuzzy não duplicados
        for idx, score in fuzzy_indices.items():
            if idx not in bm_indices:
                result = df.iloc[idx].to_dict()
                result['match_score'] = score
                combined.append((idx, result))

        # Ordenar e aplicar limite
        combined.sort(key=lambda x: (-x[1]['match_score'], x[0]))
        final_results = [item[1] for item in combined[:limit]]

        return jsonify(final_results)

    except Exception as e:
        app.logger.error(f'Erro na busca: {str(e)}')
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
