from setuptools import setup, find_packages

setup(
    name='agentbridge',  # Replace with your desired library name
    version='0.1.0',  # Start with an initial version
    description='Orchestrate LLMs in a multi agent system using Langchain and/or Llama index. Manage agent interactions, task routing, and knowledge sharing', 
    long_description=open('README.md').read(), 
    author='Siddhesh Sathe',
    author_email='thesidsat@gmail.com',
    packages=find_packages(),  
    install_requires=[
        'langchain_community==0.0.24',
        'langchain_core==0.1.26',
        'langchain_openai==0.0.7',
        'llama_index==0.10.12'
    ],
)
