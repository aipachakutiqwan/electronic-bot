"""
Chat engine class manage the bot conversation about products, orders and return policies.
"""
import time
from src.utils import utils
from src.models.products import Products
from src.models.orders import Orders
from src.controllers.rag import Rag


class ChatEngine:

    def __init__(self):
        self.rag = Rag()
        self.delimiter = "```"

    def validate_response(self, user_input, final_response, system_message, all_messages, debug=True):
        """
        Validate the response of the bot, if the bot it is not responding the user question,
        a human forwarding message will be provided.
        Args:
            :param user_input: original user input message
            :param final_response: response bot
            :param system_message: system content message
            :param all_messages: history messages
        Returns:
            :returns final_response, all_messages: string text response and all history messages
        """

        #Ask the model if the response answers the user query well
        user_message = f"""
        Customer message: {self.delimiter}{user_input}{self.delimiter}
        Agent response: {self.delimiter}{final_response}{self.delimiter}

        Does the response sufficiently answer the question?
        """
        messages = [
            {'role': 'system', 'content': system_message},
            {'role': 'user', 'content': user_message}
        ]
        evaluation_response = utils.get_completion_from_messages(messages)
        if debug:
            print(f'Evaluation to the user response: {evaluation_response}')

        # If yes, use this answer; if not, say that you will connect the user to a human
        if "Y" in evaluation_response:
            if debug: print("Model approved the response.")
            return final_response, all_messages
        else:
            if debug: print("Model disapproved the response.")
            neg_str = "I'm unable to provide the information you're looking for. \
            I'll connect you with a human representative for further assistance."
            return neg_str, all_messages


    def process_products_intents(self, user_input, all_messages, debug=True):
        """
        Process the user questions classified as products,
        lookup the products data for answer the questions.
        Args:
            :param user_input: original user input message about products
            :param all_messages: history messages
        Returns:
            :returns final_response, all_messages: string text response and all history messages
        """

        # Find the categories and products from the input message.
        # Parse to json the categories and products found.
        find_category_and_product_only = Products().find_category_and_product_only(user_input,
        Products().get_products_and_category())
        if debug:
            print(f'find_category_and_product_only: {find_category_and_product_only}')
        parsed_category_and_product_list = utils.parse_string_to_json(find_category_and_product_only)
        if debug:
            print(f'Extracted list of products.: {parsed_category_and_product_list}')

        # List all the products from the parsed list parsed_category_and_product_list.
        # This information will be used to response to the user question
        product_information = Products().generate_output_string(parsed_category_and_product_list)
        if debug:
            print("Looked up product information: {product_information}")

        # Answer the user question about products
        system_message = f"""
        You are a customer service assistant for a electronic store. \
        Respond in a friendly and helpful tone about products, with concise answers. \
        Make sure to ask the user relevant follow-up questions.
        """
        messages = [
            {'role': 'system', 'content': system_message},
            {'role': 'user', 'content': f"{self.delimiter}{user_input}{self.delimiter}"},
            {'role': 'assistant', 'content': f"Relevant product information:\n{product_information}"}
        ]

        final_response = utils.get_completion_from_messages(all_messages + messages)
        if debug:
            print("Generated response to user question: {final_response}")
        all_messages = all_messages + messages[1:]

        return self.validate_response(user_input,
                                      final_response, system_message, all_messages, debug)



    def process_orders_intents(self, user_input, all_messages, debug=True):
        """
        Process the user questions classified as orders,
        use the orders data to answer the questions.
        Args:
            :param user_input: original user input message about orders
            :param all_messages: history messages
        Returns:
            :returns final_response, all_messages: string text response and all history messages
        """
        # Answer the user question about orders
        list_orders = Orders().get_orders()
        system_message = f"""
        You are a customer service assistant for a electronic store. \
        Respond in a friendly and helpful tone about orders, with concise answers. \
        Make sure to ask the user relevant follow-up questions.
        """
        messages = [
            {'role': 'system', 'content': system_message},
            {'role': 'user', 'content': f"{self.delimiter}{user_input}{self.delimiter}"},
            {'role': 'assistant', 'content': f"Relevant orders information:\n{list_orders}"}
        ]
        final_response = utils.get_completion_from_messages(all_messages + messages)
        if debug:
            print("Generated response to user question: {final_response}")
        all_messages = all_messages + messages[1:]
        return self.validate_response(user_input, final_response,
                                      system_message, all_messages, debug)


    def process_user_message(self, user_message, context, rag_retrieval_history, debug=True):
        """
        Classify the users questions as products, orders, return policies or general questions.
        For products and orders use the application databases (json files) and for return policies
        use the Retrieval Argument Generation Method which retrieve the information from the return policies document.
        Args:
            :param user_message: user question
            :param context: initial context role for the bot which will be used to store all history messages
            :param rag_retrieval_history: RAG messages history interaction
        Returns:
            :returns response: string response to the user question
            :returns context: all interaction messages produced
            :returns rag_retrieval_history: all interaction messages using RAG approach
        """
        if debug:
            print(f'context: {context}')
            print(f'rag_retrieval_history: {rag_retrieval_history}')

        delimiter = "####"
        system_message = f"""
        You will be provided with customer service queries. \
        The customer service query will be delimited with \
        {delimiter} characters.
        Classify each query into a category. \
        Provide your output in json format with the \
        keys: category.
        categories: Products, Orders, \
        Return Policies.
        """
        messages =  [
        {'role':'system',
         'content': system_message},
        {'role':'user',
         'content': f"{delimiter}{user_message}{delimiter}"},
        ]
        response = utils.get_completion_from_messages(messages)
        classified_message = utils.parse_string_to_json(response)
        if classified_message['category'] == 'Products':
            if debug:
                print(f'Message classified as : {classified_message["category"]}')
            answer, context = self.process_products_intents(user_message, context, debug)
            return (answer, context, rag_retrieval_history)
        elif classified_message['category'] == 'Orders':
            if debug:
                print(f'Message classified as : {classified_message["category"]}')
            answer, context = self.process_orders_intents(user_message, context, debug)
            return (answer, context, rag_retrieval_history)
        elif classified_message['category'] == 'Return Policies':
            if debug:
                print(f'Message classified as : {classified_message["category"]}')
            answer, rag_retrieval_history = self.rag.query(user_message, rag_retrieval_history, debug)
            return (answer, context, rag_retrieval_history)
        else:
            # If the user message is not below the categories,
            # the bot will try to give an answer using the general knowledge
            if debug:
                print(f'Message unclassified. Bot will try to answer a general question')
            messages = [{"role": "user", "content": user_message}]
            response = utils.get_completion_from_messages(messages)
            return (response, context, rag_retrieval_history)

