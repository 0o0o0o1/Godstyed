--!nonstrict
-- 공장 몬스터 위험 능력 (공장 place 전용 Script: ServerScriptService.FactoryHazards, 공용 패키지 밖)
-- 원본: 저장소 scripts/factory_hazards.server.lua
--
-- 1) Molten Walker(molten_walker, 갓 굳은 용암 몬스터): 주변 HEAT_RADIUS 안 플레이어에게 1초마다 화염 스택 +1 (최대 10).
--    범위 안 마리 수만큼 한 번에 쌓임 (3마리면 1초에 +3). 범위 밖이면 1초마다 −1, 열기를 5초 동안 안 받으면 전부 사라짐.
--    화염 스택마다 초당 1 피해 (1~10스택 = 초당 1~10).
--    스택은 캐릭터 속성 FireStacks → 클라이언트 FactoryFireHud 가 표시. 몬스터 발밑에 범위 원(HeatRing).
-- 2) Slag Walker(slag_walker, 식은 검은 몬스터): 체력이 75% 아래로 내려가면 균열 빛이 세지고 노랗게 변함(10%에서 최대),
--    30% 아래면 깜빡임 + 불티·연기 증가 → 폭발 예고. 죽으면 범위 원이 BURST_DELAY 초 번쩍이고 암석 폭발,
--    HEAT_RADIUS 안 플레이어에게 BURST_DAMAGE 피해.
-- 3) Hook Hauler(hook_hauler, 실내): 등의 갈고리가 약점 — 앞에서 맞으면 피해 50%, 등 뒤에서 맞으면 150% + 갈고리 불티·쇳소리.
-- 피해는 적 기본 공격과 같은 방식: Humanoid:TakeDamage(피해 × DamageTaken(캐릭터)), LastHitBy 기록 (ForceField 면 막힘)

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local TweenService = game:GetService("TweenService")

local HEAT_RADIUS = 14
local MAX_STACKS = 10
local DAMAGE_PER_STACK = 1
local CLEAR_AFTER = 5 -- 열기를 이 시간(초) 동안 안 받으면 스택 전부 사라짐 (그 전에는 1초마다 −1)
local BURST_DAMAGE = 30
local BURST_DELAY = 0.35 -- 범위를 잠깐 보여 주고 터지는 시간
-- Slag Walker 균열: 체력이 CRACK_START 아래로 내려가면 균열 빛이 세지고(CRACK_FULL 에서 최대), CRACK_PULSE 아래면 깜빡임
local CRACK_START = 0.75
local CRACK_FULL = 0.1
local CRACK_PULSE = 0.3
local CRACK_STRENGTH = { 2.5, 10 } -- 균열 발광 세기 (평소 → 최대)
local CRACK_TINT = { Color3.fromRGB(255, 120, 40), Color3.fromRGB(255, 215, 130) }
local HEAT_COLOR = Color3.fromRGB(255, 120, 35)
-- 폭발 소리: Slag Walker 모델에 이미 있는 소리 (SlagFX 가 미리 불러옴). Impact = 곤봉 내려치기 쿵, HitSizzle = 피격 지글거림
local BURST_SOUNDS = {
	{ id = "rbxassetid://9118617342", volume = 0.9, speed = 0.8 },
	{ id = "rbxassetid://9119166424", volume = 0.35, speed = 1.15 },
}

local DamageTaken = require(ReplicatedStorage.Shared.Util.DamageTaken)
local enemies = workspace:WaitForChild("Enemies")

local molten = {} -- [Model] = root

local function hurt(char: Model, amount: number, by: string)
	local hum = char:FindFirstChildOfClass("Humanoid")
	if not hum or hum.Health <= 0 then
		return
	end
	char:SetAttribute("LastHitBy", by)
	hum:TakeDamage(amount * DamageTaken(char))
end

local function ring(parent: Instance, cf: CFrame, radius: number, transparency: number): Part
	local p = Instance.new("Part")
	p.Name = "HeatRing"
	p.Shape = Enum.PartType.Cylinder
	p.Size = Vector3.new(0.15, radius * 2, radius * 2)
	p.CFrame = cf * CFrame.Angles(0, 0, math.rad(90))
	p.Material = Enum.Material.Neon
	p.Color = HEAT_COLOR
	p.Transparency = transparency
	p.CanCollide, p.CanQuery, p.CanTouch, p.CastShadow = false, false, false, false
	p.Parent = parent
	return p
