from temporalio import workflow


# Import our activity, passing it through the sandbox
with workflow.unsafe.imports_passed_through():
    from agents import Agent, Runner, RunConfig, function_tool
    from examples.temporal._activity_model import ModelStubProvider
    from openai import BaseModel


class Weather(BaseModel):
    city: str
    temperature_range: str
    conditions: str


@function_tool
def get_weather(city: str) -> Weather:
    print("[debug] get_weather called")
    return Weather(city=city, temperature_range="14-20C", conditions="Sunny with wind.")

@workflow.defn
class ToolsWorkflow:
    @workflow.run
    async def run(self, question: str) -> str:
        agent = Agent(
            name="Hello world",
            instructions="You are a helpful agent.",
            tools=[get_weather],
        )

        config = RunConfig(model_provider=ModelStubProvider())
        result = await Runner.run(agent, input="What's the weather in Tokyo?", run_config=config)
        return result.final_output
