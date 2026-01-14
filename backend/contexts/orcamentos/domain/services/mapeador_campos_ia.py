"""Serviço de mapeamento assistido por IA."""
from typing import List, Dict
import re


class MapeadorCamposIA:
    """Mapeia campos do template para campos do sistema usando IA."""
    
    # Mapeamento de palavras-chave para campos
    KEYWORDS_MAP = {
        'preco_final': ['valor', 'preço', 'investimento', 'total', 'proposta'],
        'potencia_kwp': ['potência', 'kwp', 'sistema'],
        'qtd_modulos': ['módulos', 'painéis', 'quantidade'],
        'geracao_mensal': ['geração', 'mensal', 'produção'],
        'economia_mensal': ['economia', 'economiza', 'redução'],
        'payback_anos': ['payback', 'retorno', 'anos'],
        'cliente_nome': ['cliente', 'nome', 'sr', 'sra'],
        'cliente_cidade': ['cidade', 'localização', 'endereço'],
    }
    
    @staticmethod
    def extrair_labels(html: str) -> List[str]:
        """Extrai labels/placeholders do HTML."""
        # Procura por padrões como {{campo}} ou {campo}
        pattern = r'\{\{([^}]+)\}\}|\{([^}]+)\}'
        matches = re.findall(pattern, html)
        labels = [m[0] or m[1] for m in matches]
        return list(set(labels))
    
    @staticmethod
    def calcular_similaridade(label: str, keywords: List[str]) -> float:
        """Calcula similaridade entre label e keywords."""
        label_lower = label.lower()
        score = 0.0
        
        for keyword in keywords:
            if keyword in label_lower:
                score += 1.0
            elif any(char in label_lower for char in keyword):
                score += 0.3
        
        return min(score / len(keywords), 1.0) if keywords else 0.0
    
    @staticmethod
    def sugerir_mapeamento(label: str) -> Dict:
        """Sugere campo do sistema para um label."""
        melhor_campo = None
        melhor_score = 0.0
        
        for campo, keywords in MapeadorCamposIA.KEYWORDS_MAP.items():
            score = MapeadorCamposIA.calcular_similaridade(label, keywords)
            if score > melhor_score:
                melhor_score = score
                melhor_campo = campo
        
        return {
            'label_detectado': label,
            'campo_sugerido': melhor_campo,
            'confianca': round(melhor_score, 2)
        }
    
    @staticmethod
    def mapear_template(html: str) -> List[Dict]:
        """Mapeia todos os campos de um template."""
        labels = MapeadorCamposIA.extrair_labels(html)
        sugestoes = []
        
        for label in labels:
            sugestao = MapeadorCamposIA.sugerir_mapeamento(label)
            if sugestao['confianca'] > 0.3:  # Threshold mínimo
                sugestoes.append(sugestao)
        
        return sugestoes
