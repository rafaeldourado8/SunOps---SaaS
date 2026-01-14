"""Template de Kit - Configuração técnica reutilizável."""
from dataclasses import dataclass, field
from decimal import Decimal
from typing import List, Optional


@dataclass
class ItemTemplate:
    """Item do template (sem preço fixo)."""
    
    produto_id: str
    categoria: str  # MODULO, INVERSOR, ESTRUTURA, etc
    quantidade: int
    especificacao: str  # Ex: "550W Monocristalino"


@dataclass
class RegrasTemplate:
    """Regras técnicas do template."""
    
    dc_ac_min: Decimal = Decimal("1.10")
    dc_ac_max: Decimal = Decimal("1.30")
    tensao_minima: Optional[int] = None
    tensao_maxima: Optional[int] = None
    compatibilidade_eletrica: Optional[str] = None


@dataclass
class TemplateKit:
    """Template de kit - configuração técnica sem preço fixo."""
    
    id: str
    nome: str
    potencia_alvo_kwp: Decimal
    tipo: str  # RESIDENCIAL, COMERCIAL, INDUSTRIAL
    itens: List[ItemTemplate] = field(default_factory=list)
    regras: RegrasTemplate = field(default_factory=RegrasTemplate)
    recomendacao: Optional[str] = None
    ativo: bool = True
    
    def adicionar_item(self, item: ItemTemplate):
        """Adiciona item ao template."""
        self.itens.append(item)
    
    def remover_item(self, produto_id: str):
        """Remove item do template."""
        self.itens = [i for i in self.itens if i.produto_id != produto_id]
    
    @property
    def quantidade_modulos(self) -> int:
        """Quantidade total de módulos."""
        return sum(i.quantidade for i in self.itens if i.categoria == "MODULO")
    
    @property
    def tem_inversor(self) -> bool:
        """Verifica se template tem inversor."""
        return any(i.categoria == "INVERSOR" for i in self.itens)
    
    def validar(self) -> List[str]:
        """Valida template e retorna lista de erros."""
        erros = []
        
        if not self.nome:
            erros.append("Nome é obrigatório")
        
        if self.potencia_alvo_kwp <= 0:
            erros.append("Potência alvo deve ser positiva")
        
        if not self.itens:
            erros.append("Template deve ter pelo menos 1 item")
        
        if not self.tem_inversor:
            erros.append("Template deve ter pelo menos 1 inversor")
        
        if self.quantidade_modulos == 0:
            erros.append("Template deve ter pelo menos 1 módulo")
        
        return erros
