# NORMAS DO ECOSSISTEMA

Norma rígida e comum a todo software do Διαφορεύς: Pedra Angular (app-leitura),
Historinhas (app-infantil), o kit do rolo (Rolo_HTML), a Oficina e o
ateliedeotica.com.br quando existirem.

Este arquivo é normativo, não descritivo. Onde ele diverge do código, o código
está errado. Onde uma norma cita um app que já a cumpre, aquele app é a
referência de implementação — copiar de lá, não reinventar.

Versão 2 · 2026-08-08 · Escrito a partir de auditoria dos três projetos
existentes. A versão 2 acrescenta a LEI 8 e o Capítulo 1 (a Barra Angular),
decisão do Διαφορεύς, e corrige a justificativa do prefixo de token (N14, N55).

Versão 3 · 2026-09-30 · O formato volta a ser um só e generoso (N7, N8, N9):
nenhum app tem sintaxe menor que os outros, e o que um app ainda não desenha
aparece como texto. As normas que só valem para o app infantil (N51, N52)
passam para o Capítulo 14; **todo o resto vale para o ecossistema inteiro.**

Versão 4 · 2026-10-01 · LEI 9, AI FIRST: a pessoa e a IA dela pilotam as
mesmas ferramentas, e toda ferramenta ensina como ser pilotada.

Escopo verificado: `C:\Claude\app-leitura`, `C:\Claude\app-infantil`,
`C:\Claude\Rolo_HTML` e `C:\Claude\oficina`. A Oficina nasceu conforme em
2026-08-09 (`github.com/brunogreinert2/oficina`) e é hoje a referência de
implementação da LEI 8 e da LEI 2 aplicada a uma ferramenta. O
ateliedeotica.com.br ainda não existe — nasce já conforme, tendo a Oficina
como molde.

---

## Preâmbulo: o que você tem, de verdade

Não são quatro apps parecidos. São **três camadas** do mesmo objeto, e a
confusão desta pasta vem de tratá-las como se fossem a mesma coisa.

| Camada | O que é | Formato | Quem lê | Existe hoje em |
| --- | --- | --- | --- | --- |
| 1. Acervo | a verdade | `.md` com front matter | humano que edita, Pandoc, XeLaTeX, IA | app-leitura `public/livros/`, app-infantil `src/conteudo/livros/` |
| 2. Rolo | a sobrevivência | HTML estático, texto no `<body>` | IA, crawler, navegador sem JS, pendrive de 2046 | app-leitura `/rolo/`, Rolo_HTML |
| 3. App | o conforto | SPA interativa | humano com as mãos no aparelho | app-leitura, app-infantil |

A camada 3 é a única opcional. Um app que não entrega as camadas 1 e 2 não é
um app do ecossistema — é um beco sem saída.

Foi exatamente esse o diagnóstico que você fez sozinho: o Pedra Angular tinha
todos os objetivos certos e mesmo assim entregava casca vazia para a IA.
O rolo não foi remendo nem redundância. Foi a camada que faltava, descoberta
tarde. **A redundância que você acha que criou não é redundância: é a camada
2 aparecendo pela primeira vez.** O erro não foi ter dois; foi o app-infantil
ainda ter um só.

E a Filosofia UNIX está certa e permanece: um programa por necessidade. O que
o UNIX exige junto, e é o que faltava aqui, é o **formato comum entre os
programas** — o `|` do pipe. No seu ecossistema o pipe é o `.md` com front
matter. Programas diferentes, formato único.

---

## Capítulo 0 — As leis

Leis não têm exceção, não têm configuração e não se rediscutem por sessão.
Toda norma numerada abaixo existe para servir a uma delas.

Os números `N` são identificadores estáveis, não uma ordem de leitura: uma
norma nova entra com o próximo número livre, no capítulo a que pertence.
Nunca renumerar — normas se citam por número em commits e em outros
documentos.

### O princípio que explica todas elas

> Tudo pensado em quem não enxerga direito e vai no *feeling* até a
> configuração na qual ele tem condições de ler. Testando no caso mais
> difícil, o fácil se torna ridiculamente fácil.
>
> — Διαφορεύς, 2026-08-08

É esta a razão de o piso ser alto, e não um capricho. O usuário de referência
do ecossistema não é quem lê confortavelmente: é quem chega sem enxergar
direito, mexe no A+ às cegas, tenta um tema, tenta outro, e para quando
finalmente consegue ler. Toda decisão se julga por esse percurso.

Três consequências que não são óbvias e valem escrever:

1. **O caminho até a configuração boa precisa ser legível na configuração
   ruim.** Por isso a barra existe desde a primeira tela (N65) e por isso o
   A+ não pode viver escondido dentro de um menu.
2. **Nada pode depender de acerto na primeira tentativa.** Quem vai no
   *feeling* erra várias vezes de propósito. Toda escolha é reversível, ao
   vivo, sem confirmação e sem penalidade.
3. **Projetar para o caso difícil dispensa projetar para o fácil.** Contraste
   de 7:1 serve quem enxerga bem; alvo de 44 px serve o dedo firme; foco
   visível serve quem usa mouse. O contrário nunca é verdade.

**LEI 1 — Legível por humanos e por máquinas.**
Toda obra publicada deve ser recuperável em texto integral por quem apenas
busca a URL, sem executar JavaScript. "Máquina" significa, em ordem de
prioridade: LLM, crawler, `curl`, Pandoc, XeLaTeX. A IA é a leitora
privilegiada — deve gastar o mínimo e ler o máximo.

**LEI 2 — O que não está no `<body>` não existe.**
Corolário operacional da Lei 1, e a lição mais cara já aprendida aqui:
extratores de HTML descartam `<script>` e `<style>` antes de olhar. Texto
dentro de `const CORPUS_MD = ...` é tão invisível quanto uma SPA vazia.

**LEI 2-B — O que o service worker sequestra também não existe.**
Irmã da Lei 2, descoberta em 2026-08-08. Não basta o arquivo estar certo no
servidor: se o service worker devolve a casca da SPA para aquela URL, a obra
está inalcançável para todo mundo que já visitou o site uma vez — e continua
alcançável só para quem faz `fetch` puro. É o pior tipo de defeito, porque a
única testemunha que consegue ler é justamente a que não reclama.

Toda camada 2 é verificada **com o service worker instalado e no comando**,
nunca só com `fetch` e nunca só no servidor de desenvolvimento (que não tem
service worker nenhum — foi exatamente aí que este defeito se escondeu).

**LEI 3 — Zero rede em runtime.**
Nenhum artefato depende de outro sistema para funcionar. Sem CDN, sem fonte
remota, sem chamada de API para renderizar. Vale para o app, para o rolo e
para qualquer coisa que venha depois.

**LEI 4 — Acessibilidade é piso, não acabamento.**
Contraste, foco, movimento, língua e alvo de toque não são polimento de fim
de fase. Uma entrega que rebaixa o piso não é entrega.

**LEI 5 — Acessibilidade vence decoração, sempre e sem configuração.**
Quando necessidade e estética colidem, a necessidade ganha automaticamente —
nunca por meio de uma opção que alguém precise achar e ligar.

**LEI 6 — Id publicado é eterno.**
Id de obra, de asset, de âncora e de seção nunca muda depois de publicado.
Índice, pasta, título e ordem podem ser reorganizados à vontade.

**LEI 7 — O app nunca escreve no acervo.**
Leitura é sempre unidirecional. Nenhum app edita, grava de volta ou altera
arquivo de origem. Estado do usuário vive em armazenamento próprio.

**LEI 8 — A barra angular.**
Todo app abre com os mesmos quatro controles, no mesmo lugar, com a mesma
aparência: **Φ · A− · A+ · Ξ**. Nenhuma especialização os desloca, os
renomeia, os esconde ou os substitui por outra coisa. O que cada app tem de
único vem **depois** deles, nunca no lugar deles.

Primeiro o básico bem feito e robusto; a especialização é o que se constrói
sobre ele. Detalhamento no Capítulo 1.

**LEI 9 — AI FIRST.**
Tudo é feito para ser pilotado por uma pessoa e pela IA dela, com o mesmo
direito. Toda ferramenta ensina, em texto que se lê sem executar nada, como
pilotá-la; o que ela ainda não sabe fazer vira capacidade nova dela, não
contorno feito por fora. E nada nos acorrenta: nenhum software privativo,
nada pesado sem necessidade.