if __name__ == "__main__":

    context = [ {'role':'system', 'content':"You are Service Assistant"} ]
    rag_retrieval_history = []
    #user_message = "tell me about the smartx pro phone and the fotosnap camera, the dslr one. Also what tell me about your tvs"
    CHAT_ENGINE = ChatEngine()
    #user_message = "tell me about audio systems"
    #response,_ = CHAT_ENGINE.process_products_intents(user_message, [], debug=False)
    #print(response)
    #user_message = f"""I want to know about my order"""
    user_message = f"""which products do you have?"""
    #user_message = f"""do you know anything about the order order_001"""
    #user_message = f"""what is the status of the order_002"""
    #user_message = f"""could you let me know about the return policies?"""
    #user_message = f"""hello"""
    #CHAT_ENGINE.process_user_message(user_message, context, debug=False)

    exit_conditions = (":q", "quit", "exit")

    print(f'\nWelcome to Electronic BOT, we are able to answer questions about products, orders and return policies.\n')

    while True:
        user_message = input("You: ")
        if len(user_message.rstrip())==0:
            continue
        if user_message in exit_conditions:
            break
        else:
            answer, context, rag_retrieval_history = \
            CHAT_ENGINE.process_user_message(user_message, context,
                                             rag_retrieval_history, debug=False)
            print(f"Electronic Bot: {answer}")
            print(f'\n')

