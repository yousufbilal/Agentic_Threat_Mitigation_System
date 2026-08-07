# from langchain_ollama import ChatOllama
# from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# llm = ChatOllama(model="qwen2.5:3b", temperature=0)

# def my_chat_bot():
#     conversation_history = [
#         SystemMessage(content="You are a helpful assistant.")
#     ]

#     while True:
#         print(conversation_history)
#         user_input = input("You: ")

#         if user_input.lower() == "exit":
#             # print("Exiting the chat bot.")
#             break

#         conversation_history.append(HumanMessage(content=user_input))

#         response = llm.invoke(conversation_history)
#         # print("Bot:", response.content)

#         conversation_history.append(AIMessage(content=response.content))

# if __name__ == "__main__":
#     my_chat_bot()