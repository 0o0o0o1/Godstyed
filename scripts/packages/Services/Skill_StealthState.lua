--!strict
-- 은신 상태 (Skills kind "stealth", 은신 Vanish). ParryState 처럼 Skill 밑에 두고 EnemyAI·DamageDealer·Combat·Skill 이 같이 씀
-- (Enemy → Skill 순환 require 없이).
--   begin(player, character, skill, at?) 분신을 at(시전 자리, 없으면 지금 자리)에 세우고 은신 시작 (Skill 서비스가 castDelay 뒤 호출, 그사이 내 몸은 대시로 떠남)
--   finish(player, reason)            끝: "timeout" | "attack"(기본 공격) | "skill"(다른 스킬) | "hit"(피격) | "death" | "refresh"
--                                     "attack"·"skill" 이면 ambushWindow 동안 준 피해 × ambushMult (DamageDealer 가 ambushMult 로 물음)
--   redirect(player) -> (분신 몸통?, 은신 중?)  EnemyAI: 은신 중인 플레이어 대신 분신을 쫓게 (분신이 없으면 못 찾음)
--   decoyOwner(model) -> Player?      그 모델이 분신이면 주인. popDecoy(player): 분신만 연기로 사라짐 (은신은 계속)
-- 캐릭터 속성: Stealthed(클라이언트가 보고 숨김) / StealthSpeedMult(Movement·AttackSlow 가 이동 속도에 곱함)
-- 연출은 setHandler 로 Skill 서비스가 보냄 ("decoy" = 분신 사라짐, "end" = 은신 끝)

local Players = game:GetService("Players")

export type Entry = {
	token: {},
	character: Model,
	skill: any,
	decoy: Model?,
	conns: { RBXScriptConnection },
}

local StealthState = {}

local active: { [Player]: Entry } = {}
local decoys: { [Model]: Player } = {}
local ambush: { [Player]: { untilTime: number, mult: number } } = {}
local handler: ((player: Player, event: string, data: { [string]: any }) -> ())? = nil

local function folder(): Folder
	local f = workspace:FindFirstChild("StealthDecoys")
	if not f then
		f = Instance.new("Folder")
		f.Name = "StealthDecoys"
		f.Parent = workspace
	end
	return f :: Folder
end

local function notify(player: Player, event: string, data: { [string]: any })
	if handler then
		local ok, err = pcall(handler, player, event, data)
		if not ok then
			warn(("[StealthState] 연출 오류: %s"):format(tostring(err)))
		end
	end
end

function StealthState.setHandler(fn: (player: Player, event: string, data: { [string]: any }) -> ())
	handler = fn
end

function StealthState.isStealthed(player: Player): boolean
	return active[player] ~= nil
end

-- 분신: 내 캐릭터 복제, 가만히 선 기본 자세(관절 Transform 은 복제되지 않아 쉬는 자세), 발은 바닥에.
-- Humanoid 는 옷·이름표 때문에 두고 상태 기계만 끔. 누구든 피해를 주면(체력이 줄면) 연기로 사라짐
local function makeDecoy(player: Player, character: Model, at: CFrame?): Model?
	local root = character:FindFirstChild("HumanoidRootPart") :: BasePart?
	local humanoid = character:FindFirstChildOfClass("Humanoid")
	if not (root and humanoid) then
		return nil
	end
	local was = character.Archivable
	character.Archivable = true
	local ok, made = pcall(function()
		return character:Clone()
	end)
	character.Archivable = was
	if not ok or not made then
		return nil
	end
	local clone = made :: Model
	clone.Name = character.Name .. "_Decoy"
	for name in clone:GetAttributes() do
		clone:SetAttribute(name, nil)
	end
	for _, d in clone:GetDescendants() do
		if d:IsA("BaseScript") or d:IsA("ModuleScript") or d:IsA("Sound") or d:IsA("ForceField") or d:IsA("Highlight")
			or d:IsA("LinearVelocity") or d:IsA("AlignPosition") or d:IsA("AlignOrientation") or d:IsA("BodyMover") then
			d:Destroy()
		elseif d:IsA("BasePart") then
			d.CanCollide = false
			d.CanTouch = false
			d.Anchored = false
			d.Massless = true
		end
	end
	local cloneRoot = clone:FindFirstChild("HumanoidRootPart") :: BasePart?
	local cloneHumanoid = clone:FindFirstChildOfClass("Humanoid")
	if not (cloneRoot and cloneHumanoid) then
		clone:Destroy()
		return nil
	end
	cloneRoot.Anchored = true
	cloneHumanoid.EvaluateStateMachine = false
	cloneHumanoid.PlatformStand = true
	cloneHumanoid.AutoRotate = false
	cloneHumanoid.BreakJointsOnDeath = false
	cloneHumanoid.MaxHealth = 100
	cloneHumanoid.Health = 100
	-- 바닥에 서 있게 (점프 중에 써도)
	local from = at or root.CFrame
	local look = from.LookVector
	local flat = Vector3.new(look.X, 0, look.Z)
	if flat.Magnitude < 1e-3 then
		flat = Vector3.zAxis
	end
	local pos = from.Position
	local params = RaycastParams.new()
	params.FilterType = Enum.RaycastFilterType.Exclude
	params.RespectCanCollide = true
	local ignore: { Instance } = { folder() }
	for _, p in Players:GetPlayers() do
		if p.Character then
			table.insert(ignore, p.Character)
		end
	end
	local enemies = workspace:FindFirstChild("Enemies")
	if enemies then
		table.insert(ignore, enemies)
	end
	params.FilterDescendantsInstances = ignore
	local hit = workspace:Raycast(pos + Vector3.new(0, 2, 0), Vector3.new(0, -40, 0), params)
	if hit then
		pos = Vector3.new(pos.X, hit.Position.Y + humanoid.HipHeight + root.Size.Y / 2, pos.Z)
	end
	clone:PivotTo(CFrame.lookAt(pos, pos + flat.Unit))
	clone.Parent = folder()
	decoys[clone] = player
	local last = cloneHumanoid.Health
	cloneHumanoid.HealthChanged:Connect(function(health)
		if health < last and decoys[clone] then
			StealthState.popDecoy(decoys[clone])
		end
		last = health
	end)
	return clone
