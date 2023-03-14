import tiktoken
import json
import logging

# read a text file
def file_read_from_txt(path: str):
    try:
        with open(path, 'r') as f:
            return f.read()
    except:
        return None
    
# read a json file
def json_read(path: str):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except:
        return None
    
# get logger for system message, in status.log
def get_logger(logging_file_path):
    logger = logging.getLogger(logging_file_path)
    logger.setLevel(logging.DEBUG)

    # Create a file handler and set its level
    file_handler = logging.FileHandler(logging_file_path)
    file_handler.setLevel(logging.DEBUG)

    # Create a formatter and add it to the handler
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(file_handler)
    # Test the logger
    # logger.debug('This is a debug message')
    # logger.info('This is an info message')
    # logger.warning('This is a warning message')
    # logger.error('This is an error message')
    # logger.critical('This is a critical message')
    logger = logger
    logger.info('logger set!')
    return logger

# tokenize a text
def text_to_chunks(texts, word_length=1000, start_page=1):
    words = texts.split(' ')
    # print(len(words))
    chunks = []
    for i in range(0, len(words), word_length):
        chunk = words[i:] if i + word_length > len(words) else words[i:i + word_length]
        # print(len(chunk))
        chunk = ' '.join(chunk).strip()
        chunk = f'[{i // word_length + start_page}]' + ' ' + chunk
        # print(len(chunk))
        chunks.append(chunk)
    return chunks

# calculate the number of tokens used by a list of messages [provided by OpenAI]
def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301"):
  """Returns the number of tokens used by a list of messages."""
  try:
      encoding = tiktoken.encoding_for_model(model)
  except KeyError:
      encoding = tiktoken.get_encoding("cl100k_base")
  if model == "gpt-3.5-turbo-0301":  # note: future models may deviate from this
      num_tokens = 0
      for message in messages:
          num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
          for key, value in message.items():
              num_tokens += len(encoding.encode(value))
              if key == "name":  # if there's a name, the role is omitted
                  num_tokens += -1  # role is always required and always 1 token
      num_tokens += 2  # every reply is primed with <im_start>assistant
      return num_tokens
  else:
      raise NotImplementedError(f"""num_tokens_from_messages() is not presently implemented for model {model}.
  See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")