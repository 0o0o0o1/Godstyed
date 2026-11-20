-- The Foreman 소리·효과 설치 (Studio MCP execute_luau). 공용 Services 는 패턴 모듈 3개 추가(scripts/foreman_patterns/) 외에 안 건드림.
-- 패턴이 이름으로 찾는 소리: ThrowWhoosh, ChainRattle, HookHit (갈고리 던지기), CoilCrash (짐 낙하). 사이렌은 모델 속성 Siren 을 보고 ForemanFX 가 냄.
local SMASH = "rbxassetid://121917648178069"
local SOUNDS = { -- id, 볼륨, 최대 거리
	Step = {9113526269, 0.6, 90},             -- 무거운 발걸음 (아주 낮은 음)
	ChainRattle = {9113763407, 0.45, 70},     -- 사슬 덜그럭
	Growl1 = {9114630281, 0.7, 120}, Growl2 = {9125842589, 0.65, 120}, -- 확성기 너머 으르렁 (낮은 음)
	Static = {9113073932, 0.25, 70},          -- 확성기 지직 (공기 새는 소리 대체)
	SirenWail = {106098533112635, 0.8, 160},  -- 사이렌 (구형 경보 사이렌)
	Smash = {9116541751, 0.9, 110},           -- 갈고리 내려찍기 쇠 충돌
	ThrowWhoosh = {9119468100, 0.55, 70},
	HookHit = {9119072660, 0.6, 70},
	CoilCrash = {9116546593, 0.9, 140},       -- 코일 낙하 (금속 대충돌)
	GlassBreak = {6737581507, 0.8, 120},      -- 2페이즈: 운전실 유리 깨짐
	MegaBreak = {9120369181, 0.8, 120},       -- 분노: 확성기 뜯겨 나감
	HitClang = {9119072674, 0.5, 70},
	DeathCrash = {9116546593, 1.0, 160}, DeathChain = {9113763252, 0.8, 100},
}

