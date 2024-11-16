from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph

class Recibo():
    def __init__(self):
        self.file_name = "Recibo.pdf"
        self.doc = SimpleDocTemplate(self.file_name, pagesize=A4)
        self.styles = getSampleStyleSheet()
        self.style_heading1 = self.styles["Heading1"]
        self.style_normal = self.styles["Normal"]
        

    def gerarRecibo(self):
        html_text = f"""
            <br />
            <p>
            Eu <strong>nome_psicologo</strong>, portador do CPF sob o Nº cpf_psicologo, declaro que recebi de nome_paciente,
            portador do CPF de Nº cpf_paciente, a quantia de R$ valor_paciente, pela quantidade de sessoes_realizadas
            sessões de psicoterapia realizadas.
            Afirmo o presente na seguinte data:
            data do sistema
            </p>
            <p>And other formatting like <font color="blue">colored</font> text or <u>underlined</u> text.</p>
            """
        
        
        # Constrói uma lista de elementos
        titulo  = "Recibo de prestação de serviços de psicoterapia"
        elements = [
            Paragraph(titulo, self.style_heading1),  # Título com estilo Heading1
            Paragraph(html_text, self.style_normal),  # Parágrafo normal
        ]

        self.doc.build(elements)
        print(f"PDF file '{self.file_name}' created successfully!")

        



"""# Define o arquivo de saída
file_name = "example.pdf"

# Cria o template do documento
doc = SimpleDocTemplate(file_name, pagesize=A4)

# Obtém os estilos padrão
styles = getSampleStyleSheet()

# Estilo para cabeçalhos
style_heading1 = styles["Heading1"]


# Estilo normal
style_normal = styles["Normal"]"""

# Texto formatado em HTML
#html_text = f"""
#<br />
#<p>
#Eu <strong>nome_psicologo</strong>, portador do CPF sob o Nº cpf_psicologo, declaro que recebi de nome_paciente,
#portador do CPF de Nº cpf_paciente, a quantia de R$ valor_paciente, pela quantidade de sessoes_realizadas
#sessões de psicoterapia realizadas.
#Afirmo o presente na seguinte data:
#data do sistema
#</p>
#<p>And other formatting like <font color="blue">colored</font> text or <u>underlined</u> text.</p>
#"""

# Constrói uma lista de elementos
#elements = [
 #   Paragraph("Recibo de prestação de serviços de psicoterapia", style_heading1),  # Título com estilo Heading1
  #  Paragraph(html_text, style_normal),  # Parágrafo normal
#]

# Constrói o documento com os elementos
#doc.build(elements)

#print(f"PDF file '{file_name}' created successfully!")

r = Recibo()
r.gerarRecibo()
