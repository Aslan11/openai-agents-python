from __future__ import annotations

import asyncio
import concurrent.futures

from temporalio.client import Client
from temporalio.worker import Worker

from examples.temporal.activities import invoke_open_ai_model, get_weather
from examples.temporal.customer_service_workflow import CustomerServiceWorkflow
from examples.temporal.openai_types_converter import agent_data_converter
from examples.temporal.research_bot_workflow import ResearchWorkflow
from examples.temporal.tools_workflow import ToolsWorkflow
# Import the activity and workflow from our other files
from examples.temporal.hello_world_workflow import HelloWorldAgent


async def main():
    # Create client connected to server at the given address
    client = await Client.connect("localhost:7233",
                                  data_converter=agent_data_converter)

    # Run the worker
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as activity_executor:
        worker = Worker(
            client,
            task_queue="my-task-queue",
            workflows=[HelloWorldAgent, ToolsWorkflow, ResearchWorkflow, CustomerServiceWorkflow],
            activities=[invoke_open_ai_model, get_weather],
            activity_executor=activity_executor,
        )
        await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
