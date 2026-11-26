--!nonstrict
-- 언어 컨트롤러: 화면 글자를 지금 고른 언어(English / 한국어)로 보여 준다. 기본은 English.
-- 기존 코드는 그대로 영어 글자를 넣는다. 이 컨트롤러가 PlayerGui·workspace 의 글자(TextLabel·TextButton 의 Text,
-- TextBox 의 PlaceholderText, ProximityPrompt 의 ActionText·ObjectText)를 지켜보다가 번역한 글자로 바꿔 넣는다.
-- 그래서 기존 UI 코드는 고치지 않아도 되고, 나중에 새로 생기는 UI 에도 자동으로 적용된다.
--
-- 번역 데이터: Shared.Data.LanguageData (키 기반, 영어·한국어가 같은 키). 원본은 저장소 scripts/lang/ko.tsv → build_language_data.py.
--   번역 찾는 순서: 같은 글자 → 대문자로 바꾼 글자(UPPER 로 쓰는 제목) → 형식 문구("LV %d", "{value}% damage" 처럼 숫자·이름이 들어가는 문구)
--   → 여러 줄이면 줄마다. 형식 문구 안의 %s(이름 등)도 다시 번역한다. 아무것도 없으면 영어 그대로 (오류 없음).
-- 원문 보관: 바꾼 글자에는 속성 LangSource(영어 원문)를 남긴다. 화면 글자를 영어와 비교하는 코드는
--   LanguageController.sourceOf(label) 또는 label:GetAttribute("LangSource") or label.Text 를 쓴다 (TutorialController).
-- 번역하지 않을 글자: 그 객체나 조상(ScreenGui 까지)에 속성 NoTranslate = true. TextBox 에 입력된 글자는 건드리지 않는다.
-- 언어 저장은 SettingsController 가 서버 Settings 서비스("setLanguage")로 한다. 이 모듈은 화면만 맡는다.
--
-- 다른 코드에서 쓰기:
--   LanguageController.get("Skills.BladeWhirl.Name")  -- 지금 언어의 글자 (없으면 영어, 그것도 없으면 키)
--   LanguageController.translate("Inventory")         -- 영어 글자를 지금 언어로
--   LanguageController.language                        -- "en" / "ko"
--   LanguageController.changed.Event:Connect(function(lang) end)

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local LANGUAGES = { "en", "ko" }
local DEFAULT = "en"
local CACHE_LIMIT = 4000
local MAX_DEPTH = 3 -- 형식 문구 안 이름·문장을 다시 번역하는 깊이

local LanguageController = {}
LanguageController.language = DEFAULT
LanguageController.languages = LANGUAGES
LanguageController.changed = Instance.new("BindableEvent")

---------------------------------------------------------------- 데이터

local data = nil
do
	local ok, result = pcall(function()
		return require(ReplicatedStorage:WaitForChild("Shared"):WaitForChild("Data"):WaitForChild("LanguageData"))
	end)
	if ok and type(result) == "table" then
		data = result
	else
		warn("[LanguageController] LanguageData 로드 실패, 영어만 씁니다: " .. tostring(result))
		data = { entries = {}, names = { en = "English", ko = "한국어" } }
	end
end

LanguageController.names = data.names or { en = "English", ko = "한국어" }

-- 형식 문구의 자리 표시 하나를 읽는다: %d %s %.1f %02d %+.2f ... / {이름} / {1}
-- 돌려줌: 종류("num"·"str"·"name"·"index"), 이름 또는 번호, 길이. 아니면 nil
local function readSpec(text: string, i: number)
	local c = string.sub(text, i, i)
	if c == "%" then
		local spec = string.match(text, "^%%[%-%+#0]*%d*%.?%d*[dsfxi]", i)
		if spec then
			local conv = string.sub(spec, -1)
			return if conv == "s" then "str" else "num", nil, #spec
		end
	elseif c == "{" then
		local name = string.match(text, "^{([%w_]+)}", i)
		if name then
			local n = tonumber(name)
			if n then
				return "index", n, #name + 2
			end
			return "name", name, #name + 2
		end
	end
	return nil
