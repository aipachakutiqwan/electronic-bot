# Electronic-Bot

Electronic Bot manage questions about four topics:
1. Electronics products.
2. Orders.
3. Return policies.
4. General questions managed by the gpt-3.5-turbo model.

The bot uses the data in json format located in ```./data ``` to answer questions about orders and products.

For return policies, the bot uses  a Retrieval Argumented Generation (RAG) approach to query information from the documents located in  ```./src/data/rag/docs/returns_policies/return_policies.pdf. ```

## How run the bot application?:

Follow the next steps to interact with the bot by command line.

1. Set your own OPENAI_API_KEY in .env file
2. Install libraries: 
```python 
pip install .
```
2. Run chatbot: 
```python 
python3 src/controllers/chat_engine.py
```

## Conversation examples:

Questions about products:


