"""Motor de Orçamento Automático - Gera proposta em ≤ 2 minutos."""
import time
from decimal import Decimal
from typing import List
from ..dtos.orcamento_dto import (
    InputOrcamento, OutputOrcamento, SugestaoKit, CalculosFinanceiros
)
from ...domain.presets import (
    HSP_POR_CIDADE, TARIFA_MEDIA_POR_CLASSE, PRESETS_TELHADO,
    ConfiguracaoSistema
)
from ...domain.value_objects.dados_uc import TipoLigacao
from ...domain.value_objects.hsp import HSP
from ...domain.services.calculos_energeticos import (
    CalculadoraDimensionamento,
    CalculadoraGeracao,
    CalculadoraEconomia,
    CalculadoraFinanciamento
)
from ...domain.services.seletor_kit import SeletorAutomaticoKit


class MotorOrcamentoAutomatico:
    """Motor que gera orçamento completo com entradas mínimas."""
    
    def executar(self, input_data: InputOrcamento) -> OutputOrcamento:
        """
        Gera orçamento automático em ≤ 120 segundos.
        
        Fluxo:
        1. Validar entradas
        2. Buscar dados automáticos (HSP, tarifa, custo disponibilidade)
        3. Calcular dimensionamento
        4. Selecionar kit automaticamente
        5. Calcular geração
        6. Calcular financeiro
        7. Gerar alertas
        """
        inicio = time.time()
        alertas: List[str] = []
        
        # 1. Dados automáticos
        hsp_valor = self._buscar_hsp(input_data.cidade)
        if hsp_valor is None:
            alertas.append(f"HSP não encontrado para {input_data.cidade}, usando média nacional 4.5")
            hsp_valor = Decimal("4.5")
        
        hsp = HSP(hsp_valor, "CACHE_LOCAL")
        
        tarifa = TARIFA_MEDIA_POR_CLASSE.get(
            input_data.classe_tarifaria,
            Decimal("0.80")
        )
        
        tipo_ligacao = TipoLigacao(input_data.tipo_ligacao)
        custo_disponibilidade = tipo_ligacao.custo_disponibilidade
        
        fator_perdas = (
            ConfiguracaoSistema.FATOR_PERDAS_COMERCIAL
            if input_data.classe_tarifaria == "A4"
            else ConfiguracaoSistema.FATOR_PERDAS_RESIDENCIAL
        )
        
        # 2. Consumo e dimensionamento
        consumo_medio = Decimal(input_data.consumo_mensal_kwh)
        consumo_compensavel = consumo_medio - Decimal(custo_disponibilidade)
        
        if consumo_compensavel <= 0:
            alertas.append("Consumo insuficiente para compensação")
            consumo_compensavel = Decimal("100")  # Mínimo
        
        potencia_necessaria = CalculadoraDimensionamento.calcular_potencia_sistema(
            geracao_necessaria=consumo_compensavel,
            hsp=hsp,
            fator_perdas=fator_perdas
        )
        
        # 3. Seleção automática de kit
        if input_data.potencia_modulo_override:
            modulo_id = "modulo-custom"
            potencia_modulo = input_data.potencia_modulo_override
        else:
            modulo_id, potencia_modulo = SeletorAutomaticoKit.selecionar_modulo_padrao()
        
        if input_data.qtd_modulos_override:
            qtd_modulos = input_data.qtd_modulos_override
        else:
            qtd_modulos = SeletorAutomaticoKit.calcular_quantidade_modulos(
                potencia_necessaria,
                potencia_modulo
            )
        
        potencia_instalada = SeletorAutomaticoKit.calcular_potencia_instalada(
            qtd_modulos,
            potencia_modulo
        )
        
        if input_data.inversor_id_override:
            inversor_id = input_data.inversor_id_override
            # TODO: Buscar potência do banco
            potencia_inversor = potencia_instalada / Decimal("1.20")
        else:
            inversor_id, potencia_inversor = SeletorAutomaticoKit.selecionar_inversor_compativel(
                potencia_instalada
            )
        
        # Validar e ajustar DC/AC
        dc_ac_ratio, dc_ac_valido = SeletorAutomaticoKit.validar_dc_ac_ratio(
            potencia_instalada,
            potencia_inversor
        )
        
        if not dc_ac_valido:
            alertas.append(f"DC/AC ratio {dc_ac_ratio:.2f} fora do ideal (1.10-1.30)")
            qtd_modulos, inversor_id = SeletorAutomaticoKit.ajustar_kit_se_necessario(
                qtd_modulos,
                potencia_modulo,
                potencia_inversor
            )
            potencia_instalada = SeletorAutomaticoKit.calcular_potencia_instalada(
                qtd_modulos,
                potencia_modulo
            )
            dc_ac_ratio, dc_ac_valido = SeletorAutomaticoKit.validar_dc_ac_ratio(
                potencia_instalada,
                potencia_inversor
            )
        
        kit = SugestaoKit(
            modulo_id=modulo_id,
            modulo_nome=f"Módulo {potencia_modulo}W",
            potencia_modulo=potencia_modulo,
            qtd_modulos=qtd_modulos,
            inversor_id=inversor_id,
            inversor_nome=f"Inversor {potencia_inversor}kW",
            potencia_inversor=potencia_inversor,
            potencia_instalada=potencia_instalada,
            dc_ac_ratio=dc_ac_ratio,
            dc_ac_valido=dc_ac_valido
        )
        
        # 4. Geração
        geracao_mensal = CalculadoraGeracao.calcular_geracao_mensal(
            potencia_instalada,
            hsp,
            fator_perdas
        )
        geracao_anual = CalculadoraGeracao.calcular_geracao_anual(geracao_mensal)
        
        # 5. Financeiro
        financeiro = self._calcular_financeiro(
            input_data,
            kit,
            geracao_mensal,
            tarifa,
            alertas
        )
        
        # 6. Tempo de processamento
        fim = time.time()
        tempo_ms = int((fim - inicio) * 1000)
        
        if tempo_ms > 120000:  # > 2 minutos
            alertas.append(f"Processamento demorou {tempo_ms}ms (meta: ≤120s)")
        
        return OutputOrcamento(
            consumo_medio=consumo_medio,
            consumo_compensavel=consumo_compensavel,
            potencia_necessaria=potencia_necessaria,
            kit=kit,
            geracao_mensal=geracao_mensal,
            geracao_anual=geracao_anual,
            hsp_utilizado=hsp_valor,
            fator_perdas=fator_perdas,
            financeiro=financeiro,
            alertas=alertas,
            tempo_processamento_ms=tempo_ms
        )
    
    def _buscar_hsp(self, cidade: str) -> Decimal:
        """Busca HSP do cache local."""
        return HSP_POR_CIDADE.get(cidade)
    
    def _calcular_financeiro(
        self,
        input_data: InputOrcamento,
        kit: SugestaoKit,
        geracao_mensal: Decimal,
        tarifa: Decimal,
        alertas: List[str]
    ) -> CalculosFinanceiros:
        """Calcula todos os custos e retorno financeiro."""
        
        # Custos (TODO: buscar preços reais do banco)
        preco_modulo = Decimal("1200.00")
        preco_inversor = Decimal("3000.00")
        
        custo_equipamentos = (
            preco_modulo * kit.qtd_modulos +
            preco_inversor
        )
        
        preset_telhado = PRESETS_TELHADO[input_data.tipo_telhado]
        custo_estrutura = preset_telhado.custo_estrutura_por_modulo * kit.qtd_modulos
        
        custo_mao_obra = custo_equipamentos * ConfiguracaoSistema.MAO_OBRA_PERCENTUAL
        
        subtotal = custo_equipamentos + custo_estrutura + custo_mao_obra
        
        impostos = subtotal * ConfiguracaoSistema.IMPOSTOS
        margem = subtotal * ConfiguracaoSistema.MARGEM_MINIMA
        
        custo_total = subtotal + impostos + margem
        
        # Economia
        economia_mensal = CalculadoraEconomia.calcular_economia_mensal(
            geracao_mensal,
            tarifa
        )
        economia_anual = CalculadoraEconomia.calcular_economia_anual(economia_mensal)
        
        payback = CalculadoraEconomia.calcular_payback_simples(
            custo_total,
            economia_anual
        )
        
        # Financiamento
        parcela_mensal = None
        delta_mensal = None
        mes_break_even = None
        
        if input_data.forma_pagamento == "FINANCIADO":
            if not input_data.taxa_juros_mensal or not input_data.num_parcelas:
                alertas.append("Financiamento solicitado mas taxa/parcelas não informadas")
            else:
                parcela_mensal = CalculadoraFinanciamento.calcular_parcela(
                    custo_total,
                    input_data.taxa_juros_mensal,
                    input_data.num_parcelas
                )
                delta_mensal = CalculadoraFinanciamento.calcular_delta_mensal(
                    economia_mensal,
                    parcela_mensal
                )
                
                if delta_mensal < 0:
                    alertas.append(f"Parcela (R$ {parcela_mensal:.2f}) > Economia (R$ {economia_mensal:.2f})")
                    # Calcula em qual mês vira positivo
                    mes_break_even = self._calcular_mes_break_even(
                        custo_total,
                        economia_mensal,
                        parcela_mensal,
                        input_data.num_parcelas
                    )
        
        return CalculosFinanceiros(
            custo_equipamentos=custo_equipamentos,
            custo_estrutura=custo_estrutura,
            custo_mao_obra=custo_mao_obra,
            impostos=impostos,
            margem=margem,
            custo_total=custo_total,
            economia_mensal=economia_mensal,
            economia_anual=economia_anual,
            payback_anos=payback,
            parcela_mensal=parcela_mensal,
            delta_mensal=delta_mensal,
            mes_break_even=mes_break_even
        )
    
    def _calcular_mes_break_even(
        self,
        custo_total: Decimal,
        economia_mensal: Decimal,
        parcela: Decimal,
        num_parcelas: int
    ) -> int:
        """Calcula em qual mês o investimento vira positivo."""
        saldo = -custo_total
        
        for mes in range(1, num_parcelas + 1):
            saldo += economia_mensal - parcela
            if saldo >= 0:
                return mes
        
        # Após fim do financiamento
        for mes in range(num_parcelas + 1, 300):  # até 25 anos
            saldo += economia_mensal
            if saldo >= 0:
                return mes
        
        return 300  # Não compensa
