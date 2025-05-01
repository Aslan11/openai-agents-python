from __future__ import annotations

import asyncio
import concurrent.futures

from temporalio.client import Client
from temporalio.contrib.pydantic import pydantic_data_converter
from temporalio.worker import Worker

from agents import TResponseInputItem
from examples.temporal.activities import invoke_open_ai_model, get_weather
from examples.temporal.customer_service_workflow import CustomerServiceWorkflow
from examples.temporal.open_ai_converter import open_ai_data_converter
from examples.temporal.research_bot_workflow import ResearchWorkflow
from examples.temporal.tools_workflow import ToolsWorkflow
# Import the activity and workflow from our other files
from examples.temporal.hello_world_workflow import HelloWorldAgent


async def main():
    # Create client connected to server at the given address
    client = await Client.connect("localhost:7233",
                                  data_converter=open_ai_data_converter)

    item = TResponseInputItem
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
