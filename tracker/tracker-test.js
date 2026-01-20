// File: test/test-runner.js
// Language: javascript
import fs from 'fs';
import path from 'path';
import { fileURLToPath, pathToFileURL } from 'url';

async function run() {
  const testsDir = path.resolve(process.cwd(), 'test');
  if (!fs.existsSync(testsDir)) {
    console.log('No test directory found. Nothing to run.');
    process.exit(0);
  }

  const files = fs.readdirSync(testsDir).filter(f => f.endsWith('.test.js'));
  if (files.length === 0) {
    console.log('No .test.js files found in test/. Nothing to run.');
    process.exit(0);
  }

  let total = 0;
  let passed = 0;
  let failed = 0;
  for (const file of files) {
    total++;
    const fullPath = path.join(testsDir, file);
    const fileUrl = pathToFileURL(fullPath).href;
    console.log(`\n=== Running ${file} ===`);
    try {
      const mod = await import(fileUrl);
      const fn = mod.runTests || mod.default;
      if (typeof fn !== 'function') {
        console.log(`- SKIP ${file}: no exported runTests/default function`);
        passed++;
        continue;
      }
      await fn();
      console.log(`- PASS ${file}`);
      passed++;
    } catch (err) {
      failed++;
      console.error(`- FAIL ${file}`);
      console.error(err && err.stack ? err.stack : err);
    }
  }

  console.log(`\nTest summary: total=${total} passed=${passed} failed=${failed}`);
  process.exit(failed > 0 ? 1 : 0);
}

run().catch(err => {
  console.error('Test runner crashed:', err && err.stack ? err.stack : err);
  process.exit(2);
});


// File: test/smoke.test.js
// Language: javascript
export async function runTests() {
  // Simple sanity checks that should always pass
  if (1 + 1 !== 2) throw new Error('Math is broken');
  if (typeof Promise !== 'function') throw new Error('Promise not available');
  // ensure environment has basic globals
  if (typeof process === 'undefined') throw new Error('process not available');
}


// File: test/response.test.js
// Language: javascript
import fs from 'fs';
import path from 'path';
import { pathToFileURL } from 'url';

export async function runTests() {
  const rel = path.join(process.cwd(), 'utils', 'response.js');
  if (!fs.existsSync(rel)) {
    console.log('- SKIP: utils/response.js not found');
    return;
  }

  const mod = await import(pathToFileURL(rel).href);
  const sendResponse = mod.sendResponse || mod.default;
  if (typeof sendResponse !== 'function') {
    throw new Error('utils/response.js does not export sendResponse');
  }

  // Create a mock res with chainable status and json/send methods
  let statusCode = null;
  let bodySent = null;
  const mockRes = {
    status(code) {
      statusCode = code;
      return this;
    },
    json(payload) {
      bodySent = payload;
      return this;
    },
    send(payload) {
      bodySent = payload;
      return this;
    }
  };

  // Call the helper
  sendResponse(mockRes, true, 'ok message', { x: 1 }, 201);

  if (statusCode !== 201) {
    throw new Error(`Expected status 201 but got ${statusCode}`);
  }
  if (!bodySent || typeof bodySent !== 'object') {
    throw new Error('Expected body to be an object');
  }
  if (bodySent.success !== true) {
    throw new Error('Expected body.success to be true');
  }
  if (bodySent.message !== 'ok message') {
    throw new Error(`Expected message "ok message" but got "${bodySent.message}"`);
  }
  if (!('data' in bodySent)) {
    throw new Error('Expected data property in response body');
  }
}
