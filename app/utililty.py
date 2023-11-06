
from langchain.chains.router import MultiPromptChain
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
from langchain.chains.router.llm_router import LLMRouterChain, RouterOutputParser
from langchain.chains.router.multi_prompt_prompt import MULTI_PROMPT_ROUTER_TEMPLATE
import torch
from langchain.llms import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig, pipeline
from langchain.chains import LLMChain, SequentialChain
from langchain.memory import ConversationTokenBufferMemory
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.agents import initialize_agent,LLMSingleActionAgent ,Tool, AgentType ,AgentExecutor
from prompts import *
import requests
import re
from langchain.memory import ConversationSummaryMemory, ChatMessageHistory
from conversation import get_conv_template
from prompts import *
from difflib import get_close_matches

def preprocess_instance(source):
    conv = get_conv_template("ie_as_qa")
    for j, sentence in enumerate(source):
        value = sentence['value']
        if j == len(source) - 1:
            value = None
        conv.append_message(conv.roles[j % 2], value)
    prompt = conv.get_prompt()
    return prompt

def get_response(responses):
    responses = [r.split('ASSISTANT:')[-1].strip() for r in responses]
    return responses


def llm_load(MODEL_NAME):
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=True,  trust_remote_code=True)

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME, torch_dtype=torch.float32, trust_remote_code=True, device_map="auto"
    )

    generation_config = GenerationConfig.from_pretrained(MODEL_NAME)
    generation_config.max_new_tokens = 500
    generation_config.temperature = 0.0001
    generation_config.top_p = 0.95
    generation_config.do_sample = True
    generation_config.repetition_penalty = 1.15

    text_pipeline = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        return_full_text=True,
        generation_config=generation_config,
    )

    llm = HuggingFacePipeline(pipeline=text_pipeline, model_kwargs={"temperature": 0})
    
    return llm


def chain_destinations(llm ):
    # Create destination chains for each prompt
    destination_chains = {}
    for p_info in prompt_infos:
        name = p_info["name"]
        prompt_template = p_info["prompt_template"]
        prompt = PromptTemplate(template=prompt_template, input_variables=["input", 'history'])
        chain = LLMChain(llm=llm, prompt=prompt)
        destination_chains[name] = chain
    return destination_chains
        
def chain_selection(llm, query):
    memory = ConversationBufferWindowMemory( memory_key="history", input_key="input")
    # Create a default chain
    default_chain = ConversationChain(llm=llm, output_key="text", memory = memory)
    destinations = [f"{p['name']}: {p['description']}" for p in prompt_infos]
    destinations_str = "\n".join(destinations)


    router_template = MULTI_PROMPT_ROUTER_TEMPLATE.format(destinations=destinations_str)
    router_prompt = PromptTemplate(
        template=router_template,
        input_variables=["input"],
        output_parser=RouterOutputParser(),
    )
    router_chain = LLMRouterChain.from_llm(llm, router_prompt, verbose=True)
    router_response = router_chain(query)
    dist = router_response['destination']

    return dist

def prompting_selction(template, llm):
    memory = ConversationBufferWindowMemory(memory_key="history", input_key="input")
    prompt = PromptTemplate(input_variables=["input","history"], template=template)
    chain = ConversationChain(llm=llm, memory=memory, prompt=prompt, verbose=False)
    return chain


def prompting_selction_routed(template, llm, history):
    # memory = ConversationSummaryMemory(
    #     llm=llm,
    #     buffer="you are a smart assistant that alwys remeber what had been said to you and follow the instruction mention in the prompt",
    #     chat_memory=history,
    #     return_messages=True
    # )
    memory = ConversationBufferWindowMemory(memory_key="history", input_key="input")
    prompt = PromptTemplate(input_variables=["input","history"], template=template)
    chain = ConversationChain(llm=llm, memory=memory, prompt=prompt, verbose=False)
    return chain , memory

def filter_string(input_string):
    cleaned_string = input_string.replace('"', '').replace(',', '').replace(';', '').replace(':', '')
    return cleaned_string
def escape_removal(input_string):
    cleaned_string = input_string.replace("\\", '')
    return cleaned_string
def entity_name_standarization(input_string):
    cleaned_string = input_string.replace('\\', '').replace('_', '').replace(';', '').replace(':', '').replace(' ','')
    return cleaned_string.lower()
    

