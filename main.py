from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

@tool
def calculator(a: float, b:float)->str:
    """Useful for performing basic arithmietic operations with the numbers inputted"""
    print("Tool has been called")
    return f"The sum of {a} and {b} is {a+b}"
        


def main():
    # Set Groq-specific parameters
    model = ChatOpenAI(
        temperature=0,
        model="llama3-8b-8192",  # You can use "mixtral-8x7b-32768" too
        base_url="https://api.groq.com/openai/v1",  # Groq's base URL
        api_key=os.getenv("GROQ_API_KEY")  # Ensure you set this in your .env file
    )

    tools = []
    agent_executor = create_react_agent(model, tools)

    print("Welcome! I'm your AI assistant powered by Groq. Type 'quit' to exit.")
    print("You can ask me anything.")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == "quit":
            break

        print("\nAssistant: ", end="")
        for chunk in agent_executor.stream(
            {"messages": [HumanMessage(content=user_input)]}
        ):
            if "agent" in chunk and "messages" in chunk["agent"]:
                for message in chunk["agent"]["messages"]:
                    print(message.content, end="")
        print()

if __name__ == "__main__":
    main()
