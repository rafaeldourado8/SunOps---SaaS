from fpdf import FPDF
from datetime import datetime
from shared.infrastructure.pdf_generator import IPDFGenerator, PDFDocument
from ..domain.entities import Proposta

class PDF(FPDF):
    def header(self):
        # Cabeçalho da página
        self.set_font('Arial', 'B', 15)
        self.cell(80)
        self.cell(30, 10, 'SunOPS Solar - Energia Sustentável', 0, 0, 'C')
        self.ln(20)

    def footer(self):
        # Rodapé da página
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}/{{nb}}', 0, 0, 'C')

class PropostaPDFGenerator(IPDFGenerator):
    
    def generate(self, document: PDFDocument) -> str:
        proposta: Proposta = document.content['proposta']
        cliente_nome: str = document.content['cliente_nome']
        
        pdf = PDF()
        pdf.alias_nb_pages()
        pdf.add_page()
        
        # --- Título ---
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'PROPOSTA COMERCIAL', 0, 1, 'C')
        pdf.line(10, 35, 200, 35)
        pdf.ln(10)
        
        # --- Dados do Cliente ---
        pdf.set_fill_color(240, 240, 240)
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, ' Dados do Cliente', 0, 1, 'L', True)
        
        pdf.set_font('Arial', '', 11)
        pdf.cell(0, 8, f'Nome: {cliente_nome}', 0, 1)
        pdf.cell(0, 8, f'Data de Emissão: {datetime.now().strftime("%d/%m/%Y")}', 0, 1)
        pdf.ln(5)
        
        # --- Resumo Técnico ---
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, ' Resumo do Sistema', 0, 1, 'L', True)
        
        pdf.set_font('Arial', '', 11)
        pdf.cell(0, 8, f'Potência Total: {proposta.potencia_sistema_kwp:.2f} kWp', 0, 1)
        if proposta.payback_anos:
            pdf.cell(0, 8, f'Payback Estimado: {proposta.payback_anos:.1f} anos', 0, 1)
        pdf.ln(5)
        
        # --- Itens (Tabela) ---
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, ' Equipamentos e Serviços', 0, 1, 'L', True)
        
        # Cabeçalho Tabela
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(100, 10, 'Descrição', 1)
        pdf.cell(30, 10, 'Qtd', 1, 0, 'C')
        pdf.cell(60, 10, 'Valor (R$)', 1, 0, 'R')
        pdf.ln()
        
        # Corpo Tabela
        pdf.set_font('Arial', '', 10)
        for item in proposta.itens:
            total_item = item.calcular_total_preco().value
            pdf.cell(100, 10, f' {item.nome}', 1)
            pdf.cell(30, 10, str(item.quantidade), 1, 0, 'C')
            pdf.cell(60, 10, f'{total_item:,.2f}', 1, 0, 'R')
            pdf.ln()
            
        pdf.ln(5)
        
        # --- Totalização ---
        valor_total = proposta.calcular_valor_total()
        
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(130, 10, 'VALOR TOTAL:', 0, 0, 'R')
        pdf.set_text_color(0, 100, 0) # Verde
        pdf.cell(60, 10, f'R$ {valor_total.value:,.2f}', 0, 1, 'R')
        pdf.set_text_color(0, 0, 0)
        
        # Desconto
        if proposta.desconto:
             pdf.set_font('Arial', 'I', 11)
             pdf.cell(130, 8, 'Desconto aplicado:', 0, 0, 'R')
             pdf.cell(60, 8, f'- R$ {proposta.desconto.valor.value:,.2f}', 0, 1, 'R')
        
        # --- Rodapé da Proposta ---
        pdf.ln(20)
        pdf.set_font('Arial', '', 10)
        pdf.multi_cell(0, 5, 'Validade: 7 dias. Esta proposta inclui equipamentos, projeto de engenharia, homologação junto à concessionária e instalação completa.')

        pdf.output(document.output_path)
        return document.output_path