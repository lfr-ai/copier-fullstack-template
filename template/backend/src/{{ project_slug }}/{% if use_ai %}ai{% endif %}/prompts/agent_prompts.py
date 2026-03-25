"""Agent prompt templates — ReAct, function-calling, and orchestration prompts.

FIXME: All constants in this module are currently unused scaffolding.
Import and wire them into agent implementations or remove the module.
"""

from __future__ import annotations

AGENT_SYSTEM_PROMPT = (
    "You are an autonomous AI agent. You can use tools to accomplish tasks. "
    "Think step-by-step, use tools when needed, and provide clear answers."
)

AGENT_REACT_PROMPT = (
    "Answer the following question using the available tools.\n\n"
    "Available tools:\n{tools}\n\n"
    "Use this format:\n"
    "Thought: reason about what to do\n"
    "Action: tool_name\n"
    'Action Input: {{"param": "value"}}\n'
    "Observation: tool result\n"
    "... (repeat as needed)\n"
    "Thought: I have enough information\n"
    "Final Answer: the answer\n\n"
    "Question: {question}\n\n"
    "Thought:"
)

AGENT_TOOL_CALLING_PROMPT = (
    "You are an assistant with access to the following tools:\n\n"
    "{tools}\n\n"
    "To use a tool, respond with a JSON object:\n"
    '{{"tool": "tool_name", "arguments": {{"param": "value"}}}}\n\n'
    "When you have the final answer, respond with:\n"
    '{{"answer": "your final answer"}}\n\n'
    "Task: {task}\n\n"
    "Response:"
)

AGENT_PLANNER_PROMPT = (
    "Break down the following goal into a step-by-step plan. "
    "Each step should be a concrete, actionable task.\n\n"
    "Available agents: {agents}\n\n"
    "Goal: {goal}\n\n"
    "Return a numbered list of steps, each with:\n"
    "- Step description\n"
    "- Which agent should handle it\n"
    "- Expected output\n\n"
    "Plan:"
)

AGENT_ORCHESTRATOR_PROMPT = (
    "You are an orchestrator managing multiple AI agents to accomplish a goal.\n\n"
    "Available agents:\n{agents}\n\n"
    "Current plan:\n{plan}\n\n"
    "Results so far:\n{results}\n\n"
    "Current step: {current_step}\n\n"
    "Decide: should we proceed, adjust the plan, or finalize?\n\n"
    "Decision:"
)
