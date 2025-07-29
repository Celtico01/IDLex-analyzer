from presidio_analyzer import RecognizerResult, EntityRecognizer
from presidio_analyzer.nlp_engine import NlpArtifacts

class PessoaRecognizer(EntityRecognizer):
    
    def __init__(self):
        super().__init__(
            supported_entities=["PESSOA"],
            name="PessoaRecognizer",
            supported_language="pt"
        )

    def load(self) -> None:
        # Nenhum recurso externo a carregar
        pass

    def analyze(self, text: str, entities: list[str], nlp_artifacts: NlpArtifacts) -> list[RecognizerResult]:
        results = []
        # --- NER--- #
        for ent in nlp_artifacts.entities:
            if ent.label_ in ["PESSOA"]:
                result = RecognizerResult(
                    entity_type="PESSOA",
                    start=ent.start_char,
                    end=ent.end_char,
                    score=0.85
                )
                results.append(result)
        return results