É o que a LEI 1 já dizia antes de ter nome — legível por humanos e por
máquinas — levado das obras às ferramentas. (Διαφορεύς, 2026-10-01)

> A pé, em uma hora, poucos quilômetros. De moto, a praia.

---

## Capítulo 1 — A Barra Angular

O trocadilho é literal e a estrutura também: esta barra é a pedra angular dos
apps — a pedra que se assenta primeiro, no canto, e a partir da qual todo o
resto ganha esquadro. Um app que ainda não tem estes quatro botões prontos e
iguais aos dos outros não está pronto para se especializar em nada.

**N60 — Os quatro controles e o que significam.** São sempre estes quatro, com
este significado em qualquer app do ecossistema:

| Botão | Significa | Abre | Exemplo por app |
| --- | --- | --- | --- |
| **Φ** | a coleção — tudo o que este app oferece | o acervo inteiro, do começo | biblioteca (Pedra Angular) · estante (Historinhas) · catálogo (Oficina) · coleção (ótica) |
| **Ξ** | a estrutura do que está aberto — onde estou dentro disto | o sumário do que está na tela | sumário da obra · capítulos do livro · seções da página |
| **A−** | diminuir o corpo do texto | — | idêntico em todos |
| **A+** | aumentar o corpo do texto | — | idêntico em todos |

Φ é a marca e o caminho de volta ao todo. Ξ é a orientação dentro da parte.
Se um app não tem "coleção" ou não tem "estrutura interna", ele ainda tem os
quatro botões — o que falta é o app, não o botão. Nesse caso, resolva o que
Φ e Ξ abrem antes de escrever a primeira tela.

**N61 — Posição e ordem, nunca negociáveis.** Φ na extremidade esquerda da
barra do topo, Ξ na extremidade direita, A− e A+ entre os dois, nesta ordem.
Nada se insere fora desse intervalo; o que for específico do app entra
**entre** A+ e Ξ.

A ordem não é estética. A barra representa o Διαφορεύς em pé, de frente, em
posição anatômica: Φ e Ξ são as tatuagens da face anterior dos antebraços
dele, espelhadas. Trocar de lado inverte a pessoa. Ver também N54 no
Capítulo 12.

Consequência boa e não planejada: os controles de leitura ficam no meio, entre
os dois braços. É onde a mão pousa.

**N62 — Uma primitiva só, mesma aparência nos quatro botões e nos quatro
apps.** Todos herdam a mesma caixa; só o glifo muda.

```css
.ui-botao-barra {
  min-width: 2.75rem;
  min-height: 2.75rem;
  padding: var(--ui-esp-2) var(--ui-esp-3);
  border: 2px solid currentColor;
  border-radius: var(--ui-raio-2);
  background: none;
  color: var(--ui-acento);
  font-size: 1.5rem;
  font-weight: 700;
  line-height: 1;
}
.ui-botao-barra--grego { font-family: var(--ui-fonte-serifada); }
```

Mesma cor (`--ui-acento`, portanto acompanhando o tema), mesmo tamanho, mesmo
raio, mesmo alvo de toque, mesmo anel de foco (Capítulo 7). Nenhum app
redefine isso; se um app precisa de outra coisa, ou a norma muda para todos ou
o app está errado.

Os valores acima são proposta de implementação, não lei — a lei é que os
quatro sejam idênticos entre si e entre os apps. Ajustar é decisão do Διαφορεύς,
uma vez, para todos.

**N63 — Φ e Ξ são letras, nunca ícones.** Texto real, em fonte serifada,
selecionável e copiável. Nada de SVG, sprite, imagem ou fonte de ícones.
Motivo prático: acompanham o tema e o corpo do texto de graça, e sobrevivem
a qualquer navegador. Motivo real: são letras.

**N64 — Rótulo acessível obrigatório e fixo.** Os quatro botões carregam
`aria-label` em português, sempre, porque o glifo sozinho não se explica para
leitor de tela nem para quem não lê grego:

| Botão | `aria-label` |
| --- | --- |
| Φ | `Abrir <nome da coleção deste app>` |
| Ξ | `Abrir sumário` |
| A− | `Diminuir letra` |
| A+ | `Aumentar letra` |

**N65 — A barra existe desde a primeira tela.** Não aparece só ao abrir uma
obra. Se o app tem uma tela de escolha de perfil, ela também tem a barra.
Um app cujo A+ só funciona lá dentro falha para quem precisa do A+ para
conseguir ler a primeira tela.

**N66 — O que pode entrar na barra.** Só controle que valha para a tela
inteira e que o usuário use com frequência real. Entra entre A+ e Ξ. Tudo o
mais vai para dentro do Ξ. A barra não é gaveta.

**Estado hoje:**

| | Φ | Ξ | A− | A+ | Mesma aparência |
| --- | --- | --- | --- | --- | --- |
| **rolo, obra** | sim, índice dos rolos | sim, capítulos | sim | sim | **sim** — os quatro idênticos, verificado |
| **rolo, índice** | sim, índice dos rolos | sim, seções da página | sim | sim | **sim** — os quatro idênticos, verificado |
| app-leitura | sim, biblioteca | sim, sumário | sim | sim | **não** — três estilos diferentes entre os quatro |
| app-infantil | **não existe** | **não existe** | sim | sim | **não** — `.botao-icone`, outro estilo |

O rolo é a implementação de referência desde 2026-08-08, nas duas famílias de
página. Antes disso o Φ existia como `<div class="phi" aria-hidden="true">` —
enfeite que não abria nada e que leitor de tela nem via —, o Ξ não existia, e
as páginas de índice não tinham barra nenhuma: nem tema, nem A−/A+, nem
sumário, nem foco de teclado.

Duas decisões tomadas ali que valem para quem for implementar nos apps:

1. **A fila angular é a primeira fila da barra.** Numa barra que quebra em
   várias linhas no celular, "Φ na ponta esquerda e Ξ na ponta direita" só
   significa alguma coisa dentro de uma fila. As filas seguintes são o que
   aquela superfície tem de específico (ouvir, temas, abrir/recolher).
2. **A capa pode manter um Φ ornamental.** O Φ grande do cabeçalho da obra
   continua lá, `aria-hidden`, como marca; o Φ funcional vive na barra fixa.
   Leitor de tela ouve um só. Marca e controle não competem porque não estão
   no mesmo lugar.

Armadilha encontrada na implementação, digna de registro: uma regra genérica
antiga (`.barra-topo button`) tinha especificidade maior que `.ui-botao-barra`
e vencia — o resultado era Φ (um `<a>`) com uma aparência e A−/A+/Ξ
(`<button>`) com outra, dentro da mesma fila. **A primitiva precisa ganhar a
disputa de especificidade contra o que já existe**, senão a LEI 8 passa a
existir no CSS e não na tela. Conferir com `getComputedStyle` nos quatro,
nunca de olho.

Nos apps, os mesmos quatro papéis ainda usam quatro estilos incompatíveis:
`.font-button` (borda 2px na cor do texto), `.phi-button` (Georgia, sem
borda, na cor do acento), `.toc-button` (menor, sem `min-width`) e
`.botao-icone` (46px, fundo preenchido, raio 14px).

---

## Capítulo 2 — Anatomia obrigatória

**N1.** Todo app do ecossistema entrega três saídas para o mesmo conteúdo:

1. o `.md` fonte, acessível como arquivo;
2. um rolo HTML estático por obra, com o texto escrito no `<body>`;
3. a interface interativa.

**N2.** O rolo é gerado, nunca escrito à mão. O gerador vive no repositório do
app e roda no deploy.

**N3.** O rolo de uma obra e a obra no app compartilham o mesmo `id`. Um link
do app e um link do rolo falam do mesmo objeto sem tabela de conversão.
Referência: `app-leitura/scripts/rolo/gerador_rolo.py`, que usa o `id` do
`catalogo.json` como nome de arquivo.

**N4.** O rolo carrega tudo: texto, fonte, programa e voz. Um arquivo, aberto
por duplo clique, sem instalar nada, offline.

**N5.** Todo rolo tem rede de segurança: se o motor JavaScript falhar, o texto
reaparece. Implementação de referência em `rolo_template.html` linhas 569–580
(`try { montar(); } catch { documentElement.classList.remove('js') }`).

**N67.** O service worker nunca intercepta a camada 2. Todo app com service
worker declara explicitamente as rotas que ficam de fora do `navigateFallback`
— no mínimo a pasta dos rolos e a pasta do corpus cru.

