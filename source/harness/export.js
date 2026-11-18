// runs inside the harness page: turns live blocks into a render tree + exact generated code
window.RX = (() => {
  const fieldInfo = f => {
    const cls = f.constructor && f.constructor.name;
    if (f instanceof Blockly.FieldDropdown) {
      let opts = [];
      try { opts = f.getOptions().map(o => [typeof o[0] === 'string' ? o[0] : (o[0] && o[0].alt) || '?', o[1]]); } catch (e) {}
      return { k: 'dd', t: f.getText(), v: f.getValue(), opts };
    }
    if (Blockly.FieldVariable && f instanceof Blockly.FieldVariable) return { k: 'var', t: f.getText() };
    if (Blockly.FieldImage && f instanceof Blockly.FieldImage) return { k: 'icon' };
    if (Blockly.FieldTextInput && f instanceof Blockly.FieldTextInput) return { k: 'in', t: f.getText() };
    if (Blockly.FieldCheckbox && f instanceof Blockly.FieldCheckbox) return { k: 'dd', t: f.getValue() === 'TRUE' ? '✓' : '✗' };
    const t = f.getText ? f.getText() : '';
    if (!t || !t.trim()) return null;
    return { k: 't', t };
  };
  function shapeOf(b) {
    if (b.outputConnection) {
      const chk = b.outputConnection.check_;
      return chk && chk.indexOf('Boolean') >= 0 ? 'bool' : 'rep';
    }
    if (!b.previousConnection) return b.nextConnection ? 'hat' : 'hat';
    return b.nextConnection ? 'stack' : 'cap';
  }
  function tree(b) {
    const node = { type: b.type, shape: shapeOf(b), c: b.getColour(), c2: b.getColourSecondary && b.getColourSecondary(), c3: b.getColourTertiary && b.getColourTertiary(), shadow: b.isShadow(), rows: [] };
    let row = [];
    const flush = () => { if (row.length) node.rows.push({ items: row }); row = []; };
    for (const inp of b.inputList) {
      if (!inp.isVisible || inp.isVisible()) {
        if (inp.type === Blockly.NEXT_STATEMENT && inp.fieldRow.some(f => fieldInfo(f))) flush();   // label of a statement slot sits on its own line
        for (const f of inp.fieldRow) { if (f.isVisible && !f.isVisible()) continue; const fi = fieldInfo(f); if (fi) row.push(fi); }
        if (inp.type === Blockly.INPUT_VALUE) {
          const t = inp.connection && inp.connection.targetBlock();
          row.push(t ? { k: 'val', b: tree(t), name: inp.name } : { k: 'empty', name: inp.name, bool: !!(inp.connection && inp.connection.check_ && inp.connection.check_.indexOf('Boolean') >= 0) });
        } else if (inp.type === Blockly.NEXT_STATEMENT) {
          flush();
          const kids = [];
          let t = inp.connection && inp.connection.targetBlock();
          while (t) { kids.push(tree(t)); t = t.getNextBlock(); }
          node.rows.push({ stmt: inp.name, blocks: kids });
        }
      }
    }
    flush();
    return node;
  }
  function stackTree(b) { const out = []; while (b) { out.push(tree(b)); b = b.getNextBlock(); } return out; }
  function load(xmlText) {
    ws.clear();
    const dom = Blockly.Xml.textToDom(xmlText);
    Blockly.Xml.domToWorkspace(dom, ws);
    return ws.getTopBlocks(true);
  }
  function run(xmlText) {
    const tops = load(xmlText);
    const code = Blockly.Arduino.workspaceToCode(ws);
    return { trees: tops.map(stackTree), code };
  }
  function valueCode(xmlText) {
    const tops = load(xmlText);
    Blockly.Arduino.init(ws);
    const b = tops[0];
    let r = Blockly.Arduino.blockToCode(b);
    if (Array.isArray(r)) r = r[0];
    const defs = Object.values(Blockly.Arduino.definitions_ || {});
    const setups = Object.values(Blockly.Arduino.setups_ || {}).map(e => typeof e === 'string' ? e : e.code);
    return { code: r, defs, setups, tree: stackTree(b) };
  }
  function vars(names) { for (const n of names) if (!ws.getVariable(n, '')) ws.createVariable(n, '', 'v_' + n); }
  function setLocale(l) { Blockly.ScratchMsgs.setLocale(l); }
  return { run, valueCode, vars, setLocale, load, tree1: tree };
})();
// for every dropdown on a block: set each option in turn and record the generated code of that block
window.RX.variants = function (xmlText) {
  const tops = window.RX.load(xmlText);
  const b = tops[0];
  const res = [];
  const gen = () => {
    Blockly.Arduino.init(ws);
    let r = Blockly.Arduino.blockToCode(b);
    if (Array.isArray(r)) r = r[0];
    return String(r).trim();
  };
  const base = gen();
  for (const inp of b.inputList) for (const f of inp.fieldRow) {
    if (!(f instanceof Blockly.FieldDropdown) || (Blockly.FieldVariable && f instanceof Blockly.FieldVariable)) continue;
    const orig = f.getValue();
    let opts = [];
    try { opts = f.getOptions(); } catch (e) { continue; }
    const rows = [];
    for (const o of opts) {
      try { f.setValue(o[1]); rows.push([typeof o[0] === 'string' ? o[0] : (o[0].alt || '?'), o[1], gen()]); } catch (e) { rows.push([String(o[0]), o[1], 'ERR ' + e]); }
    }
    f.setValue(orig);
    res.push({ field: f.name, rows });
  }
  return { base, fields: res };
};
// generate code with start/end markers around every statement block, then strip them and return line ranges
window.RX.runMapped = function (xmlText) {
  const tops = window.RX.load(xmlText);
  const orig = Blockly.Arduino.scrub_;
  Blockly.Arduino.scrub_ = function (block, code) {
    if (code !== null && code !== '' && !block.outputConnection && !block.isShadow()) {
      if (!code.endsWith('\n')) code += '\n';
      code = '//@@s' + block.id + '\n' + code + '//@@e' + block.id + '\n';
    }
    return orig.call(this, block, code);
  };
  let raw;
  try { raw = Blockly.Arduino.workspaceToCode(ws); } finally { Blockly.Arduino.scrub_ = orig; }
  const lines = raw.split('\n'), out = [], open = {}, ranges = {};
  for (const ln of lines) {
    const m = ln.trim().match(/^\/\/@@([se])(.+)$/);
    if (m) { if (m[1] === 's') open[m[2]] = out.length; else ranges[m[2]] = [open[m[2]], out.length - 1]; continue; }
    out.push(ln);
  }
  // block ids in tree order, so the page can match them to rendered blocks
  const ids = [];
  const walk = b => { if (!b) return; ids.push(b.id); for (const c of b.getChildren(true)) walk(c); };
  const tree = tops.map(t => { const a = []; let b = t; while (b) { a.push(b); b = b.getNextBlock(); } return a; });
  const treesWithIds = tops.map(t => window.RX.stackTreeIds(t));
  return { code: out.join('\n'), ranges, trees: treesWithIds, plain: Blockly.Arduino.workspaceToCode(ws) };
};
window.RX.stackTreeIds = function (b) {
  const out = [];
  const add = (blk, node) => {
    node.id = blk.id;
    let i = 0;
    // walk the same order the tree() function used, attaching ids to nested value/statement blocks
    const nest = [];
    for (const inp of blk.inputList) {
      if (inp.type === Blockly.INPUT_VALUE) { const t = inp.connection && inp.connection.targetBlock(); if (t) nest.push(['v', t]); }
      else if (inp.type === Blockly.NEXT_STATEMENT) { const kids = []; let t = inp.connection && inp.connection.targetBlock(); while (t) { kids.push(t); t = t.getNextBlock(); } nest.push(['s', kids]); }
    }
    const vals = [], stmts = [];
    for (const r of node.rows) { if (r.items) for (const it of r.items) if (it.k === 'val') vals.push(it); if (r.stmt) stmts.push(r); }
    let vi = 0, si = 0;
    for (const [k, t] of nest) {
      if (k === 'v') { const it = vals[vi++]; if (it) add(t, it.b); }
      else { const r = stmts[si++]; if (r) t.forEach((kb, j) => add(kb, r.blocks[j])); }
    }
  };
  while (b) { const node = window.RX.tree1(b); add(b, node); out.push(node); b = b.getNextBlock(); }
  return out;
};