local FX_SOURCE = [==[
-- ForemanFX: The Foreman 소리·효과 (모델 안 스크립트, scripts/foreman_fx.lua 가 설치)
local TweenService = game:GetService("TweenService")
local model = script.Parent
local smashAnim = script:GetAttribute("SmashAnim")
local hum = model:FindFirstChildOfClass("Humanoid")
local torso = model:WaitForChild("UpperTorso", 5)
if not torso then return end
local rng = Random.new()
local function snd(n) return torso:FindFirstChild(n) end
local function play(n, lo, hi, stopAfter)
	local s = snd(n)
	if not s then return end
	s.PlaybackSpeed = rng:NextNumber(lo or 1, hi or 1)
	s:Play()
	if stopAfter then task.delay(stopAfter, function() s:Stop() end) end
end
local mega = model:FindFirstChild("LeftHand__Mega")
local mouth = mega and mega:FindFirstChild("MegaMouth")
local wave = mouth and mouth:FindFirstChild("SoundWave")
local dustRing = mouth and mouth:FindFirstChild("WaveDust")
local cab = model:FindFirstChild("UpperTorso__Paint")
local cabLight = cab and cab:FindFirstChild("CabLight")
local hook = model:FindFirstChild("RightHand__Hook")
local hookTip = hook and hook:FindFirstChild("HookTip")
local smashDust = hookTip and hookTip:FindFirstChild("SmashDust")
local smashSparks = hookTip and hookTip:FindFirstChild("SmashSparks")
local chain = model:FindFirstChild("RightHand__Rust")
local sparks = chain and chain:FindFirstChild("HitSparks")

if hum then
	local alive = true
	-- 발걸음 (쿵) + 사슬
	task.spawn(function()
		local step = 0
		while alive do
			local root = model:FindFirstChild("HumanoidRootPart")
			local speed = root and (root.AssemblyLinearVelocity * Vector3.new(1, 0, 1)).Magnitude or 0
			if hum.MoveDirection.Magnitude > 0.1 and speed > 1 then
				step += 1
				play("Step", 0.38, 0.45, 0.8)
				if step % 2 == 0 then play("ChainRattle", 0.8, 1.0, 0.6) end
				task.wait(math.clamp(9 / speed, 0.5, 1.1))
			else
				task.wait(0.2)
			end
		end
	end)
	-- 확성기 너머 으르렁 + 지직
	task.spawn(function()
		while alive do
			task.wait(rng:NextNumber(5, 10))
			if alive then
				play("Static", 0.8, 1.0, 0.8)
				task.delay(0.3, function() play(rng:NextInteger(1, 2) == 1 and "Growl1" or "Growl2", 0.42, 0.52) end)
			end
		end
	end)
	-- 맞았을 때
	local lastHealth, lastHit = hum.Health, 0
	hum.HealthChanged:Connect(function(h)
		if h < lastHealth and h > 0 and os.clock() - lastHit > 0.2 then
			lastHit = os.clock()
			if sparks then sparks:Emit(14) end
			play("HitClang", 0.6, 0.8)
		end
		lastHealth = h
	end)
	-- 내려찍기(기본 공격·짐 낙하 시작): 마커 "Impact"
	local animator = hum:FindFirstChildOfClass("Animator") or hum:WaitForChild("Animator", 5)
	local hooked = {}
	if animator and smashAnim then
		animator.AnimationPlayed:Connect(function(track)
			if track.Animation and track.Animation.AnimationId == smashAnim and not hooked[track] then
				hooked[track] = true
				track:GetMarkerReachedSignal("Impact"):Connect(function()
					play("Smash", 0.7, 0.85)
					if smashDust then smashDust:Emit(22) end
					if smashSparks then smashSparks:Emit(24) end
				end)
			end
		end)
	end
	-- 사이렌 (ForemanSiren 패턴이 속성 Siren 을 켬)
	model:GetAttributeChangedSignal("Siren"):Connect(function()
		if model:GetAttribute("Siren") then
			play("SirenWail", 0.9, 1.0, 1.8)
			if wave then wave:Emit(6) end
			if dustRing then dustRing:Emit(30) end
		end
	end)
	-- 페이즈: 2 = 운전실 유리 깨짐(BossBrain breakParts), 3 = 확성기 뜯겨 나감 → 소리 + 운전실 비상등
	model:GetAttributeChangedSignal("Phase"):Connect(function()
		local ph = model:GetAttribute("Phase")
		if ph == 2 then
			play("GlassBreak", 0.9, 1.0)
			if cabLight then cabLight.Enabled = true end
		elseif ph == 3 then
			play("MegaBreak", 0.8, 0.9)
			play("Static", 0.6, 0.7, 1.2)
			if cabLight then
				cabLight.Color = Color3.fromRGB(255, 40, 30)
				task.spawn(function()
					while alive and cabLight.Parent do
						cabLight.Brightness = 3; task.wait(0.35)
						cabLight.Brightness = 0.3; task.wait(0.35)
					end
				end)
			end
		end
	end)
	hum.Died:Once(function()
		alive = false
		for _, s in torso:GetChildren() do if s:IsA("Sound") then s:Stop() end end
		if cabLight then cabLight.Enabled = false end
	end)
else
	-- 시체 복제본: 쓰러지며 큰 쇳소리, 사슬과 갈고리가 풀려 떨어짐
	play("DeathCrash", 0.6, 0.7)
	task.delay(0.3, function() play("DeathChain", 0.7, 0.8) end)
	task.delay(0.6, function()
		for _, p in model:GetChildren() do
			if p:IsA("MeshPart") and (p.Name == "RightHand__Hook" or p.Name == "RightHand__Rust") then
				local w = p:FindFirstChild("Attach")
				if w then w:Destroy() end
				p.Massless = false
				p.CanCollide = true
				p.Anchored = false
				task.delay(4, function()
					if p.Parent then p.Anchored = true; p.CanCollide = false end
				end)
			end
		end
	end)
end
]==]

local function emitter(parent, name, props)
	local e = Instance.new("ParticleEmitter")
	e.Name = name
	for k, v in props do e[k] = v end
	e.Parent = parent
	return e
end

