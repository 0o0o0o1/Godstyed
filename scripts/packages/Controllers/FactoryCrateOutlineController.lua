--!nonstrict
-- 공장 등급 상자 테두리 빛 (공용 패키지 Controllers 의 모듈 FactoryCrateOutlineController, 공장 place 에서만 시작)
-- 서버(FactoryRaid)가 단 태그 "TierCrate" + 속성 CrateTierColor 를 보고, 가까운 상자에 등급 색 Highlight 를 단다.
-- Highlight 는 한 화면에 31개까지만 그려지므로 가까운 MAX_SHOWN 개만 (다른 효과 몫을 남김).
-- 습격 상자가 닫히기 전(속성 FadeEnd)에는 끈·불빛·테두리가 깜빡이고 마지막 5초는 빨라지며, 가까이 있으면 틱 소리.
-- 원본: 저장소 scripts/packages/Controllers/FactoryCrateOutlineController.lua (패키지 코드는 마을 place 에서만 수정, CLAUDE.md)

local ReplicatedStorage = game:GetService("ReplicatedStorage")
local PlaceConfig = require(ReplicatedStorage:WaitForChild("Shared").Config.PlaceConfig)

local FactoryCrateOutlineController = {}

local function run()
	local CollectionService = game:GetService("CollectionService")
	local Players = game:GetService("Players")

	local TAG = "TierCrate"
	local MAX_SHOWN = 16
	local MAX_DISTANCE = 160
	local UPDATE = 0.4

	local player = Players.LocalPlayer
	local camera = workspace.CurrentCamera
	local holder = Instance.new("Folder")
	holder.Name = "CrateOutlines"
	holder.Parent = camera

	local shown = {} -- [crate] = Highlight

	local function remove(crate)
		local h = shown[crate]
		if h then
			h:Destroy()
			shown[crate] = nil
		end
	end

	local function centerOf(crate: Instance): Vector3?
		if crate:IsA("BasePart") then
			return crate.Position
		elseif crate:IsA("Model") then
			local ok, cf = pcall(crate.GetPivot, crate)
			return ok and cf.Position or nil
		end
		return nil
	end

	CollectionService:GetInstanceRemovedSignal(TAG):Connect(remove)

	---------------------------------------------------------------- 닫히기 전 깜빡임 (습격 상자)
	-- 서버가 닫히기 15초 전에 상자 속성 FadeEnd(서버 시각)를 달면: 등급 끈·상자 불빛·테두리가 같은 박자로 깜빡이고
	-- 마지막 FAST_BLINK 초는 빨라짐. 밝아질 때마다 상자에서 작은 틱 소리 (TICK_RANGE 안에서만 들림).
	-- 끈 색은 내 화면에서만 바꿈 (서버 값은 그대로).
	local RunService = game:GetService("RunService")
	local FAST_BLINK = 5
	local SLOW_PERIOD, FAST_PERIOD = 0.5, 0.2 -- 한 번 켜졌다 꺼지는 시간
	local TICK_ID = "rbxasset://sounds/clickfast.wav" -- 엔진 내장 소리라 불러오기 지연 없음
	local TICK_RANGE = 30
	local DIM = Color3.fromRGB(45, 32, 26)

	local fading = {} -- [crate] = { straps = {Part}, color, light, sound, wasOn }

	local function startFade(crate: Instance)
		if fading[crate] then
			return
		end
		local entry = { straps = {}, color = crate:GetAttribute("CrateTierColor"), wasOn = true }
		local anchor
		for _, p in crate:GetDescendants() do
			if p:IsA("BasePart") then
				anchor = anchor or p
				if p.Name:find("_Metal$") then
					table.insert(entry.straps, p)
				end
			elseif p:IsA("PointLight") then
				entry.light = p
			end
		end
		if anchor then
			local s = Instance.new("Sound")
			s.SoundId = TICK_ID
			s.Volume = 0.55
			s.RollOffMode = Enum.RollOffMode.InverseTapered
			s.RollOffMinDistance, s.RollOffMaxDistance = 6, TICK_RANGE
			s.Parent = anchor
			entry.sound = s
		end
		fading[crate] = entry
	end

	local function blinkOn(fadeEnd: number): (boolean, boolean)
		local left = fadeEnd - workspace:GetServerTimeNow()
		local fast = left <= FAST_BLINK
		local period = if fast then FAST_PERIOD else SLOW_PERIOD
		return (left % period) > period * 0.4, fast -- 60% 켜짐 / 40% 꺼짐
	end

	RunService.Heartbeat:Connect(function()
		for crate, entry in fading do
			local fadeEnd = crate:GetAttribute("FadeEnd")
			if not crate.Parent or not fadeEnd then
				if entry.sound then
					entry.sound:Destroy()
				end
				fading[crate] = nil
				continue
			end
			local on, fast = blinkOn(fadeEnd)
			if on ~= entry.wasOn then
				entry.wasOn = on
				for _, p in entry.straps do
					p.Color = if on then entry.color else DIM
				end
				if entry.light then
					entry.light.Brightness = if on then 1.2 else 0.15
				end
				local h = shown[crate]
				if h then
					h.OutlineTransparency = if on then 0 else 0.8
					h.FillTransparency = if on then 0.82 else 1
				end
				if on and entry.sound then
					entry.sound.PlaybackSpeed = if fast then 1.25 else 0.9
					entry.sound:Play()
				end
			end
		end
	end)

	local function watchFade(crate: Instance)
		if crate:GetAttribute("FadeEnd") then
			startFade(crate)
		end
		crate:GetAttributeChangedSignal("FadeEnd"):Connect(function()
			if crate:GetAttribute("FadeEnd") then
				startFade(crate)
			end
		end)
	end
	for _, c in CollectionService:GetTagged(TAG) do
		watchFade(c)
	end
	CollectionService:GetInstanceAddedSignal(TAG):Connect(watchFade)

	while true do
		local char = player.Character
		local root = char and char:FindFirstChild("HumanoidRootPart")
		local from = if root then root.Position else camera.CFrame.Position
		local list = {}
		for _, crate in CollectionService:GetTagged(TAG) do
			local color = crate:GetAttribute("CrateTierColor")
			local pos = crate:IsDescendantOf(workspace) and color and not crate:GetAttribute("CrateOpen") and centerOf(crate)
			if pos then
				local d = (pos - from).Magnitude
				if d <= MAX_DISTANCE then
					table.insert(list, { crate = crate, d = d, color = color })
				end
			end
		end
		table.sort(list, function(a, b)
			return a.d < b.d
		end)
		local keep = {}
		for i = 1, math.min(MAX_SHOWN, #list) do
			local e = list[i]
			keep[e.crate] = true
			local h = shown[e.crate]
			if not h then
				h = Instance.new("Highlight")
				h.Adornee = e.crate
				h.DepthMode = Enum.HighlightDepthMode.Occluded
				h.OutlineTransparency = 0
				h.FillTransparency = 0.82
				h.Parent = holder
				shown[e.crate] = h
			end
			h.OutlineColor = e.color
			h.FillColor = e.color
		end
		for crate in shown do
			if not keep[crate] then
				remove(crate)
			end
		end
		task.wait(UPDATE)
	end
end

function FactoryCrateOutlineController.init()
	if game.PlaceId ~= PlaceConfig.FACTORY then
		return -- 공장 place 에서만
	end
	task.spawn(run)
end

return FactoryCrateOutlineController