Em `vite-plugin-pwa`/Workbox, o `generateSW` registra por padrão uma
`NavigationRoute` que devolve `index.html` para **toda** navegação, e a lista
de exceções nasce vazia. Referência da correção:

```ts
workbox: {
  navigateFallbackDenylist: [/^\/rolo(\/|$)/, /^\/livros(\/|$)/],
}
```

O `(\/|$)` não é enfeite: sem ele, `/rolo` sem barra final continua sendo
sequestrado; com ele, `/roloteria` continua sendo rota legítima da SPA.

**Proibido:** publicar obra que só exista dentro de uma SPA.

**Estado hoje:** app-leitura cumpre N1 e, desde 2026-08-08, cumpre N67 —
antes disso `/rolo` era inalcançável por navegador para qualquer pessoa que
já tivesse visitado o site, e só respondia a `fetch`. **app-infantil viola
N1** — não tem camada 2. Sete livros existem apenas dentro do bundle. É a
maior lacuna aberta do ecossistema, e quando ela for fechada o N67 já vale
desde o primeiro dia.

---

## Capítulo 3 — O formato único

**N6.** Todo conteúdo é um arquivo `.md`: front matter YAML + texto. Sem
exceção, em qualquer app.

**N7.** O formato é um só, para o ecossistema inteiro, e é generoso: nenhum
app tem uma sintaxe menor que a dos outros. Um arquivo escrito para um app
serve para qualquer outro. A sintaxe comum:

| No texto | É |
| --- | --- |
| `#{1,}` seguido de espaço e texto | cabeçalho, profundidade arbitrária (N10) |
| linha não vazia | parágrafo (CommonMark) |
| `> texto` | citação, assinatura (`> Ὁ Διαφορεύς παρῆν`), linha de interlinear |
| `[[Nome]]` | ligação a um personagem ou a outra obra (wikilink) |
| `![descrição](caminho)` ou `{{img:id}}` sozinha na linha | imagem |
| `[^n]` e `[^n]: nota` no fim | nota |
| `^id` e `^por`, `^grc`… no fim da linha | âncora (N12) e idioma (N76) |
| `[216a]`, `[1.1]` | marcador canônico (N11) |
| bloco ` ```verso ` ou ` ```interlinear ` | uma linha do arquivo, uma linha na tela |

Fora do formato: tabela, `==realce==`, HTML/XML e a palavra `null` vazada. A
régua executável é o esquema e o validador do acervo
(`app-leitura/scripts/acervo/frontmatter.schema.json` e `validar_corpus.py`),
que o conferidor do Pórtico usa no navegador.

**Cada app desenha o que já sabe desenhar; o que ainda não sabe, mostra como
texto, e nunca quebra.** Uma sintaxe que um app ainda não desenha é trabalho a
fazer nele, não proibição no formato. Revisão de 2026-09-30 (Διαφορεύς): a
versão anterior desta norma (três regras, sem `>`, sem wikilink, sem `![]()`)
descrevia o parser dos livrinhos do app-infantil e fazia qualquer leitor desta
norma proibir no acervo o que o acervo usa.

**N8.** O texto é limpo, o front matter é rico. Toda riqueza — mídia, tema,
abertura, quiz, narração, identidade, licença — entra por declaração no front
matter e âncora por id, não por marcação espalhada no texto.

**N9.** Imagem se escreve de um dos dois jeitos do N7: `{{img:id}}` (o asset
declarado no front matter, com descrição e licença lá) ou `![descrição](caminho)`.
Toda imagem tem descrição, para quem não a vê.

**N10.** Profundidade de cabeçalho não tem teto. O limite de 6 é herança do
HTML de 1991, não regra do Markdown. Níveis 7+ saem como
`<div role="heading" aria-level="N">`. Já provado em produção: `LATIM.html`
com 8 níveis, `ProvaDeFogo` com 17.

**N11.** Marcador canônico nunca é reformatado. `[327a]`, `1094a1`, `Jo 1:1`,
`§1` são endereços, não texto. Podem ser destacados; não podem ser tocados.

**N12.** Âncora `^id` no markdown vira `id="id"` no HTML, nos dois sentidos e
nas duas camadas. Sujeita à Lei 6.

**Estado hoje (2026-09-30):** cada app tem o parser do seu uso, e nenhum é "o
certo" do outro. O app-leitura (`remark`) e o rolo desenham o formato quase
inteiro; falta a imagem (`{{img:id}}` e `![]()`), que chega com as obras
ilustradas (Piso & Marcgrave). O app-infantil (`src/motor/parser.ts`) desenha
cabeçalho, imagem e parágrafo; `>` e wikilink aparecem como texto até um
livrinho pedir por eles.

---

## Capítulo 4 — Tokens visuais

**N13.** Todo valor de cor, espaço, raio, sombra e transição é um token. Valor
literal em regra de estilo é proibido, exceto nos casos do N20.

**N14.** Prefixo único: `--ui-`. Nomes semânticos em português, descrevendo
**função**, nunca aparência.

Motivo do prefixo: distinguir, de relance, peça do sistema de peça local.
`--ui-fundo` é comum aos quatro apps; `--app-fundo` é só daquele app.
Sem o prefixo não dá para saber qual é qual sem abrir outro arquivo.

Nota de 2026-08-08: a primeira versão desta norma justificava o prefixo neutro
pela separação entre a pseudonímia do Διαφορεύς e o nome real na ótica. **Esse
argumento não vale** — o registro `.app.br` já exige e expõe o nome real, e a
decisão do Διαφορεύς é conviver com isso. A pseudonímia segue como escolha de tom
e de estética, nunca como requisito de segurança. Não reabrir.

Motivo do nome funcional: no tema pergaminho o acento não é azul, e um token
`--ui-azul` com valor marrom é uma mentira que se propaga por anos.

**N15.** Vocabulário canônico. As três grafias atuais são substituídas por
esta, e apenas por esta:

| Token | Papel | Hoje no app-leitura | Hoje no app-infantil | Hoje no rolo |
| --- | --- | --- | --- | --- |
| `--ui-fundo` | fundo da página | `--color-bg` | `--fundo` | `--bg` |
| `--ui-superficie` | cartão, painel, diálogo | `--color-surface` | `--cartao` | `--surface` |
| `--ui-texto` | texto corrido | `--color-text` | `--texto` | `--ink` |
| `--ui-texto-suave` | texto secundário | `--color-muted` | `--texto-suave` | — |
| `--ui-acento` | link, destaque, marcador | `--color-accent` | `--destaque` | `--accent` |
| `--ui-titulo` | cor de título (herda acento) | — | `--titulo` | — |
| `--ui-linha` | separador decorativo | `--color-border` | — | `--line` |
| `--ui-contorno` | borda que identifica componente | `--color-borda-ui` | `--borda` | — |
| `--ui-erro` | estado de erro | `--color-error` | — | — |
| `--ui-realce-fundo` / `--ui-realce-texto` | achado de busca, marca-texto | `--hl-bg` / `--hl-fg` | — | — |
| `--ui-realce-atual-fundo` / `--ui-realce-atual-texto` | ocorrência atual | `--hl-cur-bg` / `--hl-cur-fg` | — | — |
| `--ui-sombra` | cor ou valor da sombra | `--shadow-color` | `--sombra` | — |
| `--ui-papel` | marca d'água de fundo | — | `--papel` | — |
| `--ui-foco` | anel de foco de teclado | — | — | — |
| `--ui-escala-fonte` | multiplicador de corpo | — | — | `--font-scale` |

`--ui-linha` e `--ui-contorno` são tokens distintos e continuam distintos
mesmo quando um tema lhes dá o mesmo valor. A separação é semântica e tem
piso diferente (ver N29). Está justificada em
`app-leitura/scripts/medir_contraste.py` linhas 149–153.

`--ui-foco` é token novo: nenhum dos três o tem hoje, e o rolo usa
`--ui-acento` no lugar — o que produz um anel de foco a 1,89:1 no tema
pergaminho dele. Ver N26.

**N16.** Tema é trocado por `data-theme` **no elemento `html`**, nunca no
`body`. O rolo hoje usa `body` e deve migrar.

**N17.** O tema padrão vive em `:root` e não tem seletor próprio. Sair do
padrão é `delete documentElement.dataset.theme`. Referência:
`app-leitura/src/components/ThemeDialog.tsx` linha 53.

