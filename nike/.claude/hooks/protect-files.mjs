#!/usr/bin/env node
import process from 'node:process'
import path from 'node:path'

let raw = ''
for await (const chunk of process.stdin) raw += chunk

let input
try {
  input = JSON.parse(raw || '{}')
} catch {
  console.error('Blocked: hook received invalid JSON.')
  process.exit(2)
}

const filePath = String(input?.tool_input?.file_path ?? '').replaceAll('\\', '/')
const normalized = path.posix.normalize(filePath)
const protectedPatterns = [
  /(^|\/)\.env(?:\.|$)/i,
  /(^|\/)secrets?(\/|$)/i,
  /(^|\/)credentials?[^/]*\.json$/i,
  /(^|\/)\.git(\/|$)/i,
  /\.(pem|key|p12|pfx)$/i,
]

if (normalized.includes('../') || protectedPatterns.some(pattern => pattern.test(normalized))) {
  console.error(`Blocked: ${filePath || '<unknown path>'} is protected. Use an example/template file and ask the user to manage the real secret locally.`)
  process.exit(2)
}

process.exit(0)
