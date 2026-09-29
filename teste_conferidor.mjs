// teste_conferidor.mjs — o conferidor do navegador tem de dar o MESMO veredito
// que o validador do portão (validar_corpus.py), arquivo por arquivo.
//
//   node teste_conferidor.mjs <esquema.json> <regras.json> <pasta-do-corpus> <validacao.csv>
//
// validacao.csv é a saída do validar_corpus.py sobre a mesma pasta. Compara,
// por arquivo, cada regra e o número de ocorrências. Sai com 1 se divergir.
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const C = require('./conferidor.js');
const [esqP, regP, raiz, csvP] = process.argv.slice(2);
const ctx = C.preparar(JSON.parse(fs.readFileSync(esqP, 'utf8')), JSON.parse(fs.readFileSync(regP, 'utf8')));

// csv simples: arquivo,regra,nivel,ocorrencias,linha,exemplo (exemplo pode ter aspas)
const esperado = new Map();
const linhas = fs.readFileSync(csvP, 'utf8').split(/\r?\n/).slice(1).filter(Boolean);
for (const l of linhas) {
  const m = /^("(?:[^"]|"")*"|[^,]*),([^,]+),([^,]+),(\d+),/.exec(l);
  if (!m) continue;
  const arq = m[1].replace(/^"|"$/g, '').replace(/""/g, '"');
  if (!esperado.has(arq)) esperado.set(arq, {});
  esperado.get(arq)[m[2]] = Number(m[4]);
}

function andar(d) {
  return fs.readdirSync(d, { withFileTypes: true }).flatMap(e =>
    e.isDirectory() ? andar(path.join(d, e.name)) : e.name.endsWith('.md') ? [path.join(d, e.name)] : []);
}

let ok = 0, dif = 0;
const porRegra = {};
for (const p of andar(raiz)) {
  const rel = path.relative(raiz, p).split(path.sep).join('/');
  const ach = C.conferir(fs.readFileSync(p, 'utf8'), ctx);
  const js = Object.fromEntries(Object.entries(ach).map(([r, v]) => [r, v.length]));
  const py = esperado.get(rel) || {};
  const regras = new Set([...Object.keys(js), ...Object.keys(py)]);
  const difs = [...regras].filter(r => js[r] !== py[r]);
  if (difs.length) {
    dif++;
    for (const r of difs) (porRegra[r] ||= []).push(`${rel}: py=${py[r] ?? 0} js=${js[r] ?? 0}`);
  } else ok++;
}
console.log(`iguais: ${ok} · divergentes: ${dif}`);
for (const [r, casos] of Object.entries(porRegra)) {
  console.log(`\n${r}: ${casos.length} arquivo(s)`);
  casos.slice(0, 4).forEach(c => console.log('   ' + c));
}
process.exit(dif ? 1 : 0);
