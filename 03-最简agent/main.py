import argparse
import ast
import json
import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from typing import Any, Callable
from zoneinfo import ZoneInfo

from openai import OpenAI


MAX_LOOP_COUNT = 5
MODEL_NAME = os.environ.get("DEEPSEEK_MODEL", "deepseek-v4-flash")


client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)


def get_current_time(timezone: str = "Asia/Shanghai") -> str:
    """获取指定时区的当前时间。"""
    now = datetime.now(ZoneInfo(timezone))
    return now.strftime("%Y-%m-%d %H:%M:%S %Z")


def calculate(expression: str) -> str:
    """计算简单数学表达式，只允许数字和基础四则运算。"""
    allowed_nodes = (
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.FloorDiv,
        ast.Mod,
        ast.Pow,
        ast.USub,
        ast.UAdd,
        ast.Constant,
        ast.Load,
    )

    tree = ast.parse(expression, mode="eval")
    for node in ast.walk(tree):
        if not isinstance(node, allowed_nodes):
            raise ValueError("表达式中包含不允许的内容")
        if isinstance(node, ast.Constant) and not isinstance(node.value, (int, float)):
            raise ValueError("表达式只能包含数字")

    result = eval(compile(tree, "<calculate>", "eval"), {"__builtins__": {}}, {})
    return str(result)


TOOL_FUNCTIONS: dict[str, Callable[..., str]] = {
    "get_current_time": get_current_time,
    "calculate": calculate,
}


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "获取指定时区的当前时间。",
            "parameters": {
                "type": "object",
                "properties": {
                    "timezone": {
                        "type": "string",
                        "description": "IANA 时区名称，例如 Asia/Shanghai 或 America/New_York。",
                    }
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "计算简单数学表达式，例如 12 * (3 + 4)。",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "只包含数字、括号和基础运算符的数学表达式。",
                    }
                },
                "required": ["expression"],
            },
        },
    },
]


def call_llm(context_memory: list[dict[str, Any]]) -> Any:
    """推理阶段：把当前上下文交给模型。"""
    return client.chat.completions.create(
        model=MODEL_NAME,
        messages=context_memory,
        tools=TOOLS,
        tool_choice="auto",
    )


def execute_tool(tool_call: Any) -> dict[str, str]:
    """行动阶段：执行一个工具调用，并返回可写入上下文的工具反馈。"""
    function_name = tool_call.function.name
    raw_arguments = tool_call.function.arguments or "{}"

    try:
        arguments = json.loads(raw_arguments)
        tool_function = TOOL_FUNCTIONS[function_name]
        result = tool_function(**arguments)
    except Exception as error:
        result = f"工具执行失败：{error}"

    return {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": result,
    }


def run_agent(user_input: str, system_prompt: str) -> str:
    """最小并行 Agent 控制循环。"""
    context_memory: list[dict[str, Any]] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input},
    ]

    current_loop = 1
    while current_loop <= MAX_LOOP_COUNT:
        response = call_llm(context_memory)
        message = response.choices[0].message
        context_memory.append(message.model_dump(exclude_none=True))

        tool_calls = message.tool_calls or []
        if tool_calls:
            with ThreadPoolExecutor(max_workers=len(tool_calls)) as executor:
                futures = [
                    executor.submit(execute_tool, tool_call)
                    for tool_call in tool_calls
                ]
                tool_results = [future.result() for future in futures]

            context_memory.extend(tool_results)
            current_loop += 1
            continue

        return message.content or ""

    return "错误：达到最大循环次数，Agent 未能完成任务。"


def main() -> None:
    parser = argparse.ArgumentParser(description="最小并行 Agent 控制循环")
    parser.add_argument("question", nargs="*", help="用户原始问题")
    parser.add_argument(
        "--system",
        default="你是一个会按需调用工具的中文助理。信息不足时可以调用工具，工具完成后继续推理并给出最终回答。",
        help="系统提示词",
    )
    args = parser.parse_args()

    user_input = " ".join(args.question).strip()
    if not user_input:
        user_input = input("请输入你的问题：").strip()

    final_answer = run_agent(user_input, args.system)
    print(final_answer)


if __name__ == "__main__":
    main()
