#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from languagemodel import InitModel

loaded_model = None
loaded_tokenizer = None

def GetModelAndTokenizer():
    if loaded_model != None and loaded_tokenizer != None:
        return (loaded_model, loaded_tokenizer)
    else:
        raise ValueError("Model is not initialized")

def main():
    global loaded_model, loaded_tokenizer
    """Set up LLM."""
    print("Setting up LLM")
    model, tokenizer = InitModel()
    loaded_model = model
    loaded_tokenizer = tokenizer
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'llmsite.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
