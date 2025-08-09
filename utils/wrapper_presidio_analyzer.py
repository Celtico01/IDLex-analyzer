from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import (
    NlpEngineProvider, 
    NlpEngine,
    TransformersNlpEngine
)

from customized_recognizers.cpf_recognizer import CPFRecognizer
from customized_recognizers.rg_recognizer import RGRecognizer
from customized_recognizers.cep_recognizer import CEPRecognizer
from customized_recognizers.endereco_recognizer import EnderecoRecognizer
from customized_recognizers.pessoa_recognizer import PessoaRecognizer

def create_model_spacy(language : str, spacy_model : str) -> NlpEngine:
    engine_pt = NlpEngineProvider(nlp_configuration={
        'nlp_engine_name': 'spacy',
        'models': [
            {
                "lang_code": language,
                "model_name": spacy_model
            }
        ]
    })
    return engine_pt.create_engine()

def create_model_transformers(language: str, spacy_model: str, transformers_model: str):
    engine = TransformersNlpEngine(models=[{
        "lang_code": language,
        "model_name": {
            "spacy": spacy_model,
            "transformers": transformers_model
        }
    }])
    return engine



def create_analyzer(nlp_engine: object, supported_languages: list[str]) -> AnalyzerEngine:
    analyzer = AnalyzerEngine(
        nlp_engine=nlp_engine,
        supported_languages=supported_languages
    )

    analyzer.registry.add_recognizer(CPFRecognizer())
    analyzer.registry.add_recognizer(RGRecognizer())
    analyzer.registry.add_recognizer(CEPRecognizer())
    analyzer.registry.add_recognizer(EnderecoRecognizer())
    analyzer.registry.add_recognizer(PessoaRecognizer())

    return analyzer
