from pathlib import Path

import dotenv
import yaml
from core.utils.function_utils import functions, function, property, PropertyType

config_dir = Path(__file__).parent.parent.resolve() / "config"

# load yaml config
with open(config_dir / "config.yml", 'r') as f:
    config_yaml = yaml.safe_load(f)

# load .env config
config_env = dotenv.dotenv_values(config_dir / "config.env")

# config parameters
telegram_token = config_yaml["telegram_token"]
openai_api_key = config_yaml["openai_api_key"]
openai_api_base = config_yaml.get("openai_api_base", None)
allowed_telegram_usernames = config_yaml["allowed_telegram_usernames"]
new_dialog_timeout = config_yaml["new_dialog_timeout"]
enable_message_streaming = config_yaml.get("enable_message_streaming", True)
return_n_generated_images = config_yaml.get("return_n_generated_images", 1)
n_chat_modes_per_page = config_yaml.get("n_chat_modes_per_page", 5)
mongodb_uri = f"mongodb://mongo:{config_env['MONGODB_PORT']}"

# chat_modes
with open(config_dir / "chat_modes.yml", 'r') as f:
    chat_modes = yaml.safe_load(f)


# add functions without params to OPENAI_COMPLETION_OPTIONS['functions']
# fn = lambda x: x**x  # any function, notice: below fn=fn is passed, not fn=fn()
# YOUR_FUNCTION = function(fn=fn, name="fn_name", description="fn_description")
# OPENAI_COMPLETION_OPTIONS['functions'].append(YOUR_FUNCTION.to_json())
# name and description can be in any lang (uk) and gotta be descriptive/verbose for gpt.
OPENAI_COMPLETION_OPTIONS = {
    "temperature": 1,
    "max_tokens": 1000,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
    # list of functions without params, initialize it here.
    "functions": [
        function(fn=print, name="print", description="print function").to_json()  # stub
    ],
}


# used to call specific function, use via:
# core.chat.chat_service.get_function_call_options(your_function: function)
# set function params/properties before passing:
# (we will have a collection of funcs later)
# YOUR_FUNCTION.properties.add(
#         property(
#             "property_name",
#             PropertyType.string,
#             "property_description"
#         )
# )
# name and description can be in any lang (uk) and gotta be descriptive/verbose for gpt.
# PropertyType also got integer and bool, and these can be set:
# enum=['big', 'small']  # it doesn't strictly define options for gpt, only loosely
# default=['small']  # default value
OPENAI_FUNCTION_CALL_OPTIONS = {
    "temperature": 0,
    "max_tokens": 1000,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
    #"functions": [YOUR_FUNCTION.to_json()],  # we will add 1 specific function here, with params
    #"function_call": {"name": YOUR_FUNCTION.name}  # used to call specific function
    "function_call": {}
}

# stub
f = function(fn=print, name="print", description="print function")
f.properties.add(
    property(
        "printText",
        PropertyType.string,
        "text to print",
        default="default"
    )
)

from core.chat.chat_service import get_function_call_options
fn_call_opts = get_function_call_options(f)
