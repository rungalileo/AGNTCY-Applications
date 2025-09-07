# Remote Agents with AGP

This repository demonstrates an agentic application that uses a remote agent with Agent Gateway Protocol. It has the following simple topology:

```bash
client <-----> Gateway <----> Server
```

- Client contains a Langgraph application
- Server is a FastAPI application that contains the remote agent
- Gateway is a message broker.

## Requirements

- Python 3.12+
- A virtual environment is recommended for isolating dependencies.
- a `.env` at the proejct root with your OpenAI API key (or a global env file with the same located at `~/.config/secrets/myapps.env`)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/agntcy/agentic-apps
   cd your-repo/remote_agent_agp
   ```

### Docker Remote Agent

There are convenience scripts for building Docker images for both Windows and Linux. Instructions below are for windows and Linux is almost identical.

On Windows Make sure you can execute PS scripts:

```Powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

```Powershell
cd remote_agent_agp\remote_agent_docker
.\build_image.ps1
```

After everything is done, you should have a similar output. The image is large because there is still much debugging happening.

```Powershell
> docker images    
REPOSITORY              TAG       IMAGE ID       CREATED              SIZE
agp_remote_agent        latest    054fbed666f9   About a minute ago   4.32GB
```

## Running the Application

### Gateway

#### Docker

   ```Powershell
   cd .\remote_agent_agp\
   run_gw_image.ps1
   ```

### Remote Agent

The preferred method to run the AGP remote agent is Docker

### Run Docker

Run remote agent:

```Powershell
.\run_image.ps1
```

### Local

You can run the server app by executing from /agentic-apps/remote_agent_agp/app:

   ```bash
   python main.py
   ```

### Client

You can run the client app by executing from `agentic-apps/remote_agent_agp/client`:

   ```bash
   python agp.py
   ```

### Output

On a successful run you should an output similar to the following:

- client:

```bash
{"timestamp": "2025-03-12 07:13:42,912", "level": "INFO", "message": "{'event': 'final_result', 'result': {'messages': [HumanMessage(content='Write a story about a cat', additional_kwargs={}, response_metadata={}, id='c97f93dd-0c55-4109-862b-a34d6fd5aeba'), AIMessage(content='cats are wise', additional_kwargs={}, response_metadata={}, id='c79d1515-340e-43b6-b16c-9e04ae2c3058')]}}", "module": "agp", "function": "<module>", "line": 212, "logger": "graph_client", "pid": 20472}
```

- server:

```bash
{"timestamp": "2025-03-12 07:13:42,910", "level": "INFO", "message": "Received message{\"agent_id\": \"remote_agent\", \"output\": {\"messages\": [{\"role\": \"assistant\", \"content\": \"cats are wise\"}]}, \"model\": \"gpt-4o\", \"metadata\": {\"id\": \"d90cafe8-8f0c-4012-937f-df98356262cc\"}}, from agent <builtins.PyAgentSource object at 0x0000020A5BA2A5F0>", "module": "main", "function": "connect_to_gateway", "line": 184, "logger": "app", "pid": 5808}
```

- Gateway

```bash
2025-03-12T14:13:21.043726Z  INFO data-plane-gateway ThreadId(32) agp_service: running service
2025-03-12T14:13:34.776879Z  INFO data-plane-gateway ThreadId(04) agp_datapath::message_processing: new connection received from remote: (remote: Some(172.17.0.1:49344) - local: Some(172.17.0.2:46357))
2025-03-12T14:13:42.881719Z  INFO data-plane-gateway ThreadId(07) agp_datapath::message_processing: new connection received from remote: (remote: Some(172.17.0.1:46470) - local: Some(172.17.0.2:46357))
2025-03-12T14:13:42.954498Z  INFO data-plane-gateway ThreadId(04) agp_datapath::message_processing: end of stream conn_index=1
```

## Langgraph Studio

- Run gateway and server

```Powershell
cd .\remote_agent_agp\client_studio\
langgraph dev
```
