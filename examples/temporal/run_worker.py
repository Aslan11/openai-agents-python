from __future__ import annotations

import asyncio
import concurrent.futures

from temporalio.client import Client
from temporalio.worker import Worker

from agents import TResponseInputItem
from examples.temporal.adapters.model_activity import invoke_open_ai_model
from examples.temporal.workflows.agents_as_tools_workflow import AgentsAsToolsWorkflow
from examples.temporal.workflows.get_weather_activity import get_weather
from examples.temporal.workflows.customer_service_workflow import CustomerServiceWorkflow
from examples.temporal.adapters.open_ai_converter import open_ai_data_converter
from examples.temporal.workflows.research_bot_workflow import ResearchWorkflow
from examples.temporal.workflows.tools_workflow import ToolsWorkflow
from examples.temporal.workflows.hello_world_workflow import HelloWorldAgent


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
            workflows=[HelloWorldAgent, ToolsWorkflow, ResearchWorkflow, CustomerServiceWorkflow,
                       AgentsAsToolsWorkflow],
            activities=[invoke_open_ai_model, get_weather],
            activity_executor=activity_executor,
        )
        await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
