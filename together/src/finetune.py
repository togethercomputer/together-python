import requests
from typing import Optional
import urllib.parse
import posixpath


class Finetune:
    def __init__(self, together_api_key) -> None:
        self.together_api_key = together_api_key
        self.endpoint_url = (
            "http://localhost:8895/v1/fine-tunes/"  # TODO Assign correct endpoint
        )

    def create_finetune(
        self,
        training_file: str,  # training file_id
        validation_file: Optional[str] = None,  # validation file_id
        model: Optional[str] = None,
        n_epochs: Optional[int] = 4,
        batch_size: Optional[int] = None,
        learning_rate_multiplier: Optional[float] = None,
        prompt_loss_weight: Optional[float] = 0.01,
        compute_classification_metrics: Optional[bool] = False,
        classification_n_classes: Optional[int] = None,
        classification_positive_class: Optional[str] = None,
        classification_betas: Optional[list] = None,
        suffix: Optional[str] = None,
    ):
        parameter_payload = {
            "training_file": training_file,
            "validation_file": validation_file,
            "model": model,
            "n_epochs": n_epochs,
            "batch_size": batch_size,
            "learning_rate_multiplier": learning_rate_multiplier,
            "prompt_loss_weight": prompt_loss_weight,
            "compute_classification_metrics": compute_classification_metrics,
            "classification_n_classes": classification_n_classes,
            "classification_positive_class": classification_positive_class,
            "classification_betas": classification_betas,
            "suffix": suffix,
        }

        # HTTP headers for authorization
        headers = {
            "Authorization": f"Bearer {self.together_api_key}",
            "Content-Type": "application/json",
        }

        # send request
        try:
            response = requests.post(
                self.endpoint_url, headers=headers, json=parameter_payload
            ).json()
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            raise ValueError(f"Error raised by fine-tune endpoint: {e}")

        return response

    def list_finetune(self):
        headers = {
            "Authorization": f"Bearer {self.together_api_key}",
        }

        # send request
        try:
            response = requests.get(self.endpoint_url, headers=headers).json()
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            raise ValueError(f"Error raised by endpoint: {e}")

        return response

    def retrieve_finetune(self, fine_tune_id: str):
        retrieve_url = urllib.parse.urljoin(self.endpoint_url, fine_tune_id)

        headers = {
            "Authorization": f"Bearer {self.together_api_key}",
        }

        # send request
        try:
            response = requests.get(retrieve_url, headers=headers).json()
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            raise ValueError(f"Error raised by endpoint: {e}")

        return response

    def cancel_finetune(self, fine_tune_id: str):
        relative_path = posixpath.join(fine_tune_id, "cancel")
        retrieve_url = urllib.parse.urljoin(self.endpoint_url, relative_path)

        headers = {
            "Authorization": f"Bearer {self.together_api_key}",
        }

        # send request
        try:
            response = requests.post(retrieve_url, headers=headers).json()
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            raise ValueError(f"Error raised by endpoint: {e}")

        return response  # this should be null

    def list_finetune_events(self, fine_tune_id: str):
        # TODO enable stream
        relative_path = posixpath.join(fine_tune_id, "events")
        retrieve_url = urllib.parse.urljoin(self.endpoint_url, relative_path)

        headers = {
            "Authorization": f"Bearer {self.together_api_key}",
        }

        # send request
        try:
            response = requests.get(retrieve_url, headers=headers).json()
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            raise ValueError(f"Error raised by endpoint: {e}")

        return response

    def delete_finetune_model(self, model: str):
        model_url = "https://api.together.xyz/api/models"
        delete_url = urllib.parse.urljoin(model_url, model)

        headers = {
            "Authorization": f"Bearer {self.together_api_key}",
        }

        # send request
        try:
            response = requests.delete(delete_url, headers=headers).json()
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            raise ValueError(f"Error raised by endpoint: {e}")

        return response