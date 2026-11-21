--!nonstrict
-- 공장 습격 + 공장 등급 상자 (공장 place 전용 Script: ServerScriptService.FactoryRaid, 공용 패키지 밖)
-- 원본: 저장소 scripts/factory_raid.server.lua
--
-- 1) 공장 습격 = 상가 습격(ShopRaid)을 셔터 없이 연 공간에서 하는 것
--    웨이브마다 Workspace.FactoryEnemies.FactoryRaidSites 의 지점 몇 곳이 무작위 등급으로 "열린다"
--    → 그 자리에 등급 빛 + 등급 상자 + 등급만큼의 적(지점 속성 EnemyId)이 나타나고, 시간이 되면 빛·상자가 사라진다.
--    닫힐 때 플레이어 근처(ENEMY_KEEP_RANGE)에 없는 습격 적은 같이 사라지고, 싸우던 적은 남는다 (다시 태어나지 않음).
--    등급·확률·시간·적 수·상자 수·상자 내용물은 상가와 같은 ShopRaidConfig 를 쓴다.
-- 2) 공장 등급 상자 = 맵에 놓인 고정 상자 (속성 FactoryCrate = 예전 CrateConfig 상자 종류 이름, 기록용)
--    채워질 때마다 등급을 새로 뽑고, 열면 상가 상자처럼 내용물이 튀어나와 연 사람에게 빨려 들어간다.
--    고정 상자에는 등급별 경비 적(GUARD_COUNT)이 플레이어가 다가올 때 상자 둘레에 나타난다 (종류 = 가까운 습격 지점 몬스터).
-- 야외 몬스터(slag_walker·molten_walker 자리)는 습격·경비 모두 Molten·Slag 반반 (홀수면 Molten 한 마리 더).
-- 등급은 상자 모델 속성 CrateTier / CrateTierColor + 태그 "TierCrate" → 클라이언트 FactoryCrateOutline 이 테두리 빛을 그린다.

local CollectionService = game:GetService("CollectionService")
local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local ServerScriptService = game:GetService("ServerScriptService")
local ServerStorage = game:GetService("ServerStorage")

local SITES_PER_WAVE = 9 -- 웨이브마다 열리는 지점 수 (지점 26곳)
local SITE_RADIUS = 11 -- 지점 중심에서 상자를 놓는 범위
local ENEMY_SCATTER = 10
local ENEMY_KEEP_RANGE = 50 -- 닫힐 때 이 거리 안에 플레이어가 있는 습격 적은 남긴다
local NOTIFY_RANGE = 90 -- 닫힘 경고를 받는 거리
local TAG = "TierCrate"

-- 습격 지점 적 수 (상가 ShopRaidConfig 2·3·5·6·10 보다 많게, 공장 전용)
local RAID_ENEMIES = { Common = 4, Uncommon = 6, Rare = 8, Epic = 10, Legendary = 14 }
-- 고정 상자 경비 적 수 (등급별). 플레이어가 GUARD_WAKE 안에 처음 들어오면 상자 둘레에 나타나고,
-- 상자가 열리거나 GUARD_IDLE 초 동안 아무도 GUARD_SLEEP 안에 없으면 (살아 있는 경비만) 사라졌다가 다시 다가오면 또 나온다
local GUARD_COUNT = { Common = 2, Uncommon = 3, Rare = 5, Epic = 7, Legendary = 10 }
local GUARD_WAKE = 110
local GUARD_SLEEP = 170
local GUARD_IDLE = 30
local GUARD_RING = { 7, 16 } -- 상자에서 경비가 서는 거리
local GUARD_DEFAULT = "slag_walker"
local GUARD_SKIP_NEAR_BOSS = 140 -- 보스 마당 상자는 경비 안 붙임 (보스 마당 경비가 따로 있음)

-- 공용 서비스가 다 시작될 때까지 (Main 이 Loot·Enemy init 에서 만드는 폴더)
workspace:WaitForChild("Drops")
workspace:WaitForChild("Enemies")

local Services = ServerScriptService:WaitForChild("Services")
local LootService = require(Services.Loot)
local EnemyService = require(Services.Enemy)
local InventoryService = require(Services.Inventory)
local RewardLogic = require(Services.Enemy.RewardLogic)
local ShopRaidLogic = require(Services.ShopRaid.ShopRaidLogic)
local Kits = require(ServerStorage.MapTools.Kits)
local SR = require(ReplicatedStorage.Shared.Config.ShopRaidConfig)
local CrateConfig = require(ReplicatedStorage.Shared.Config.CrateConfig)