def neom_apis(pload, url, token=None):
    url = url
    payload = pload

    headers = {
        'x-api-secret': 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcGlrZXkiOiJmZTZmOTQ0MC02NDUwLTExZWQtODdjZS04ZjNkMjZhZTM4ZmEiLCJyZXNvdXJjZXMiOlsidXNlciIsInJlcXVlc3QiXSwiaWF0IjoxNjY4NDUzNDU0LCJleHAiOjE3MDAwMTEwNTQsImF1ZCI6ImhvbG9ncmFtLXRlc3RpbmciLCJpc3MiOiJnYS1hcGktc2VydmljZXMtZGV2In0.pkyv0c7fyCGJ3rCaSVLGTnhYWaQ_pLUv8dbZe6YbFJtxIH6v_vuTzGUQ_ep4TZnIn0G_iIJ3qVjwIlLx2NHXH5ywomy34zcOA0xwBBEv1Moh4viVSVuKIVAkTjMJ7iT7ZC09M0JutqXuBiMnBICVSSQq-HNY3YRwvNl6aWlLH_FDi8HxUGae2NKrxMjI33rP81WUPnX63P9E3GFgBUIlAy61L6FL2qOZ29s9FmPwTjBJSDv02311wF3sSI45wMgfneKBMquNmaxY2UUz1Fsprb_PJXWkM9fslAlxb34UJVKjHhUnNlZa8Fu9PSQ5cPA6h-aNFurBL-CZTsk1b1aoSg',
        'systemId': 'Hologram App',
        'timestamp': '2022-09-05T08:15:30-05:00',
        'messageId': '02fbdf20-78c6-4f96-af02-bc3fb1ae6cf5',
        'x-api-key': 'fe6f9440-6450-11ed-87ce-8f3d26ae38fa',
        'Authentication': 'Bearer ' + token if token else '',
    }
    
    print('token:', token)

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.text

def entity_exctraction( query, generator, entity_types, assigned_types ):    
    
    best_entity = None
    best_output = None
    difference = [item for item in entity_types if item not in assigned_types]

    for entity_type in difference:
        example = {"conversations": [{"from": "human", "value": f"Text: {query}"}, {"from": "gpt", "value": "I've read this text."}, {"from": "human", "value": f"What describes {entity_type} in the text?"}, {"from": "gpt", "value": "[]"}]}
        prompt = preprocess_instance(example['conversations'])
        outputs = generator(prompt, max_length=256, return_full_text=False)
        if not best_output or len(outputs[0]['generated_text']) > len(best_output):
            best_output = outputs[0]['generated_text']
            best_entity = entity_type
    if not best_output :
        return None, None
    else:
        return best_entity , best_output
    
def check_nested_key_existence(dictionary, key):
    if isinstance(dictionary, dict):
        if key in dictionary:
            return True
        for k in dictionary:
            if isinstance(dictionary[k], dict) or isinstance(dictionary[k], list):
                result = check_nested_key_existence(dictionary[k], key)
                if result:
                    return True
    elif isinstance(dictionary, list):
        for item in dictionary:
            result = check_nested_key_existence(item, key)
            if result:
                return True
    return False

def change_key_value(dictionary, key, new_value):
    if isinstance(dictionary, dict):
        for k in dictionary:
            if k == key:
                dictionary[k] = new_value
            elif isinstance(dictionary[k], dict) or isinstance(dictionary[k], list):
                change_key_value(dictionary[k], key, new_value)
    elif isinstance(dictionary, list):
        for item in dictionary:
            change_key_value(item, key, new_value)

def check_none_values(dictionary):
    if isinstance(dictionary, dict):
        for k in dictionary:
            if dictionary[k] is None:
                return True
            elif isinstance(dictionary[k], dict) or isinstance(dictionary[k], list):
                result = check_none_values(dictionary[k])
                if result:
                    return True
    elif isinstance(dictionary, list):
        for item in dictionary:
            result = check_none_values(item)
            if result:
                return True
    return False

def map_dict_values(dict1, dict2):
    if isinstance(dict2, dict):
        for k in dict2:
            if k in dict1:
                dict2[k] = dict1[k]
            elif isinstance(dict2[k], dict) or isinstance(dict2[k], list):
                map_dict_values(dict1, dict2[k])
    elif isinstance(dict2, list):
        for item in dict2:
            map_dict_values(dict1, item)
            
def get_best_match(word, data_list):
    matches = get_close_matches(word, data_list, n=1, cutoff=0.6)
    if matches:
        return [(data_list.index(matches[0]), matches[0])]
    else:
        return []