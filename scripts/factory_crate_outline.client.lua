--!nonstrict
-- 공장 등급 상자 테두리 빛 (공장 place 전용 LocalScript: StarterPlayerScripts.FactoryCrateOutline)
-- 원본: 저장소 scripts/factory_crate_outline.client.lua
-- 서버(FactoryRaid)가 단 태그 "TierCrate" + 속성 CrateTierColor 를 보고, 가까운 상자에 등급 색 Highlight 를 단다.
-- Highlight 는 한 화면에 31개까지만 그려지므로 가까운 MAX_SHOWN 개만 (다른 효과 몫을 남김).

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
