import os
import google.generativeai as genai
from typing import Dict, Any, Optional


class GeminiService:
    """Serviço para integração com Gemini Flash e Pro"""
    
    def __init__(self):
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        self.flash_model = genai.GenerativeModel('gemini-pro')
        self.pro_model = genai.GenerativeModel('gemini-pro')
    
    async def generate(self, prompt: str, system_prompt: str = "", context: str = "") -> str:
        """Gera resposta usando Gemini"""
        full_prompt = f"{system_prompt}\n\n{context}\n\nMensagem: {prompt}"
        response = self.flash_model.generate_content(full_prompt)
        return response.text
    
    async def preprocess_with_flash(self, message: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Preprocessamento rápido com Gemini Flash"""
        prompt = f"""Analise a mensagem e extraia:
1. Intent (vendas, suporte, duvida, transferir_humano)
2. Urgência (baixa, media, alta)
3. Entidades relevantes (valores, datas, produtos)

Mensagem: {message}
Contexto: {context}

Responda em JSON."""
        
        response = self.flash_model.generate_content(prompt)
        return self._parse_json_response(response.text)
    
    async def generate_response_with_pro(
        self, 
        message: str, 
        context: Dict[str, Any],
        rules: str,
        agent_type: str
    ) -> str:
        """Geração de resposta final com Gemini Pro"""
        prompt = f"""Você é um agente de {agent_type} especializado em energia solar.

REGRAS:
{rules}

CONTEXTO DA CONVERSA:
{context}

MENSAGEM DO CLIENTE:
{message}

Responda de forma humanizada, natural e empática. Não invente informações."""
        
        response = self.pro_model.generate_content(prompt)
        return response.text
    
    def _parse_json_response(self, text: str) -> Dict[str, Any]:
        """Parse de resposta JSON do Gemini"""
        import json
        import re
        
        # Extrair JSON do texto
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        return {}
