from __future__ import annotations

import asyncio
import concurrent.futures
from temporalio.client import Client
from temporalio.contrib.pydantic import pydantic_data_converter
from temporalio.worker import Worker

from examples.temporal.openai_types_converter import agent_data_converter
from examples.temporal.tools_workflow import ToolsWorkflow
# Import the activity and workflow from our other files
from .activities import get_model_response
from .hello_world_workflow import HelloWorldAgent


async def main():
    # Create client connected to server at the given address
    client = await Client.connect("localhost:7233",
                                  # data_converter=pydantic_data_converter
                                  data_converter=agent_data_converter)

    # Run the worker
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as activity_executor:
        worker = Worker(
            client,
            task_queue="my-task-queue",
            workflows=[HelloWorldAgent, ToolsWorkflow],
            activities=[get_model_response],
            activity_executor=activity_executor,
        )
        await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
