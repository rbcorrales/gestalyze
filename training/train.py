import argparse
import os
from training.model_factory import ModelFactory

def main():
    parser = argparse.ArgumentParser(description='Train ASL recognition models')
    parser.add_argument('--model-type', type=str, required=True,
                      choices=['custom', 'online'],
                      help='Type of model to train')
    parser.add_argument('--model-path', type=str, required=True,
                      help='Path to save the trained model')
    parser.add_argument('--dataset-name', type=str, required=True,
                      help='Name of the dataset to use')
    args = parser.parse_args()

    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(args.model_path), exist_ok=True)
    
    # Create trainer instance
    trainer = ModelFactory.create_trainer(args.model_type, args.model_path, args.dataset_name)
    
    # Train the model
    print(f"Training {args.model_type} model...")
    trainer.train()

    print(f"Training completed. Model saved to {args.model_path}")

if __name__ == '__main__':
    main()
