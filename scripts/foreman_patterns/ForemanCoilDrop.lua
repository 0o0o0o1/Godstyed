--!nonstrict
-- 패턴 (Foreman 전용, 분노): 짐 낙하. 갈고리로 땅을 내리치면(windup) 천장 크레인에 걸려 있던 강철 코일들이 떨어진다
-- 범위(area) 안의 플레이어마다 하나는 발밑에, 나머지는 보스 주변에 흩어진다 (모두 count개). 떨어질 자리에 원(warn초)이 표시되고
-- 하나씩(stagger초 간격) 떨어져 radius 안의 플레이어에게 피해. 원 사이 빈칸으로 피한다
-- 떨어진 코일은 wallTime 동안 진짜 장애물(충돌)로 남는다. 끝나면 recover 빈틈 (Opening)
-- 수치: anim, windup, count, area, minDistance, radius, warn, stagger, damage, wallTime, recover
-- 소리: 모델 UpperTorso 의 Sound "CoilCrash" (ForemanFX 설치 스크립트)

local Players = game:GetService("Players")
local TweenService = game:GetService("TweenService")
local Debris = game:GetService("Debris")

local Telegraph = require(script.Parent.Parent.Telegraph)

local HEIGHT_TOLERANCE = 8
local IMPACT_MARKER_TIME = 0.8
local DROP_HEIGHT = 55
local DROP_TIME = 0.3

local tracks = setmetatable({}, { __mode = "k" })
local rng = Random.new()

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

-- 강철 코일: 옆으로 누운 두꺼운 원통 + 가운데 구멍(어두운 원통) + 묶음 띠 2개
local function makeCoil(radius: number): Model
	local m = Instance.new("Model")
	m.Name = "ForemanSteelCoil"
	local len = radius * 1.1
	local outer = Instance.new("Part")
	outer.Name = "Coil"
	outer.Shape = Enum.PartType.Cylinder
	outer.Size = Vector3.new(len, radius * 1.6, radius * 1.6)
	outer.Material = Enum.Material.Metal
	outer.Color = Color3.fromRGB(118, 116, 112)
	outer.Anchored = true
	outer.CanCollide = true
	outer.CanQuery = false
	outer.CanTouch = false
	outer.Parent = m
	local hole = Instance.new("Part")
	hole.Name = "Hole"
	hole.Shape = Enum.PartType.Cylinder
	hole.Size = Vector3.new(len + 0.05, radius * 0.55, radius * 0.55)
	hole.Material = Enum.Material.SmoothPlastic
	hole.Color = Color3.fromRGB(18, 17, 16)
	hole.Anchored = true
	hole.CanCollide = false
	hole.CanQuery = false
	hole.CanTouch = false
	hole.Parent = m
	for _, x in { -len * 0.28, len * 0.28 } do
		local band = Instance.new("Part")
		band.Name = "Band"
		band.Shape = Enum.PartType.Cylinder
		band.Size = Vector3.new(0.25, radius * 1.64, radius * 1.64)
		band.Material = Enum.Material.CorrodedMetal
		band.Color = Color3.fromRGB(90, 55, 35)
		band.Anchored = true
		band.CanCollide = false
		band.CanQuery = false
		band.CanTouch = false
		band:SetAttribute("Offset", x)
		band.Parent = m
	end
	m.PrimaryPart = outer
	return m
end

local function placeCoil(m: Model, cf: CFrame)
	for _, p in m:GetChildren() do
		local x = p:GetAttribute("Offset") or 0
		p.CFrame = cf * CFrame.new(x, 0, 0)
	end
end

