import fs from 'fs';
import path from 'path';

export async function GET() {
  const filePath = path.join(process.cwd(), 'public', 'qmk_configurator', 'index.html');
  try {
    const html = await fs.promises.readFile(filePath, 'utf-8');
    return new Response(html, {
      headers: {
        'Content-Type': 'text/html; charset=utf-8'
      }
    });
  } catch {
    return new Response('Not found', { status: 404 });
  }
}
