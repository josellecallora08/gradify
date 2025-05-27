class AssessmentType:
    EVALUATE_REALIZATION="Evaluate Realization"
    EVALUATE_TRAINEES="Evaluate Trainees"
    CONTENT_GENERATOR = "Content Generator"
    def __str__(self) -> str:
        return self.value