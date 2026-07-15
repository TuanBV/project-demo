#!/usr/bin/env node
import { spawnSync } from 'node:child_process'
import { existsSync, readFileSync, readdirSync, statSync } from 'node:fs'
import { dirname, extname, join, relative, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..')
const mode = process.argv.includes('--full') ? 'full' : process.argv.includes('--security') ? 'security' : 'quick'
const results = []

function result(name, status, detail = '') {
  results.push({ name, status, detail })
  const icon = status === 'PASS' ? '✓' : status === 'FAIL' ? '✗' : '•'
  console.log(`${icon} ${name}: ${status}${detail ? ` — ${detail}` : ''}`)
}

function run(name, command, args, cwd = root, optional = false) {
  const proc = spawnSync(command, args, { cwd, encoding: 'utf8', shell: process.platform === 'win32' })
  if (proc.error) {
    result(name, optional ? 'SKIP' : 'FAIL', proc.error.message)
    return optional
  }
  if (proc.status === 0) {
    result(name, 'PASS')
    return true
  }
  const output = `${proc.stdout || ''}\n${proc.stderr || ''}`.trim().split(/\r?\n/).slice(-20).join('\n')
  result(name, 'FAIL', output || `exit ${proc.status}`)
  return false
}

function walk(dir, output = []) {
  if (!existsSync(dir)) return output
  for (const entry of readdirSync(dir)) {
    if (['.git', 'node_modules', 'dist', 'coverage', '__pycache__', '.venv'].includes(entry)) continue
    const full = join(dir, entry)
    const st = statSync(full)
    if (st.isDirectory()) walk(full, output)
    else output.push(full)
  }
  return output
}

function scanText(name, patterns) {
  const textExt = new Set(['.py','.js','.cjs','.mjs','.vue','.json','.yml','.yaml','.md','.txt','.sql','.toml','.ini','.sh','.ps1',''])
  const findings = []
  for (const file of walk(root)) {
    const rel = relative(root, file).replaceAll('\\','/')
    if (rel === 'api/.env') { findings.push(`${rel}: tracked secret file must not exist`); continue }
    if (!textExt.has(extname(file).toLowerCase())) continue
    let text
    try { text = readFileSync(file, 'utf8') } catch { continue }
    for (const { regex, label, allow = [] } of patterns) {
      if (allow.some(x => rel === x || rel.startsWith(x))) continue
      if (regex.test(text)) findings.push(`${rel}: ${label}`)
      regex.lastIndex = 0
    }
  }
  if (findings.length) {
    result(name, 'FAIL', findings.slice(0, 20).join('\n'))
    return false
  }
  result(name, 'PASS')
  return true
}

scanText('Merge conflict markers', [
  { regex: /^(<{7}|={7}|>{7})/m, label: 'merge conflict marker' },
])

scanText('Secret scan', [
  { regex: /-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----/, label: 'private key material' },
  { regex: /\bEAA[A-Za-z0-9_-]{40,}\b/, label: 'Facebook access token pattern' },
  { regex: /\bAIza[0-9A-Za-z_-]{30,}\b/, label: 'Google API key pattern' },
  { regex: /\bAKIA[0-9A-Z]{16}\b/, label: 'AWS access key pattern' },
  { regex: /^(?:MAIL_PASSWORD|JWT_SECRET|MYSQL_PASSWORD)\s*=\s*(?:"(?!CHANGE_ME|\$\{|")[^"\r\n]{8,}"|'(?!CHANGE_ME|\$\{|'')[^'\r\n]{8,}'|(?!CHANGE_ME|\$\{|settings\.|self\.|os\.|$)[A-Za-z0-9_!@#$%^&*+=-]{8,})\s*$/m, label: 'hard-coded sensitive environment value', allow: ['PROJECT-AUDIT.md'] },
])

run('Python syntax compile', 'python', ['-m', 'compileall', '-q', 'api', 'worker', 'queue', 'storage'])

const frontend = join(root, 'frontend')
const nodeModules = join(frontend, 'node_modules')
if (!existsSync(nodeModules)) {
  result('Frontend dependency state', 'SKIP', 'run `cd frontend && npm ci`')
} else if (mode === 'full') {
  run('Frontend lint', 'npm', ['exec', '--', 'eslint', '.', '--ext', '.vue,.js,.jsx,.cjs,.mjs', '--ignore-path', '.gitignore'], frontend)
  run('Frontend unit tests', 'npm', ['run', 'test:unit', '--', '--run'], frontend)
  run('Frontend production build', 'npm', ['run', 'build'], frontend)
} else {
  result('Frontend heavy checks', 'SKIP', 'use --full')
}

if (mode === 'full' || mode === 'security') {
  if (existsSync(join(frontend, 'node_modules'))) run('Production dependency audit', 'npm', ['audit', '--omit=dev', '--audit-level=high'], frontend, true)
  else result('Production dependency audit', 'SKIP', 'frontend dependencies not installed')
}

if (mode === 'full') {
  if (existsSync(join(root, 'docker-compose.yml'))) run('Docker Compose config', 'docker', ['compose', 'config'], root, true)
  const pytestFiles = walk(root).filter(f => /(^|\/)(test_[^/]+|[^/]+_test)\.py$/.test(f.replaceAll('\\','/')))
  if (pytestFiles.length) run('Backend tests', 'python', ['-m', 'pytest', '-q'], root)
  else result('Backend tests', 'SKIP', 'no Python test files found')
}

const failed = results.filter(x => x.status === 'FAIL')
console.log(`\nQuality gate mode=${mode}: ${failed.length ? 'FAIL' : 'PASS'} (${results.length} checks, ${failed.length} failed)`)
process.exit(failed.length ? 1 : 0)
