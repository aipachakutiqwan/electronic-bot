import time
from src.utils import utils
from src.models.products import Products
from src.models.orders import Orders
from src.controllers.rag import Rag


class ChatEngine:

    def __init__(self):
        self.rag = Rag()
        self.delimiter = "```"

    def validate_response(self, user_input, final_response, system_message, user_message, all_messages, debug=True):

        # Step 4: Ask the model if the response answers the initial user query well
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
            print("Step 6: Model evaluated the response.")


        # Step 5: If yes, use this answer; if not, say that you will connect the user to a human
        if "Y" in evaluation_response:
            if debug: print("Step 7: Model approved the response.")
            return final_response, all_messages
        else:
            if debug: print("Step 7: Model disapproved the response.")
            neg_str = "I'm unable to provide the information you're looking for. \
            I'll connect you with a human representative for further assistance."
            return neg_str, all_messages


    def process_products_intents(self, user_input, all_messages, debug=True):

        # Step 1: Find the categories and products from the input message.
        #         Parse to json the categories and products found.
        find_category_and_product_only = Products().find_category_and_product_only(user_input,
        Products().get_products_and_category())
        if debug:
            print(f'find_category_and_product_only: {find_category_and_product_only}')
        parsed_category_and_product_list = utils.parse_string_to_json(find_category_and_product_only)
        if debug:
            print(f'parsed_category_and_product_list: {parsed_category_and_product_list}')
            print("Step 2: Extracted list of products.")

        # Step 2: List all the products from the parsed list parsed_category_and_product_list.
        #         This information will be used to response to the user question
        product_information = Products().generate_output_string(parsed_category_and_product_list)
        if debug:
            #print(f'product_information: {product_information}')
            print("Step 3: Looked up product information.")

        # Step 3: Answer the user question
        system_message = f"""
        You are a customer service assistant for a electronic store. \
        Respond in a friendly and helpful tone, with concise answers. \
        Make sure to ask the user relevant follow-up questions.
        """
        messages = [
            {'role': 'system', 'content': system_message},
            {'role': 'user', 'content': f"{self.delimiter}{user_input}{self.delimiter}"},
            {'role': 'assistant', 'content': f"Relevant product information:\n{product_information}"}
        ]

        final_response = utils.get_completion_from_messages(all_messages + messages)
        if debug:
            print(f'final_response to the user: {final_response}')
            print("Step 4: Generated response to user question.")
        all_messages = all_messages + messages[1:]

        return self.validate_response(user_input, final_response, system_message, user_message, all_messages, debug)



    def process_orders_intents(self, user_input, all_messages, debug=True):

        # Step 1: Answer the user question about orders
        list_orders = Orders().get_orders()
        system_message = f"""
        You are a customer service assistant for a electronic store. \
        Respond in a friendly and helpful tone, with concise answers. \
        Make sure to ask the user relevant follow-up questions.
        """
        messages = [
            {'role': 'system', 'content': system_message},
            {'role': 'user', 'content': f"{self.delimiter}{user_input}{self.delimiter}"},
            {'role': 'assistant', 'content': f"Relevant orders information:\n{list_orders}"}
        ]

        final_response = utils.get_completion_from_messages(all_messages + messages)
        if debug:
            print(f'final_response to the user: {final_response}')
            print("Step 4: Generated response to user question.")
        all_messages = all_messages + messages[1:]

        return self.validate_response(user_input, final_response, system_message, user_message, all_messages, debug)


    def process_user_message(self, user_message, context, chat_history, debug=True):
        if debug:
            print(f'context: {context}')
            print(f'chat_history: {chat_history}')

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
            return self.process_products_intents(user_message, context, debug)
        elif classified_message['category'] == 'Orders':
            if debug:
                print(f'Message classified as : {classified_message["category"]}')
            return self.process_orders_intents(user_message, context, debug)
        elif classified_message['category'] == 'Return Policies':
            if debug:
                print(f'Message classified as : {classified_message["category"]}')
            # TODO: merge chat_history and context
            answer, chat_history = self.rag.query(user_message, chat_history, debug)
            return answer, context
        else:
            if debug:
                print(f'Message unclassified.')
            messages = [{"role": "user", "content": user_message}]
            response = utils.get_completion_from_messages(messages)
            #neg_str = f"I'm unable to provide the information you're looking for. I'll connect you with a human representative for further assistance."
            return response, context

if __name__ == "__main__":

    context = [ {'role':'system', 'content':"You are Service Assistant"} ]
    chat_history = []
    #user_message = "tell me about the smartx pro phone and the fotosnap camera, the dslr one. Also what tell me about your tvs"
    CHAT_ENGINE = ChatEngine()
    #user_message = "tell me about audio systems"
    #response,_ = CHAT_ENGINE.process_products_intents(user_message, [], debug=False)
    #print(response)
    #user_message = f"""I want to know about my order"""
    #user_message = f"""which products do you have?"""
    #user_message = f"""do you know anything about the order order_001"""
    #user_message = f"""what is the status of the order_002"""
    #user_message = f"""could you let me know about the return policies?"""
    user_message = f"""hello"""
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
            answer, context = CHAT_ENGINE.process_user_message(user_message, context, chat_history, debug=True)
            print(f"Electronic Bot: {answer}")
            print(f'\n')

