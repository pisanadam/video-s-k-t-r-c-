// Animasyon HTML'ini (varsayılan fps-nerede.html) kare kare MP4'e çevirir.
// Kullanım: [HTML=ali-jenny.html | HTML='sigma.html?v=3'] node scripts/render-fps-nerede.cjs [çıktı.mp4] [fps]
// Gerekenler: playwright (chromium) + ffmpeg. three.js CDN'den yüklenir;
// THREE_PATH ortam değişkeni verilirse yerel three.module.js kullanılır.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

const OUT = path.resolve(process.argv[2] || 'fps-nerede.mp4');
const FPS = Number(process.argv[3] || 30);
const W = 1280, H = 720;

(async () => {
  const browser = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const page = await browser.newPage({ viewport: { width: W, height: H } });
  page.on('pageerror', e => console.error('sayfa hatası:', e.message));
  if (process.env.THREE_PATH) {
    await page.route(/three\.module\.js$/, r => r.fulfill({ path: process.env.THREE_PATH, contentType: 'text/javascript' }));
  }
  const [htmlFile, query] = (process.env.HTML || 'fps-nerede.html').split('?');
  const file = 'file://' + path.resolve(__dirname, '..', htmlFile) + '?' + (query ? query + '&' : '') + 'render=1';
  await page.goto(file);
  await page.waitForFunction(() => window.READY === true, null, { timeout: 60000 });
  const DUR = await page.evaluate(() => window.DUR);

  const tmp = fs.mkdtempSync(path.join(require('os').tmpdir(), 'fpsnerede-'));
  const wav = path.join(tmp, 'ses.wav');
  fs.writeFileSync(wav, Buffer.from(await page.evaluate(() => window.renderAudioWav()), 'base64'));

  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error',
    '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-',
    '-i', wav, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '27', '-preset', 'slow',
    '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', OUT], { stdio: ['pipe', 'inherit', 'inherit'] });

  const frames = Math.round(DUR * FPS);
  for (let i = 0; i < frames; i++) {
    await page.evaluate(t => window.renderAt(t), i / FPS);
    const buf = await page.screenshot({ type: 'jpeg', quality: 92 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (i % 60 === 0) console.log(`kare ${i}/${frames}`);
  }
  ff.stdin.end();
  await new Promise((res, rej) => ff.on('close', c => c === 0 ? res() : rej(new Error('ffmpeg ' + c))));
  await browser.close();
  fs.rmSync(tmp, { recursive: true, force: true });
  console.log('bitti:', OUT);
})().catch(e => { console.error(e); process.exit(1); });
