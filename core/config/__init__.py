from pathlib import Path

import yaml

config_dir = Path(__file__).parent.parent.resolve() / "config"
with open(config_dir / "config.yml", 'r') as f:
    config = yaml.safe_load(f)

openai_api_key = config["openai_api_key"]
openai_api_base = config.get("openai_api_base", None)
openai_model = config["openai_model"]

novaposhta_api_key = config["novaposhta_api_key"]
novaposhta_api_url = config["novaposhta_api_url"]

telegram_token = config["telegram_token"]
allowed_telegram_usernames = config["allowed_telegram_usernames"]
new_dialog_timeout = config["new_dialog_timeout"]
enable_message_streaming = config.get("enable_message_streaming", True)
return_n_generated_images = config.get("return_n_generated_images", 1)
n_chat_modes_per_page = config.get("n_chat_modes_per_page", 5)

mongodb_uri = f"mongodb://mongo:{config['mongodb_port']}"

chromadb_uri = config['chromadb_uri']
chromadb_port = config['chromadb_port']

# chat_modes
with open(config_dir / "chat_modes.yml", 'r') as f:
    chat_modes = yaml.safe_load(f)