end

-- 발밑 높이 (HRP 아래 HipHeight + 반 높이)
local function groundOffset(model: Model, root: BasePart): number
	local hum = model:FindFirstChildOfClass("Humanoid")
	return -((hum and hum.HipHeight or 2) + root.Size.Y / 2) + 0.1
end

---------------------------------------------------------------- Molten Walker 열기

local function setupMolten(model: Model, root: BasePart)
	-- 멀리서는 클라이언트(FactoryFireHud)가 숨기고 가까이 와야 보임. 여러 마리가 겹쳐도 바닥이 형광으로 덮이지 않게
	-- 빛나지 않는 재질(SmoothPlastic) + 옅게
	local r = ring(model, root.CFrame * CFrame.new(0, groundOffset(model, root), 0), HEAT_RADIUS, 0.82)
	r.Material = Enum.Material.SmoothPlastic
	r.Anchored = false
	r.Massless = true
	local w = Instance.new("WeldConstraint")
	w.Part0, w.Part1 = root, r
	w.Parent = r
	molten[model] = root
	local hum = model:FindFirstChildOfClass("Humanoid")
	hum.Died:Once(function()
		molten[model] = nil
		if r.Parent then
			r:Destroy()
		end
	end)
	model.Destroying:Once(function()
		molten[model] = nil
	end)
end

---------------------------------------------------------------- Slag Walker 죽음 폭발

-- 근처의 죽은 Slag Walker 모델 (살아 있는 Humanoid 가 없고 SlagFX 가 든 모델)
local function slagCorpsesNear(pos: Vector3, radius: number): { Model }
	local found = {}
	local function check(m: Instance)
		if m:IsA("Model") and m:FindFirstChild("SlagFX") then
			local hum = m:FindFirstChildOfClass("Humanoid")
			if (not hum or hum.Health <= 0) and (m:GetPivot().Position - pos).Magnitude <= radius then
				table.insert(found, m)
			end
		end
	end
	for _, a in workspace:GetChildren() do
		check(a)
		if a:IsA("Folder") then
			for _, b in a:GetChildren() do
				check(b)
			end
		end
	end
	return found
end

