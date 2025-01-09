from huggingface_hub import HfApi

from scope3ai.tracers.huggingface.chat import HUGGING_FACE_CHAT_TASK
from scope3ai.tracers.huggingface.image_to_image import HUGGING_FACE_IMAGE_TO_IMAGE_TASK
from scope3ai.tracers.huggingface.speech_to_text import HUGGING_FACE_SPEECH_TO_TEXT_TASK
from scope3ai.tracers.huggingface.text_to_image import HUGGING_FACE_TEXT_TO_IMAGE_TASK
from scope3ai.tracers.huggingface.text_to_speech import HUGGING_FACE_TEXT_TO_SPEECH_TASK
from scope3ai.tracers.huggingface.translation import HUGGING_FACE_TRANSLATION_TASK


def get_models_by_task(task: str):
    """
    Retrieves all models from Hugging Face Hub filtered by a specific task.

    Parameters:
        task (str): The task to filter models by (e.g., "text-classification", "image-classification").

    Returns:
        list: A list of dictionaries containing model information for the specified task.
    """
    api = HfApi()
    try:
        models = api.list_models(task=task)
        return [model.id for model in models]
    except Exception as e:
        print(f"Error retrieving models: {e}")
        return []


# Example usage
def get_all_models_by_tasks():
    tasks = [
        HUGGING_FACE_CHAT_TASK,
        HUGGING_FACE_IMAGE_TO_IMAGE_TASK,
        HUGGING_FACE_SPEECH_TO_TEXT_TASK,
        HUGGING_FACE_TEXT_TO_IMAGE_TASK,
        HUGGING_FACE_TEXT_TO_SPEECH_TASK,
        HUGGING_FACE_TRANSLATION_TASK,
    ]
    models_by_tasks = {}
    for task in tasks:
        models = get_models_by_task(task)
        models_by_tasks[task] = models

    return models_by_tasks