**N18.** A paleta existe em **um** lugar. Nenhuma cópia manual em TypeScript,
JSON, manifesto ou meta tag. Onde a interface precisar da cor de um tema
(preview de botão, `theme-color`, `manifest.json`), o valor é lido do CSS em
tempo de execução ou gerado a partir dele em build — nunca redigitado.

**Estado hoje:** violado. `app-leitura/src/components/ThemeDialog.tsx` linhas
28–38 redigita 18 valores dos nove temas; `index.html`, `vite.config.ts` e um
fallback redigitam `#2b2620` e `#faf7f2`. O botão de preview de tema é
justamente o que uma pessoa com baixa visão usa para escolher — é o pior
lugar possível para uma cópia que pode dessincronizar em silêncio.

**N19.** Escalas fechadas. Nenhum valor avulso fora destas:

| Escala | Valores permitidos |
| --- | --- |
| espaço | `--ui-esp-1` a `--ui-esp-8`: 0,25 / 0,5 / 0,75 / 1 / 1,5 / 2 / 3 / 4 rem |
| raio | `--ui-raio-0` a `--ui-raio-3`: 0 / 0,25rem / 0,5rem / 1rem, mais `--ui-raio-pilula` (999px) e `--ui-raio-circulo` (50%) |
| sombra | `--ui-sombra-1` (repouso), `--ui-sombra-2` (elevado), `--ui-sombra-3` (modal) |

Hoje o app-leitura tem 8 raios em 3 unidades diferentes e 11 espaços distintos
abaixo de 1rem; o app-infantil tem 9 raios em px. Nenhum dos dois precisa
dessa variedade — é ruído, não vocabulário.

**N20.** Únicos valores literais permitidos em regra de estilo, porque a
unidade correta é mesmo o pixel: espessura de borda (`1px`, `2px`, `3px`),
deslocamento e desfoque de `box-shadow`, `border-radius: 50%`,
`outline-offset`. Tudo o mais é token.

---

## Capítulo 5 — Tipografia e corpo de texto

**N21.** Nenhum tamanho de fonte em pixel absoluto, em lugar nenhum, incluindo
o que o JavaScript escreve em tempo de execução.

O controle de corpo do usuário é um **multiplicador** aplicado sobre valores
em `rem`. Implementação de referência: `--font-scale` do
`rolo_template.html`, entre 0,8 e 2,6.

**Estado hoje:** violado nos dois apps, pelo mesmo mecanismo.
`app-leitura/src/components/FontControls.tsx` linha 46 grava `${px}px`;
`app-infantil/src/telas/preferencias.ts` linha 97 grava `${px}px`. Os dois
declaram o padrão corretamente em unidade relativa no CSS e o destroem no
primeiro `useEffect`/`aplicarTamanho`.

Consequência: **os dois apps ignoram o tamanho de fonte que a pessoa já
configurou no Android, no iOS ou no navegador.** Para o público dos dois apps
— um leitor idoso de baixa visão e uma criança de 7 anos cujo pai já
aumentou a fonte do tablet — essa é justamente a configuração que já foi
feita antes de o app abrir.

Correção: guardar o multiplicador, não o pixel. O intervalo do app-leitura
(12–256 px, sem teto tímido) está certo em espírito e vira 0,66× a 14×; o
teto de 30 px do app-infantil é apertado demais para o mesmo público e sobe.

**N22.** Fonte sempre embutida, nunca CDN (Lei 3). Famílias canônicas do
ecossistema:

| Papel | Família | Origem |
| --- | --- | --- |
| leitura, padrão adulto | Atkinson Hyperlegible | arquivo local, 400/700, normal e itálico |
| leitura, padrão infantil | OpenDyslexic | arquivo local, 400/700 |
| serifada | Georgia, `'Times New Roman'`, serif | sistema |
| monoespaçada | `ui-monospace`, Consolas, monospace | sistema |

OpenDyslexic é padrão apenas no app-infantil, por decisão sua de 2026-07-19;
é opção em todos os outros. Padrão nunca é imposição: as três continuam
trocáveis pelo usuário em qualquer app.

**N23.** Toda família embutida tem a licença ao lado do arquivo. Hoje
`app-leitura/public/fonts/` cumpre; `app-leitura/scripts/rolo/fontes/` e
`Rolo_HTML/fontes/` não têm licença nenhuma.

**N70 — Um desenho, cobertura completa: a montagem principal + suplemento.**
Quando a fonte escolhida pelo seu desenho não cobre todos os caracteres do
corpus, **não se troca a fonte nem se aceita o buraco**. Declaram-se duas
faces sob a **mesma família**, e o `unicode-range` deixa o navegador escolher
por caractere:

```css
@font-face { font-family:'X'; src:url(x-400.woff) format('woff'); }
@font-face { font-family:'X'; src:url(x-suplemento-400.woff2) format('woff2');
             unicode-range: U+0370-03FF, U+1F00-1FFF, …; }
```

O suplemento vem **declarado por último**: onde as duas faces casam, o
algoritmo do CSS fica com a última.

Regras da montagem:

1. **As faixas se medem, não se escolhem a olho.** São exatamente os blocos
   que a face principal não cobre e o suplemento cobre. Ler os dois arquivos
   com `fontTools` e comparar os `cmap`.
2. **A pontuação do dia a dia fica fora da lista.** Travessão, aspas curvas,
   reticências e apóstrofo aparecem em qualquer frase em português; desviá-los
   troca o desenho no meio de uma linha. Se a face principal os tem, ela os
   serve.
3. **O nome do arquivo diz o papel, não a escrita.** `-suplemento-`, nunca
   `-grego-`: a lista cresce, e um nome estreito vira mentira.
4. **O que nenhuma das faces cobre continua no fallback**, e isso se declara
   por escrito no comentário do arquivo.
5. **Nunca confiar no número da versão de uma fonte.** Conferir a tabela
   `name` do binário (ver N71).

**Estado hoje:** montagem em vigor no app-leitura e no app-infantil, com a
**mesma lista de dez faixas** — 868 caracteres que antes caíam numa fonte de
sistema no meio da página. Vale para a Oficina e para toda superfície nova.

**N71 — A procedência de uma fonte se lê no binário, não no arquivo ao lado.**
`OFL.txt` e `README.md` são soltos: viajam entre pastas, sobrevivem a forks e
ficam para trás quando o binário sai. A tabela `name` viaja dentro do arquivo.

```bash
python -c "
from fontTools.ttLib import TTFont
f = TTFont('X-Regular.otf', lazy=True)
for nid in (0,1,5,8,9): print(nid, f['name'].getDebugName(nid))
"
```

Dois casos reais, ambos de 2026-08-09: o repositório do EB Garamond
distribuía um `OFL.txt` com copyright de um fork cujos binários já tinham sido
removidos de lá; e o pacote npm `open-dyslexic` publica como "2.001" um build
**anterior** ao "0.920" — o projeto renumerou depois de reescrever a fonte.
Nos dois casos o texto ao lado mentia e o binário dizia a verdade.

**N72 — A pilha termina em fonte nossa; o sistema operacional é último
recurso.** Nenhum caractere que o ecossistema publica pode depender do
aparelho para ter forma. Fonte do sistema entra apenas depois de todas as
nossas, e para o que nenhuma delas cobre.

**A serifada canônica é a Cardo** (David J. Perry, OFL). Ela é o piso: cobre
latim com macrons e breves, grego politônico e hebraico com niqud — as três
escritas do acervo, num desenho só. Toda pilha de fonte, em qualquer
superfície, passa por ela antes de chegar ao sistema:

```
<escolha do usuário> → <suplemento da própria família> → Cardo → <SO> → genérica
```

Medida contra a EB Garamond antes de escolher: a Garamond ganha em cirílico
(87% contra 0%) e em latim estendido (100% contra 65%), mas **não tem um
caractere hebraico**. O acervo tem 39 obras em hebraico e nenhuma em russo.
Se um dia entrar russo, a Garamond entra como suplemento pela N70 — não como
substituta.

**Por que isto é norma e não gosto.** Georgia existe no Windows e no iPhone e
**não existe no Android**; Segoe UI só existe no Windows. Antes desta norma o
mesmo versículo em hebraico saía com uma letra no computador, outra no tablet
e outra no celular — e nenhuma dessas era escolha do projeto. É o mesmo
problema das vozes do TTS, com a diferença de que a fonte tem conserto.

