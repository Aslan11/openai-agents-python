import asyncio
import logging

from temporalio.client import Client
from temporalio.common import WorkflowIDReusePolicy

# Import the workflow from the previous code
from .workflows import HelloWorldAgent


async def main():
    logging.basicConfig(level=logging.DEBUG)

    # Create client connected to server at the given address
    client = await Client.connect("localhost:7233")

    # Execute a workflow
    result = await client.execute_workflow(HelloWorldAgent.run, "my name", id="my-workflow-id", task_queue="my-task-queue",
                                           id_reuse_policy=WorkflowIDReusePolicy.TERMINATE_IF_RUNNING)

    print(f"Result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
