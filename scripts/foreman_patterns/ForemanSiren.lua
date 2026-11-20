--!nonstrict
-- 패턴 (Foreman 전용, 2페이즈): 확성기 사이렌. 확성기를 앞으로 겨누고(windup) 앞 넓은 범위에 음파를 쏜다
-- 범위 안의 플레이어는 피해를 입는다(push 가 있으면 뒤로 밀려남 — 2026-11-21부터 정의에서 뺌, 밀치기는 ForemanShove). 옆이나 보스 뒤로 피한다
-- 높이 판정은 바닥 기준(보스 크기와 무관)
-- 사이렌 소리에 끌려 갇혀 있던 작업자들이 보스 사방(summonRadius, 벽이 있으면 벽 앞)에서 나온다: summons = { { id, count }, ... } (2026-11-21: 종류별 2마리씩 6마리)
-- 이 보스가 부른 졸개가 maxSummons 이상 살아 있으면 그만큼 덜 부른다. 실패하면 Output 에 [ForemanSiren] 경고
-- 울리는 동안 모델 속성 Siren = true (ForemanFX 가 음파 효과·소리), 끝나면 recover 빈틈 (Opening)
-- 확성기가 떨어져 나가면(분노, breakParts) 이 패턴은 쓰지 않는다 (정의의 maxPhase = 2)
-- 수치: anim, windup, length, width, damage, push?, blare, summons, summonRadius, maxSummons, recover

local Debris = game:GetService("Debris")

local Telegraph = require(script.Parent.Parent.Telegraph)

local HEIGHT_TOLERANCE = 9
local SIREN_MARKER_TIME = 0.9

local tracks = setmetatable({}, { __mode = "k" })
local summons = setmetatable({}, { __mode = "k" }) -- [보스 모델] = { 졸개 모델 }

local function anim(ctx, id: string?)
	if not id then
		return nil
	end
	local cache = tracks[ctx.humanoid]
	if not cache then
		cache = {}
		tracks[ctx.humanoid] = cache
	end
	if not cache[id] then
		local animator = ctx.humanoid:FindFirstChildOfClass("Animator")
		if not animator then
			return nil
		end
		local a = Instance.new("Animation")
		a.AnimationId = id
		local t = animator:LoadAnimation(a)
		t.Priority = Enum.AnimationPriority.Action
		t.Looped = false
		cache[id] = t
	end
	return cache[id]
end

local function flat(v: Vector3): Vector3
	local f = Vector3.new(v.X, 0, v.Z)
	return if f.Magnitude > 0.01 then f.Unit else Vector3.zAxis
end

local function shove(player: Player, velocity: Vector3, duration: number)
	local character = player.Character
	local hrp = character and character:FindFirstChild("HumanoidRootPart")
	if not hrp then
		return
	end
	local att = Instance.new("Attachment")
	att.Name = "ForemanShove"
	att.Parent = hrp
	local lv = Instance.new("LinearVelocity")
	lv.Name = "ForemanShove"
	lv.Attachment0 = att
	lv.RelativeTo = Enum.ActuatorRelativeTo.World
	lv.VelocityConstraintMode = Enum.VelocityConstraintMode.Vector
	lv.MaxForce = 4e5
	lv.VectorVelocity = velocity
	lv.Parent = hrp
	Debris:AddItem(lv, duration)
	Debris:AddItem(att, duration)
end

local function aliveSummons(model: Model): number
	local list = summons[model]
	if not list then
		return 0
	end
	local n = 0
	for i = #list, 1, -1 do
		local m = list[i]
		local h = m.Parent and m:FindFirstChildOfClass("Humanoid")
		if h and h.Health > 0 then
			n += 1
		else
			table.remove(list, i)
		end
	end
	return n
end

