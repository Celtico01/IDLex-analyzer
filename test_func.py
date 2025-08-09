from utils.wrapper_presidio_analyzer import (
    create_model_spacy, 
    create_model_transformers,
    create_analyzer
)
from utils.const import *
from utils.pos_processamento import (
    pos_processamento_cpf,
    pos_processamento_cep
)
FUNCOES_POS_PROCESSAMENTO = [
    pos_processamento_cpf,
    pos_processamento_cep,
]

from const_test import *
import textwrap
from presidio_analyzer import RecognizerResult

MAX_CHUNK_SIZE = 450  # Seguro para modelos com 512 tokens

def chunk_text(text, max_length=MAX_CHUNK_SIZE):
    """
    Quebra o texto em chunks de até `max_length` caracteres preservando palavras inteiras.
    """
    return textwrap.wrap(text, width=max_length, break_long_words=False, break_on_hyphens=False)

def analize(text):
    if NLP == 'spacy':
        nlp_engine = create_model_spacy(
            language=LANGUAGE,
            spacy_model=SPACY_MODEL
        )
    elif NLP == 'transformers':
        nlp_engine = create_model_transformers(
            language=LANGUAGE,
            spacy_model=SPACY_MODEL,
            transformers_model=TRANSFORMER_MODEL
        )

    analyzer = create_analyzer(nlp_engine, supported_languages=[LANGUAGE])

    # Quebra o texto em pedaços menores
    chunks = chunk_text(text)
    results = []
    current_offset = 0

    for chunk in chunks:
        chunk_results = analyzer.analyze(
            text=chunk,
            language=LANGUAGE,
            entities=ENTIDADES if isinstance(ENTIDADES, list) else [e.strip() for e in ENTIDADES.split(' ') if e.strip()]
        )

        # Ajusta os offsets para o texto original
        for result in chunk_results:
            adjusted_result = RecognizerResult(
                entity_type=result.entity_type,
                start=result.start + current_offset,
                end=result.end + current_offset,
                score=result.score,
                analysis_explanation=result.analysis_explanation,
                recognition_metadata=result.recognition_metadata
            )
            results.append(adjusted_result)

        current_offset += len(chunk)

    # Pós-processamento
    resultado_processado = results
    for func in FUNCOES_POS_PROCESSAMENTO:
        resultado_processado = func(text, resultado_processado)

    return resultado_processado



def carregar_anotacoes_em_dict(caminho_arquivo):
    """
    Lê um arquivo JSON com estrutura:
    {
        "id1": [
            {"ENTIDADE1": {"inicio": ..., "fim": ..., "texto": ...}},
            {"ENTIDADE2": {"inicio": ..., "fim": ..., "texto": ...}},
            ...
        ],
        ...
    }

    Retorna um dicionário no formato:
    {
        "id1": [
            {"entidade": ..., "inicio": ..., "fim": ..., "texto": ...},
            ...
        ],
        ...
    }
    """
    import json

    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        dados = json.load(f)

    resultado = {}

    for id_doc, anotacoes in dados.items():
        entidades_arquivo = []
        for anotacao in anotacoes:
            for entidade, info in anotacao.items():
                entidades_arquivo.append({
                    "entidade": entidade,
                    "inicio": info["inicio"],
                    "fim": info["fim"],
                    "texto": info["texto"]
                })
        resultado[id_doc] = entidades_arquivo

    return resultado