local rng = Random.new()

-- 야외 용암 몬스터(slag_walker·molten_walker)는 반반 섞어서 (홀수면 molten 이 한 마리 더)
local WALKERS = { slag_walker = true, molten_walker = true }
local function enemyKinds(kind: string, count: number): { [string]: number }
	if WALKERS[kind] then
		return { molten_walker = math.ceil(count / 2), slag_walker = math.floor(count / 2) }
	end
	return { [kind] = count }
end

local function notify(player: Player, text: string, color: Color3?, kind: string?)
	pcall(InventoryService.notify, player, text, color, kind)
end

local function setTier(model: Instance, tier: string?)
	model:SetAttribute("CrateTier", tier)
	model:SetAttribute("CrateTierColor", tier and SR.TIERS[tier].light or nil)
end

-- 상자 열기: 등급 드랍을 굴려 위로 튀어나오게, 연 사람 전용 (땅에 닿으면 빨려 들어감)
local function grant(player: Player, tier: string, position: Vector3)
	LootService.drop(position + Vector3.new(0, 2, 0), RewardLogic.rollDrops(SR.CRATE_DROPS[tier], rng), 6, player)
end

local function makePrompt(anchor: BasePart, tier: string, hold: number): ProximityPrompt
	local prompt = Instance.new("ProximityPrompt")
	prompt.Name = "CratePrompt"
	prompt.ActionText = "Search"
	prompt.ObjectText = tier .. " Crate"
	prompt.HoldDuration = hold
	prompt.MaxActivationDistance = SR.INTERACT_DISTANCE
	prompt.RequiresLineOfSight = false
	prompt.Parent = anchor
	return prompt
end

---------------------------------------------------------------- 고정 등급 상자

local fixedCrates = {} -- { inst, anchor, open, spawned, guards = {Model}, idleSince }

local function registerFixed(inst: Instance)
	local parts = {}
	if inst:IsA("BasePart") then
		table.insert(parts, inst)
	end
	for _, d in inst:GetDescendants() do
		if d:IsA("BasePart") then
			table.insert(parts, d)
		end
	end
	local anchor = if inst:IsA("BasePart") then inst else (inst.PrimaryPart or parts[1])
	if not anchor then
		warn("[FactoryRaid] 파트 없는 상자: " .. inst:GetFullName())
		return
	end
	local saved = {}
	local tier = ShopRaidLogic.rollTier(SR, rng)
	setTier(inst, tier)
	inst:SetAttribute("CrateOpen", false)
	CollectionService:AddTag(inst, TAG)
	local prompt = makePrompt(anchor, tier, CrateConfig.HOLD_DURATION)
	local entry = { inst = inst, anchor = anchor, open = false, spawned = false, guards = {}, idleSince = nil }
	table.insert(fixedCrates, entry)

	prompt.Triggered:Connect(function(player)
		if not prompt.Enabled then
			return
		end
		prompt.Enabled = false
		entry.open = true
		grant(player, tier, anchor.Position)
		inst:SetAttribute("CrateOpen", true)
		for _, p in parts do
			saved[p] = { p.Transparency, p.CanCollide }
			p.Transparency, p.CanCollide = 1, false
		end
		task.delay(inst:GetAttribute("RespawnTime") or CrateConfig.DEFAULT_RESPAWN_TIME, function()
			if not inst.Parent then
				return
			end
			for p, s in saved do
				p.Transparency, p.CanCollide = s[1], s[2]
			end
			tier = ShopRaidLogic.rollTier(SR, rng) -- 다시 채워질 때마다 새 등급
			setTier(inst, tier)
			prompt.ObjectText = tier .. " Crate"
			inst:SetAttribute("CrateOpen", false)
			entry.open, entry.spawned = false, false -- 새 등급 경비가 다시 나올 수 있게
			prompt.Enabled = true
		end)
	end)
end

---------------------------------------------------------------- 습격 지점

local sites = {}
local readyAt = {}
local busy = {}

local function ignoreList(): { Instance }
	local list = { workspace.Enemies, workspace.Drops }
	for _, p in Players:GetPlayers() do
		if p.Character then
			table.insert(list, p.Character)
		end
	end
	for _, s in sites do
		table.insert(list, s)
	end
	return list
end