Onde a Cardo é apenas rede de segurança (o app-infantil, por exemplo), ela se
declara com `unicode-range` restrito ao que falta, para não pesar: os 143 KB
só são baixados se aparecer grego ou hebraico na tela.

**O que ainda cai no sistema, declarado:** árabe (1 obra) e cirílico. Nenhuma
das fontes embutidas os cobre. Isso se escreve no comentário do arquivo, para
não parecer resolvido.

**Estado hoje:** em vigor no app-leitura (onde a Cardo substituiu a Georgia
como padrão de leitura) e no app-infantil. Verificado ao vivo: as três opções
de fonte de cada app renderizam latim, grego politônico, hebraico e macrons a
partir de fonte própria.

**N73 — A guarnição: DejaVu Sans fecha toda pilha, e nenhuma fonte
proprietária entra nela.** Depois da fonte escolhida e do piso (Cardo) vem a
**DejaVu Sans**, e só então a genérica. Fonte do sistema operacional não
aparece em pilha nenhuma.

```
<escolha> → <suplemento da família> → Cardo → DejaVu Guarnicao → serif
```

**Por que existe.** O corpus não é fechado: os apps importam arquivos e aceitam
texto colado. Um caractere que ninguém previu tinha duas saídas ruins — caixa
vazia, ou o desenho do aparelho, diferente em cada um. Com a guarnição, ele cai
sempre na mesma letra, em qualquer sistema, offline.

**Por que a Sans e não a Serif.** Medido: a DejaVu **Serif** não tem um
caractere hebraico e não tem árabe. A **Sans** tem 5955 caracteres e cobre
cirílico (100%), armênio, georgiano, hebraico (48% + 90% das formas) e árabe
(64%) — justamente o que caía no sistema. O contraste de desenho contra a
serifada de leitura é proposital: é sinal de que ali entrou algo fora do
previsto.

**Proibido em pilha de fonte:** `Times New Roman` (proprietária da Monotype),
`Georgia`, `Segoe UI`, `Arial` e qualquer outra do sistema. Não é questão de
licença — é que elas não existem em todo aparelho, e o que não existe em todo
aparelho não pode fazer parte da identidade.

**Documento novo é documento novo.** Aba de impressão e `iframe` de impressão
não herdam as `@font-face` do app: redeclará-las lá dentro é obrigatório.
Foi assim que a tabela do alfabeto grego saía no papel com a fonte do
aparelho — e no papel não há conserto depois.

**Φ e Ξ são letras gregas.** A marca do ecossistema (LEI 8) precisa vir de
fonte nossa como qualquer outro caractere. Desenhá-la com a fonte do aparelho
faz a marca mudar de forma entre um aparelho e outro — o oposto do que a
LEI 8 existe para garantir.

**Estado hoje:** em vigor no app-leitura (incluindo a aba de impressão), no
app-infantil (incluindo a tabela impressa) e na Oficina. **Pendente:** o rolo
ainda desenha Φ e Ξ com Georgia, no `rolo_template.html` e no
`gerador_rolo.py`.

**N74 — Peso do traço é escolha do leitor.** Face filológica costuma ser mais
leve que fonte de tela: medido pela área do desenho, Cardo tem 111,7 de tinta
contra 134,0 da Georgia — 17% a menos. Quem vem de uma sente a outra fina.

`font-weight` não resolve quando a família só tem 400 e 700: o 700 da Cardo
tem 161,5, é negrito e não corpo de texto. O contorno
(`-webkit-text-stroke` com `paint-order: stroke fill`) preenche o vão sem
trocar de fonte e sem pular degrau.

Três passos, ajustáveis pelo leitor, com o meio como padrão — porque é o que
devolve o peso que o app tinha antes. `paint-order: stroke fill` é obrigatório:
sem ele o contorno cresce para dentro e fecha o buraco do a, do e e do o.

**N24.** O `lang` correto (N33) continua obrigatório mesmo com a cobertura
resolvida: é ele que faz o TTS pronunciar grego como grego, e é o que permite
ao sistema escolher a fonte certa para árabe e cirílico, que seguem no
fallback.

**N25.** Medida de linha é declarada em `ch`, não em largura de caixa. Alvo:
`--ui-medida: 66ch`. Hoje o app-leitura usa `max-width: 42rem` e o
app-infantil `760px` — os dois entregam medida diferente conforme a fonte
escolhida, e o `760px` do app-infantil ainda é fixo em pixel.

---

## Capítulo 6 — Cor e contraste

**N26.** Pisos, medidos e não estimados:

| Par | Piso |
| --- | --- |
| texto corrido sobre o fundo | 7:1 |
| texto secundário sobre o fundo | 7:1 |
| texto sobre superfície (cartão, diálogo, drawer) | 7:1 |
| realce de busca e marca-texto | 7:1 |
| acento sobre fundo, quando é link ou texto | 4,5:1 |
| **anel de foco de teclado sobre o fundo** | **3:1, sem exceção** |
| contorno que identifica componente | 3:1 |
| separador decorativo | sem piso |

**N27.** Todo tema fixo passa por script de medição antes de existir. O script
lê os valores **do CSS publicado**, nunca de uma cópia digitada — medir uma
cópia é medir outra coisa. Implementação de referência:
`app-leitura/scripts/medir_contraste.py`, que já mede razão WCAG e simula
protanopia, deuteranopia e tritanopia (Viénot, Brettel e Mollon, 1999).

Este script é patrimônio do ecossistema e vale para todos os apps. Falta nele:
o par contra `--ui-superficie`, o par do anel de foco, e uma passagem pelos
temas do rolo — que hoje não são medidos por script nenhum.

**N69.** Ao medir contraste no navegador, **desligue as transições antes**.
`getComputedStyle(el).color` logo depois de trocar de tema devolve o valor
intermediário da transição, não o do tema — e num painel que não está
compondo quadros a transição nunca avança, então o valor fica congelado no
tema ANTERIOR. Em 2026-08-09 isso fez o mesmo botão medir 1,89:1 e 6,95:1 no
mesmo tema, dependendo só de quando se olhou.

```js
const s = document.createElement('style');
s.textContent = '*{transition:none!important}';
document.head.appendChild(s);
/* ... medir aqui ... */
s.remove();
```

Regra geral: propriedade animável medida logo após a mudança não é
observação, é palpite com número do lado.

**N28.** Toda cor escolhida pelo usuário em tempo de execução passa por
derivação com contraste garantido. O usuário escolhe fundo e acento; texto,
superfície, contorno e título são **derivados**, nunca escolhidos.
Implementação de referência: `derivarPaleta` e `garantirContraste` em
`app-infantil/src/telas/preferencias.ts` linhas 171–229.

Este é o melhor mecanismo do ecossistema e o app-leitura não o tem. Ele
resolve o problema que nenhum script de build resolve: cor que só existe
depois que o app abriu.

**N29.** Nenhum estado é comunicado apenas por cor. Sempre cor **mais** forma,
símbolo ou palavra. Regra da casa desde 2026-07-19, por causa da sua
protanomalia.

Referências corretas: quiz do app-infantil revela com ✓/✗ além da cor; cada
poço de tinta tem nome falável em `aria-label`; o realce da ocorrência atual
da busca no app-leitura é laranja e não amarelo, porque sob tritanopia o
amarelo colapsava com o realce comum — medido, não chutado.

**N30.** Quando o conteúdo propõe um tema e o usuário tem outro, o usuário
ganha. Tema de livro é convidado, nunca dono. E tema de acessibilidade
(alto contraste) ignora tema de conteúdo automaticamente, sem depender de
configuração — aplicação direta da Lei 5. Implementação de referência:
`aplicarTemaDeLivro` em `app-infantil/src/telas/preferencias.ts` linhas
114–125.

---

## Capítulo 7 — Foco, toque e teclado

**N31.** Foco de teclado sempre visível, em todo elemento focável, em todo
tema. Anel obrigatório:

```css
:focus-visible {
  outline: 2px solid var(--ui-foco);
  outline-offset: 2px;
}
```

`outline: none` sem substituto imediato é proibido.

O anel usa `--ui-foco`, token próprio, **nunca** o token de acento
diretamente — ver o que aconteceu no rolo (N26).

Onde o fundo do próprio elemento for a cor do anel, reescreva `--ui-foco`
localmente no contêiner; por ser variável, todo o interior herda. Referência:
`.update-banner` em `app-leitura/src/styles.css`.

