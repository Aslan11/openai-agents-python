from __future__ import annotations

import dataclasses
from inspect import isclass
from typing import Any, cast, Type, Union, Optional, Callable, Awaitable

from temporalio.converter import AdvancedJSONEncoder, JSONTypeConverter, _JSONTypeConverterUnhandled, \
    CompositePayloadConverter, DefaultPayloadConverter, DataConverter, JSONPlainPayloadConverter

from agents import Tool, FunctionTool, RunContextWrapper


class ToolsJSONEncoder(AdvancedJSONEncoder):
    def default(self, o: Any) -> Any:
        print(f"ToolsJSONEncoder: {o}")
        if isinstance(o, FunctionTool):
            t = cast(FunctionTool, o)
            return {
                "name": t.name,
                "description": t.description,
                "params_json_schema": super().default(t.params_json_schema),
                "strict_json_schema": super().default(t.strict_json_schema),
            }
        if isinstance(o, Callable):
            # This is a function or method, so we can return its name
            return o.__name__
        return super().default(o)


def empty(ctx: RunContextWrapper[Any], input: str) -> Awaitable[Any]:
    pass


class ToolsJSONTypeConverter(JSONTypeConverter):
    def to_typed_value(
            self, hint: Type, value: Any
    ) -> Union[Optional[Any], _JSONTypeConverterUnhandled]:
        if isclass(hint):
            if issubclass(hint, Tool):
                return FunctionTool(name=value["name"],
                                    description=value["description"],
                                    params_json_schema=value["params_json_schema"],
                                    strict_json_schema=value["strict_json_schema"],
                                    on_invoke_tool=empty)
            if issubclass(hint, Callable):
                return empty
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
