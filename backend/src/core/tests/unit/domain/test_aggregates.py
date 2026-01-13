import pytest
from src.core.domain.orcamentos.aggregates import StatusOrcamento
from src.core.domain.orcamentos.exceptions import (
    StatusInvalidoException, OrcamentoInvalidoException
)

class TestOrcamento:
    
    def test_criar_orcamento_valido(self, orcamento_valido):
        assert orcamento_valido.status == StatusOrcamento.RASCUNHO
        assert orcamento_valido.cliente_nome == "João Silva"
    
    def test_aprovar_orcamento(self, orcamento_valido):
        orcamento_valido.aprovar("Admin")
        assert orcamento_valido.status == StatusOrcamento.APROVADO
        assert orcamento_valido.aprovado_por == "Admin"
    
    def test_enviar_orcamento_aprovado(self, orcamento_valido):
        orcamento_valido.aprovar("Admin")
        orcamento_valido.enviar()
        assert orcamento_valido.status == StatusOrcamento.ENVIADO
        assert orcamento_valido.enviado_em is not None
    
    def test_enviar_orcamento_nao_aprovado_deve_falhar(self, orcamento_valido):
        with pytest.raises(StatusInvalidoException):
            orcamento_valido.enviar()
    
    def test_aceitar_orcamento(self, orcamento_valido):
        orcamento_valido.aprovar("Admin")
        orcamento_valido.enviar()
        orcamento_valido.aceitar()
        assert orcamento_valido.status == StatusOrcamento.ACEITO
    
    def test_calcular_total(self, orcamento_valido):
        total = orcamento_valido.calcular_total()
        assert total.valor > 0
    
    def test_eventos_sao_gerados(self, orcamento_valido):
        eventos = orcamento_valido.obter_eventos()
        assert len(eventos) > 0
    
    def test_criar_sem_cliente_deve_falhar(self, kit_valido):
        from src.core.domain.orcamentos.aggregates import Orcamento
        from src.core.domain.orcamentos.value_objects import OrcamentoId
        import uuid
        
        with pytest.raises(OrcamentoInvalidoException):
            Orcamento(
                id=OrcamentoId(str(uuid.uuid4())),
                kit=kit_valido,
                cliente_nome="",
                cliente_contato="11999999999"
            )