**Estado hoje:** cumprido nos dois apps desde 2026-08-08, com `--ui-foco`
medido em todos os temas (mínimo 4,65:1, piso 3:1). O rolo cumpre desde
sempre, com duas ressalvas abertas: usa o acento como anel, o que produz
1,89:1 no tema pergaminho dele (N26), e ainda tem um
`.item-acao:focus-visible { outline: none }` na linha 128 do template, que
troca o anel por mudança de fundo — violação da própria norma, pendente.

**N32.** Alvo de toque mínimo 44×44 px, declarado em unidade relativa
(`2.75rem`), nunca em pixel fixo — senão o alvo não cresce quando o corpo do
texto cresce.

**Estado hoje:** app-leitura cumpre e é a referência (26 declarações de
`2.75rem`, com alvos maiores onde o erro motor custa mais caro).
app-infantil usa 44–56 px, acima do piso mas em pixel fixo. **O rolo viola o
piso**: `.coordenada .copiar` e `.ouvir-secao` a 38px, `.menu-secao` a 38×38,
`.item-acao` a 40px.

**N33.** Ampliação de alvo se faz com `padding` compensado por `margin`
negativa, nunca aumentando o corpo da fonte — o texto não pode dançar quando
o alvo cresce. Referência: `app-leitura/src/styles.css` linhas 1005–1012.

**N34.** Nem tudo que é tocável vira `<button>`. Um livro tem milhares de
marcadores canônicos, e milhares de paradas de tabulação atrapalhariam a
navegação por teclado muito mais do que ajudariam. A decisão está tomada e
documentada em `app-leitura/src/styles.css` linhas 1000–1004; quem revisar
que não a desfaça por reflexo.

**N35.** Todo app e todo rolo têm link "pular para o texto" como primeiro
elemento focável. O rolo cumpre; os dois apps não têm.

---

## Capítulo 8 — Movimento

**N36.** `prefers-reduced-motion` é obrigatório e a regra é sempre a mesma:

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

Duração quase nula, **não** `animation: none`. `none` impede o disparo de
`animationend` e quebra em silêncio qualquer código que espere o fim da
animação para seguir. O efeito visual é o mesmo; os eventos continuam
existindo. O rolo ainda usa a forma antiga (`rolo_template.html` linha 42) e
deve migrar.

**N37 bis.** Quando o movimento suprimido era o único sinal de um estado, a
regra de movimento reduzido **repõe um sinal estático** no mesmo bloco. Nunca
se apaga a animação e se deixa o vazio.

Casos já resolvidos, como referência: `.ref-flash` do app-leitura vira realce
estático em `--hl-bg`; `.retomada` do app-infantil vira fundo estático em
`--destaque` a 18%. Nos dois, o próprio temporizador de JavaScript que já
existia retira a classe depois — o realce não fica preso na tela.

**Estado hoje:** cumprido nos dois apps desde 2026-08-08. O rolo cumpre desde
sempre, na forma antiga.

**N37.** Nenhum movimento é a única forma de comunicar informação. Se a
animação transmite estado, o estado também aparece em texto, forma ou
símbolo. Corolário do N29 aplicado ao tempo.

---

## Capítulo 9 — Língua e voz

**N38.** Todo trecho em língua estrangeira carrega `lang` correto. Isso não é
metadado decorativo: é o que faz um leitor de tela e o TTS pronunciarem grego
como grego.

| Escrita | `lang` | `dir` |
| --- | --- | --- |
| português | `pt-BR` | ltr |
| grego antigo | `grc` — nunca `el`, que é o moderno, outra fonética | ltr |
| grego moderno | `el` | ltr |
| hebraico | `he` | rtl |
| latim | `la` | ltr |
| inglês | `en` | ltr |

**N39.** A detecção por faixa Unicode é a mesma em todo o ecossistema:
hebraico `U+0590–U+05FF`; grego `U+0370–U+03FF` e `U+1F00–U+1FFF`; cirílico
`U+0400–U+04FF`. Implementação de referência: `idioma_da_linha` em
`gerador_rolo.py` linhas 45–53.

**N40.** Código de idioma desconhecido nunca some em silêncio. Ele é coletado
e relatado ao fim da execução. Referência: `IDIOMAS_DESCONHECIDOS` em
`gerador_rolo.py` linhas 79–98 — foi assim que se descobriu que 326 páginas
em inglês estavam se declarando português.

**N41.** O TTS escolhe a voz **por trecho**, a partir do `lang` do trecho —
nunca uma voz global para o documento inteiro. Referência: `idiomaDoTexto` em
`rolo_template.html` linhas 304–308.

**N42.** Todo TTS do ecossistema carrega os três contornos de bug do
Chrome/Windows, já resolvidos e testados: atraso entre `cancel()` e `speak()`;
referência viva ao utterance para o coletor de lixo não matar a fala; e
fatiamento do texto em pedaços curtos encadeados por `onend`, contra a pausa
espontânea aos ~15 s. Implementação de referência: `app-infantil/src/tts.ts`,
com teste em `src/tts.test.ts`.

**N75 — A detecção decide sozinha só quando tem certeza; no resto, herda o
cabeçalho.** Faixa Unicode separa hebraico, grego e cirílico com certeza —
eles têm letras próprias. Português, inglês e latim dividem o mesmo alfabeto e
só podem ser distinguidos por palavras de função, que é palpite: só decide com
sinal claro **e** folga sobre o segundo colocado. Trecho com menos de seis
palavras não dá amostra nenhuma e herda o `language:` do arquivo — nunca um
`pt-BR` fixo. Era esse chute fixo que fazia a introdução em inglês do Leviathan
sair com sotaque brasileiro. Implementação de referência: `idiomaDoTexto` em
`app-leitura/src/lib/idioma.ts`.

**N76 — A etiqueta de idioma: `^por`, `^eng`, `^lat`, `^grc`, `^heb`, `^rus`.**
No fim da linha, mesma sintaxe da âncora de endereço que o corpus já usa:

```
In the beginning was the Word. ^eng
Curto ^eng
Linha com endereço e idioma. ^gn-1-1 ^eng
```

Quatro regras, e as quatro valem em **todas** as superfícies:

1. **Escrito vence inferido.** Havendo etiqueta, a detecção nem é consultada.
2. **A lista é fechada.** Só esses códigos viram idioma; qualquer outra âncora
   continua sendo endereço de passagem. Se fosse aberta, um `^ab` qualquer
   trocaria a voz sem que nada no texto denunciasse o erro — e para esse erro
   não há aviso, só uma frase saindo com a fonética errada.
3. **Convive com o endereço.** A etiqueta sai primeiro; o `^gn-1-1` continua
   intacto para o extrator de âncoras.
4. **É opcional.** Serve para o que a detecção não resolve: linha curta, verso
   solto, título de duas palavras, e sobretudo o interlinear, onde as linhas
   alternam de língua a cada uma.

A lista de códigos tem de ser **idêntica** nas duas implementações — `CODIGOS`
em `app-leitura/src/lib/idioma.ts` e `ETIQUETAS_IDIOMA` em `gerador_rolo.py`.
É o mesmo arquivo `.md` sendo lido nas duas superfícies; uma lista que diverge
faz o app e o rolo lerem o mesmo texto em vozes diferentes.

**N77 — Buscar `lang` no DOM sem limitar o escopo é um bug silencioso.** O
documento tem `<html lang="pt-BR">`; um `closest('[lang]')` solto encontra
sempre esse, em todo bloco, e desliga a detecção do texto inteiro sem que nada
no código pareça errado. A busca termina na raiz do corpo do texto. Referência:
`collectItems` em `app-leitura/src/components/TtsControl.tsx`.

**N79 — Faixa Unicode se escreve com `\u`, nunca com o caractere literal.**
Um caractere colado num arquivo pode se decompor — e uma classe de regex
decomposta continua sendo código válido, que compila, roda e não avisa nada.

Aconteceu: a classe do hebraico do app estava escrita com os caracteres crus, e
o U+FB1D se decompôs em U+05D9 + U+05B4. Para o motor de regex a classe virou
"U+0590–U+05FF, mais U+05D9 solto, mais a faixa **U+05B4–U+FB4F**" — vinte e
cinco mil pontos de código que não são hebraico, incluindo todo o grego
politônico. Consequência: Homero, o Novo Testamento grego e o corpo de Platão
saíam marcados `lang="he" dir="rtl"`, escritos da direita para a esquerda. O
grego *sem* acentos escapava, o que fazia o defeito parecer aleatório.

