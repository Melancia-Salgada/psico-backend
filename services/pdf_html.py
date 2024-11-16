from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph

class Recibo():
    def __init__(self):
        self.file_name = "Reciboooooooooo.pdf"
        self.doc = SimpleDocTemplate(self.file_name, pagesize=A4) # Cria o template do documento
        self.styles = getSampleStyleSheet() # Obtém os estilos padrão
        self.style_heading1 = self.styles["Heading1"] # Estilo para cabeçalhos
        self.style_normal = ParagraphStyle(
            "NormalCustom",  # Nome do estilo
            parent=self.styles["Normal"],  # Baseado no estilo Normal
            fontSize=14,  # Tamanho da fonte
            leading=18,  # Espaçamento entre linhas
        )
        

    def gerarRecibo(self,nome,cpf,data,nome_paciente, cpf_paciente, valor_paciente):
        try:

            html_text = f"""
            <br />
            <p>
            Eu, <strong>{nome}</strong>, portador do CPF de Nº <strong>{cpf}</strong>, 
            declaro que recebi de <strong>{nome_paciente}</strong>
            portador do CPF de Nº <strong>{cpf_paciente} </strong>, a quantia de <strong> R$ {valor_paciente}</strong> referente ao total de <strong>4</strong>
            sessões de psicoterapia realizadas.<br />
            Afirmo os elementos descritos acima na seguinte data:
            <br />
            <strong>{data}</strong>
            </p>
            """
            #<p>And other formatting like <font color="blue">colored</font> text or <u>underlined</u> text.</p>
                
            
            
            # Constrói uma lista de elementos
            titulo  = "RECIBO DE PAGAMENTO"
            elements = [
                Paragraph(titulo, self.style_heading1),  # Título com estilo Heading1
                Paragraph(html_text, self.style_normal),  # Parágrafo normal
            ]

            self.doc.build(elements)
            print(f"PDF file '{self.file_name}' created successfully!")
        except Exception as ex:
            print(f"error: ",ex)
        
        

        



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