-- 지점 근처 빈 바닥 찾기 (위에서 아래로 광선, 평평하고 주변에 부딪히는 것이 없는 곳)
local function findSpot(center: Vector3, taken: { Vector3 }): CFrame?
	local rp = RaycastParams.new()
	rp.FilterType = Enum.RaycastFilterType.Exclude
	rp.FilterDescendantsInstances = ignoreList()
	local op = OverlapParams.new()
	op.FilterType = Enum.RaycastFilterType.Exclude
	for _ = 1, 30 do
		local a, r = rng:NextNumber(0, math.pi * 2), rng:NextNumber(3, SITE_RADIUS)
		local from = center + Vector3.new(math.cos(a) * r, 6, math.sin(a) * r)
		local hit = workspace:Raycast(from, Vector3.new(0, -14, 0), rp)
		if hit and hit.Normal.Y > 0.9 and math.abs(hit.Position.Y - center.Y) < 4 then
			local ok = true
			for _, t in taken do
				if (t - hit.Position).Magnitude < 5 then
					ok = false
					break
				end
			end
			if ok then
				local cf = CFrame.new(hit.Position) * CFrame.Angles(0, rng:NextNumber(0, math.pi * 2), 0)
				op.FilterDescendantsInstances = { hit.Instance, table.unpack(ignoreList()) }
				for _, h in workspace:GetPartBoundsInBox(cf * CFrame.new(0, 2.3, 0), Vector3.new(4.5, 4, 4.5), op) do
					if h.CanCollide then
						ok = false
						break
					end
				end
				if ok then
					return cf
				end
			end
		end
	end
	return nil
end

local function runSite(site: BasePart, tier: string)
	local t = SR.TIERS[tier]
	busy[site] = true
	readyAt[site] = math.huge
	local made = {} -- 닫힐 때 지울 것
	local crates = {}
	local enemies = {}
	local ok, err = pcall(function()
		local center = site.Position
		-- 등급 빛 (지점 위)
		local holder = Instance.new("Part")
		holder.Name, holder.Anchored, holder.CanCollide, holder.CanQuery, holder.CanTouch = "FactoryRaidLight", true, false, false, false
		holder.Transparency, holder.Size, holder.Position = 1, Vector3.one, center + Vector3.new(0, 9, 0)
		local light = Instance.new("PointLight")
		light.Color, light.Brightness, light.Range, light.Shadows = t.light, 2.2, 30, false
		light.Parent = holder
		holder.Parent = workspace
		table.insert(made, holder)
		-- Legendary: 하늘로 솟는 빛기둥
		if t.beam then
			local base = Instance.new("Part")
			base.Name, base.Anchored, base.CanCollide, base.CanQuery, base.CanTouch = "FactoryRaidBeam", true, false, false, false
			base.Transparency, base.Size, base.Position = 1, Vector3.one, center + Vector3.new(0, 1, 0)
			local a0, a1 = Instance.new("Attachment"), Instance.new("Attachment")
			a1.Position = Vector3.new(0, 500, 0)
			a0.Parent, a1.Parent = base, base
			local beam = Instance.new("Beam")
			beam.Attachment0, beam.Attachment1 = a0, a1
			beam.Width0, beam.Width1, beam.LightEmission, beam.FaceCamera = 6, 10, 1, true
			beam.Color = ColorSequence.new(t.light)
			beam.Transparency = NumberSequence.new({ NumberSequenceKeypoint.new(0, 0.15), NumberSequenceKeypoint.new(1, 1) })
			beam.Parent = base
			base.Parent = workspace
			table.insert(made, base)
		end
		-- 등급 상자
		local kit = Kits.get("FurnitureKit").Loot_SupplyStack
		local taken = {}
		for _ = 1, t.crates do
			local cf = findSpot(center, taken)
			if cf then
				table.insert(taken, cf.Position)
				local crate = kit:Clone()
				crate.Name = tier .. "Crate"
				crate:PivotTo(cf)
				local anchor
				for _, p in crate:GetDescendants() do
					if p:IsA("BasePart") then
						anchor = anchor or p
						p.Anchored = true
						if p.Name:find("_Metal$") then
							p.Color, p.Material = t.light, Enum.Material.Neon -- 묶은 끈이 등급 색으로 빛남 (상가와 같음)
						end
					end
				end
				local glow = Instance.new("PointLight")
				glow.Color, glow.Brightness, glow.Range = t.light, 1.2, 10
				glow.Parent = anchor
				setTier(crate, tier)
				CollectionService:AddTag(crate, TAG)
				local prompt = makePrompt(anchor, tier, SR.HOLD_DURATION)
				prompt.Triggered:Connect(function(player)
					if not prompt.Enabled then
						return
					end
					prompt.Enabled = false
					grant(player, tier, anchor.Position)
					crate:Destroy()
				end)
				crate.Parent = workspace
				table.insert(crates, crate)
			end
		end
		-- 등급만큼 적
		local count = RAID_ENEMIES[tier] or t.enemies
		for kind, n in enemyKinds(site:GetAttribute("EnemyId"), count) do
			if n > 0 then
				for _, m in EnemyService.spawnTemporary(kind, center, n, ENEMY_SCATTER) do
					table.insert(enemies, m)
				end
			end
		end
		if t.announce then
			for _, player in Players:GetPlayers() do
				notify(player, ("A %s cache is glowing in the steelworks!"):format(tier), t.light, "good")
			end
		end
		-- 경고 → 닫기
		task.wait(math.max(0, t.duration - SR.WARNING_TIME))
		for _, player in Players:GetPlayers() do
			local root = player.Character and player.Character:FindFirstChild("HumanoidRootPart")
			if root and (root.Position - center).Magnitude < NOTIFY_RANGE then
				notify(player, ("The %s cache fades in %d seconds!"):format(tier, SR.WARNING_TIME), t.light, "warn")
			end
		end
		local deadline = os.clock() + SR.WARNING_TIME
		local on = true
		while os.clock() < deadline do
			on = not on
			light.Brightness = on and 2.2 or 0.35
			task.wait(on and 0.35 or 0.15)
		end
	end)
	if not ok then
		warn(("[FactoryRaid] %s 습격 실패: %s"):format(site.Name, tostring(err)))
	end
	-- 정리
	for _, c in crates do
		if c.Parent then
			c:Destroy()
		end
	end
	for _, m in made do
		m:Destroy()
	end
	for _, model in enemies do
		local hum = model.Parent and model:FindFirstChildOfClass("Humanoid")
		local root = model:FindFirstChild("HumanoidRootPart")
		if hum and hum.Health > 0 and root then
			local near = false
			for _, player in Players:GetPlayers() do
				local pr = player.Character and player.Character:FindFirstChild("HumanoidRootPart")
				if pr and (pr.Position - root.Position).Magnitude < ENEMY_KEEP_RANGE then
					near = true
					break
				end
			end
			if not near then
				model:Destroy()
			end
		end
	end
	busy[site] = nil
	readyAt[site] = os.clock() + SR.REOPEN_COOLDOWN
