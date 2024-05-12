from django.test import TestCase,Client
from django.urls import reverse
import datetime

from ..query_generator import QueryGenerator

from openai.types.chat import ChatCompletionMessage
from openai.types.chat.chat_completion import ChatCompletion, Choice 
from openai.types.chat.chat_completion_chunk import ChatCompletionChunk, ChoiceDelta
from openai.types.chat.chat_completion_chunk import Choice as StreamChoice

from unittest.mock import patch,MagicMock

class FakeClient:
    pass

class FakeCompletion:
    
    client = FakeClient()
    
    def create(self,text):
        return 'ok'
    


class QueryGeneratorTestCase(TestCase):
    
    query_generator = QueryGenerator()

    @patch('openai.OpenAI',FakeClient)
    def test_catch_openai_exception(self):
        result = self.query_generator.get_query("")
        self.assertEqual(result, 'error')
            
            

    