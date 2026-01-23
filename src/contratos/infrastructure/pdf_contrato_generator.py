from fpdf import FPDF
from datetime import datetime
from shared.infrastructure.pdf_generator import IPDFGenerator, PDFDocument
from ..domain.entities import Contrato # Assegure-se que a entidade Contrato existe

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(80)
        self.cell(30, 10, 'SunOPS Solar - Contrato de Prestação de Serviços', 0, 0, 'C')
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}/{{nb}}', 0, 0, 'C')

class ContratoPDFGenerator(IPDFGenerator):
    
    def generate(self, document: PDFDocument) -> str:
        contrato = document.content.get('contrato')
        cliente_nome = document.content.get('cliente_nome')
        
        pdf = PDF()
        pdf.alias_nb_pages()
        pdf.add_page()
        
        # Título e Data
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 10, f'Campo Grande, {datetime.now().strftime("%d de %B de %Y")}', 0, 1, 'R')
        pdf.ln(10)
        
        # Identificação das Partes
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, '1. DAS PARTES', 0, 1)
        pdf.set_font('Arial', '', 11)
        pdf.multi_cell(0, 6, f'CONTRATANTE: {cliente_nome}, doravante denominado simplesmente CONTRATANTE.\n\nCONTRATADA: SunOPS Solar Energia Fotovoltaica, doravante denominada CONTRATADA.')
        pdf.ln(5)
        
        # Objeto
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, '2. DO OBJETO', 0, 1)
        pdf.set_font('Arial', '', 11)
        pdf.multi_cell(0, 6, 'O presente contrato tem como objeto a prestação de serviços de projeto, fornecimento e instalação de sistema de geração de energia fotovoltaica, conforme especificações técnicas anexas.')
        pdf.ln(5)
        
        # Valor (Se houver objeto contrato com valor)
        if contrato and hasattr(contrato, 'valor_total'):
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 10, '3. DO PREÇO E FORMA DE PAGAMENTO', 0, 1)
            pdf.set_font('Arial', '', 11)
            pdf.multi_cell(0, 6, f'Pela execução dos serviços objeto deste contrato, o CONTRATANTE pagará à CONTRATADA a importância total de R$ {contrato.valor_total.value:,.2f}.')
        
        # Assinaturas
        pdf.ln(30)
        y = pdf.get_y()
        pdf.line(20, y, 90, y)
        pdf.line(120, y, 190, y)
        
        pdf.cell(90, 5, 'SunOPS Solar', 0, 0, 'C')
        pdf.cell(10, 5, '', 0, 0)
        pdf.cell(90, 5, cliente_nome, 0, 1, 'C')
        
        pdf.output(document.output_path)
        return document.output_path