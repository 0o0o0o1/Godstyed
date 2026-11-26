# -*- coding: utf-8 -*-
"""번역 원본 ko.tsv 를 검사하고 Roblox ModuleScript 소스 LanguageData.lua 를 만든다.

ko.tsv 형식 (" | " 로 구분, UTF-8):
  ## 구역이름              → 이후 줄의 자동 키 앞부분 (예: UI.Settings)
  키 | 영어 | 한국어        → 키가 '-' 이면 "구역이름.영어단어CamelCase" 로 자동 생성 (모듈이 읽을 때 같은 규칙으로 만든다)
  "# " 로 시작하는 줄은 주석. 글자 안의 줄바꿈은 \\n 으로 쓴다.
형식 문구: 영어에 %d %s %.1f {value} 같은 자리가 있으면 형식 문구. 한국어 쪽은
  같은 자리를 같은 순서로 쓰거나, 순서를 바꿀 땐 {1} {2} (몇 번째 자리), 이름 자리는 {value} 처럼 같은 이름.

LanguageData.lua = 머리말 + (주석 뺀) TSV 원문 + 읽는 코드. Studio 에도 같은 내용을 넣는다.
실행: python scripts/lang/build_language_data.py  → scripts/packages/Shared/LanguageData.lua
      python scripts/lang/build_language_data.py --chunks 20000  → 붙여 넣을 조각 정보와 검사합(checksum) 출력
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "ko.tsv"
OUT = HERE.parent / "packages" / "Shared" / "LanguageData.lua"

SPEC = re.compile(r"%%|%[-+#0]*\d*\.?\d*[dsfxi]|\{[A-Za-z_]\w*\}")

HEADER = """--!strict
-- 언어 데이터 (자동 생성 — 직접 고치지 말 것). 원본: 저장소 scripts/lang/ko.tsv → build_language_data.py
-- 아래 SOURCE 는 TSV 원문 (키 | 영어 | 한국어). 키가 '-' 이면 "## 구역" + 영어 단어로 키를 만든다.
-- 돌려줌: { names = { en, ko }, entries = { [키] = { en = 영어, ko = 한국어 } } }. 영어·한국어가 같은 키를 쓴다.
-- 쓰는 곳: Controllers.LanguageController. 형식 문구 규칙은 그쪽 머리말 참고.

local SOURCE = [==[
"""

FOOTER = """]==]

local entries = {}
local used = {}
local section = ""

local function autoKey(sec: string, en: string): string
	local words = {}
	for word in string.gmatch(en, "[%w]+") do
		if #words >= 6 then
			break
		end
		table.insert(words, string.upper(string.sub(word, 1, 1)) .. string.lower(string.sub(word, 2)))
	end
	local base = if #words > 0 then table.concat(words) else "Text"
	local key = if sec ~= "" then sec .. "." .. base else base
	local k, n = key, 2
	while used[k] do
		k = key .. "_" .. n
		n += 1
	end
	return k
end

for line in string.gmatch(SOURCE, "[^\\n]+") do
	if string.sub(line, 1, 3) == "## " then
		section = string.match(string.sub(line, 4), "^%s*(.-)%s*$")
	elseif string.sub(line, 1, 2) ~= "# " then
		local key, en, ko = string.match(line, "^(.-) | (.-) | (.*)$")
		if key and en and en ~= "" then
			en = string.gsub(en, "\\\\n", "\\n")
			ko = string.gsub(ko, "\\\\n", "\\n")
			if key == "" or key == "-" then
				key = autoKey(section, en)
			end
			if not used[key] then
				used[key] = true
				entries[key] = { en = en, ko = ko }
			end
		end
	end
end

return {
	names = { en = "English", ko = "한국어" },
	entries = entries,
}
"""


def specs(text):
    return [m for m in SPEC.findall(text) if m != "%%"]


def checksum(text):
    # Studio 쪽과 같은 계산: UTF-8 바이트 (위치 * 바이트) 합을 2^31-1 로 나눈 나머지
    total = 0
    for i, b in enumerate(text.encode("utf-8"), 1):
        total = (total + i * b) % 2147483647
    return total


def main():
    errors = []
    seen_en = {}
    body = []
    count = 0
    for ln, raw in enumerate(SRC.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.rstrip("\r")
        if not line.strip() or line.startswith("# "):
            continue
        if "]==]" in line:
            errors.append(f"{ln}: ]==] 는 쓸 수 없음")
        if line.startswith("## "):
            body.append(line)
            continue
        cols = line.split(" | ")
        if len(cols) != 3:
            errors.append(f"{ln}: 칸이 3개가 아님 ({len(cols)}) {line[:60]}")
            continue
        key, en, ko = cols
        if not en:
            errors.append(f"{ln}: 영어 없음")
            continue
        if en in seen_en:
            errors.append(f"{ln}: 영어 중복 (먼저 {seen_en[en]}줄) {en[:50]}")
            continue
        seen_en[en] = ln
        se, sk = specs(en), specs(ko)
        if se and not re.search(r"\{\d+\}", ko):
            named_en = [s for s in se if s.startswith("{")]
            if named_en:
                missing = [s for s in sk if s.startswith("{") and s not in named_en]
                if missing:
                    errors.append(f"{ln}: 한국어에 없는 이름 자리 {missing}")
            elif len(se) != len(sk):
                errors.append(f"{ln}: 자리 개수 다름 en{se} ko{sk}")
        body.append(line)
        count += 1

    if errors:
        print("\n".join(errors))
        sys.exit(1)

    tsv = "\n".join(body) + "\n"
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(HEADER + tsv + FOOTER, encoding="utf-8", newline="\n")
    print(f"{count} entries -> {OUT}  (tsv {len(tsv.encode('utf-8'))} bytes, checksum {checksum(tsv)})")

    if "--chunks" in sys.argv:
        size = int(sys.argv[sys.argv.index("--chunks") + 1])
        lines = tsv.splitlines(keepends=True)
        chunk, n, start = [], 0, 1
        for i, l in enumerate(lines, 1):
            chunk.append(l)
            n += len(l.encode("utf-8"))
            if n >= size or i == len(lines):
                print(f"chunk lines {start}-{i} ({n} bytes)")
                chunk, n, start = [], 0, i + 1


if __name__ == "__main__":
    main()
