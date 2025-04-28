from __future__ import annotations

from datetime import timedelta
from typing import Any

from temporalio import workflow


# Import our activity, passing it through the sandbox
with workflow.unsafe.imports_passed_through():
    from agents import Agent, Runner, RunConfig, function_tool, Tool, RunContextWrapper
    from examples.temporal._activity_model import ModelStubProvider
    from openai import BaseModel


class Weather(BaseModel):
    city: str
    temperature_range: str
    conditions: str



def activity_as_tool(
    tool_name: str | None,
    tool_description: str | None,
) -> Tool:
    @function_tool(
        name_override=tool_name, # or _transforms.transform_string_function_style(self.name),
        description_override=tool_description or "",

    )
    async def run_activity(city: str) -> Weather:
        return str(await workflow.execute_activity(
            tool_name,
            input,
            start_to_close_timeout=timedelta(seconds=10),
        ))
    return run_activity


@workflow.defn
class ToolsWorkflow:
    @workflow.run
    async def run(self, question: str) -> str:
        agent = Agent(
            name="Hello world",
            instructions="You are a helpful agent.",
            tools=[activity_as_tool("get_weather", "Get the weather for a city.")],
        )

        config = RunConfig(model_provider=ModelStubProvider())
        result = await Runner.run(agent, input="What's the weather in Tokyo?", run_config=config)
        return result.final_output
