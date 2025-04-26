from dataclasses import dataclass
from datetime import timedelta
from typing import AsyncIterator

from temporalio import workflow

# Import our activity, passing it through the sandbox
with workflow.unsafe.imports_passed_through():
    from agents import Agent, Runner, RunConfig, ModelProvider, Model, TResponseInputItem, ModelSettings, Tool, \
        AgentOutputSchemaBase, Handoff, ModelTracing, ModelResponse
    from .activities import get_model_response, ModelInput, GetModelResponseInput
    from agents.items import TResponseStreamEvent


class ActivityModel(Model):

    def __init__(self, model_name: str):
        self.model_name = model_name

    async def get_response(
            self,
            system_instructions: str | None,
            input: str | list[TResponseInputItem],
            model_settings: ModelSettings,
            tools: list[Tool],
            output_schema: AgentOutputSchemaBase | None,
            handoffs: list[Handoff],
            tracing: ModelTracing,
            *,
            previous_response_id: str | None,
    ) -> ModelResponse:
        model_input = ModelInput(system_instructions=system_instructions, input=input,
                                 model_settings=model_settings,
                                 tools=tools, output_schema=output_schema, handoffs=handoffs, tracing=tracing,
                                 previous_response_id=previous_response_id)
        # tracing = tracing,
        return await workflow.execute_activity(
            get_model_response, GetModelResponseInput(self.model_name, model_input),
            start_to_close_timeout=timedelta(seconds=5)
        )

    def stream_response(self, system_instructions: str | None, input: str | list[TResponseInputItem],
                        model_settings: ModelSettings, tools: list[Tool], output_schema: AgentOutputSchemaBase | None,
                        handoffs: list[Handoff], tracing: ModelTracing, *, previous_response_id: str | None) -> \
            AsyncIterator[TResponseStreamEvent]:
        raise NotImplementedError()


class ModelStubProvider(ModelProvider):
    def get_model(self, model_name: str | None) -> Model:
        return ActivityModel(model_name)


@workflow.defn
class HelloWorldAgent:
    @workflow.run
    async def run(self, name: str) -> str:
        # return await workflow.execute_activity(
        #     say_hello, name, schedule_to_close_timeout=timedelta(seconds=5)
        # )
        agent = Agent(
            name="Assistant",
            instructions="You only respond in haikus.",
        )
        config = RunConfig(model_provider=ModelStubProvider())
        result = await Runner.run(agent, input="Tell me about recursion in programming.", run_config=config)
        return result.final_output
