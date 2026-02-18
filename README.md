# multilingual-vocab-agent-langflow
multilingual-vocab-agent-langflow is an agentic language-learning system built with Langflow and LLMs that generates dynamic reading stories from user-defined vocabulary. It uses custom components, tool-calling agents, multilingual vocab storage, and intent routing for story creation and vocab management.

The architecture in langflow is as follows:

<img width="1311" height="863" alt="image" src="https://github.com/user-attachments/assets/d5600285-1d7c-4658-92bf-79d2c4d3e520" />

## There are 2 operations that this agent can perform:

### 1. To add the vocabulary via csv or single word at a time.
## There are 2 ways to upload the vocabulary.(english or german) 

### 1. Via csv file
Note: Please do not mix both English and German words in a single csv (yet working on this use case and accept csv with different headers as well) 

Example:

de_vocab.csv should contain content in the format shown below:
word
Haus
Baum
Straße
Apfel
Buch
Wasser
Freund
Schule
Zeit
Stadt
### 2. Adding a single word at a time

In the playground you can mention as follows:
Add this English word: Fever

It would display as 
The English word "Fever" has been added to the vocabulary.
<img width="781" height="718" alt="image" src="https://github.com/user-attachments/assets/636a30d3-5d15-4231-b9e7-26726ada3467" />
### 2. We can later generate a story using the vocab as well 
Example:
<img width="814" height="675" alt="image" src="https://github.com/user-attachments/assets/8e1d9c5c-bcd6-477a-947f-6a8791dc1304" />


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
