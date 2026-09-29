# Pedra Angular

Os melhores textos da humanidade, traduzidos com rigor filológico e legíveis no
celular de qualquer pessoa, em poucos megabytes, de graça. *Não é compra, não é
pirataria, não é ficar sem.*

Esta é a porta de entrada do ecossistema. Quem chega aqui — eu ou qualquer
instância de Claude — lê esta página antes de criar qualquer coisa nova.

---

## As duas peças principais

Estão no ar. Tudo o mais que existe no ecossistema existe para alimentar uma
destas duas, ou para levá-las ao papel.

### App-Leitura · `pedraangular.app.br`

O acervo adulto: mais de mil obras em português, grego, latim, hebraico e
inglês. Leitura com voz, nove temas de alto contraste, fontes embarcadas,
interface em três idiomas, editor embutido. Para quem lê o texto inteiro, e
para quem precisa que o texto se ajuste ao olho.

### App-Infantil · `historinhas.app.br`

Adaptações bilíngues português/grego, pouca linha por página, tipos desenhados
para quem está aprendendo a ler. Cabe inteiro em um megabyte — abre em qualquer
celular. Para o Theo, para o Davi, e para toda criança que chega ao grego antes
de chegar à escola.

### Linha de livros físicos · a terceira principal, em preparo

Quando a Oficina e o Gerador entregarem o PDF e o livro estiver no mundo
físico, esta linha ganha domínio, ficha e lugar ao lado das outras duas.
Enquanto isso, ela se prepara: Encheirídion de Epicteto em azul-noite, linha
econômica em Fólio φ, cadernos de pauta ampliada, calendário bíblico. O
catálogo completo de formatos está na aba **Formatos físicos**.

---

## As três camadas

Não são apps parecidos. São três camadas do mesmo objeto, e confundi-las é a
origem de quase todo erro de arquitetura aqui.

| Camada | O que é | Formato | Quem lê |
|---|---|---|---|
| 1. Acervo | a verdade | `.md` com front matter | humano que edita, Pandoc, XeLaTeX, IA |
| 2. Rolo | a sobrevivência | HTML estático, texto no `<body>` | IA, crawler, navegador sem JS, pendrive de 2046 |
| 3. App | o conforto | SPA interativa | humano com as mãos no aparelho |

A camada 3 é a única opcional. Um app que não entrega as camadas 1 e 2 não é um
app do ecossistema — é um beco sem saída.

---

## Tudo o mais é derivado

Derivado quer dizer o que a palavra diz: vem de. Uma peça nova não estreia uma
identidade — ela herda a que já existe, porque neste projeto a identidade visual
**é** parte da acessibilidade. Contraste medido, par de cores que não colapsa
sob dicromacia, tipo legível: mudar o tom é mexer em quem consegue ler.

O que se herda, sem discussão:

- **A Barra Angular.** Φ · A− · A+ · Ξ, nesta ordem, na primeira fila, desde a
  primeira tela. É a LEI 8, e esta página a cumpre — inclusive esta página.
- **Os nove temas**, token a token, como estão no `styles.css` do app-leitura.
  Nenhuma peça inventa paleta própria.
- **O par de tipos.** Cardo lê, Atkinson Hyperlegible é a alternativa para
  baixa visão, OpenDyslexic para dislexia, DejaVu guarnece o imprevisto.
- **Zero rede em runtime.** Nenhuma fonte de CDN, nenhuma chamada de API para
  desenhar a tela.

Rosa e roxo nunca são sinal distintivo em nada do Pedra Angular: sob
protanomalia o rosa lê cinza e o roxo lê azul, e o sinal some sem avisar.

---

## Antes de criar qualquer coisa nova

1. **Situar no caminho.** Toda peça ocupa um ponto do percurso que a aba
   **As peças** descreve. Se a peça nova não ocupa nenhum, ou o percurso mudou,
   ou a peça não é do ecossistema.
2. **Ler a aba Normas** — as oito leis e a Barra Angular, no mínimo — e o
   `README.md` da pasta em que vai mexer.
3. **Herdar os tokens**, os nove temas e o par de tipos. Copiar do app que já
   cumpre, nunca reinventar.
4. **Medir, não estimar.** Par de cores novo passa pelo Laboratório de Cores,
   sob visão normal e as três dicromacias, antes de virar norma.
5. **Preservar a proveniência.** Licença CC com atribuição completa, e
   `revisado: false` só vira `true` por mão humana — nunca por script, nunca
   por IA.

---

## Como esta página é feita

Ela não guarda conteúdo próprio. O `gerar.py` ao lado lê os arquivos que já são
a verdade do ecossistema — o `NORMAS.md`, o catálogo da Oficina, os temas do
`styles.css` — e monta a página a partir deles. Editou a norma, roda de novo.

É a mesma regra que o resto do ecossistema segue: uma verdade por assunto, e o
derivado se refaz a partir dela.
