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
```console
Welcome to Electronic BOT, we are able to answer questions about products, orders and return policies.
```
```console
You: hello, could you help me with some questions?
```
```console
Electronic Bot: Of course! I'm here to help. What questions do you have about our products?
```
```console
You: could you give me information about gamming consoles?
```
```console
Electronic Bot: Sure! We have a couple of gaming consoles and accessories available. Here are some details:
1. GameSphere X:
   - Brand: GameSphere
   - Model Number: GS-X
   - Features: 4K gaming, 1TB storage, backward compatibility, online multiplayer
   - Description: A next-generation gaming console for the ultimate gaming experience.
   - Price: $499.99
   - Warranty: 1 year
   - Rating: 4.9 out of 5
2. ProGamer Controller:
   - Brand: ProGamer
   - Model Number: PG-C100
   - Features: Ergonomic design, customizable buttons, wireless, rechargeable battery
   - Description: A high-quality gaming controller for precision and comfort.
   - Price: $59.99
   - Warranty: 1 year
   - Rating: 4.2 out of 5
Let me know if you have any specific questions or if there's anything else I can assist you with!
```
```console
You: which is the best for profesional gamers GameSphere X or ProGamer Controller?
```
```console
Electronic Bot: Both the GameSphere X and the ProGamer Controller are excellent options for professional gamers, but they serve different purposes. 
The GameSphere X is a next-generation gaming console that offers 4K gaming, 1TB storage, backward compatibility, and online multiplayer. It provides a complete gaming experience with advanced features and high-quality graphics.
On the other hand, the ProGamer Controller is a high-quality gaming controller designed for precision and comfort. It features an ergonomic design, customizable buttons, wireless connectivity, and a rechargeable battery. It is a great choice for gamers who prefer using a controller for their gaming sessions.
Ultimately, the choice between the GameSphere X and the ProGamer Controller depends on your specific needs and preferences. If you are looking for a complete gaming system with advanced features, the GameSphere X would be a suitable option. However, if you already have a gaming console and are looking for a high-quality controller, the ProGamer Controller would be a great choice.
Do you have any specific requirements or preferences that can help me provide a more tailored recommendation?
```
```console
You: ok, I will decide later about gamming consoles. Another question, what is the best laptop available at this moment?
```
```console
Electronic Bot: The best laptop available at the moment is the TechPro Desktop. It features an Intel Core i7 processor, 16GB RAM, 1TB HDD, and NVIDIA GeForce GTX 1660 graphics. It is a powerful desktop computer suitable for both work and play. The price for the TechPro Desktop is $999.99. Is there anything else I can assist you with?
```
- Questions about orders

```console
You: ok thanks for the laptop information. by the way what about my order 003, do you have any information?
```
```console
Electronic Bot: Thank you for providing your order number. Let me check the status of your order 003 for you. 
After checking, I can see that your order 003, which includes the ZoomMaster Camcorder, is currently in transit. The estimated delivery date is scheduled for November 19th, 2023. 
If you have any further questions or need assistance with anything else, please let me know.
```
```console
You: Great, and did you received my order 002?
```
```console
Electronic Bot: Yes, we have received your order 002. It is currently marked as "Received" and the status was updated on November 18th at 08:25. The total amount for this order is $99.99. The product in this order is the WaveSound Soundbar from the brand WaveSound. Is there anything else I can assist you with regarding your order?
```
```console
You: good, what about the order number 999?     
```
```console
Electronic Bot: I apologize, but I couldn't find any information about order number 999. Could you please provide me with the correct order number or any other details related to your order?
```
- Questions about return policies

```console
You: ok, I think I am confusing the order number. One last thing, I would like to know about your return policies, what the the return period for a product?
```
```console
Electronic Bot: The return period for most items at Electronic bot is 30 days from the receipt of delivery.
```
```console
You: ok, good to know about the return period but how could I return a product?
```
```console
Electronic Bot: You can return a product by following these steps:
1. Visit the Electronic bot Returns Support Centre.
2. Select the item you want to return and the reason for the return.
3. Choose your preferred return method from the available options, such as drop off services, specialty carrier team, locker and Electronic bot Hub Counter locations, or using a scanned QR code at designated return locations.
4. If eligible, you may receive a pre-paid returns label to use for the return.
5. Package the item securely, ensuring it is in the same condition as when you received it.
6. Attach the returns label to the package, if provided.
7. Drop off the package at the designated return location or arrange for a pickup, depending on the chosen return method.
Please note that certain types of items may not be eligible for return or cancellation. It is important to review the Conditions of Use & Sale for more information on eligibility and instructions for cancellation.
```
```console
You: fine, and what about the removal of personal data when I return a product, may I have more details about that?
```
```console
Electronic Bot: When returning a product to Electronic bot, you are required to delete, remove, and eliminate all personal data that pertains to you or any third party that may be present on the item. You must also delink any account that may be associated with the item. Failure to do so may result in a data breach for which you will be held responsible. Additionally, you must remove any items from the returned product and its box that do not pertain to the original item received from Electronic bot.
```
```console
You: it was good to know about this personal data removal when I return products, one last question, how could I contact you If I returned a wrong item?
```
```console
Electronic Bot: To contact us regarding a returned wrong item, please email us at customerservice@electronicbot.com as soon as possible.
```
```console
You: ok, that is fine, thanks for all the provided information, it was very helpful.   
```
```console
Electronic Bot: You're welcome! I'm glad I could help. If you have any more questions in the future, feel free to ask. Have a great day!
```
```console
Electronic Bot: You're welcome! Goodbye and take care!
```