A regra não é estética. Faixa literal é a única categoria de erro do ecossistema
em que **olhar o código não adianta**: os dois textos são idênticos na tela.

**N78 — Voz aproximada é anunciada, e voz ausente pula o trecho.** Latim não
tem voz em sistema nenhum: cai no italiano, no espanhol ou no português, nessa
ordem. Quem ouve merece saber que é aproximação em vez de achar que é a
pronúncia certa. E se não houver nem aproximação, o trecho é pulado com aviso —
melhor calar do que ler com a fonética errada.

**Estado hoje.** A lógica de língua estava escrita **três vezes** (duas em
Python, uma em JavaScript) e **em nenhum dos dois apps**. O app-leitura foi
corrigido em 2026-08-14; o app-infantil continua aberto:

| Projeto | `lang` por trecho | Voz por trecho | Etiqueta `^eng` |
| --- | --- | --- | --- |
| rolo / `gerador_rolo.py` | sim, correto | sim, correto | sim |
| app-leitura | sim — `idioma.ts`, fonte única | sim, com aviso de aproximação | sim |
| app-infantil | **não** — nenhum `lang` além do `pt-BR` do documento | **não** — `fala.lang = 'pt-BR'` fixo | não |

A lacuna que resta é a do app-infantil — cujo livro do alfabeto grego foi ideia
do Davi e é o conteúdo que ele mais usou: escreve `Α`, `α` e `Αλφα` sem nenhum
`lang` e fala tudo com voz brasileira. A transliteração ("Alfa", "Beta") no
`alfabetos.ts` é um contorno inteligente para o nome falado, mas os caracteres
gregos da tela e da tabela impressa continuam mudos quanto ao idioma.

---

## Capítulo 10 — Impressão

**N43.** Impressão é sempre A4, e o conteúdo é projetado para caber. Nada de
desenho quebrando em três páginas. Regra vinda de teste real com as crianças.

**N44.** A orientação vem da proporção do conteúdo, não de um padrão fixo:
`viewBox` mais alto que largo → retrato; caso contrário, paisagem.
Implementação de referência: `imprimirParaColorir` em
`app-infantil/src/impressao/motorImpressao.ts` linhas 35–48.

**N45.** A folha impressa respeita os tokens de tipografia e a estrutura, mas
usa tinta econômica: preto sobre branco. Cinzas literais avulsos são
proibidos.

**Estado hoje:** `app-leitura/src/lib/printSection.ts` linhas 38–49 usa
`#1a1a1a`, `#444`, `#ccc` e `#333` fixos, alheios a qualquer tema e a
qualquer token.

**N46.** Todo bloco de impressão esconde o que é controle e mantém o que é
obra: barra de ferramentas, setas, botões de copiar e menus saem;
texto, marcador e âncora ficam. Referência: `@media print` em
`rolo_template.html` linhas 165–168.

---

## Capítulo 11 — Persistência e soberania

**N47.** Estado do usuário nunca vive no acervo (Lei 7) e nunca se perde numa
atualização. Toda tela de ajustes diz isso em português claro, como já faz o
app-infantil.

**N48.** O acesso ao armazenamento passa por uma camada de abstração, para a
troca de backend não tocar em quem chama. Referência:
`app-infantil/src/armazenamento/armazenamento.ts`.

**N49.** Preferência de aparência é por perfil, quando o app tem perfis, e
sobrevive a troca de conteúdo.

**N50.** Nenhum dado do usuário sai do aparelho. Sem telemetria, sem conta,
sem sincronização silenciosa. Corolário da Lei 3.

---

## Capítulo 12 — Identidade e selo

**N53.** `Ὁ Διαφορεύς παρῆν` é o selo da persona filosófica adulta. Assina o
Pedra Angular, o rolo e os futuros livros físicos. **Não entra no
app-infantil**, em nenhuma tela, rodapé ou colofão.

**N54.** Φ à esquerda e Ξ à direita são restrição de projeto, não preferência
estética, e desde a LEI 8 valem em **todos** os apps, não só no Pedra Angular.
São as tatuagens da face anterior dos antebraços do Διαφορεύς; a barra o
representa em pé, de frente, em posição anatômica de referência. Não trocar os
símbolos, não trocar de lado, não substituir por ícone (N63).

**N55.** A pseudonímia do Διαφορεύς é escolha de tom e de estética, **não**
requisito de segurança — o registro `.app.br` já exige e expõe o nome real, e
a decisão do Διαφορεύς é conviver com isso. Portanto: nenhuma norma, arquitetura
ou nome de token deve ser justificado por proteção de identidade, e o assunto
não se reabre a cada sessão. Escrever com sobriedade continua valendo; esconder
não.

---

## Capítulo 13 — Cópias, duplicação e verificação

**N56.** Existe uma fonte de verdade por artefato. Cópia em outro repositório
é **vendorizada**: carimbada com versão no topo, marcada como não editável, e
propagada por script — nunca editada no destino.

**Estado hoje:** violado no kit do rolo, e já com dano.

| Arquivo | `Rolo_HTML/` | `app-leitura/scripts/rolo/` | Situação |
| --- | --- | --- | --- |
| `rolo_template.html` | 583 linhas | 583 linhas | idênticos byte a byte — por sorte, não por processo |
| `gerador_rolo.py` | 688 linhas | 1226 linhas | **já divergiram** |
| `fontes/Atkinson-*.woff2` | idênticos | idênticos | duplicados |

O gerador bifurcou em 538 linhas sem que nada avisasse. O template ainda não
bifurcou, mas não há nada impedindo — só o fato de ninguém ter editado os
dois.

**N57.** Todo arquivo gerado declara no topo que é gerado, por qual script, e
a partir de qual fonte. Nenhum derivado entra no controle de versão
(`dist/rolo/` continua fora do git).

**N58.** Antes de concluir qualquer entrega, nesta ordem:

1. `npm test` passa (onde houver suíte);
2. `npm run build` passa limpo;
3. o script de contraste roda com zero reprovas;
4. teste em viewport móvel;
5. teste offline;
6. o rolo da obra tocada abre e mostra o texto **com o JavaScript
   desligado**;
7. o rolo abre a partir do **site construído, com o service worker instalado
   e no comando** — não do servidor de desenvolvimento, que não tem service
   worker, e não por `fetch`, que não passa por ele.

**N68.** Quando o gerador muda, a verificação roda o conjunto **completo**,
nunca uma amostra. Caminho raro só existe no corpus inteiro: em 2026-08-08 uma
constante apagada derrubou o deploy porque `--piloto` produziu zero
redirecionamentos e o corpo do laço que a usava nunca executou — `--tudo` tem
dois. Amostra prova que o caminho comum funciona; ela não prova nada sobre o
resto.

Corolário barato e obrigatório: ao **apagar ou renomear** qualquer nome de
módulo (constante, função), procurar por ele em todo o repositório antes de
concluir. Python só descobre nome inexistente quando a linha executa.

Os passos 6 e 7 verificam as Leis 1 e 2-B e não são opcionais. Para o passo 7
no app-leitura: `npm run build`, gerar ao menos um rolo em `dist/rolo`, subir
a configuração `app-leitura-publicado` do `launch.json` da raiz, carregar a
página uma vez, recarregar para o service worker assumir, e só então navegar
até `/rolo/`. Conferir `navigator.serviceWorker.controller` — se for `null`,
o teste não valeu.

**N59.** Toda sessão de trabalho termina atualizando o handoff do projeto e
committando. Créditos são escassos e a sessão pode morrer a qualquer momento.

---

## Capítulo 14 — Só no app infantil

Pedagogia dos livrinhos para crianças (Historinhas). Estas duas normas valem
só lá; tudo o mais neste arquivo vale para o ecossistema inteiro. Os números
ficam os mesmos de sempre (N51, N52), porque são citados em código.

**N51.** Recompensa é fixa e previsível, nunca aleatória. Terminar o livro X
sempre dá a insígnia Y. Sem mecânica de sorte — o gatilho de dopamina
aleatório é exatamente o que o projeto existe para não reproduzir.

**N52.** Métrica de acerto é registrada em silêncio e nunca exibida à criança
como nota. Zero gate: qualquer resposta revela a correta com explicação, e
nada trava o avanço. Progressão se dá por **participação**, jamais por acerto.

---

