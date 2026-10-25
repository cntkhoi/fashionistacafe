#!/usr/bin/env node
// File "móc" của Agent Office: Claude Code gọi file này ở mỗi thao tác (xem hooks/settings.example.json),
// file đọc sự kiện từ stdin, lọc bớt còn vài trường ngắn rồi gửi về máy chủ văn phòng.
// Không có AGENT_OFFICE_TOKEN thì không làm gì cả (máy cá nhân chưa cài, CI...). Lỗi mạng bị bỏ qua:
// văn phòng không bao giờ được làm chậm hay làm hỏng phiên làm việc.
//
// Biến môi trường:
//   AGENT_OFFICE_TOKEN   trùng với secret OFFICE_TOKEN của Worker; trên máy cá nhân có thể để trong ~/.agent-office/token
//   AGENT_OFFICE_URL     mặc định https://agent-office.cntkhoi.workers.dev
//   AGENT_OFFICE_PROJECT tên dự án hiện trên văn phòng (mặc định: tên dự án Claude, không có thì tên repo)
import { readFileSync, writeFileSync } from "node:fs";
import { homedir, tmpdir } from "node:os";
import { basename, join } from "node:path";

// Cài trong repo (.claude/settings.json) thì chỉ chạy trên cloud: trên máy cá nhân đã có bản cài chung trong
// ~/.claude/settings.json, chạy cả hai thì mỗi sự kiện bị gửi hai lần.
if (process.argv.includes("--cloud-only") && !process.env.CLAUDE_CODE_REMOTE) process.exit(0);

let token = process.env.AGENT_OFFICE_TOKEN;
if (!token) {
  try {
    token = readFileSync(join(homedir(), ".agent-office", "token"), "utf8").trim();
  } catch {
    process.exit(0);
  }
}
if (!token) process.exit(0);

const url = (process.env.AGENT_OFFICE_URL || "https://agent-office.cntkhoi.workers.dev").replace(/\/+$/, "");

let raw = "";
try {
  raw = readFileSync(0, "utf8");
} catch {
  process.exit(0);
}
let ev;
try {
  ev = JSON.parse(raw);
} catch {
  process.exit(0);
}

const SKIP = new Set(["PostToolUse"]);
if (!ev || SKIP.has(ev.hook_event_name)) process.exit(0);

// Phiên trên cloud có mã cố định qua các lần khởi động lại; trên máy thì dùng session_id.
const session = process.env.CLAUDE_CODE_REMOTE_SESSION_ID || ev.session_id || "unknown";
const statePath = join(tmpdir(), `agent-office-${session.replace(/[^\w-]/g, "")}.json`);

let state = {};
try {
  state = JSON.parse(readFileSync(statePath, "utf8"));
} catch {
  state = {};
}
let stateChanged = false;

const cut = (s, n) => {
  if (typeof s !== "string") return undefined;
  const t = s.replace(/\s+/g, " ").trim();
  return t.length > n ? `${t.slice(0, n - 1)}…` : t;
};

// Che khoá bí mật trong lệnh trước khi gửi đi.
const mask = (s) =>
  s &&
  s
    .replace(/\b(sk|ghp|gho|github_pat|xox[abp]|AKIA)[-_A-Za-z0-9]{8,}/g, "***")
    .replace(/((?:token|key|secret|password|passwd|pwd|auth)[\w-]*\s*[=:]\s*)\S+/gi, "$1***")
    .replace(/(Bearer\s+)\S+/gi, "$1***");

let promptKind;
if (ev.hook_event_name === "UserPromptSubmit" && typeof ev.prompt === "string") {
  const p = ev.prompt;
  const title = p.match(/Thread title: "([^"\n]{1,200})"/);
  if (title && state.title !== title[1]) {
    state.title = title[1];
    stateChanged = true;
  }
  const project = p.match(/(?:^|\n)Project: "([^"\n]{1,100})"/);
  if (project && state.project !== project[1]) {
    state.project = project[1];
    stateChanged = true;
  }
  // Phiên điều phối (CEO) của dự án Claude nhận tin "thread-activity" về các thread khác.
  if (!state.coordinator && /<wake reason="thread-activity"/.test(p)) {
    state.coordinator = true;
    stateChanged = true;
  }
  promptKind = /<task-notification>/.test(p)
    ? "task"
    : /<relay from=|<coordinator-relay>/.test(p)
      ? "relay"
      : /<wake reason="(external-event|scheduled|reminder)"/.test(p)
        ? "event"
        : "user";
}
if (ev.tool_name === "mcp__hearthbot__rename_thread" && ev.tool_input?.title) {
  state.title = String(ev.tool_input.title).slice(0, 200);
  stateChanged = true;
}
if (stateChanged) {
  try {
    writeFileSync(statePath, JSON.stringify(state));
  } catch {
    // không ghi được thì lần sau đọc lại từ tin nhắn
  }
}

const ti = ev.tool_input && typeof ev.tool_input === "object" ? ev.tool_input : {};
const input = {};
for (const [k, n] of [
  ["file_path", 200],
  ["path", 200],
  ["notebook_path", 200],
  ["pattern", 80],
  ["description", 120],
  ["subagent_type", 40],
  ["url", 200],
  ["query", 120],
  ["skill", 60],
  ["question", 160],
  ["title", 120],
]) {
  const v = cut(ti[k], n);
  if (v) input[k] = v;
}
if (typeof ti.command === "string") input.command = mask(cut(ti.command, 200));
// Danh sách việc: checklist của thread (✓ ✱ ○) hoặc TodoWrite.
if (typeof ti.text === "string" && ev.tool_name === "mcp__hearthbot__update_progress_checklist") input.checklist = ti.text.slice(0, 2000);
if (Array.isArray(ti.todos)) {
  input.todos = ti.todos.slice(0, 30).map((t) => ({ content: cut(t.content, 120), status: t.status }));
}

const body = {
  v: 1,
  event: ev.hook_event_name,
  session,
  at: Date.now(),
  host: process.env.CLAUDE_CODE_REMOTE ? "cloud" : "local",
  project: process.env.AGENT_OFFICE_PROJECT || state.project || basename(process.env.CLAUDE_PROJECT_DIR || ev.cwd || "") || undefined,
  title: state.title,
  coordinator: state.coordinator || undefined,
  agentId: ev.agent_id,
  agentType: ev.agent_type,
  tool: ev.tool_name,
  toolUseId: ev.tool_use_id,
  input: Object.keys(input).length ? input : undefined,
  promptKind,
  notification: cut(ev.message, 160),
  notificationType: ev.notification_type,
  error: ev.hook_event_name === "PostToolUseFailure" ? cut(String(ev.error ?? "lỗi"), 160) : undefined,
  reason: ev.reason || ev.source,
  model: process.env.ANTHROPIC_MODEL || undefined,
};

try {
  await fetch(`${url}/api/ingest`, {
    method: "POST",
    headers: { "content-type": "application/json", authorization: `Bearer ${token}` },
    body: JSON.stringify(body),
    signal: AbortSignal.timeout(4000),
  });
} catch {
  // máy chủ văn phòng tắt hoặc mạng bị chặn: bỏ qua
}
process.exit(0);