return {
	run = function(ctx, targetRoot: BasePart, p)
		local root, model = ctx.root, ctx.model
		ctx.stop()
		ctx.face(targetRoot.Position)
		ctx.setGearState("Attacking", true)
		local track = anim(ctx, p.anim)
		if track then
			track:Play(0.1, 1, IMPACT_MARKER_TIME / p.windup)
		end
		task.wait(p.windup)
		ctx.setGearState("Attacking", false)
		if not ctx.alive() then
			return
		end

		-- 떨어질 자리: 범위 안의 플레이어 발밑 먼저, 나머지는 보스 주변
		local center = root.Position
		local spots = {}
		for _, player in Players:GetPlayers() do
			local hrp = player.Character and player.Character:FindFirstChild("HumanoidRootPart")
			local hum = player.Character and player.Character:FindFirstChildOfClass("Humanoid")
			if hrp and hum and hum.Health > 0 and (hrp.Position - center).Magnitude <= p.area and #spots < p.count then
				table.insert(spots, hrp.Position)
			end
		end
		local tries = 0
		while #spots < p.count and tries < 60 do
			tries += 1
			local a = rng:NextNumber(0, math.pi * 2)
			local r = rng:NextNumber(p.minDistance or 8, p.area)
			local s = center + Vector3.new(math.cos(a) * r, 0, math.sin(a) * r)
			local ok = true
			for _, q in spots do
				if Vector3.new(s.X - q.X, 0, s.Z - q.Z).Magnitude < p.radius * 2.2 then
					ok = false
					break
				end
			end
			if ok then
				table.insert(spots, s)
			end
		end

		local remaining = #spots
		for i, s in spots do
			local ground = Telegraph.ground(model, s)
			task.delay((i - 1) * p.stagger, function()
				local done = Telegraph.circle(ground, p.radius, p.warn, Color3.fromRGB(255, 170, 40))
				task.wait(p.warn - DROP_TIME)
				local coil = makeCoil(p.radius)
				local yaw = rng:NextNumber(0, math.pi * 2)
				local landed = CFrame.new(ground + Vector3.new(0, p.radius * 0.8, 0)) * CFrame.Angles(0, yaw, 0)
				local start = landed + Vector3.new(0, DROP_HEIGHT, 0)
				placeCoil(coil, start)
				coil.Parent = workspace
				local t0 = os.clock()
				while os.clock() - t0 < DROP_TIME do
					local a = (os.clock() - t0) / DROP_TIME
					placeCoil(coil, start:Lerp(landed, a * a))
					task.wait()
				end
				placeCoil(coil, landed)
				done(true)
				Telegraph.hit(model, function(r)
					local o = r.Position - ground
					return Vector3.new(o.X, 0, o.Z).Magnitude <= p.radius and math.abs(o.Y) <= HEIGHT_TOLERANCE
				end, p.damage)
				-- 먼지·소리
				local dust = Instance.new("ParticleEmitter")
				dust.Texture = "rbxasset://textures/particles/smoke_main.dds"
				dust.Color = ColorSequence.new(Color3.fromRGB(95, 88, 80), Color3.fromRGB(70, 65, 60))
				dust.Transparency = NumberSequence.new(0.5, 1)
				dust.Size = NumberSequence.new(1.5, 5)
				dust.Lifetime = NumberRange.new(0.8, 1.5)
				dust.Speed = NumberRange.new(6, 12)
				dust.SpreadAngle = Vector2.new(90, 20)
				dust.Drag = 3
				dust.Enabled = false
				dust.Parent = coil.PrimaryPart
				dust:Emit(25)
				local torso = model:FindFirstChild("UpperTorso")
				local src = torso and torso:FindFirstChild("CoilCrash")
				if src then
					local s2 = src:Clone()
					s2.PlaybackSpeed = rng:NextNumber(0.85, 1.05)
					s2.Parent = coil.PrimaryPart
					s2:Play()
				end
				-- wallTime 뒤 가라앉으며 사라짐
				task.delay(p.wallTime, function()
					for _, part in coil:GetChildren() do
						if part:IsA("BasePart") then
							part.CanCollide = false
							TweenService:Create(part, TweenInfo.new(1), { Transparency = 1 }):Play()
						end
					end
					Debris:AddItem(coil, 1.2)
				end)
				remaining -= 1
			end)
		end
		local t0 = os.clock()
		while remaining > 0 and os.clock() - t0 < #spots * p.stagger + p.warn + 1 do
			task.wait()
		end
		if not ctx.alive() then
			return
		end
		model:SetAttribute("Opening", true)
		task.wait(p.recover)
	end,
}
