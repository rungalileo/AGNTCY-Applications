# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import asyncio
import logging

from dotenv import load_dotenv, find_dotenv

from agp_api.gateway.gateway_container import GatewayContainer
from agp_api.agent.agent_container import AgentContainer
from core.logging_config import configure_logging
from rest.app import create_fastapi_app

# Define logger at the module level
logger = logging.getLogger("app")


class Config:
    """Configuration class for AGP (Agent Gateway Protocol) client.
    This class manages configuration settings for the AGP system, containing container
    instances for gateway and agent management, as well as remote agent specification.
    Attributes:
        gateway_container (GatewayContainer): Container instance for gateway management
        agent_container (AgentContainer): Container instance for agent management
        remote_agent (str): Specification of remote agent, defaults to "server"
    """

    gateway_container = GatewayContainer()
    agent_container = AgentContainer(local_agent="code_analyzer")
    # For client
    remote_agent = "code_analyzer"


async def main() -> None:
    """
    Entry point for running the application.

    This function performs the following:
    - Configures logging globally.
    - Loads environment variables from a `.env` file.
    - Retrieves the address for the remote gateway
    - Connects to the gateway and waits for incoming messages

    Returns:
        None
    """
    configure_logging()
    logger.info("Starting AGP application...")

    # GatewayHolder.create_gateway()
    Config.gateway_container.set_config(
        endpoint="http://127.0.0.1:46357", insecure=True
    )
    Config.gateway_container.set_fastapi_app(create_fastapi_app())

    # Call connect_with_retry
    _ = await Config.gateway_container.connect_with_retry(
        agent_container=Config.agent_container, max_duration=10, initial_delay=1)

    try:
        await Config.gateway_container.start_server(
            agent_container=Config.agent_container
        )
    except RuntimeError as e:
        logger.error("Runtime error: %s", e)
    except Exception as e:
        logger.info("Unhandled error: %s", e)


if __name__ == "__main__":
    # 1) load global/shared first
    load_dotenv(os.path.expanduser("~/.config/secrets/myapps.env"), override=False)
    # 2) then load per-app .env (if present) to override selectively
    load_dotenv(find_dotenv(usecwd=True), override=True)
    asyncio.run(main())