## Anexo A — Conformidade hoje

Instantâneo de 2026-08-08, para saber por onde começar.

| Norma | app-leitura | app-infantil | rolo |
| --- | --- | --- | --- |
| **LEI 8 / N60–N66 barra angular** | parcial (tem os 4, aparência divergente) | **viola** (sem Φ, sem Ξ) | **referência** |
| **Oficina** (superfície nova, 2026-08-09) | cumpre LEI 8, LEI 1/2, LEI 3, N13–N14, N21, N26, N29, N31, N36, N38 — nasceu conforme | | |
| N1 três camadas | cumpre | **viola** | é a camada 2 |
| N7 formato único (revisto 2026-09-30) | quase todo (falta imagem) | parcial (sem `>`, wikilink) | quase todo (falta imagem) |
| N10 profundidade sem teto | cumpre | cumpre | cumpre |
| N14–15 vocabulário de token | divergente | divergente | divergente |
| N18 paleta única | **viola** | cumpre | cumpre |
| N19 escalas fechadas | **viola** | **viola** | **viola** |
| N21 corpo relativo | **viola** | **viola** | **referência** |
| N22 fonte embutida | cumpre | cumpre | cumpre |
| N23 licença junto | parcial | cumpre | **viola** |
| N25 medida em `ch` | **viola** | **viola** | **viola** |
| N26 pisos de contraste | cumpre (9/9 medidos) | cumpre | cumpre (acento do pergaminho corrigido para 6,95:1) |
| N27 script de medição | **referência** | não tem | não tem |
| N28 derivação em runtime | não tem | **referência** | não se aplica |
| N29 nunca só cor | cumpre | **referência** | cumpre |
| N30 soberania de tema | não se aplica | **referência** | não se aplica |
| N31 anel de foco | cumpre | cumpre | cumpre |
| N32 alvo de toque relativo | **referência** | parcial (px) | **viola** |
| N35 pular para o texto | **viola** | **viola** | **referência** (obra e índice) |
| N36 reduced-motion | cumpre | cumpre | cumpre |
| N38–41 língua e voz | **viola** | **viola** | **referência** |
| N43–44 impressão A4 | parcial | **referência** | cumpre |
| N51–52 recompensa e zero gate | não se aplica | **referência** | não se aplica |
| N56 cópia vendorizada | **viola** | cumpre | **viola** |

**Onde começar, em ordem de custo-benefício.**

1. ~~`prefers-reduced-motion` nos dois apps~~ — **feito em 2026-08-08.**
2. ~~Anel de `:focus-visible` e token `--ui-foco` nos dois apps~~ — **feito em
   2026-08-08.**
3. **A Barra Angular (LEI 8)** — a primitiva `.ui-botao-barra` uma vez, os
   quatro botões nos três projetos, e a troca do corpo de fonte para
   multiplicador junto, porque A− e A+ são dois dos quatro. Atenção: há
   migração do valor de corpo já salvo de usuários reais.
4. `lang` por trecho — portar `idioma_da_linha` para TypeScript, uma vez, e
   usar nos dois apps; o TTS por trecho vem junto de graça.
5. Pendências do rolo abertas pelos itens 1 e 2: trocar o anel de foco para
   um token próprio (hoje 1,89:1 no pergaminho), tirar o
   `outline: none` da linha 128, e migrar para a forma nova do N36. Bloqueado
   por N56 — o template está duplicado em dois lugares e é preciso decidir
   qual é o canônico antes de editar.

Depois, o item grande: **o rolo do app-infantil** (N1). É o que falta para o
ecossistema fechar, e é conteúdo autoral seu que hoje só existe dentro de um
bundle.

---

## Anexo B — Para agentes de IA

Se você é um modelo trabalhando neste ecossistema, estas são as regras que
não se violam, mesmo com pedido explícito para "só desta vez":

1. Nunca publicar obra que exista apenas dentro de uma SPA (Lei 1 e 2).
2. Nunca escrever tamanho de fonte em pixel absoluto (N21).
3. Nunca remover anel de foco sem pôr outro no mesmo commit (N31).
4. Nunca introduzir animação sem `prefers-reduced-motion` (N36).
5. Nunca escrever valor literal de cor, espaço, raio ou sombra fora dos
   casos do N20 (N13).
6. Nunca renomear id publicado (Lei 6).
7. Nunca editar arquivo dentro de pasta vendorizada (N56).
8. Nunca fazer o app escrever no acervo (Lei 7).
9. Nunca comunicar estado apenas por cor (N29).
10. Nunca usar `Ὁ Διαφορεύς παρῆν` no app-infantil (N53).
11. Nunca remover, deslocar, renomear ou trocar por ícone os quatro botões da
    barra angular — Φ, A−, A+, Ξ (LEI 8, N60–N66). Φ à esquerda e Ξ à
    direita, sempre.
12. Nunca introduzir framework CSS, pré-processador ou etapa de build de
    estilo.
13. Nunca adicionar dependência de rede em runtime (Lei 3).
14. Nunca fixar `lang` ou voz de TTS no documento inteiro: é sempre por trecho
    (N41), e etiqueta escrita vence detecção (N76).
15. Nunca ampliar a lista de códigos da etiqueta de idioma em uma superfície
    só — as duas mudam juntas ou nenhuma muda (N76).
16. Nunca escrever faixa Unicode com o caractere literal; sempre `\u` (N79).
17. Nunca proibir num app uma sintaxe do formato comum (N7) — `>`,
    `[[wikilink]]`, `![]()`, `{{img:id}}`. O que um app ainda não desenha
    aparece como texto: é trabalho a fazer nele, não regra a impor ao arquivo.
18. Nunca contornar em silêncio uma ferramenta do ecossistema: use-a antes do
    "seu jeito", e o que ela não souber fazer vira proposta de capacidade nela
    (LEI 9).

Antes de mexer em aparência, leia este arquivo inteiro. Antes de concluir,
rode o N58.

Se encontrar conflito entre este arquivo e o `CLAUDE.md` de um app, este
arquivo vence e o conflito deve ser relatado, não resolvido em silêncio.

---

## Anexo C — De onde veio cada norma

Nada aqui é invenção. Cada norma foi extraída de algo que já funciona em um
dos três projetos. O que cada um contribuiu:

**Pedra Angular / app-leitura.** A medição de contraste que lê o CSS
publicado e simula três dicromacias. Os nove temas ordenados por propósito,
com o número ao lado. O alvo de toque em unidade relativa. A ampliação de alvo
sem mexer no corpo do texto. A decisão de não transformar mil marcadores em
mil paradas de tabulação. A âncora de leitura que devolve a pessoa ao mesmo
ponto depois de mudar o corpo da fonte. A detecção de idioma que herda o
cabeçalho em vez de chutar, o aviso de voz aproximada, e a etiqueta `^eng` —
que reaproveitou a âncora de endereço em vez de inventar sintaxe nova.

**O rolo / Rolo_HTML.** A Lei 2 inteira, aprendida do jeito caro. O
interruptor `html.js` e a rede de segurança do `try/catch`. O anel de foco em
todo lugar. `prefers-reduced-motion`. `lang` e `dir` por linha, com `grc`
distinto de `el`. O relatório de idiomas desconhecidos. O multiplicador de
corpo de fonte. A âncora que vira endereço. A profundidade sem teto provada em
17 níveis.

**Historinhas / app-infantil.** A derivação de paleta com contraste garantido
em tempo de execução — o único mecanismo do ecossistema que protege uma cor
escolhida depois que o app abriu. A regra de nunca comunicar estado só por
cor. A soberania do usuário sobre o tema, com acessibilidade vencendo
decoração sem configuração. O parser de três regras em 64 linhas testáveis.
O texto burro com front matter rico. O TTS com os três bugs do Chrome
contornados e testados. A impressão A4 com orientação derivada do conteúdo.
O zero gate e a recompensa previsível.

---

## O que ficou pendente da sua decisão

Uma só, e ela muda todos os arquivos abaixo dela: **o vocabulário de token do
N15.** Escrevi a norma com prefixo `--ui-` e nomes em português porque o
prefixo neutro protege a separação entre o Διαφορεύς e o seu nome real na
ótica, e porque os nomes portugueses do app-infantil são os mais claros dos
três conjuntos. Se preferir outro esquema, é só dizer — mas decida antes de
qualquer refatoração começar, porque trocar depois custa o dobro.

O resto das normas não depende dessa escolha.