local function burst(position: Vector3, ground: number)
	local fx = Instance.new("Folder")
	fx.Name = "SlagBurst"
	fx.Parent = workspace
	local base = CFrame.new(position.X, ground, position.Z)
	-- 폭발 소리는 경고가 시작될 때 미리 만들어 둔다 (터지는 순간 만들면 불러오기·전달 지연으로 늦게 들림).
	-- Slag Walker 가 이미 쓰는(미리 불러온) 소리라 바로 난다: 묵직한 쿵 + 짧은 지글거림, 크기는 기본 공격 쿵 정도
	local holder = Instance.new("Part")
	holder.Name = "BurstSound"
	holder.Anchored, holder.CanCollide, holder.CanQuery, holder.CanTouch = true, false, false, false
	holder.Transparency, holder.Size, holder.CFrame = 1, Vector3.one, base + Vector3.new(0, 2, 0)
	holder.Parent = fx
	local sounds = {}
	for _, s in BURST_SOUNDS do
		local snd = Instance.new("Sound")
		snd.SoundId = s.id
		snd.Volume, snd.PlaybackSpeed = s.volume, s.speed
		snd.RollOffMode = Enum.RollOffMode.InverseTapered
		snd.RollOffMinDistance, snd.RollOffMaxDistance = 10, 90
		snd.Parent = holder
		table.insert(sounds, snd)
	end
	-- 경고: 범위 원이 바로 나타나 BURST_DELAY 동안 번쩍이고 터짐 (밝은 테두리 + 옅은 안쪽)
	local rim = ring(fx, base * CFrame.new(0, -0.03, 0), HEAT_RADIUS + 0.5, 0.15)
	rim.Anchored = true
	local warnRing = ring(fx, base, HEAT_RADIUS, 0.55)
	warnRing.Anchored = true
	warnRing.Color = Color3.fromRGB(255, 170, 70)
	TweenService:Create(warnRing, TweenInfo.new(BURST_DELAY, Enum.EasingStyle.Quad, Enum.EasingDirection.In), { Transparency = 0.25 }):Play()
	task.wait(BURST_DELAY)
	warnRing:Destroy()
	rim:Destroy()
	-- 폭발: 빛 + 퍼지는 불덩이 + 암석 조각
	local ball = Instance.new("Part")
	ball.Shape = Enum.PartType.Ball
	ball.Material = Enum.Material.Neon
	ball.Color = HEAT_COLOR
	ball.Size = Vector3.one * 3
	ball.CFrame = base + Vector3.new(0, 2, 0)
	ball.Anchored, ball.CanCollide, ball.CanQuery, ball.CanTouch, ball.CastShadow = true, false, false, false, false
	ball.Transparency = 0.2
	ball.Parent = fx
	local light = Instance.new("PointLight")
	light.Color, light.Brightness, light.Range = HEAT_COLOR, 6, 30
	light.Parent = ball
	TweenService:Create(ball, TweenInfo.new(0.35, Enum.EasingStyle.Quad, Enum.EasingDirection.Out), { Size = Vector3.one * HEAT_RADIUS * 2, Transparency = 1 }):Play()
	TweenService:Create(light, TweenInfo.new(0.5), { Brightness = 0 }):Play()
	for _, snd in sounds do
		snd:Play()
	end
	-- 시체의 슬래그 껍질을 폭발과 같은 순간에 날려 보냄 (SlagFX 는 1.1초 뒤에 천천히 떨어뜨림 → 폭발과 안 맞았음).
	-- 여기서 껍질을 지우면 SlagFX 의 1.1초 처리는 남은 게 없어 건너뜀. 날아가는 조각은 아래 암석이 대신함
	-- (껍질 파트는 CanQuery 가 꺼져 있어 범위 검색에 안 잡힘 → SlagFX 가 든 시체 모델을 workspace 2단계까지 찾음)
	for _, corpse in slagCorpsesNear(base.Position, 8) do
		for _, p in corpse:GetChildren() do
			if p:IsA("MeshPart") and p.Name:find("__Slag$") then
				p:Destroy()
			end
		end
		-- 죽을 때 SlagFX 가 낸 긴 균열음(3초)은 예고로만 쓰고 폭발 순간 끊음 (소리가 겹쳐 과했음)
		for _, s in corpse:GetDescendants() do
			if s:IsA("Sound") and (s.Name == "Death" or s.Name == "DeathHiss") then
				s:Stop()
			end
		end
	end
	for _ = 1, 14 do
		local rock = Instance.new("Part")
		rock.Size = Vector3.new(math.random(5, 12) / 10, math.random(5, 10) / 10, math.random(5, 12) / 10)
		rock.Color = Color3.fromRGB(40, 36, 34)
		rock.Material = Enum.Material.Basalt
		rock.CFrame = base * CFrame.new(math.random(-15, 15) / 10, 2, math.random(-15, 15) / 10)
		rock.CanCollide, rock.CanQuery, rock.CanTouch = true, false, false
		rock.CollisionGroup = "Enemies" -- 플레이어·적과 안 부딪히게 (Enemy 서비스가 만드는 그룹)
		rock.Parent = fx
		rock.AssemblyLinearVelocity = Vector3.new(math.random(-30, 30), math.random(25, 45), math.random(-30, 30))
	end
	-- 피해
	for _, player in Players:GetPlayers() do
		local char = player.Character
		local root = char and char:FindFirstChild("HumanoidRootPart")
		if root and (root.Position - base.Position).Magnitude <= HEAT_RADIUS + 1.5 then
			hurt(char, BURST_DAMAGE, "Slag Walker")
		end
	end
	task.delay(3, function()
		fx:Destroy()
	end)
end

