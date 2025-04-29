from __future__ import annotations

import dataclasses
from inspect import isclass
from typing import Any, cast, Type, Union, Optional, Callable, Awaitable, get_origin, get_args

from openai import NotGiven
from temporalio.converter import AdvancedJSONEncoder, JSONTypeConverter, _JSONTypeConverterUnhandled, \
    CompositePayloadConverter, DefaultPayloadConverter, DataConverter, JSONPlainPayloadConverter

from agents import Tool, FunctionTool, RunContextWrapper


class ToolsJSONEncoder(AdvancedJSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, NotGiven):
            return "NOT_GIVEN"
        return super().default(o)


def empty(ctx: RunContextWrapper[Any], input: str) -> Awaitable[Any]:
    pass


class ToolsJSONTypeConverter(JSONTypeConverter):
    def to_typed_value(
            self, hint: Type, value: Any
    ) -> Union[Optional[Any], _JSONTypeConverterUnhandled]:
        if hint is object:
            return value
        if value == "NOT_GIVEN":
            return NotGiven()
        return JSONTypeConverter.Unhandled


class ToolPayloadConverter(CompositePayloadConverter):

    def __init__(self) -> None:
        # Replace default JSON plain with our own that has our encoder and type
        # converter
        json_converter = JSONPlainPayloadConverter(
            encoder=ToolsJSONEncoder,
            custom_type_converters=[ToolsJSONTypeConverter()],
        )
        super().__init__(
            *[
                c if not isinstance(c, JSONPlainPayloadConverter) else json_converter
                for c in DefaultPayloadConverter.default_encoding_payload_converters
            ]
        )


agent_data_converter = dataclasses.replace(
    DataConverter.default,
    payload_converter_class=ToolPayloadConverter,
)
