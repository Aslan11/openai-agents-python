import asyncio
import logging

from temporalio.client import Client
from temporalio.common import WorkflowIDReusePolicy

from examples.temporal.openai_types_converter import agent_data_converter
from examples.temporal.research_bot_workflow import ResearchWorkflow

async def main():
    logging.basicConfig(level=logging.DEBUG)

    # Create client connected to server at the given address
    client = await Client.connect(
        "localhost:7233",
        data_converter=agent_data_converter
    )

    # Execute a workflow
    result = await client.execute_workflow(ResearchWorkflow.run,
                                           "Caribbean vacation spots in April, optimizing for surfing, hiking and water sports",
                                           id="research-workflow",
                                           task_queue="my-task-queue",
                                           id_reuse_policy=WorkflowIDReusePolicy.TERMINATE_IF_RUNNING)

    print(f"Result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
