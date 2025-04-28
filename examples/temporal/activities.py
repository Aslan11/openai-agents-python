from dataclasses import dataclass
from typing import TypedDict

from temporalio import activity

from agents import ModelResponse, OpenAIResponsesModel, OpenAIProvider, TResponseInputItem, ModelSettings, Tool, \
    AgentOutputSchemaBase, Handoff, ModelTracing
from examples.basic.tools import Weather


@dataclass
class ModelInput:
    system_instructions: str | None
    input: str | list[TResponseInputItem]
    model_settings: ModelSettings
    tools: list[Tool]
    output_schema: AgentOutputSchemaBase | None
    handoffs: list[Handoff]
    tracing: ModelTracing
    previous_response_id: str | None


@dataclass
class GetModelResponseInput:
    model_name: str | None
    model_input: ModelInput


@activity.defn
async def get_model_response(input: GetModelResponseInput) -> ModelResponse:
    provider = OpenAIProvider()
    model = provider.get_model(input.model_name)
    return await model.get_response(**vars(input.model_input))

@activity.defn
async def get_weather(city: str) -> Weather:
    print("[debug] get_weather called")
    return Weather(city=city, temperature_range="14-20C", conditions="Sunny with wind.")
