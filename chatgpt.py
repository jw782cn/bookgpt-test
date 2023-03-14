import openai
import os
import logging
import utils
import json

# handle chatgpt session and get responses

class ChatGPT():
    def __init__(self, logger=None, model=None) -> None:
        # parameters
        self.default_system_prompt = None
        self.model = None
        self.prompt_failure_times = None
        self.log_conversation = None 
        self.conversation_file_path = None
        
        # configuration
        self._get_config()
    
        # logging
        self.logger = logger
        self.conversation_logger = None
        self._conversation_logger()

        # set model
        if model:
            self.model = model
        self.messages = []
        self.num_tokens = 0
        self.num_tokens
        self.apikey = None

        # settings
        self._set_apikey()

        # TODO: can be stored in database
        # record messages and responses in history in this format {"message": message, "response": response, "num_tokens": num_tokens}
        self.history = []
        
    # high level function to send message and get response
    def send_message(self, user_message, system_message=None, make_json=False):
        if make_json:
            # make sure the response is json, try again if not, maximum prompt_failure_times
            fail = 0
            # TODO: retry methods can be flexible
            # e.g. use different prompt, use different temperature, use different top_p
            while fail < self.prompt_failure_times:
                response = self._send_message(user_message, system_message)
                try:
                    response = json.loads(response)
                    if self.logger:
                        self.logger.info(f"Success: Got json response")
                    return response
                except:
                    if self.logger:
                        self.logger.error(f"Fail {fail+1}: Cannot get json response, retrying...")
                fail += 1
            if self.logger:
                self.logger.error(f"Fail {fail+1}: Cannot get json response, giving up")
            return None
        else:
            return self._send_message(user_message, system_message)
        

    # send message and get response
    def _send_message(self, user_message, system_message=None):
        if not system_message:
            # default system message
            system_message = self.default_system_prompt
        # log usage before sending message
        # only log usage for gpt-3.5-turbo-0301
        if self.model == "gpt-3.5-turbo-0301":
            num_tokens_before = utils.num_tokens_from_messages(
                self.messages, model=self.model)
            if self.logger:
                self.logger.info(
                    f"Sending message, num_tokens_before: {num_tokens_before}")
        else:
            if self.logger:
                self.logger.info(
                    "Sending message!")
            if self.log_conversation:
                # only log conversation when log_conversation is True
                self.conversation_logger.info(f"Conversation: {len(self.history)}\n")
                self.conversation_logger.info(f"System: {system_message}")
                self.conversation_logger.info(f"User: {user_message}")
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ]
        # print(messages)
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
        )
        # log usage'usage': {'prompt_tokens': 56, 'completion_tokens': 31, 'total_tokens': 87}
        usage = response["usage"]
        finish_reason = response['choices'][0]['finish_reason']
        response_message = str(response['choices'][0]['message']['content'])
        # Every response will include a finish_reason. The possible values for finish_reason are:
        # stop: API returned complete model output
        # length: Incomplete model output due to max_tokens parameter or token limit
        # content_filter: Omitted content due to a flag from our content filters
        # null: API response still in progress or incomplete
        if finish_reason == "stop":
            if self.log_conversation:
                # only log conversation when log_conversation is True
                self.conversation_logger.info(f"Response: {response_message}")
                self.conversation_logger.info(f"Usage: {usage['total_tokens']}\n")
            if self.logger:
                self.logger.info(f"Response got!")
            # TODO: may use database to store history
            self.history.append(
                {"message": user_message, "response": response_message, "num_tokens": usage["total_tokens"]})
            return response_message
        else:
            if self.logger:
                self.logger.warning(
                    f"Response finished with reason: {finish_reason}")
            if self.log_conversation:
                # only log conversation when log_conversation is True
                self.conversation_logger.warning(f"Conversation: {len(self.history)} failed\n")
            return None

    # get system configuration
    def _get_config(self):
        config = utils.json_read("config.json")
        self.default_system_prompt = config["default_system_prompt"]
        self.model = config["model"]
        self.prompt_failure_times = config["prompt_failure_times"]
        self.log_conversation = config["log_conversation"]
        self.conversation_file_path = config["conversation_file_path"]
    
    # set conversation logger in chatgpt
    def _conversation_logger(self):
        if self.log_conversation:
            self.conversation_logger = logging.getLogger("conversation")
            self.conversation_logger.setLevel(logging.INFO)
            fh = logging.FileHandler(self.conversation_file_path)
            fh.setLevel(logging.INFO)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            fh.setFormatter(formatter)
            self.conversation_logger.addHandler(fh)
            if self.logger:
                self.logger.info("Set conversation logger")
        
    # set api key
    def _set_apikey(self, apikey=None):
        if apikey:
            self.apikey = apikey
        else:
            # You can set your API key in the environment variable OPENAI_API_KEY
            self.apikey = os.environ.get('OPENAI_API_KEY')
        if self.logger:
            self.logger.info("Set API key to " + self.apikey)
