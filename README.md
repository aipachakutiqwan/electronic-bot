# Electronic-Bot

Electronic Bot manage questions about four topics:
1. Electronics products.
2. Orders.
3. Return policies.
4. General questions managed by the gpt-3.5-turbo model.

The bot uses the data in json format located in ```./data ``` to answer questions about orders and products.

For return policies, the bot uses  a Retrieval Argumented Generation (RAG) approach to query information from the document located in  ```./src/data/rag/docs/returns_policies/return_policies.pdf. ```

## Architecture

The following diagram describe the application architecture with its different components and how is managed the conversational flow.

![Architecture](./docs/architecture.png?  "Title")



## How run the bot application?

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

- Questions about products
```
Welcome to Electronic BOT, we are able to answer questions about products, orders and return policies.

You: hello, could you help me with some questions?
Electronic Bot: Of course! I'm here to help. What questions do you have about our products?

You: could you give me information about gamming consoles?
Electronic Bot: Sure! We have a couple of gaming consoles and accessories available. 
One option is the GameSphere X, a next-generation gaming console by GameSphere. It features 4K gaming, 1TB storage, backward compatibility, and online multiplayer. It comes with a 1-year warranty and is priced at $499.99. 
We also have the ProGamer Controller, a high-quality gaming controller by ProGamer. It has an ergonomic design, customizable buttons, wireless connectivity, and a rechargeable battery. It also comes with a 1-year warranty and is priced at $59.99.
Is there anything specific you would like to know about these gaming consoles or any other gaming accessories?

You: which is the best for profesional gamers GameSphere X or ProGamer Controller?
Electronic Bot: Both the GameSphere X and ProGamer Controller are excellent options for professional gamers, but they serve different purposes. 
The GameSphere X is a next-generation gaming console that offers 4K gaming, 1TB storage, backward compatibility, and online multiplayer. It provides a complete gaming experience with advanced features and high-quality graphics. 
On the other hand, the ProGamer Controller is a high-quality gaming controller with an ergonomic design, customizable buttons, wireless connectivity, and a rechargeable battery. It is designed to enhance precision and comfort during gameplay.
Ultimately, the choice between the GameSphere X and ProGamer Controller depends on your specific needs and preferences. If you are looking for a comprehensive gaming experience with advanced features, the GameSphere X would be a great choice. If you prefer a high-quality controller that offers customization options and comfort, the ProGamer Controller would be a suitable option.
Do you have any specific requirements or preferences that can help me provide a more tailored recommendation?



```


