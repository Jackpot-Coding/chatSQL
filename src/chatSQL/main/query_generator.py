from openai import OpenAI

class QueryGenerator:
    
    def getQuery(self,prompt):
        
        try:  
        
            client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
            
            completion = client.chat.completions.create(
                    model="lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF",
                    messages=[
                        {"role": "system", "content": "Do not explain code."},
                        {"role": "system", "content": "Always replay in Italian."},
                        {"role": "system", "content": "Always wrap code in a markdown code block"},
                        {"role": "user", "content": prompt}
                    ],
                )
            
            if completion.choices:
                message = completion.choices[0].message
                return message.content
            
            return 'interpretation'
        
        except Exception:
            return 'error'