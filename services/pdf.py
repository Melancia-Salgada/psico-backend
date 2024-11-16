from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4



#função que converte de milímetros pra pontos
def mm2p(milimetros):
    return milimetros/0.352777



cnv = canvas.Canvas('meu_pdf.pdf', pagesize=A4)


"""nomes = ['caio','marcos','joao']
eixo = 100
for nome in nomes:
    cnv.drawString(mm2p(eixo),mm2p(150),nome)  #utiliza parametros x e y do plano cartesiano
    eixo+=30"""


"""nomes = ['caio','marcos','joao']
eixo = 100
for nome in nomes:
    cnv.drawString(mm2p(100),mm2p(eixo),nome)  #utiliza parametros x e y do plano cartesiano
    eixo+=20"""

cnv.drawString(mm2p(100),mm2p(150),'Tes')

#criar um círculo
cnv.circle(mm2p(100),mm2p(150),mm2p(100))


#criar uma linha -> precisa passar os pontos onde a linha começa e termina
cnv.line(mm2p(100),mm2p(150),mm2p(120),mm2p(160))

#criar um retangulo
cnv.rect(200,250,300,350)

#anexar imagem
cnv.drawImage('../luna.jpg',40,250,width=190,height=500)



cnv.save()