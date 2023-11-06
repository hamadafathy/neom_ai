import re
import json
from utililty import *
import uuid
from langchain.memory import  ChatMessageHistory

class NeomBot:
    session_data = {}  # Class variable to store user_data and hist for each session

    def __init__(self, llm, query, session_id,llm_ent):
        self.session_id = session_id
        self.init_session_data()
        self.get_session_data()
        self.llm = llm
        self.query = query
        self.llm_ent = llm_ent
        

    def init_session_data(self):
        """Initializes session data if not already present."""
        if self.session_id not in NeomBot.session_data:
            NeomBot.session_data[self.session_id] = {
                "user_data": {}, 
                "hist": [], 
                "input_review":{}, 
                "flags": {"otp_vallidated": False, "explore_chains": False, 'form_selected': False,'submit_confirmation': False}, 
                "user_token":[], 
                "template":[],
                "history": ChatMessageHistory(),  # Initialize history here
                "chain_1": None , # Initialize chain here
                "memory" : None,
                'llm_response' : [],
                'entity_types' : [],
                'json_structure' : [],
                'assigned_types': [],
                'selected_forms' : [],
                'submission_forms_ent': [],
                'required_form': [],
                'service_flag':[]

            }

    def get_session_data(self):
        """Retrieves session data for the current session."""
        session = NeomBot.session_data[self.session_id]
        self.user_data = session["user_data"]
        self.hist = session["hist"]
        self.input_review = session["input_review"]
        self.flags = session["flags"]
        self.user_token = session["user_token"]
        self.template = session["template"]
        self.history = session["history"]  # Retrieve history here
        self.chain_1 = session["chain_1"]
        self.memory = session["memory"]
        self.llm_response = session["llm_response"]
        self.entity_types = session["entity_types"]
        self.json_structure = session["json_structure"]
        self.assigned_types = session["assigned_types"]
        self.selected_forms = session["selected_forms"]
        self.submission_forms_ent = session["submission_forms_ent"]
        self.required_form = session["required_form"]
        self.service_flag = session["service_flag"]
        
    
    def predict_response(self, query):
        prompt_template = Auth_Prompt_Template
        self.chain = prompting_selction(prompt_template, self.llm)
        return self.chain.predict(input=query)
    
    
    def predict_response_routed(self, query ):
        if not self.chain_1:
            prompt_template = self.template[0]
            self.chain_1, self.memory = prompting_selction_routed(prompt_template, self.llm, self.history )
            NeomBot.session_data[self.session_id]["chain_1"] = self.chain_1
            NeomBot.session_data[self.session_id]["memory"] = self.memory
        return self.chain_1.predict(input=query)
    
    def predict_response_confirmed(self, query ):
        prompt_template = confirmation_prompt
        self.chain_2 = prompting_selction(prompt_template, self.llm )
        return self.chain_2.predict(input=query)


    def handle_match(self, entity_obj):

        if 'entity' in self.entity_obj:
            entity = self.entity_obj['entity']
            value = self.entity_obj['value']
        else:
            for entity, value in self.entity_obj.items():
                entity = entity
                value = value
                print(f"Entity: {entity}, Value: {value}")
        

        if entity_name_standarization(entity) == 'nationality':
            self.response = self.handle_nationality(value)
        elif entity_name_standarization(entity) in ['idtype', 'iqama', 'passport', 'nationaid']:
            self.handle_id_type(value)
            print('id type:', entity, value)
        elif entity_name_standarization(entity) in ['idnumber', 'iqamanumber', 'iqamaid', 'passportnumber','passportid', 'nationalidnumber']:
            self.handle_id_number(value)
        elif entity_name_standarization(entity) in ['receivedotp', 'otp']:
            self.handle_otp(value)

    def handle_match_2(self, entity_obj_2):

        if entity_obj_2 in  self.entity_types[0]:
            self.ent_index = self.entity_types[0].index(entity_obj_2)
            self.json_data = json.load(open(self.json_structure[0][self.ent_index]))

    def handle_responses(self, json_path):
        self.json_data = json.load(open(json_path))
        self.json_data['custom']['robot']['en']["robotSays"] = self.response
        return self.json_data
    
    def handle_nationality(self, value):
        nationality = filter_string(value)
        self.user_data['nationality'] = nationality[0].upper() + nationality[1:].lower()
        auth_user = self.user_authentications()
        return self.response
        
    def handle_id_type(self, value):
        id_type = filter_string(value)
        self.user_data['type'] = filter_string(id_type)[0].upper() + filter_string(id_type)[1:].lower()
        self.response= self.handle_responses('authentication_mapping/authentication_identification_number.json')
        return self.response
    
    def handle_id_number(self, value):
        id_number = filter_string(value)
        self.user_data['id'] = id_number
        self.response= self.handle_responses('authentication_mapping/authentication_nationality.json')
        return self.response
    
    def user_authentications(self):
        auth_url = "https://testgs.neom.com/api/user/auth"
        auth_response = neom_apis(self.user_data, auth_url)
        auth_response = json.loads(auth_response)
        if 'statusCode' in auth_response:
            self.response = 'you have been authorized and an otp has been sent via email. please note that, the otp expires in 2 minutes'
            self.response = self.handle_responses('authentication_mapping/authentication_otp.json')
            return self.response
        else:
            self.response = 'Your request is not valid, please revise your personal data and try again'
            self.response = self.handle_responses('authentication_mapping/authentication_otp.json')
            return self.response
    
    def handle_otp(self, value):
        otp_number = filter_string(value)
        extracted_data = {key: self.user_data[key] for key in ('id', 'type')}
        extracted_data['otp'] = otp_number
        otp_response = self.validate_otp(extracted_data)
        self.response = self.validate_and_resend_otp(otp_response)
        return self.response


    def validate_and_resend_otp(self, otp_response):
        self.json_data = json.load(open('authentication_mapping/authentication_otp.json'))
        
        
        if 'statusCode' in otp_response:
            self.user_token.append(otp_response['userProfile']['token'])
            self.response = "Thank you " + otp_response['userProfile']['username'] + """. Let us proceed with the services that we provide:
                            Iqama , Work , VISA , Customs , Tourism , Flying , Marine.
                            Please choose one of them to be able to continue"""
            self.response = self.handle_responses('authentication_mapping/onboarding.json')
            self.flags['otp_validated'] = True
        else:
            self.response = 'Your ' + otp_response['message'] + '\nAnother otp has been sent to your email'
            self.response = self.handle_responses('authentication_mapping/authentication_otp.json')
            self.resend_otp()  # Resend OTP if not validated

        return self.response


    def resend_otp(self):
        otp_url = "https://testgs.neom.com/api/user/auth"  # Replace with the actual OTP resend API endpoint

        try:
            otp_response = neom_apis( self.user_data, otp_url)
            otp_response = json.loads(otp_response)
            if otp_response.status_code == 200:
                print("OTP resent successfully")
            else:
                print("Failed to resend OTP. Status code:", otp_response.status_code)
        except requests.exceptions.RequestException as e:
            print("Failed to resend OTP:", str(e))

        
    def validate_otp(self, extracted_data):
        otp_url = "https://testgs.neom.com/api/user/otp"
        auth_response = neom_apis(extracted_data,otp_url)
        auth_response = json.loads(auth_response)
        if 'statusCode' in  auth_response:
            self.flags['otp_vallidated'] = True
        return auth_response
    
    def create_request_id(self, service_id):
        req_url = "https://testgs.neom.com/api/request"
        service_id = {"serviceId": service_id}
        print('service_id:',service_id)
        req_response = neom_apis(service_id, req_url, self.user_token[0])
        self.new_request_id = json.loads(req_response)
        print('new_request_id:', self.new_request_id)
        if 'errorCode' not in self.new_request_id:
            self.new_request_id = self.new_request_id['newRequestId']
        return self.response
    
    def confirmation(self):
        if self.query.lower() == 'yes':
            self.requestId = 988774757
            req_url = f"https://testgs.neom.com/api/user/request/{self.requestId}"
            print('required_form:', self.required_form[0][0])
            submit_response = neom_apis(self.required_form[0][0], req_url, self.user_token[0])
            self.response = f"{submit_response}"
            return self.response
    
    def route_chain(self):
        self.dist = chain_selection(self.llm, self.query) 
        self.selected_prompt = all_prompts_temp[all_prompts_names.index(self.dist)]
        self.entity_types.append(entity_list[all_prompts_names.index(self.dist)])
        self.json_structure.append(jsons_structures[all_prompts_names.index(self.dist)])
        self.selected_forms.append(submission_forms[all_prompts_names.index(self.dist)])
        self.submission_forms_ent.append(submission_forms_flags[all_prompts_names.index(self.dist)])
        self.service_flag.append(services_ids[all_prompts_names.index(self.dist)])
        self.template.append(self.selected_prompt)
        self.routed_chain = prompting_selction_routed(self.selected_prompt, self.llm, self.history )
        return self.routed_chain, self.dist
    
    def information_extraction(self):
        if len(self.hist) > 1:
            self.response_rephrased = self.predict_response_routed("Given the following text: '" + self.hist[-2]  + "'. Please extract and return the question omly from the text. ")
            self.text =  self.response_rephrased + ' ' + self.query            
            self.best_entity , self.best_output = entity_exctraction( self.text, self.llm_ent, self.entity_types[0], self.assigned_types)
            # self.extracted_entity_value = self.predict_response_routed(f'Your task is to extract the entity and its value in a dictionary format {{"entity": , "value":, }} from the following response: {self.text} using the following entity list: {self.entity_types[0]}. If the entity in the response is not in the entity list, please return "None".')

            # self.extracted_entity_value = self.predict_response_routed(f'your task is to just extract the entity and its value in a dictionary format {{"entity": , "value":, }} from the following response: {self.text}')
            print('self.extracted_entity_value :', self.extracted_entity_value )
            if self.best_output:
                self.assigned_types.append(self.best_entity)
                print('information_extraction assigned_types:', self.assigned_types)
                print('self.best_entity , self.best_output:' , self.best_entity , self.query)
                self.input_review[self.best_entity] =  self.query
                self.confirmation()
                if  self.flags['form_selected'] :
                    self.parameters_mapping()

            
    def selected_chain_response_mapping(self):
        self.response_rephrased = self.predict_response_routed("Given the following text: '" + self.hist[-1] + "'. Please extract and return the question omly from the text. ")         
        self.best_entity , self.best_output = entity_exctraction( self.response_rephrased, self.llm_ent, self.entity_types[0], self.assigned_types)
        print('response mapping:', self.best_entity)
        print('jsons:', self.json_structure[0])
        print('selected entities:', self.entity_types[0])
        self.ent_index = self.entity_types[0].index(self.best_entity )
        print('ent_index:',self.ent_index )
        self.json_data = json.load(open(self.json_structure[0][self.ent_index]))
        self.json_data['custom']['robot']['en']["robotSays"] =  self.response
        self.response = self.json_data
        return self.response
    
    
    def auth_response_mapping(self):
        try:
            self.response_rephrased = self.predict_response("Given the following text: '" + self.response  + "'. Please extract and return the question omly from the text. ")         
            self.best_entity , self.best_output = entity_exctraction( self.response_rephrased, self.llm_ent, auth_entity, [])
            self.json_data = json.load(open(auth_jsons[auth_entity.index(self.best_entity)]))
            self.json_data['custom']['robot']['en']["robotSays"] =  self.response
            self.response = self.json_data
            return self.response
        except:
            pass
    
    
    def parameters_mapping(self):
        change_key_value(self.required_form[0], self.best_entity, self.query)
        print('change_key_valu:', change_key_value(self.required_form[0], self.best_entity, self.query))
        
        
    def form_selection(self):
        if len(self.selected_forms[0]) > 1:
            if get_best_match(self.query, self.submission_forms_ent[0]):
                best_match_ind = get_best_match(self.query, self.submission_forms_ent[0])[0][0]
                self.required_form.append(self.selected_forms[0][best_match_ind])
                print('get_best_match:',self.required_form )
                self.flags['form_selected'] = True
                service_id = self.service_flag[0][best_match_ind]
                self.create_request_id(service_id)
        elif len(self.selected_forms[0]) == 1:
            self.required_form.append(self.selected_forms[0][0])
            service_id = self.service_flag[0][0]
            self.create_request_id(service_id)
            self.flags['form_selected'] = True 
               
        else:
            return "form not detected yet"
        
    def confirmation_chain(self):
        self.response = self.predict_response_confirmed(self.query)
        if self.query.lower() == 'yes':
            return self.response
        else:
            self.explore_chain()
        
    def explore_chain(self):
        """Predicts a response using a routed chain and stores it."""
        self.response = self.predict_response_routed(self.query)
        self.hist.append(self.response)
        if not self.flags['form_selected'] and len(self.selected_forms)>0:
            self.form_selection()
        self.information_extraction()
        print(self.selected_forms)
        
            
        self.history.add_message(self.query)
        self.history.add_message(self.response)
        print('self.input_review:', self.input_review)
        self.selected_chain_response_mapping()
        return self.response
        
        
    # Define similar methods for handle_id_type, handle_id_number, handle_otp
    def user_auth_chain(self):

        self.response = self.predict_response(self.query)
        self.llm_response.append(self.response)
        try:
            self.response_1 = self.predict_response('just extract the entity and its value in a dictionary format {"entity": , "value":, } from the following response ' + self.query )
            
            self.response_1 = escape_removal(self.response_1)
            self.entity_obj = json.loads(self.response_1)            
            self.handle_match(self.entity_obj )
        except:
            pass
        
        self.auth_response_mapping()
        return self.response
        
    def run(self):
        self.query = self.query
        if self.query == "quit":
            return
        if self.flags['otp_vallidated'] and not self.flags['explore_chains']:
            self.route_chain()
            self.flags['explore_chains'] = True
            
            
        if not self.flags['otp_vallidated']  :
            self.response = self.user_auth_chain()
        # elif not check_none_values(self.required_form):
        #     self.response = self.confirmation_chain()
        elif  self.flags['otp_vallidated'] and not self.flags['submit_confirmation'] :
            self.response = self.explore_chain()
            
        return self.response

