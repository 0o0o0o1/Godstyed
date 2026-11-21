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
	local r = ring(model, root.CFrame * CFrame.new(0, groundOffset(model, root), 0), HEAT_RADIUS, 0.88)
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

local function burst(position: Vector3, ground: number)
	local fx = Instance.new("Folder")
	fx.Name = "SlagBurst"
	fx.Parent = workspace
	local base = CFrame.new(position.X, ground, position.Z)
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
	local sound = Instance.new("Sound")
	sound.SoundId = "rbxasset://sounds/collide.wav"
	sound.Volume, sound.PlaybackSpeed = 1.6, 0.45
	sound.RollOffMaxDistance = 120
	sound.Parent = ball
	sound:Play()
	for _ = 1, 10 do
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
			end
		end
	end
end