return {
	run = function(ctx, targetRoot: BasePart, p)
		local root, model = ctx.root, ctx.model
		if not model:FindFirstChild("LeftHand__Mega") or model.LeftHand__Mega.Transparency >= 1 then
			return -- 확성기가 떨어져 나갔으면 못 씀
		end
		ctx.stop()
		ctx.face(targetRoot.Position)
		ctx.setGearState("Attacking", true)
		local track = anim(ctx, p.anim)
		if track then
			track:Play(0.1, 1, SIREN_MARKER_TIME / p.windup)
		end
		local g = Telegraph.ground(model, root.Position)
		local dir = flat(root.CFrame.LookVector)
		local lane = Telegraph.lane(CFrame.lookAt(g, g + dir), p.length, p.width, p.windup)
		task.wait(p.windup)
		if not ctx.alive() then
			lane.done(false)
			ctx.setGearState("Attacking", false)
			return
		end
		lane.done(true)
		model:SetAttribute("Siren", true)

		local origin = root.Position
		local got = Telegraph.hit(model, function(r)
			local o = r.Position - origin
			local along = o:Dot(dir)
			local side = o - dir * along
			return along > -1 and along <= p.length and Vector3.new(side.X, 0, side.Z).Magnitude <= p.width / 2
				and r.Position.Y - g.Y <= HEIGHT_TOLERANCE and r.Position.Y - g.Y >= -3
		end, p.damage)
		for _, pl in (if p.push and p.push > 0 then got else {}) do
			local hrp = pl.Character and pl.Character:FindFirstChild("HumanoidRootPart")
			if hrp then
				local away = flat(hrp.Position - origin)
				shove(pl, (away * 0.6 + dir * 0.4).Unit * p.push + Vector3.new(0, 18, 0), 0.3)
			end
		end

		-- 졸개 부르기: 종류를 섞어 보스 둘레에 고르게 (Enemy 서비스는 순환 참조를 피하려고 여기서 불러온다)
		local room = (p.maxSummons or 6) - aliveSummons(model)
		local queue = {}
		local longest = 0
		for _, s in p.summons or {} do
			longest = math.max(longest, s.count or 0)
		end
		for i = 1, longest do -- slag, molten, hook, slag, molten, hook 순서
			for _, s in p.summons or {} do
				if i <= (s.count or 0) then
					table.insert(queue, s.id)
				end
			end
		end
		while #queue > room do
			table.remove(queue)
		end
		if #queue > 0 then
			local ok, Enemy = pcall(require, script.Parent.Parent.Parent)
			if not ok or type(Enemy) ~= "table" or not Enemy.spawnTemporary then
				warn("[ForemanSiren] Enemy 서비스를 못 불러옴: " .. tostring(Enemy))
			else
				local params = RaycastParams.new()
				params.FilterType = Enum.RaycastFilterType.Exclude
				local ignore = { model }
				local enemies = workspace:FindFirstChild("Enemies")
				if enemies then
					table.insert(ignore, enemies)
				end
				params.FilterDescendantsInstances = ignore
				params.RespectCanCollide = true
				local base = math.random() * math.pi * 2
				local radius = p.summonRadius or 18
				summons[model] = summons[model] or {}
				for i, id in queue do
					local a = base + (i - 1) / #queue * math.pi * 2
					local out = Vector3.new(math.cos(a), 0, math.sin(a))
					local from = g + Vector3.new(0, 3, 0)
					local hit = workspace:Raycast(from, out * radius, params)
					local dist = if hit then math.max(4, hit.Distance - 3) else radius
					local at = Telegraph.ground(model, from + out * dist)
					local made = Enemy.spawnTemporary(id, at, 1, 0)
					if #made == 0 then
						warn(("[ForemanSiren] 소환 실패: %s"):format(id))
					end
					for _, m in made do
						m:SetAttribute("SummonedBy", model.Name)
						table.insert(summons[model], m)
					end
				end
			end
		end

		task.wait(p.blare)
		model:SetAttribute("Siren", nil)
		ctx.setGearState("Attacking", false)
		if not ctx.alive() then
			return
		end
		model:SetAttribute("Opening", true)
		task.wait(p.recover)
	end,
}