end

local FactoryRaid = {}

function FactoryRaid.startWave(forceTier: string?): number
	local now = os.clock()
	local picked = ShopRaidLogic.pickShops(sites, SITES_PER_WAVE, function(site)
		return not busy[site] and (readyAt[site] or 0) <= now
	end, rng)
	local best = 0
	for _, site in picked do
		local tier = if forceTier and SR.TIERS[forceTier] then forceTier else ShopRaidLogic.rollTier(SR, rng)
		best = math.max(best, table.find(SR.ORDER, tier) or 1)
		task.spawn(runSite, site, tier)
		task.wait(SR.OPEN_STAGGER)
	end
	if #picked > 0 then
		for _, player in Players:GetPlayers() do
			notify(player, "Caches are glowing across the steelworks.", SR.TIERS[SR.ORDER[best]].light)
		end
	end
	return #picked
end

-- 고정 상자
for _, d in workspace:GetDescendants() do
	if type(d:GetAttribute("FactoryCrate")) == "string" then
		task.spawn(registerFixed, d)
	end
end

-- 습격 지점 (편집할 때만 보이고 게임 중에는 숨김)
local folder = workspace:FindFirstChild("FactoryRaidSites", true)
if folder then
	for _, p in folder:GetChildren() do
		if p:IsA("BasePart") and p:GetAttribute("EnemyId") then
			p.Transparency, p.CanCollide, p.CanQuery, p.CanTouch = 1, false, false, false
			table.insert(sites, p)
		end
	end
