from training.base_trainer import BaseTrainer
from training.custom_trainer import CustomTrainer
from training.online_trainer import OnlineTrainer

class ModelFactory:
    @staticmethod
    def create_trainer(model_type: str, model_path: str, dataset_name: str = None) -> BaseTrainer:
        """
        Create a trainer instance based on the specified model type.
        
        Args:
            model_type (str): Type of model to create ('custom' or 'online')
            model_path (str): Path to save/load the model
            dataset_name (str, optional): Name of the dataset to use for online training
            
        Returns:
            BaseTrainer: An instance of the appropriate trainer class
            
        Raises:
            ValueError: If an invalid model type is specified
        """
        if model_type.lower() == 'custom':
            return CustomTrainer(dataset_name, model_path)
        elif model_type.lower() == 'online':
            return OnlineTrainer(model_path, dataset_name)
        else:
            raise ValueError(f"Invalid model type: {model_type}. Must be 'custom' or 'online'.")