local function install(model)
	local o = model:FindFirstChild("ForemanFX"); if o then o:Destroy() end
	local torso, mega, cab, hook, chain = model.UpperTorso, model.LeftHand__Mega, model.UpperTorso__Paint, model.RightHand__Hook, model.RightHand__Rust
	for _, p in { torso, mega, cab, hook, chain } do
		for _, c in p:GetChildren() do
			if c:IsA("ParticleEmitter") or c:IsA("Sound") or c:IsA("Light") or (c:IsA("Attachment") and (c.Name == "MegaMouth" or c.Name == "HookTip")) then c:Destroy() end
		end
	end
	-- 확성기 입 (메쉬 바운딩 앞쪽 끝: 확성기는 -Z(앞) 방향)
	local mouth = Instance.new("Attachment"); mouth.Name = "MegaMouth"
	mouth.Position = Vector3.new(0, 0, -mega.Size.Z * 0.45); mouth.Parent = mega
	emitter(mouth, "SoundWave", {
		Texture = "rbxasset://textures/particles/sparkles_main.dds", Color = ColorSequence.new(Color3.fromRGB(255, 240, 210)),
		Transparency = NumberSequence.new({NumberSequenceKeypoint.new(0, 0.4), NumberSequenceKeypoint.new(1, 1)}),
		Size = NumberSequence.new(1, 9), Lifetime = NumberRange.new(0.5, 0.7), Speed = NumberRange.new(30, 40),
		EmissionDirection = Enum.NormalId.Front, SpreadAngle = Vector2.new(12, 12), LightEmission = 0.4, Enabled = false,
	})
	emitter(mouth, "WaveDust", {
		Texture = "rbxasset://textures/particles/smoke_main.dds", Color = ColorSequence.new(Color3.fromRGB(110, 102, 92)),
		Transparency = NumberSequence.new(0.55, 1), Size = NumberSequence.new(1, 4), Lifetime = NumberRange.new(0.6, 1.0),
		Speed = NumberRange.new(20, 30), EmissionDirection = Enum.NormalId.Front, SpreadAngle = Vector2.new(35, 20), Drag = 3, Enabled = false,
	})
	-- 운전실 비상등 (2페이즈부터)
	local cl = Instance.new("PointLight"); cl.Name = "CabLight"; cl.Color = Color3.fromRGB(255, 160, 60); cl.Brightness = 1.2; cl.Range = 12
	cl.Shadows = false; cl.Enabled = false; cl.Parent = cab
	-- 갈고리 끝 (내려찍기 먼지·불티)
	local tip = Instance.new("Attachment"); tip.Name = "HookTip"; tip.Position = Vector3.new(0, -hook.Size.Y * 0.4, 0); tip.Parent = hook
	local spark = {
		Texture = "rbxasset://textures/particles/sparkles_main.dds",
		Color = ColorSequence.new(Color3.fromRGB(255, 225, 150), Color3.fromRGB(255, 120, 40)), LightEmission = 1, LightInfluence = 0,
		Size = NumberSequence.new(0.2, 0), Lifetime = NumberRange.new(0.3, 0.6), Speed = NumberRange.new(12, 22),
		SpreadAngle = Vector2.new(80, 80), Acceleration = Vector3.new(0, -40, 0), Drag = 2, Enabled = false,
	}
	emitter(tip, "SmashSparks", spark)
	emitter(tip, "SmashDust", {
		Texture = "rbxasset://textures/particles/smoke_main.dds", Color = ColorSequence.new(Color3.fromRGB(95, 88, 80), Color3.fromRGB(70, 65, 60)),
		Transparency = NumberSequence.new(0.5, 1), Size = NumberSequence.new(1.5, 5), Lifetime = NumberRange.new(0.7, 1.3),
		Speed = NumberRange.new(6, 12), SpreadAngle = Vector2.new(85, 85), Drag = 4, Rotation = NumberRange.new(0, 360), Enabled = false,
	})
	emitter(chain, "HitSparks", spark)
	local n = 0
	for name, d in SOUNDS do
		local s = Instance.new("Sound")
		s.Name = name; s.SoundId = "rbxassetid://" .. d[1]; s.Volume = d[2]
		s.RollOffMode = Enum.RollOffMode.InverseTapered; s.RollOffMinDistance = 10; s.RollOffMaxDistance = d[3]
		s.Parent = torso
		n += 1
	end
	local sc = Instance.new("Script")
	sc.Name = "ForemanFX"; sc.Source = FX_SOURCE
	sc:SetAttribute("SmashAnim", SMASH)
	sc.Parent = model
	return n
end

return "installed " .. install(game.ServerStorage.Assets.Enemies.Foreman)
