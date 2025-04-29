from dataclasses import dataclass
from typing import Union, Optional, List, Literal, Iterable, TypedDict

import httpx
from openai import AsyncOpenAI, NotGiven, NOT_GIVEN
from openai._types import Headers, Query, Body
from openai.types import ResponsesModel, Metadata, Reasoning
from openai.types.responses import ResponseInputParam, ResponseIncludable, ResponseTextConfigParam, \
    response_create_params, ToolParam, Response
from temporalio import activity

from examples.basic.tools import Weather


# @dataclass
# class ModelInput:
#     system_instructions: str | None
#     input: str | list[TResponseInputItem]
#     model_settings: ModelSettings
#     tools: list[Tool]
#     output_schema: AgentOutputSchemaBase | None
#     handoffs: list[Handoff]
#     tracing: ModelTracing
#     previous_response_id: str | None
#
#
# @dataclass
# class GetModelResponseInput:
#     model_name: str | None
#     model_input: ModelInput
#

# @activity.defn
# async def get_model_response(input: GetModelResponseInput) -> ModelResponse:
#     provider = OpenAIProvider()
#     model = provider.get_model(input.model_name)
#     return await model.get_response(**vars(input.model_input))

@activity.defn
async def get_weather(city: str) -> Weather:
    print("[debug] get_weather called")
    return Weather(city=city, temperature_range="14-20C", conditions="Sunny with wind.")

# @dataclass
class OpenAIActivityInput(TypedDict, total=False):
    input: Union[str, ResponseInputParam]
    model: ResponsesModel
    include: Optional[List[ResponseIncludable]] | NotGiven = NOT_GIVEN
    instructions: Optional[str] | NotGiven = NOT_GIVEN
    max_output_tokens: Optional[int] | NotGiven = NOT_GIVEN
    metadata: Optional[Metadata] | NotGiven = NOT_GIVEN
    parallel_tool_calls: Optional[bool] | NotGiven = NOT_GIVEN
    previous_response_id: Optional[str] | NotGiven = NOT_GIVEN
    reasoning: Optional[Reasoning] | NotGiven = NOT_GIVEN
    service_tier: Optional[Literal["auto", "default", "flex"]] | NotGiven = NOT_GIVEN
    store: Optional[bool] | NotGiven = NOT_GIVEN
    stream: Optional[Literal[False]] | Literal[True] | NotGiven = NOT_GIVEN
    temperature: Optional[float] | NotGiven = NOT_GIVEN
    text: ResponseTextConfigParam | NotGiven = NOT_GIVEN
    tool_choice: response_create_params.ToolChoice | NotGiven = NOT_GIVEN
    tools: Iterable[ToolParam] | NotGiven = NOT_GIVEN
    top_p: Optional[float] | NotGiven = NOT_GIVEN
    truncation: Optional[Literal["auto", "disabled"]] | NotGiven = NOT_GIVEN
    user: str | NotGiven = NOT_GIVEN
    extra_headers: Headers | None = None
    extra_query: Query | None = None
    extra_body: Body | None = None
    timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN


@activity.defn
async def invoke_open_ai_model(input: OpenAIActivityInput) -> str:
    client = AsyncOpenAI()
    response = await client.responses.create(**input)
    return response.to_json()

@dataclass
class Weather:
    city: str
    temperature_range: str
    conditions: str

@activity.defn
async def get_weather(city: str) -> Weather:
    """
    Get the weather for a given city.
    """
    return Weather(city=city, temperature_range="14-20C", conditions="Sunny with wind.")