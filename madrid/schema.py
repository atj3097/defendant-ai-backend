import graphene
import openai
import os
from graphene import ObjectType, String, Field, List, ID
import firebase_admin
from firebase_admin import credentials, firestore

# Make sure you have the OPENAI_API_KEY in your environment variables
openai.api_key = os.environ["OPENAI_API_KEY"]

cred = credentials.Certificate('firebase_key.json')
firebase_admin.initialize_app(cred)
db = firestore.client()


class Document(ObjectType):
    document_id = ID(required=True)
    document_type = String(required=True)
    file_path = String(required=True)

class ResearchQuery(ObjectType):
    query_id = ID(required=True)
    query_text = String(required=True)

class CaseStrategy(ObjectType):
    strategy_id = ID(required=True)
    strategy_text = String(required=True)

class Case(ObjectType):
    case_id = ID(required=True)
    case_number = String(required=True)
    client_name = String(required=True)
    case_type = String(required=True)
    status = String(required=True)
    documents = List(Document)
    research_queries = List(ResearchQuery)
    case_strategies = List(CaseStrategy)

class User(ObjectType):
    user_id = ID(required=True)
    email = String(required=True)
    cases = List(Case)

class AIGeneratedResponse(ObjectType):
    response_id = ID(required=True)
    response_text = String(required=True)

class Query(ObjectType):
    user = Field(User, user_id=ID(required=True))
    case = Field(Case, case_id=ID(required=True))
    generate_ai_response = Field(AIGeneratedResponse, input_text=String(required=True))

    def resolve_user(self, info, user_id):
        # Implement your logic to fetch the user by user_id
        pass

    def resolve_case(self, info, case_id):
        # Implement your logic to fetch the case by case_id
        pass

    def resolve_generate_ai_response(self, info, input_text):
        response = openai.Completion.create(
            engine="your_engine_name",  # Replace with your desired engine name (e.g., "davinci-codex")
            prompt=input_text,
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.8
        )
        response_text = response.choices[0].text.strip()
        return AIGeneratedResponse(response_id="some_unique_id", response_text=response_text)

schema = graphene.Schema(query=Query)