end
print(("[FactoryRaid] 습격 지점 %d곳"):format(#sites))

---------------------------------------------------------------- 고정 상자 경비

local bossPoint = nil
do
	local spawns = workspace:FindFirstChild("EnemySpawns", true)
	for _, p in spawns and spawns:GetChildren() or {} do
		if p:IsA("BasePart") and p:GetAttribute("EnemyId") == "foreman" then
			bossPoint = p.Position
		end
	end
end

-- 상자 근처 습격 지점의 적 종류 (구역마다 다른 몬스터), 없으면 기본
local function guardKind(pos: Vector3): string
	local best, bestD = GUARD_DEFAULT, 160
	for _, s in sites do
		local d = (s.Position - pos).Magnitude
		if d < bestD then
			best, bestD = s:GetAttribute("EnemyId"), d
		end
	end
	return best
end

-- 상자 둘레 바닥 (높은 곳 상자면 그 아래 땅에 서도 됨)
local function guardSpot(center: Vector3): Vector3?
	local rp = RaycastParams.new()
	rp.FilterType = Enum.RaycastFilterType.Exclude
	rp.FilterDescendantsInstances = ignoreList()
	local op = OverlapParams.new()
	op.FilterType = Enum.RaycastFilterType.Exclude
	for _ = 1, 20 do
		local a, r = rng:NextNumber(0, math.pi * 2), rng:NextNumber(GUARD_RING[1], GUARD_RING[2])
		local hit = workspace:Raycast(center + Vector3.new(math.cos(a) * r, 6, math.sin(a) * r), Vector3.new(0, -60, 0), rp)
		if hit and hit.Normal.Y > 0.8 then
			op.FilterDescendantsInstances = { hit.Instance, table.unpack(ignoreList()) }
			local blocked = false
			for _, h in workspace:GetPartBoundsInBox(CFrame.new(hit.Position + Vector3.new(0, 3.5, 0)), Vector3.new(3, 5, 3), op) do
				if h.CanCollide then
					blocked = true
					break
				end
			end
			if not blocked then
				return hit.Position
			end
		end
	end
	return nil
end

local function aliveGuards(entry): { Model }
	local alive = {}
	for _, m in entry.guards do
		local hum = m.Parent and m:FindFirstChildOfClass("Humanoid")
		if hum and hum.Health > 0 then
			table.insert(alive, m)
		end
	end
	entry.guards = alive
	return alive
end

local function nearestPlayer(pos: Vector3): number
	local best = math.huge
	for _, player in Players:GetPlayers() do
		local root = player.Character and player.Character:FindFirstChild("HumanoidRootPart")
		local hum = player.Character and player.Character:FindFirstChildOfClass("Humanoid")
		if root and hum and hum.Health > 0 then
			best = math.min(best, (root.Position - pos).Magnitude)
		end
	end
	return best
end

task.spawn(function()
	task.wait(5) -- registerFixed 가 다 끝나게
	for _, entry in fixedCrates do
		local pos = entry.anchor.Position
		entry.kind = guardKind(pos)
		entry.skip = bossPoint ~= nil and (pos - bossPoint).Magnitude < GUARD_SKIP_NEAR_BOSS
	end
	while true do
		for _, entry in fixedCrates do
			if entry.skip or not entry.inst.Parent then
				continue
			end
			local pos = entry.anchor.Position
			local d = nearestPlayer(pos)
			local alive = aliveGuards(entry)
			if not entry.open and not entry.spawned and d <= GUARD_WAKE then
				entry.spawned = true
				local want = (GUARD_COUNT[entry.inst:GetAttribute("CrateTier")] or 2) - #alive
				for kind, n in enemyKinds(entry.kind, math.max(0, want)) do
					for _ = 1, n do
						local at = guardSpot(pos)
						if at then
							for _, m in EnemyService.spawnTemporary(kind, at, 1, 0) do
								table.insert(entry.guards, m)
							end
						end
					end
				end
				entry.idleSince = nil
			elseif d > GUARD_SLEEP and #alive > 0 then
				entry.idleSince = entry.idleSince or os.clock()
				if os.clock() - entry.idleSince > GUARD_IDLE then
					for _, m in alive do
						m:Destroy()
					end
					entry.guards = {}
					entry.spawned = false -- 다시 다가오면 또 나옴 (상자가 아직 안 열렸으면)
					entry.idleSince = nil
				end
			else
				entry.idleSince = nil
			end
		end
		task.wait(1)
	end
end)
_G.FactoryRaid = FactoryRaid -- 개발용: 서버 콘솔에서 _G.FactoryRaid.startWave("Legendary")

if #sites > 0 then
	task.spawn(function()
		task.wait(SR.FIRST_WAVE_DELAY)
		while true do
			local ok, err = pcall(FactoryRaid.startWave)
			if not ok then
				warn("[FactoryRaid] 웨이브 실패: " .. tostring(err))
			end
			task.wait(SR.WAVE_INTERVAL)
		end
	end)
end
