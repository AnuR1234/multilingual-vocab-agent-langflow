# multilingual-vocab-agent-langflow
multilingual-vocab-agent-langflow is an agentic language-learning system built with Langflow and LLMs that generates dynamic reading stories from user-defined vocabulary. It uses custom components, tool-calling agents, multilingual vocab storage, and intent routing for story creation and vocab management.

The architecture in langflow is as follows:

<img width="1311" height="863" alt="image" src="https://github.com/user-attachments/assets/d5600285-1d7c-4658-92bf-79d2c4d3e520" />


# ⚡️ Quickstart

### Install locally (recommended)

Requires Python 3.10–3.13 and [uv](https://docs.astral.sh/uv/getting-started/installation/) (recommended package manager).

#### Install

From a fresh directory, run:
```shell
uv pip install langflow -U
```

The latest Langflow package is installed.
For more information, see [Install and run the Langflow OSS Python package](https://docs.langflow.org/get-started-installation#install-and-run-the-langflow-oss-python-package).

#### Run

To start Langflow, run:
```shell
uv run langflow run
```

Langflow starts at http://127.0.0.1:7860.

That's it! You're ready to build with Langflow! 🎉

## 📦 Other install options

### Run from source
If you've cloned this repository and want to contribute, run this command from the repository root:
```shell
make run_cli
```
For more information, see [DEVELOPMENT.md](./DEVELOPMENT.md).

### Docker
Start a Langflow container with default settings:
```shell
docker run -p 7860:7860 langflowai/langflow:latest
```
Langflow is available at http://localhost:7860/.
For configuration options, see the [Docker deployment guide](https://docs.langflow.org/deployment-docker).
