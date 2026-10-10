// 临时测试：桩化 DOM/localStorage，真实执行 index.html 脚本并模拟图鉴全流程
const fs = require('fs');
const html = fs.readFileSync(__dirname + '/../index.html', 'utf8');
const js = html.match(/<script>([\s\S]*?)<\/script>/)[1];

// ---- DOM 桩 ----
function makeEl(id) {
  const el = {
    id, innerHTML: '', textContent: '', style: {}, _classes: new Set(),
    addEventListener() {},
    classList: {
      add(c) { el._classes.add(c); },
      remove(c) { el._classes.delete(c); },
      contains(c) { return el._classes.has(c); },
    },
  };
  return el;
}
const elements = {};
global.document = {
  getElementById: (id) => elements[id] || (elements[id] = makeEl(id)),
  createElement: () => ({ style: {}, value: '' }),
  body: { appendChild() {}, removeChild() {} },
  querySelectorAll: () => [],
  execCommand: () => true,
};
const store = {};
global.localStorage = {
  getItem: (k) => (k in store ? store[k] : null),
  setItem: (k, v) => { store[k] = String(v); },
};
global.window = { isSecureContext: false, open() {}, scrollTo() {} };
global.navigator = {};

// ---- 执行页面脚本 + 测试（同一作用域） ----
const test = `
let pass = 0, fail = 0;
function T(cond, msg) {
  if (cond) { pass++; console.log('✅', msg); }
  else { fail++; console.log('❌', msg); }
}
T(elements.grid.innerHTML.includes('薯条蘸麦旋风'), '初始渲染：卡片含配方名');
T(elements.grid.innerHTML.split('class="card"').length - 1 === 14, '初始渲染：14 张卡片');
T(String(elements.colCount.textContent) === '0', '图鉴计数初始 = 0');
T(elements.unlockBox.style.display === 'none', '彩蛋初始隐藏');

openModal(0);
T(elements.modal.classList.contains('on'), '打开弹窗');
T(elements.colBtn.textContent.includes('标记为已尝'), '按钮初始文案');
T(elements.modalOrder.innerHTML.includes('点单话术'), '弹窗展示点单话术');

toggleCollected();
T(String(elements.colCount.textContent) === '1', '标记后计数 = 1');
T(elements.colBar.style.width === '7.142857142857142%', '进度条宽度 ≈7.14%');
T(elements.colBtn.textContent.includes('已尝过'), '按钮切换为已尝状态');
T(elements.grid.innerHTML.includes('col-tick'), '网格出现已尝标记');

for (let i = 1; i < 14; i++) { openModal(i); toggleCollected(); }
T(String(elements.colCount.textContent) === '14', '集齐 14 个');
T(elements.unlockBox.style.display === 'block', '彩蛋解锁显示');
T(elements.colHint.textContent.includes('集齐') || elements.colHint.textContent.includes('已集齐'), '提示文案切换');

openModal(13); toggleCollected();
T(String(elements.colCount.textContent) === '13', '取消标记后 = 13');
T(elements.unlockBox.style.display === 'none', '彩蛋重新隐藏');

// 本地持久化校验
const saved = JSON.parse(store['mcdLab.collected'] || '[]');
T(saved.length === 13, 'localStorage 持久化 13 条');

console.log('--- 结果: ' + pass + ' 通过 / ' + fail + ' 失败 ---');
if (fail > 0) throw new Error('测试失败');
`;
try {
  eval(js + '\n' + test);
  console.log('=== 图鉴全流程验证完成 ===');
} catch (e) {
  console.log('💥 运行时错误:', e.message);
  process.exit(1);
}
