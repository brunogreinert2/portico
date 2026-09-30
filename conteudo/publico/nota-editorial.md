# Nota editorial

O Pedra Angular reúne textos que outros prepararam com cuidado — editores,
tradutores, digitalizadores — e os oferece de um jeito que dure, que se possa
citar e que qualquer pessoa ou programa consiga ler. Esta nota diz o que o
acervo faz com esses textos e o que não faz.

## De onde vêm os textos

Cada obra diz a sua fonte no próprio arquivo (`source`, `source_repo`,
`source_file`, `base_edition`) e a sua licença (`license`). As principais:

- **Perseus Digital Library** (Tufts) e **First1KGreek** (Leipzig): textos gregos
  e latinos e traduções inglesas, em TEI, sob CC BY-SA 4.0. Convertidos do XML
  de origem, com o commit do repositório anotado.
- **The Latin Library**: textos latinos de edições antigas, em domínio público.
- **Bíblias**: Almeida 1911, Tradução Brasileira 1917 e Bíblia Livre (via
  github.com/damarals/biblias), Vulgata Clementina, Douay-Rheims, o Codex de
  Leningrado (WLC), o SBLGNT (CC BY 4.0) e a Septuaginta de Swete (First1KGreek).
- **eBooksBrasil**: traduções em português, sob os termos gerais do site
  (distribuição gratuita, sem uso comercial).
- **Trabalho próprio**: transcrições por OCR de exemplares digitalizados,
  traduções e interlineares, marcados com `pa_exclusive`.

## O que o acervo normaliza

- **Os metadados.** Todo arquivo tem um front matter na mesma norma
  (`frontmatter.schema.json`): campos em inglês, valores de lista fechada, nenhum
  campo vazio. Um portão automático recusa o arquivo que não está na norma.
- **O endereço.** Cada obra tem uma URN no padrão CTS; cada passagem, uma âncora
  (`#marker-216a`, `#anchor-gn-1-1`). Endereço publicado não muda nunca: quando o
  texto muda, o endereço antigo continua levando ao mesmo ponto.
- **As notas.** Nota de editor ou de tradutor sai do texto corrido e vai para o
  fim, como nota numerada.
- **A estrutura.** Os marcadores da tradição (Stephanus, Bekker, capítulo e
  versículo, páginas de Spanheim) viram marcadores visíveis; o verso mantém a
  quebra de linha.

## O que o acervo preserva

- **O texto da fonte.** Não se moderniza grafia, não se "corrige" o editor.
  Suplemento do editor fica entre ⟨ ⟩, trecho espúrio entre [ ], como na edição.
- **Os erros conhecidos, até serem conferidos.** Erro de digitalização
  corrigido é corrigido contra a fonte, e a correção fica no histórico público do
  repositório. Erro ainda não conferido (por exemplo, o OCR da Septuaginta de
  Swete) fica como está, e é apontado.
- **A voz de quem preparou.** Quem preparou cada arquivo está no campo
  `processing`, pessoas e programas (inclusive modelos de linguagem usados como
  ferramenta), sem esconder nenhum.

## Como citar

Cada obra traz, no topo da sua página em https://pedraangular.app.br/rolo/, a
citação pronta e o BibTeX. O acervo inteiro tem versões numeradas, e cada versão
fica guardada no Zenodo, com DOI: o acervo como um todo se cita por
[10.5281/zenodo.23068915](https://doi.org/10.5281/zenodo.23068915), que leva sempre
à versão mais nova — e é por ali também que se baixa o acervo completo.

## Correções

Erro encontrado? O histórico e o código estão em
https://github.com/brunogreinert2/app-leitura. Toda correção entra pelo mesmo
portão e fica registrada.

> Ὁ Διαφορεύς παρῆν
