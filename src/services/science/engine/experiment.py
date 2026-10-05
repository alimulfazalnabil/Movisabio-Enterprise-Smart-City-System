from src.services.science.models.schemas import Experiment

class ExperimentEngine:
    def validate_reproducibility(self, experiment: Experiment) -> bool:
        """
        An experiment can only be marked as reproducible if it has explicit versions bound to code and dataset.
        """
        if not experiment.code_version or experiment.code_version == "LATEST":
            return False
            
        if not experiment.dataset_version or experiment.dataset_version == "LATEST":
            return False
            
        if not experiment.parameters:
            return False
            
        return True
