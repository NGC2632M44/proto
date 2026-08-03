#!/bin/bash
# 容器 Stop hook:通知 + proto 自采集
# 1. 通知(限流 300s):提取成果摘要 → 宿主 toast
# 2. proto-retrospect(不限流):每会话采集关键信号 → protocol inbox
# 注意:文件必须 LF 行尾

INPUT_FILE=$(mktemp)
cat > "$INPUT_FILE" 2>/dev/null

# ── proto-retrospect(不限流, 每会话运行) ──
node /home/node/.claude/hooks/proto-retrospect.js < "$INPUT_FILE" &

# ── 通知(限流 300s) ──
MARK=/home/node/.claude/.last-notify-ts
SKIP=0
if [ -f "$MARK" ]; then
  NOW=$(date +%s)
  LAST=$(stat -c %Y "$MARK" 2>/dev/null || echo 0)
  if [ $((NOW - LAST)) -lt 300 ]; then
    SKIP=1
  fi
fi
if [ $SKIP -eq 0 ]; then
  touch "$MARK"
  node /home/node/.claude/hooks/notify-send.js < "$INPUT_FILE"
fi

rm -f "$INPUT_FILE"
exit 0
