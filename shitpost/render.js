// Renders scene.html frame by frame in headless Chromium and pipes JPEGs into ffmpeg.
// usage: node render.js <scene.html> <audio.wav> <out.mp4>
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const path = require('path');
const [scene, audio, out] = process.argv.slice(2);
const FPS = 30;
(async () => {
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--allow-file-access-from-files'] });
  const p = await b.newPage({ viewport: { width: 1280, height: 720 } });
  await p.goto('file://' + path.resolve(scene));
  const dur = await p.evaluate(() => window.DURATION);
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
    '-i', audio, '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p',
    '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  const frames = Math.round(dur * FPS);
  for (let f = 0; f < frames; f++) {
    await p.evaluate(t => renderAt(t), f / FPS);
    const buf = await p.locator('#stage').screenshot({ type: 'jpeg', quality: 92 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (f % 150 === 0) console.log(`frame ${f}/${frames}`);
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r)); await b.close();
})();
