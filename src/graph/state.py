from typing_extensions import Annotated, Sequence, TypedDict
import operator
from langchain_core.messages import BaseMessage
import json

def merge_dicts(a: dict[str, any], b: dict[str, any]) -> dict[str, any]:
    """Merges two dictionaries."""
    return {**a, **b}

# Define agent state
class AgentState(TypedDict):
    """Represents the state of an agent."""
    messages: Annotated[Sequence[BaseMessage], operator.add]
    data: Annotated[dict[str, any], merge_dicts]
    metadata: Annotated[dict[str, any], merge_dicts]

class CustomJSONEncoder(json.JSONEncoder):
    """
    Custom JSON encoder to handle non-serializable objects.
    """
    def default(self, o):
        if hasattr(o, 'to_dict'):
            return o.to_dict()
        if hasattr(o, '__dict__'):
            return o.__dict__
        return str(o)

def show_agent_reasoning(output, agent_name):
    """
    Prints the reasoning of an agent in a formatted way.

    Args:
        output: The output of the agent, can be a dict, list, or JSON string.
        agent_name: The name of the agent.
    """
    print(f"\n{'=' * 10} {agent_name.center(28)} {'=' * 10}")

    try:
        if isinstance(output, str):
            # If output is a string, try to parse it as JSON
            output = json.loads(output)
        
        # Pretty print the output (either parsed or already a dict/list)
        print(json.dumps(output, indent=2, cls=CustomJSONEncoder))

    except (json.JSONDecodeError, TypeError):
        # Fallback to printing the raw output if it's not valid JSON 
        # or contains non-serializable types not handled by the encoder.
        print(output)

    print("=" * 48)
