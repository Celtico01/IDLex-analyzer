import re
from presidio_analyzer import RecognizerResult, EntityRecognizer
from presidio_analyzer.nlp_engine import NlpArtifacts

class EnderecoRecognizer(EntityRecognizer):
    def __init__(self):
        super().__init__(
            supported_entities=["ENDERECO"],
            name="EnderecoRecognizer",
            supported_language="pt"
        )

    def load(self) -> None:
        # Nenhum recurso externo a carregar
        pass

    def analyze(self, text: str, entities: list[str], nlp_artifacts: NlpArtifacts) -> list[RecognizerResult]:
        results = []
        # --- NER ---
        for ent in nlp_artifacts.entities:
            if ent.label_ in ["LOCATION"]:
                result = RecognizerResult(
                    entity_type="ENDERECO",
                    start=ent.start_char,
                    end=ent.end_char,
                    score=0.85
                )
                results.append(result)
        return results
'''
        # --- Regex ---
        padroes = [
            r"(Rua|Avenida|Av\.?|Travessa|Estrada|Rodovia|)\s+[\w\s\-º°]+?,\s*n[º°]?\s*\d+[^,\n]*?(Bairro\s+[\w\s\-]+)?[^,\n]*?(?=(,|\n|$))",
        ]

        for padrao in padroes:
            for match in re.finditer(padrao, text, flags=re.IGNORECASE):
                result = RecognizerResult(
                    entity_type="ENDERECO",
                    start=match.start(),
                    end=match.end(),
                    score=0.9
                )
                results.append(result)
'''
        
