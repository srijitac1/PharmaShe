# Ollama

----

Ollama is a lightweight, open-source framework that enables local deployment and interaction with large language models (LLMs) using an efficient and portable format. It is particularly useful for running fine-tuned or customized models on personal workstations or local servers without depending on cloud inference APIs.

## 1. Installation

Ollama can be installed on macOS, Linux, or Windows using the official installer or command line. For Linux environments, the following command installs Ollama directly from the official repository:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

On the Kaya server, the default quota for the home directory (`/home/sbms003/your_id`) is limited, so you must install Ollama under the group directory (`/group/sbms003/your_id`).

## 2. Execution

On the Kaya server, you must specify the model storage paths for Ollama under the group directory as shown below:

```bash
$ vi ~/.bashrc
export OLLAMA_MODELS=/group/sbms003/your_id/ollama/models
export PATH="/group/sbms003/your_id/ollama/bin:$PATH"
```

Since the Kaya server’s standard user environment does not have sudo privileges, there are two options for running Ollama.

## 2.1. Running Ollama Directly

Ollama provides an HTTP REST API service through TCP port 11434. To allow remote access instead of local-only access, set the following environment variables:

```bash
$ tmux new-session -t ollama	# keep running in the background
$ ollama serve			# local-only access
# Or run ollama serve with environment variables. You can also set these in ~/.bashrc.
$ OLLAMA_HOST=0.0.0.0 OLLAMA_ORIGINS='*' ollama serve
```

## 2.2. Registering and Running as a User-Level Service

You can register Ollama as a user-level service. The override.conf file may be included, omitted, or modified as needed. However, note that service logs are difficult to check on the Kaya server.

```bash
$ # Set service environment variables
$ mkdir -p ~/.config/systemd/user/ollama.service.d
$ cat > ~/.config/systemd/user/ollama.service.d/override.conf
[Service]
Environment="OLLAMA_HOST=0.0.0.0" OLLAMA_ORIGINS='*' "OLLAMA_MODELS=/group/sbms003/your_id/ollama/models"

$ # Create the service definition file
$ cat > ~/.config/systemd/user/ollama.service
[Unit]
Description=Ollama Service

[Service]
ExecStart=/group/sbms003/sji/ollama/bin/ollama serve
Restart=always
RestartSec=3

[Install]
WantedBy=default.target

$ # Reload and start the service
$ systemctl --user daemon-reload
$ systemctl --user enable ollama
$ systemctl --user start ollama
```

## 3. Custom Fine-tuned Model Conversion

Models are distributed and executed in the GGUF (GPT-Generated Unified Format), a quantized format optimized for performance on CPUs and GPUs with minimal memory requirements. Fine-tuned models trained using PyTorch framework must be converted to the GGUF format before they can be loaded by Ollama. The conversion is typically performed through the llama.cpp conversion tools, which support exporting Hugging Face–compatible models to .gguf.

```bash
$ git clone https://github.com/ggerganov/llama.cpp
$ cd llama.cpp
$ python convert_hf_to_gguf.py \
    /path/to/fine-tuned-model \
    --outtype q8_0 \
    --outfile ../your_finetuned_model_q8_0.gguf
```

## 4. Model Loading and Execution

Once the model has been converted, it can be loaded and executed using a simple Modelfile. A Modelfile defines the model’s name, path, and metadata for Ollama to recognize. This is the Modelfile we used for the project.

```yaml
FROM ./gemma3-1b-it-lora-8bit-trainer_q8_0.gguf

SYSTEM """
You are an expert AI assistant specializing in Pharmaceutical Formulation Development. 
Your role is to provide accurate, evidence-based, and precise information regarding drug formulation, excipient compatibility, process optimization, an
d regulatory considerations. 
Always prioritize factual accuracy and technical details over creativity.
"""

PARAMETER temperature 0.7 
PARAMETER top_p 0.85
PARAMETER repeat_last_n 64
PARAMETER repeat_penalty 1.1

TEMPLATE """
<start_of_turn>user
{{ .System }}

{{ .Prompt }}<end_of_turn>
<start_of_turn>model
"""

PARAMETER stop "<end_of_turn>"
```

Now we can build and run the model:
```bash
$ ollama create gemma3-1b-pharma -f ./Modelfile
$ ollama ls
$ ollama run gemma3-1b-pharma
```