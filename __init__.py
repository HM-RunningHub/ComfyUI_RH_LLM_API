from .node import *

NODE_CLASS_MAPPINGS = {
                        "RH_LLMAPI_NODE": RH_LLMAPI_Node,
                    }
NODE_DISPLAY_NAME_MAPPINGS = {
    "RH_LLMAPI_NODE": "Runninghub LLM API Node",
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']