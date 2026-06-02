from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="qwen2.5:3b")

code_to_review = """
import boto3
client = boto3.client('s3', aws_access_key_id='AKIAIOSFODNN7EXAMPLE')
"""

prompt = "Review this code for security issues:\n" + code_to_review

result = llm.invoke(prompt)

print(result)