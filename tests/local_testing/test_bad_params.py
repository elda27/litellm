#### What this tests ####
#    This tests chaos monkeys - if random parts of the system are broken / things aren't sent correctly - what happens.
#    Expect to add more edge cases to this over time.

import os
import sys
import traceback

import pytest

sys.path.insert(
    0, os.path.abspath("../..")
)  # Adds the parent directory to the system path
import litellm
from litellm import completion, embedding
from litellm.utils import Message

# litellm.set_verbose = True
user_message = "Hello, how are you?"
messages = [{"content": user_message, "role": "user"}]
model_val = None


def test_completion_with_no_model():
    # test on empty
    with pytest.raises(TypeError):
        response = completion(messages=messages)


def test_completion_with_empty_model():
    # test on empty
    try:
        response = completion(model=model_val, messages=messages)
    except Exception as e:
        print(f"error occurred: {e}")
        pass


def test_completion_invalid_param_cohere():
    try:
        litellm.set_verbose = True
        response = completion(model="command-nightly", messages=messages, seed=12)
        pytest.fail(f"This should have failed cohere does not support `seed` parameter")
    except Exception as e:
        assert isinstance(e, litellm.UnsupportedParamsError)
        print("got an exception=", str(e))
        if "cohere does not support parameters: ['seed']" in str(e):
            pass
        else:
            pytest.fail(f"An error occurred {e}")


def test_completion_function_call_cohere():
    try:
        response = completion(
            model="command-nightly", messages=messages, functions=["TEST-FUNCTION"]
        )
        pytest.fail(f"An error occurred {e}")
    except Exception as e:
        print(e)
        pass


def test_completion_function_call_openai():
    try:
        messages = [{"role": "user", "content": "What is the weather like in Boston?"}]
        response = completion(
            model="gpt-3.5-turbo",
            messages=messages,
            functions=[
                {
                    "name": "get_current_weather",
                    "description": "Get the current weather in a given location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The city and state, e.g. San Francisco, CA",
                            },
                            "unit": {
                                "type": "string",
                                "enum": ["celsius", "fahrenheit"],
                            },
                        },
                        "required": ["location"],
                    },
                }
            ],
        )
        print(f"response: {response}")
    except Exception:
        pass


# test_completion_function_call_openai()


def test_completion_with_no_provider():
    # test on empty
    try:
        model = "cerebras/btlm-3b-8k-base"
        response = completion(model=model, messages=messages)
    except Exception as e:
        print(f"error occurred: {e}")
        pass