end

local function removeDecoy(player: Player, entry: Entry, reason: string)
	local decoy = entry.decoy
	entry.decoy = nil
	if not decoy then
		return
	end
	decoys[decoy] = nil
	local at = if decoy.Parent then decoy:GetPivot() else nil
	decoy:Destroy()
	if at then
		notify(player, "decoy", { origin = at, reason = reason, character = entry.character, skill = entry.skill })
	end
end

function StealthState.begin(player: Player, character: Model, skill: any, at: CFrame?)
	if active[player] then
		StealthState.finish(player, "refresh")
	end
	local humanoid = character:FindFirstChildOfClass("Humanoid")
	if not humanoid or humanoid.Health <= 0 or character ~= player.Character then
		return
	end
	local token = {}
	local entry: Entry = { token = token, character = character, skill = skill, decoy = nil, conns = {} }
	active[player] = entry
	entry.decoy = makeDecoy(player, character, at)
	character:SetAttribute("Stealthed", true)
	character:SetAttribute("StealthSpeedMult", 1 + (skill.speedBoost or 0))
	-- 맞으면 끊김 (사용자 결정), 죽으면 끝
	local last = humanoid.Health
	table.insert(entry.conns, humanoid.HealthChanged:Connect(function(health)
		if health <= 0 then
			StealthState.finish(player, "death")
		elseif health < last - 0.01 then
			StealthState.finish(player, "hit")
		end
		last = health
	end))
	table.insert(entry.conns, character.AncestryChanged:Connect(function()
		if not character:IsDescendantOf(workspace) then
			StealthState.finish(player, "death")
		end
	end))
	task.delay(skill.duration or 4, function()
		local e = active[player]
		if e and e.token == token then
			StealthState.finish(player, "timeout")
		end
	end)
end

function StealthState.finish(player: Player, reason: string)
	local entry = active[player]
	if not entry then
		return
	end
	active[player] = nil
	for _, c in entry.conns do
		c:Disconnect()
	end
	removeDecoy(player, entry, reason)
	local character = entry.character
	if character.Parent then
		character:SetAttribute("Stealthed", nil)
		character:SetAttribute("StealthSpeedMult", nil)
	end
	if reason == "attack" or reason == "skill" then
		ambush[player] = { untilTime = os.clock() + (entry.skill.ambushWindow or 1), mult = entry.skill.ambushMult or 1 }
	end
	notify(player, "end", { reason = reason, character = character, skill = entry.skill })
end

-- 분신만 사라짐 (맞음). 은신은 계속
function StealthState.popDecoy(player: Player)
	local entry = active[player]
	if entry then
		removeDecoy(player, entry, "hit")
	end
end

function StealthState.redirect(player: Player): (BasePart?, boolean)
	local entry = active[player]
	if not entry then
		return nil, false
	end
	local decoy = entry.decoy
	local root = decoy and decoy.Parent and decoy:FindFirstChild("HumanoidRootPart") :: BasePart?
	return root, true
end

function StealthState.decoyOwner(model: Instance?): Player?
	return if model and model:IsA("Model") then decoys[model] else nil
end

-- 끊은 공격의 피해 배율 (없으면 1)
function StealthState.ambushMult(player: Player): number
	local a = ambush[player]
	if not a then
		return 1
	end
	if os.clock() > a.untilTime then
		ambush[player] = nil
		return 1
	end
	return a.mult
end

function StealthState.clear(player: Player)
	StealthState.finish(player, "death")
	ambush[player] = nil
end

return StealthState