-- 체력이 낮을수록 균열이 밝게 벌어짐 (SlagFX 의 피격 번쩍임이 끝난 뒤 다시 맞춤)
local function setupCracks(model: Model, hum: Humanoid)
	local sas, light, emitters = {}, nil, {}
	for _, d in model:GetDescendants() do
		if d:IsA("SurfaceAppearance") and d.Parent.Name:find("__Slag$") then
			table.insert(sas, d)
		elseif d:IsA("PointLight") and d.Name == "SlagGlow" then
			light = d
		elseif d:IsA("ParticleEmitter") and (d.Name == "Embers" or d.Name == "Smoke") then
			table.insert(emitters, { d, d.Rate })
		end
	end
	if #sas == 0 then
		return
	end
	local baseLight = light and light.Brightness or 0.6
	local level, token = 0, 0
	local function apply(strengthMul: number, seconds: number)
		local strength = CRACK_STRENGTH[1] + (CRACK_STRENGTH[2] - CRACK_STRENGTH[1]) * level
		local tint = CRACK_TINT[1]:Lerp(CRACK_TINT[2], level)
		local info = TweenInfo.new(seconds, Enum.EasingStyle.Sine)
		for _, sa in sas do
			TweenService:Create(sa, info, { EmissiveStrength = strength * strengthMul, EmissiveTint = tint }):Play()
		end
		if light then
			TweenService:Create(light, info, { Brightness = (baseLight + 3 * level) * strengthMul }):Play()
		end
	end
	local function update()
		if hum.Health <= 0 then
			return
		end
		local ratio = hum.Health / math.max(hum.MaxHealth, 1)
		level = math.clamp((CRACK_START - ratio) / (CRACK_START - CRACK_FULL), 0, 1)
		for _, e in emitters do
			e[1].Rate = e[2] * (1 + 4 * level)
		end
		token += 1
		local my = token
		task.delay(0.35, function() -- SlagFX 피격 번쩍임(0.3초) 뒤
			if my ~= token or hum.Health <= 0 then
				return
			end
			apply(1, 0.25)
			if ratio < CRACK_PULSE then
				-- 곧 터질 것 같은 깜빡임: 다음 피격 전까지 반복
				task.wait(0.25)
				local bright = true
				while my == token and hum.Health > 0 and model.Parent do
					bright = not bright
					apply(bright and 1.35 or 0.7, 0.22)
					task.wait(0.24)
				end
			end
		end)
	end
	hum.HealthChanged:Connect(update)
	update()
end

local function setupSlag(model: Model, root: BasePart)
	local hum = model:FindFirstChildOfClass("Humanoid")
	setupCracks(model, hum)
	hum.Died:Once(function()
		if root.Parent then
			local ground = root.Position.Y + groundOffset(model, root)
			task.spawn(burst, root.Position, ground)
		end
	end)
end

---------------------------------------------------------------- Hook Hauler 등 약점
-- 앞에서 맞으면 피해 FRONT_MULT, 등 뒤에서 맞으면 BACK_MULT (옆은 그대로). 등에 박힌 크레인 갈고리 = 약점.
-- 공용 Combat.DamageDealer 가 피해마다 EnemyService.damageTakenMultiplier(적, 때린 사람 위치)를 부르므로
-- 공장 place 에서만 그 함수를 감싸 hook_hauler 일 때 배율을 곱한다 (공용 패키지는 그대로).

local FRONT_MULT = 0.5
local BACK_MULT = 1.5
local SIDE_DOT = 0.3 -- 보는 방향과 때린 방향의 내적이 이보다 크면 앞, −이보다 작으면 뒤

local weakFx = setmetatable({}, { __mode = "k" }) -- [Model] = { sparks, sound, last }

local function setupWeakPoint(model: Model)
	local hook = model:FindFirstChild("UpperTorso__Paint") -- 등에 박힌 갈고리
	local sparksSrc = model:FindFirstChild("HitSparks", true)
	local clangSrc = model:FindFirstChild("HitClang", true)
	if not hook then
		return
	end
	local sparks
	if sparksSrc then
		sparks = sparksSrc:Clone()
		sparks.Name = "WeakSparks"
		sparks.Enabled = false
		sparks.Parent = hook
	end
	local sound
	if clangSrc then
		sound = clangSrc:Clone()
		sound.Name = "WeakClang"
		sound.PlaybackSpeed = clangSrc.PlaybackSpeed * 1.35 -- 더 높고 날카로운 쇳소리
		sound.Volume = clangSrc.Volume * 0.9
		sound.Parent = hook
	end
	weakFx[model] = { sparks = sparks, sound = sound, last = 0 }
end