end

local function isTemplate(en: string): boolean
	local i = 1
	while i <= #en do
		local c = string.sub(en, i, i)
		if c == "%" and string.sub(en, i + 1, i + 1) == "%" then
			i += 2
		else
			local kind, _, len = readSpec(en, i)
			if kind == "num" or kind == "str" or kind == "name" then
				return true
			end
			i += len or 1
		end
	end
	return false
end

-- 영어 형식 문구 → Lua 패턴 + 자리 표시 목록
local function compile(en: string)
	local parts, specs = { "^" }, {}
	local literal = 0
	local i = 1
	while i <= #en do
		local c = string.sub(en, i, i)
		if c == "%" and string.sub(en, i + 1, i + 1) == "%" then
			table.insert(parts, "%%")
			literal += 1
			i += 2
		else
			local kind, name, len = readSpec(en, i)
			if kind == "str" then
				table.insert(parts, "(.-)")
				table.insert(specs, { kind = "str" })
				i += len
			elseif kind == "num" or kind == "name" then
				table.insert(parts, "([%-%+]?[%d%.,]+)")
				table.insert(specs, { kind = "num", name = name })
				i += len
			else
				if string.find(c, "[%^%$%(%)%%%.%[%]%*%+%-%?]") then
					table.insert(parts, "%" .. c)
				else
					table.insert(parts, c)
				end
				if string.find(c, "%S") then
					literal += 1
				end
				i += 1
			end
		end
	end
	table.insert(parts, "$")
	return table.concat(parts), specs, literal
end

local exact = {} -- [영어] = 키
local upper = {} -- [대문자 영어] = 키
local templates = {} -- { pattern, specs, key, literal }
local byKey = data.entries or {}

for key, entry in byKey do
	local en = entry.en
	if type(en) ~= "string" or en == "" then
		continue
	end
	if isTemplate(en) then
		local pattern, specs, literal = compile(en)
		table.insert(templates, { pattern = pattern, specs = specs, key = key, literal = literal })
	else
		if exact[en] == nil then
			exact[en] = key
		end
		local up = string.upper(en)
		if upper[up] == nil then
			upper[up] = key
		end
	end
end
-- 글자가 많이 고정된 문구부터 (짧은 일반 문구가 긴 문구를 가로채지 않게)
table.sort(templates, function(a, b)
	if a.literal ~= b.literal then
		return a.literal > b.literal
	end
	return a.key < b.key
end)

---------------------------------------------------------------- 번역

local cache = {}
local cacheCount = 0

local function textFor(key: string, lang: string): string?
	local entry = byKey[key]
	if not entry then
		return nil
	end
	local t = entry[lang]
	if type(t) == "string" and t ~= "" then
		return t
	end
	return nil
end

local translate -- 앞 선언 (형식 문구 안 이름을 다시 번역)

-- 한국어 형식 문구에 잡은 값을 채운다. {1}{2} = 번호, {이름} = 영어와 같은 이름, %d·%s = 순서대로
local function render(out: string, captures, specs, depth: number): string
	local values = {}
	for i, spec in specs do
		local v = captures[i]
		if spec.kind == "str" and v ~= "" then
			v = translate(v, depth + 1)
		end
		values[i] = v
	end
	local result = {}
	local nextIndex = 1
	local i = 1
	while i <= #out do
		local c = string.sub(out, i, i)
		if c == "%" and string.sub(out, i + 1, i + 1) == "%" then
			table.insert(result, "%")
			i += 2
		else
			local kind, name, len = readSpec(out, i)
			if kind == "index" then
				table.insert(result, values[name] or "")
				i += len
			elseif kind == "name" then
				local found = ""
				for k, spec in specs do
					if spec.name == name then
						found = values[k]
						break
					end
				end
				table.insert(result, found)
				i += len
			elseif kind == "num" or kind == "str" then
				table.insert(result, values[nextIndex] or "")
				nextIndex += 1
				i += len
			else
				table.insert(result, c)
				i += 1
			end
		end
	end
	return table.concat(result)
end

