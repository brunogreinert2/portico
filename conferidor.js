/*
 * conferidor.js — confere um .md contra a norma do acervo, no navegador.
 * Pedra Angular · /portico/contribuir.html
 *
 * NAO TEM REGRA PROPRIA. Executa as mesmas que o portao do acervo:
 *   frontmatter.schema.json  (app-leitura/scripts/acervo — o esquema)
 *   regras.json              (exportado de validar_corpus.py — o corpo)
 * O comportamento espelha validar_corpus.py linha a linha; o teste
 * teste_conferidor.mjs compara os dois no corpus inteiro.
 *
 * Nada sai do aparelho: o arquivo e lido aqui mesmo (LEI 3, N50).
 */
(function (raiz) {
  'use strict';

  // ------------------------------------------------------------------ YAML
  // So o subconjunto que front matter usa: chave: valor, listas [a, b] e
  // "- item", aspas, numeros, true/false, null. Mapa aninhado vira objeto.
  function escalar(bruto) {
    var t = bruto.trim();
    if (t === '' || t === '~' || t === 'null' || t === 'Null' || t === 'NULL') return null;
    if (t === 'true' || t === 'True') return true;
    if (t === 'false' || t === 'False') return false;
    if (/^[-+]?\d+$/.test(t)) return parseInt(t, 10);
    if (/^[-+]?\d*\.\d+$/.test(t)) return parseFloat(t);
    if (t[0] === '"' && t[t.length - 1] === '"' && t.length > 1) {
      try { return JSON.parse(t); } catch (e) { return t.slice(1, -1); }
    }
    if (t[0] === "'" && t[t.length - 1] === "'" && t.length > 1) return t.slice(1, -1).replace(/''/g, "'");
    return t;
  }

  function semComentario(v) {
    var dentro = null;
    for (var i = 0; i < v.length; i++) {
      var c = v[i];
      if (dentro) { if (c === dentro) dentro = null; continue; }
      if (c === '"' || c === "'") { if (i === 0 || /\s|\[|,/.test(v[i - 1])) dentro = c; continue; }
      if (c === '#' && (i === 0 || /\s/.test(v[i - 1]))) return v.slice(0, i);
    }
    return v;
  }

  function lista(bruto) {
    var t = bruto.trim().slice(1, -1).trim();
    if (!t) return [];
    var itens = [], atual = '', dentro = null;
    for (var i = 0; i < t.length; i++) {
      var c = t[i];
      if (dentro) { atual += c; if (c === dentro) dentro = null; continue; }
      if (c === '"' || c === "'") { dentro = c; atual += c; continue; }
      if (c === ',') { itens.push(escalar(atual)); atual = ''; continue; }
      atual += c;
    }
    itens.push(escalar(atual));
    return itens;
  }

  function parseYAML(texto) {
    var linhas = texto.split(/\r?\n/), meta = {}, chave = null;
    for (var i = 0; i < linhas.length; i++) {
      var l = linhas[i];
      if (!l.trim() || /^\s*#/.test(l)) continue;
      var item = /^\s+-\s?(.*)$/.exec(l) || /^-\s(.*)$/.exec(l);
      if (item && chave) {
        if (!Array.isArray(meta[chave])) meta[chave] = [];
        meta[chave].push(escalar(semComentario(item[1])));
        continue;
      }
      if (/^\s/.test(l) && chave) {                 // continuacao ou mapa aninhado
        var sub = /^\s+([^:#]+):\s*(.*)$/.exec(l);
        if (sub && (meta[chave] === null || typeof meta[chave] === 'object' && !Array.isArray(meta[chave]))) {
          if (meta[chave] === null) meta[chave] = {};
          meta[chave][sub[1].trim()] = escalar(semComentario(sub[2]));
        } else if (typeof meta[chave] === 'string') {
          meta[chave] += ' ' + l.trim();
        }
        continue;
      }
      var m = /^([^\s:#][^:]*?):(?:\s+(.*)|\s*)$/.exec(l);
      if (!m) throw new Error('linha ' + (i + 1) + ' não é "chave: valor": ' + l.trim().slice(0, 60));
      chave = m[1].trim();
      var v = semComentario(m[2] || '').trim();
      if (v[0] === '[' && v[v.length - 1] === ']') meta[chave] = lista(v);
      else if (v === '|' || v === '>' || v === '|-' || v === '>-') meta[chave] = '';
      else meta[chave] = escalar(v);
    }
    return meta;
  }

  // ------------------------------------------------------------ JSON Schema
  // O subconjunto de draft 2020-12 que o esquema usa.
  function tipoDe(v) {
    if (v === null) return 'null';
    if (Array.isArray(v)) return 'array';
    if (typeof v === 'number') return Number.isInteger(v) ? 'integer' : 'number';
    return typeof v;                                     // string, boolean, object
  }
  function igual(a, b) { return JSON.stringify(a) === JSON.stringify(b); }

  function validar(esq, v, caminho, raizEsq, erros) {
    if (esq.$ref) {
      var nome = esq.$ref.replace('#/$defs/', '');
      validar(raizEsq.$defs[nome], v, caminho, raizEsq, erros);
    }
    function erro(kw, msg) { erros.push({ keyword: kw, caminho: caminho, instancia: v, mensagem: msg }); }
    if (esq.type) {
      var t = tipoDe(v), ok = esq.type === t || (esq.type === 'number' && t === 'integer');
      if (!ok) { erro('type', 'tipo ' + t + ', esperado ' + esq.type); return; }
    }
    if (esq.enum && !esq.enum.some(function (e) { return igual(e, v); })) erro('enum', 'fora da lista');
    if ('const' in esq && !igual(esq.const, v)) erro('const', 'tem de ser ' + JSON.stringify(esq.const));
    if (typeof v === 'string') {
      if (esq.minLength && v.length < esq.minLength) erro('minLength', 'vazio');
      if (esq.pattern && !new RegExp(esq.pattern, 'u').test(v)) erro('pattern', 'formato inválido');
    }
    if (typeof v === 'number' && 'minimum' in esq && v < esq.minimum) erro('minimum', 'menor que ' + esq.minimum);
    if (esq.not) { var e0 = []; validar(esq.not, v, caminho, raizEsq, e0); if (!e0.length) erro('not', 'valor proibido'); }
    if (esq.oneOf) {
      var bons = esq.oneOf.filter(function (s) { var e = []; validar(s, v, caminho, raizEsq, e); return !e.length; }).length;
      if (bons !== 1) erro('oneOf', 'não bate com nenhuma forma aceita');
    }
    if (Array.isArray(v)) {
      if (esq.minItems && v.length < esq.minItems) erro('minItems', 'lista curta');
      if (esq.uniqueItems) {
        var vistos = v.map(function (x) { return JSON.stringify(x); });
        if (vistos.some(function (x, i) { return vistos.indexOf(x) !== i; })) erro('uniqueItems', 'item repetido');
      }
      if (esq.items) v.forEach(function (x, i) { validar(esq.items, x, caminho.concat(i), raizEsq, erros); });
    }
    if (tipoDe(v) === 'object') {
      (esq.required || []).forEach(function (k) {
        if (!(k in v)) erros.push({ keyword: 'required', caminho: caminho, propriedade: k, mensagem: k });
      });
      if (esq.properties) Object.keys(esq.properties).forEach(function (k) {
        if (k in v) validar(esq.properties[k], v[k], caminho.concat(k), raizEsq, erros);
      });
      if (esq.additionalProperties === false && esq.properties) {
        var extras = Object.keys(v).filter(function (k) { return !(k in esq.properties); });
        if (extras.length) erro('additionalProperties', extras.join(', '));
      }
    }
    (esq.allOf || []).forEach(function (s) {
      if (s['if']) {
        var e1 = []; validar(s['if'], v, caminho, raizEsq, e1);
        if (!e1.length && s.then) validar(s.then, v, caminho, raizEsq, erros);
      } else validar(s, v, caminho, raizEsq, erros);
    });
  }

  // ------------------------------------------------------------- a norma
  function preparar(esquema, regras) {
    var campoAntigo = {}, valorAntigo = {};
    Object.keys(esquema.properties).forEach(function (novo) {
      var p = esquema.properties[novo];
      (p['x-antes'] || []).forEach(function (a) { if (a !== novo) campoAntigo[a] = novo; });
      if (p['x-valores-antes']) valorAntigo[novo] = p['x-valores-antes'];
    });
    // \w e \b do Python sao Unicode; os do JavaScript so conhecem ASCII (em
    // latim, "nullæ" teria um \b entre o l e o æ). Traduz os dois. O \w das
    // regras so aparece dentro de classe [...].
    var W = '\\p{L}\\p{N}\\p{M}_';
    var B = '(?:(?<=[' + W + '])(?![' + W + '])|(?<![' + W + '])(?=[' + W + ']))';
    function rx(p, flags) {
      return new RegExp(p.replace(/\\w/g, W).replace(/\\b/g, B), flags || 'u');
    }
    return {
      esquema: esquema, regras: regras, campoAntigo: campoAntigo, valorAntigo: valorAntigo,
      removidos: esquema['x-removidos'] || {},
      linha: regras.regras_linha.map(function (r) { return { codigo: r.codigo, rx: rx(r.regex) }; }),
      cerca: rx(regras.cerca), notaUso: rx(regras.nota_uso, 'gu'), notaDef: rx(regras.nota_def),
      ancorasFim: rx(regras.ancoras_fim), etiquetas: regras.etiquetas_idioma,
      codigo: regras.codigo ? rx(regras.codigo, 'gu') : null, ignoraCodigo: regras.ignora_codigo || []
    };
  }

  function vazio(v) { return v === null || v === undefined || (typeof v === 'string' && !v.trim()); }
  function repr(v) { return v === null ? 'None' : typeof v === 'string' ? "'" + v + "'" : JSON.stringify(v); }

  function conferirMeta(meta, ctx, achar) {
    var props = ctx.esquema.properties;
    Object.keys(meta).forEach(function (k) {
      var v = meta[k];
      if (vazio(v)) achar('F20-vazio', 0, k + ': ' + repr(v));
      if (k in ctx.campoAntigo) achar('F10-migravel-campo', 0, k + ' -> ' + ctx.campoAntigo[k]);
      else if (k in ctx.removidos) achar('F13-campo-removido', 0, k + ': ' + ctx.removidos[k]);
      else if (!(k in props)) achar('F30-campo-desconhecido', 0, k);
    });
    var fonte = meta.source;
    if (typeof fonte === 'string' && /URN:\s*urn:cts:/.test(fonte) && !('urn' in meta))
      achar('F12-urn-no-source', 0, /urn:cts:\S+/.exec(fonte)[0]);

    var migrado = {};
    Object.keys(meta).forEach(function (k) {
      var v = meta[k];
      if (vazio(v) || k in ctx.removidos) return;
      var novo = ctx.campoAntigo[k] || k;
      if (novo in ctx.valorAntigo && typeof v === 'string' && v in ctx.valorAntigo[novo]) {
        var t = ctx.valorAntigo[novo][v];
        achar('F11-migravel-valor', 0, novo + ': ' + v + ' -> ' + (Array.isArray(t) ? '[' + t.join(', ') + ']' : t));
        v = t;
      }
      if (novo === 'translator' && typeof v === 'string') v = [v];
      if (Array.isArray(migrado[novo]) && Array.isArray(v))
        v = migrado[novo].concat(v.filter(function (x) { return migrado[novo].indexOf(x) < 0; }));
      migrado[novo] = v;
    });
    if (typeof fonte === 'string' && !('urn' in migrado)) {
      var u = /URN:\s*(urn:cts:[^\s"]+)/.exec(fonte);
      if (u) migrado.urn = u[1].replace(/\.+$/, '');
    }

    var erros = [];
    validar(ctx.esquema, migrado, [], ctx.esquema, erros);
    erros.forEach(function (e) {
      if (e.keyword === 'additionalProperties') return;
      if (e.keyword === 'required') achar('F31-obrigatorio-ausente', 0, e.propriedade);
      else achar('F32-valor-invalido', 0, (e.caminho.join('.') || '(raiz)') + ': ' +
        (typeof e.instancia === 'object' && e.instancia !== null ? JSON.stringify(e.instancia).slice(0, 60) : e.instancia));
    });

    if (['primary_text', 'translation', 'interlinear', 'commentary'].indexOf(migrado.type) >= 0 &&
        !('urn' in migrado) && !migrado.pa_exclusive) achar('A01-sem-urn', 0, '');
  }

  function conferirCorpo(corpo, desloc, ctx, achar) {
    var usos = {}, defs = {}, ancoras = {}, primeira = {}, ordemUsos = [], ordemDefs = [], ordemAnc = [];
    var dentroCerca = null;
    corpo.split('\n').forEach(function (linha, idx) {
      var i = idx + desloc + 1;
      var c = ctx.cerca.exec(linha);
      if (c) {
        if (dentroCerca === null) {
          dentroCerca = c[1].trim();
          if (ctx.regras.cercas_permitidas.indexOf(dentroCerca) < 0) achar('C10-cerca', i, linha.trim().slice(0, 80));
        } else dentroCerca = null;
        return;
      }
      // D24: entre crases é código citado numa nota editorial, não vazamento
      var semCodigo = ctx.codigo ? linha.replace(ctx.codigo, '') : linha;
      ctx.linha.forEach(function (r) {
        var alvo = ctx.ignoraCodigo.indexOf(r.codigo) >= 0 ? semCodigo : linha;
        var mm = r.rx.exec(alvo);
        if (mm) {
          var ini = Math.max(0, mm.index - 30);
          achar(r.codigo, i, alvo.slice(ini, mm.index + mm[0].length + 30).trim());
        }
      });
      var d = ctx.notaDef.exec(linha);
      if (d && !(d[1] in defs)) { defs[d[1]] = i; ordemDefs.push(d[1]); }
      ctx.notaUso.lastIndex = 0;
      var u;
      while ((u = ctx.notaUso.exec(linha)) !== null) {
        if (!(d && u.index === 0) && !(u[1] in usos)) { usos[u[1]] = i; ordemUsos.push(u[1]); }
        if (u[0] === '') ctx.notaUso.lastIndex++;
      }
      var fim = ctx.ancorasFim.exec(linha);
      if (fim) {
        var rxA = /\^([\p{L}\p{N}\p{M}_-]+)/gu, a;
        while ((a = rxA.exec(fim[1])) !== null) {
          if (ctx.etiquetas.indexOf(a[1]) >= 0) continue;
          if (!(a[1] in ancoras)) { ancoras[a[1]] = 0; primeira[a[1]] = i; ordemAnc.push(a[1]); }
          ancoras[a[1]]++;
        }
      }
    });
    ordemUsos.forEach(function (n) { if (!(n in defs)) achar('C11-nota-sem-definicao', usos[n], '[^' + n + ']'); });
    ordemDefs.forEach(function (n) { if (!(n in usos)) achar('C12-definicao-sem-uso', defs[n], '[^' + n + ']:'); });
    ordemAnc.forEach(function (n) { if (ancoras[n] > 1) achar('C13-ancora-duplicada', primeira[n], '^' + n + ' x' + ancoras[n]); });
  }

  var RE_FM = /^---[ \t]*\r?\n([\s\S]*?)\r?\n---[ \t]*(?:\r?\n|$)/;

  /** Devolve { regra: [[linha, exemplo], ...] }, como validar_arquivo do Python. */
  function conferir(texto, ctx) {
    var achados = {};
    function achar(regra, linha, ex) { (achados[regra] = achados[regra] || []).push([linha, ex]); }
    if (texto.charCodeAt(0) === 0xFEFF) texto = texto.slice(1);
    var m = RE_FM.exec(texto), corpo = texto, desloc = 0, meta = null;
    if (!m) achar('F00-sem-front-matter', 1, '');
    else {
      corpo = texto.slice(m[0].length);
      desloc = (m[0].match(/\n/g) || []).length;
      try { meta = parseYAML(m[1]); } catch (e) { achar('F01-yaml-invalido', 1, e.message); }
    }
    if (meta) conferirMeta(meta, ctx, achar);
    conferirCorpo(corpo, desloc, ctx, achar);
    return achados;
  }

  var api = { parseYAML: parseYAML, preparar: preparar, conferir: conferir };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  raiz.Conferidor = api;

  // --------------------------------------------------------------- a tela
  if (typeof document === 'undefined') return;
  function iniciar() {
    var caixa = document.getElementById('conferidor');
    if (!caixa) return;
    caixa.hidden = false;
    var entrada = document.getElementById('conf-arquivo');
    var colar = document.getElementById('conf-texto');
    var botao = document.getElementById('conf-colado');
    var zona = document.getElementById('conf-zona');
    var saida = document.getElementById('conf-resultado');
    var ctx = null;

    Promise.all([
      fetch('frontmatter.schema.json').then(function (r) { return r.json(); }),
      fetch('regras.json').then(function (r) { return r.json(); })
    ]).then(function (v) { ctx = preparar(v[0], v[1]); })
      .catch(function () { saida.textContent = 'Não consegui carregar a norma (frontmatter.schema.json e regras.json).'; });

    function el(tag, cls, txt) { var e = document.createElement(tag); if (cls) e.className = cls; if (txt != null) e.textContent = txt; return e; }

    function mostrar(nome, texto) {
      if (!ctx) { saida.textContent = 'A norma ainda está carregando. Tente de novo em um instante.'; return; }
      var ach = conferir(texto, ctx), R = ctx.regras;
      var erros = Object.keys(ach).filter(function (r) { return R.nivel[r] === 'erro'; });
      var avisos = Object.keys(ach).filter(function (r) { return R.nivel[r] !== 'erro'; });
      var bloco = el('section', 'conf-bloco ' + (erros.length ? 'conf-reprovado' : 'conf-aprovado'));
      bloco.appendChild(el('h3', null, (erros.length ? '✗ ' : '✓ ') + nome));
      bloco.appendChild(el('p', 'conf-veredito', erros.length
        ? erros.length + ' problema(s) que o portão do acervo barra.'
        : 'Dentro da norma' + (avisos.length ? ', com ' + avisos.length + ' aviso(s).' : '.')));
      var ul = el('ul', 'conf-lista');
      erros.concat(avisos).forEach(function (r) {
        var li = el('li', R.nivel[r] === 'erro' ? 'conf-erro' : 'conf-aviso');
        li.appendChild(el('strong', null, (R.nivel[r] === 'erro' ? 'Erro: ' : 'Aviso: ') + R.descricao[r] + ' — ' + ach[r].length + '×'));
        ach[r].slice(0, 3).forEach(function (x) {
          if (x[0] || x[1]) li.appendChild(el('code', 'conf-ex', (x[0] ? 'linha ' + x[0] + ': ' : '') + x[1]));
        });
        if (ach[r].length > 3) li.appendChild(el('span', 'conf-mais', '… e mais ' + (ach[r].length - 3)));
        li.appendChild(el('p', 'conf-dica', '→ ' + (R.como_consertar[r] || '')));
        ul.appendChild(li);
      });
      if (ul.children.length) bloco.appendChild(ul);
      saida.insertBefore(bloco, saida.firstChild);
      bloco.setAttribute('tabindex', '-1');
      bloco.focus();
    }

    function lerArquivos(lista) {
      Array.prototype.forEach.call(lista, function (f) {
        var r = new FileReader();
        r.onload = function () { mostrar(f.name, String(r.result)); };
        r.readAsText(f, 'utf-8');
      });
    }
    entrada.addEventListener('change', function () { lerArquivos(entrada.files); entrada.value = ''; });
    botao.addEventListener('click', function () { if (colar.value.trim()) mostrar('texto colado', colar.value); });
    ['dragenter', 'dragover'].forEach(function (t) {
      zona.addEventListener(t, function (e) { e.preventDefault(); zona.classList.add('conf-sobre'); });
    });
    ['dragleave', 'drop'].forEach(function (t) {
      zona.addEventListener(t, function () { zona.classList.remove('conf-sobre'); });
    });
    zona.addEventListener('drop', function (e) { e.preventDefault(); lerArquivos(e.dataTransfer.files); });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', iniciar);
  else iniciar();
})(typeof window !== 'undefined' ? window : globalThis);