local Services = game:GetService("ServerScriptService"):WaitForChild("Services")
local EnemyService = require(Services.Enemy)
local baseMultiplier = EnemyService.damageTakenMultiplier
EnemyService.damageTakenMultiplier = function(humanoid: Humanoid, from: Vector3?): number
	local mult = baseMultiplier(humanoid, from)
	local model = humanoid.Parent
	if not from or not model or model:GetAttribute("EnemyId") ~= "hook_hauler" then
		return mult
	end
	local root = model:FindFirstChild("HumanoidRootPart")
	if not root then
		return mult
	end
	local to = Vector3.new(from.X - root.Position.X, 0, from.Z - root.Position.Z)
	if to.Magnitude < 0.1 then
		return mult
	end
	local dot = to.Unit:Dot(root.CFrame.LookVector)
	if dot >= SIDE_DOT then
		return mult * FRONT_MULT
	elseif dot <= -SIDE_DOT then
		local fx = weakFx[model]
		if fx and os.clock() - fx.last > 0.15 then -- 여러 타가 한꺼번에 들어와도 효과는 한 번
			fx.last = os.clock()
			if fx.sparks then
				fx.sparks:Emit(16)
			end
			if fx.sound then
				fx.sound:Play()
			end
		end
		return mult * BACK_MULT
	end
	return mult
end

-- 개발용 확인: ServerStorage.FactoryHazardsTest:Invoke(humanoid, from) → 지금 적용되는 받는 피해 배율
do
	local probe = Instance.new("BindableFunction")
	probe.Name = "FactoryHazardsTest"
	probe.OnInvoke = function(humanoid, from)
		return EnemyService.damageTakenMultiplier(humanoid, from)
	end
	probe.Parent = game:GetService("ServerStorage")
end

---------------------------------------------------------------- 적 감시

local function onEnemy(model: Instance)
	if not model:IsA("Model") then
		return
	end
	local id = model:GetAttribute("EnemyId")
	if not id then
		model:GetAttributeChangedSignal("EnemyId"):Wait()
		id = model:GetAttribute("EnemyId")
	end
	local root = model:WaitForChild("HumanoidRootPart", 5)
	local hum = model:FindFirstChildOfClass("Humanoid")
	if not root or not hum or hum.Health <= 0 then
		return
	end
	if id == "molten_walker" then
		setupMolten(model, root)
	elseif id == "slag_walker" then
		setupSlag(model, root)
	elseif id == "hook_hauler" then
		setupWeakPoint(model)
	end
end

for _, m in enemies:GetChildren() do
	task.spawn(onEnemy, m)
end
enemies.ChildAdded:Connect(function(m)
	task.spawn(onEnemy, m)
end)

---------------------------------------------------------------- 화염 스택 (1초마다)

-- 범위 안 Molten Walker 수 (마리 수만큼 한 번에 쌓임)
local function heatCount(pos: Vector3): number
	local n = 0
	for model, root in molten do
		if model.Parent and root.Parent and (root.Position - pos).Magnitude <= HEAT_RADIUS then
			n += 1
		end
	end
	return n
end
local lastHeat = setmetatable({}, { __mode = "k" }) -- [Model] = 마지막으로 열기를 받은 os.clock

Players.PlayerAdded:Connect(function(player)
	player.CharacterAdded:Connect(function(char)
		char:SetAttribute("FireStacks", 0)
	end)
end)

while true do
	task.wait(1)
	for _, player in Players:GetPlayers() do
		local char = player.Character
		local root = char and char:FindFirstChild("HumanoidRootPart")
		local hum = char and char:FindFirstChildOfClass("Humanoid")
		if root and hum and hum.Health > 0 then
			local stacks = char:GetAttribute("FireStacks") or 0
			local n = heatCount(root.Position)
			if n > 0 then
				stacks = math.min(MAX_STACKS, stacks + n)
				lastHeat[char] = os.clock()
			elseif os.clock() - (lastHeat[char] or 0) >= CLEAR_AFTER then
				stacks = 0 -- 열기를 CLEAR_AFTER 초 동안 안 받으면 전부 사라짐
			else
				stacks = math.max(0, stacks - 1)
			end
			char:SetAttribute("FireStacks", stacks)
			if stacks > 0 then
				hurt(char, stacks * DAMAGE_PER_STACK, "Burning")
				char:SetAttribute("BurnTick", (char:GetAttribute("BurnTick") or 0) + 1) -- 클라이언트 화면 번쩍임
			end
		end
	end
end