local function translateBody(body: string, lang: string, depth: number): string?
	local key = exact[body] or upper[string.upper(body)]
	if key then
		return textFor(key, lang)
	end
	if depth > MAX_DEPTH then
		return nil
	end
	for _, t in templates do
		local captures = { string.match(body, t.pattern) }
		if captures[1] ~= nil then
			local out = textFor(t.key, lang)
			if out then
				return render(out, captures, t.specs, depth)
			end
			return nil
		end
	end
	return nil
end

local function translatePlain(text: string, lang: string, depth: number): string
	local lead, body, trail = string.match(text, "^(%s*)(.-)(%s*)$")
	if body == "" or not string.find(body, "%a") then
		return text
	end
	local out = translateBody(body, lang, depth)
	if out then
		return lead .. out .. trail
	end
	-- 여러 줄이면 줄마다
	if string.find(body, "\n") then
		local lines = string.split(body, "\n")
		local changed = false
		for i, line in lines do
			local t = translatePlain(line, lang, depth)
			if t ~= line then
				lines[i] = t
				changed = true
			end
		end
		if changed then
			return lead .. table.concat(lines, "\n") .. trail
		end
		return text
	end
	-- 여러 문장이 이어 붙은 글(특성 설명 + 등급별 추가 문장 등): 앞에서부터 가장 길게 번역되는 문장 묶음을 찾는다
	if depth <= MAX_DEPTH and string.find(body, "[%.!%?] %S") then
		local sentences = {}
		local pos = 1
		while true do
			local s, e = string.find(body, "[%.!%?] ", pos)
			if not s then
				table.insert(sentences, string.sub(body, pos))
				break
			end
			table.insert(sentences, string.sub(body, pos, s))
			pos = e + 1
		end
		if #sentences > 1 and #sentences <= 12 then
			local out, changed = {}, false
			local i = 1
			while i <= #sentences do
				local found, foundJ = nil, i
				for j = #sentences, i, -1 do
					if not (i == 1 and j == #sentences) then
						local t = translateBody(table.concat(sentences, " ", i, j), lang, depth + 1)
						if t then
							found, foundJ = t, j
							break
						end
					end
				end
				if found then
					table.insert(out, found)
					changed = true
				else
					table.insert(out, sentences[i])
				end
				i = foundJ + 1
			end
			if changed then
				return lead .. table.concat(out, " ") .. trail
			end
		end
	end
	return text
end

-- RichText 태그(<font ...>, <b> 등)는 그대로 두고 태그 사이 글자만 번역한다
local function translateRich(text: string, lang: string, depth: number): string
	local whole = translatePlain(text, lang, depth)
	if whole ~= text or not string.find(text, "<[/%a][^<>]*>") then
		return whole
	end
	local out = {}
	local pos = 1
	while true do
		local s, e = string.find(text, "<[/%a][^<>]*>", pos)
		if not s then
			table.insert(out, translatePlain(string.sub(text, pos), lang, depth))
			break
		end
		if s > pos then
			table.insert(out, translatePlain(string.sub(text, pos, s - 1), lang, depth))
		end
		table.insert(out, string.sub(text, s, e))
		pos = e + 1
	end
	return table.concat(out)
end

translate = function(text: string, depth: number?): string
	local lang = LanguageController.language
	if lang == DEFAULT or type(text) ~= "string" or text == "" or not string.find(text, "%a") then
		return text
	end
	depth = depth or 0
	if depth == 0 then
		local hit = cache[text]
		if hit then
			return hit
		end
	end
	local ok, result = pcall(translateRich, text, lang, depth)
	if not ok or type(result) ~= "string" then
		result = text
	end
	if depth == 0 then
		if cacheCount >= CACHE_LIMIT then
			table.clear(cache)
			cacheCount = 0
		end
		cache[text] = result
		cacheCount += 1
	end
	return result
end

function LanguageController.translate(text: string): string
	return translate(text, 0)
end

-- 키로 지금 언어의 글자. 없으면 영어 → fallback → 키 순서
function LanguageController.get(key: string, fallback: string?): string
	return textFor(key, LanguageController.language) or textFor(key, DEFAULT) or fallback or key
end

---------------------------------------------------------------- 화면 글자 적용

local PROPS = {
	TextLabel = { "Text" },
	TextButton = { "Text" },
	TextBox = { "PlaceholderText" },
	ProximityPrompt = { "ActionText", "ObjectText" },
}

local states = setmetatable({}, { __mode = "k" }) -- [객체] = { [속성] = { src = 영어, out = 보여 준 글자 } }
local started = false

local function propsOf(inst: Instance)
	return PROPS[inst.ClassName]
end

local function skipped(inst: Instance): boolean
	local node = inst
	for _ = 1, 30 do
		if not node then
			return false
		end
		if node:GetAttribute("NoTranslate") == true then
			return true
		end
		if node:IsA("LayerCollector") or node == workspace then
			return false
		end
		node = node.Parent
	end
	return false
end

local function apply(inst: Instance, prop: string)
	local state = states[inst]
	if not state then
		return
	end
	local current = inst[prop]
	local entry = state[prop]
	if entry and current == entry.out then
		return -- 방금 이 컨트롤러가 쓴 글자
	end
	local out = translate(current, 0)
	if out == current then
		state[prop] = nil
		if prop == "Text" and inst:GetAttribute("LangSource") ~= nil then
			inst:SetAttribute("LangSource", nil)
		end
		return
	end
	state[prop] = { src = current, out = out }
	if prop == "Text" then
		inst:SetAttribute("LangSource", current)
	end
	inst[prop] = out
end

-- 언어가 바뀌면 원문으로 다시 번역한다
local function reapply(inst: Instance)
	local state = states[inst]
	local props = propsOf(inst)
	if not (state and props) then
		return
	end
	for _, prop in props do
		local entry = state[prop]
		local src = if entry then entry.src else inst[prop]
		local out = translate(src, 0)
		if out == src then
			state[prop] = nil
			if prop == "Text" and inst:GetAttribute("LangSource") ~= nil then
				inst:SetAttribute("LangSource", nil)
			end
		else
			state[prop] = { src = src, out = out }
			if prop == "Text" then
				inst:SetAttribute("LangSource", src)
			end
		end
		if inst[prop] ~= out then
			inst[prop] = out
		end
	end
end

local function watch(inst: Instance)
	local props = propsOf(inst)
	if not props or states[inst] then
		return
	end
	if skipped(inst) then
		return
	end
	states[inst] = {}
	for _, prop in props do
		inst:GetPropertyChangedSignal(prop):Connect(function()
			apply(inst, prop)
		end)
		if LanguageController.language ~= DEFAULT then
			apply(inst, prop)
		end
	end
end

local function onAdded(inst: Instance)
	if PROPS[inst.ClassName] then
		watch(inst)
	end
end

-- 큰 맵에서도 멈추지 않게 나눠서 훑는다
local function scan(root: Instance)
	local list = root:GetDescendants()
	for i, inst in list do
		if PROPS[inst.ClassName] then
			watch(inst)
		end
		if i % 4000 == 0 then
			task.wait()
		end
	end
end

function LanguageController.sourceOf(inst: Instance): string
	local state = states[inst]
	local entry = state and state.Text
	return if entry then entry.src else inst.Text
end

function LanguageController.setLanguage(lang: string)
	if not table.find(LANGUAGES, lang) then
		lang = DEFAULT
	end
	if lang == LanguageController.language then
		return
	end
	LanguageController.language = lang
	table.clear(cache)
	cacheCount = 0
	if started then
		for inst in states do
			if inst.Parent then
				reapply(inst)
			end
		end
	end
	LanguageController.changed:Fire(lang)
end

function LanguageController.init()
	if started then
		return
	end
	started = true
	local player = Players.LocalPlayer
	local playerGui = player:WaitForChild("PlayerGui")
	playerGui.DescendantAdded:Connect(onAdded)
	workspace.DescendantAdded:Connect(onAdded)
	task.spawn(scan, playerGui)
	task.spawn(scan, workspace)
end

return LanguageController
