-- Hook Hauler 소리·효과 설치 (Studio MCP execute_luau 로 실행). 공용 Services 코드는 건드리지 않음.
-- HookFX 는 살아 있는 적(Humanoid 있음)과 시체 복제본(Humanoid 없음) 둘 다에서 돈다.
local ATTACK_ANIM = "rbxassetid://129093537179092"
local SOUNDS = { -- ProSoundEffects (Roblox 라이선스 효과음): id, 볼륨, 최대 거리
	ChainDrag = {9113763407, 0.22, 55},   -- 사슬 계속 덜그럭 (움직일 때 반복)
	Step = {9113526269, 0.45, 60},        -- 무거운 발걸음 (낮은 음으로)
	Jingle = {9113763590, 0.3, 45},       -- 사슬 짤랑
	Growl1 = {9114630281, 0.5, 80}, Growl2 = {9125842589, 0.45, 80}, -- 마스크 너머 숨·으르렁 (낮은 음)
	Swing = {9119468100, 0.45, 60},       -- 휘두르는 바람 소리
	Impact = {9116541751, 0.75, 90},      -- 쇠 부딪힘 (타격)
	HitClang = {9119072660, 0.5, 60},     -- 맞을 때
	DeathChain = {9113763252, 0.7, 80}, DeathDrop = {9116554603, 0.7, 80},
}

local FX_SOURCE = [==[
-- HookFX: Hook Hauler 소리·효과 (모델 안 스크립트, scripts/hook_hauler_fx.lua 가 설치)
local model = script.Parent
local attackAnim = script:GetAttribute("AttackAnim")
local hum = model:FindFirstChildOfClass("Humanoid")
local torso = model:WaitForChild("UpperTorso", 5)
local hookPart = model:FindFirstChild("RightHand__Paint")
if not (torso and hookPart) then return end
local rng = Random.new()
local function snd(n) return torso:FindFirstChild(n) end
local function play(n, lo, hi, stopAfter)
	local s = snd(n)
	if not s then return end
	s.PlaybackSpeed = rng:NextNumber(lo or 1, hi or 1)
	s:Play()
	if stopAfter then task.delay(stopAfter, function() s:Stop() end) end
end
local chainPart = model:FindFirstChild("UpperTorso__Rust")
local sparks = chainPart and chainPart:FindFirstChild("HitSparks")
local tip = hookPart:FindFirstChild("HookTip")
local tipSparks = tip and tip:FindFirstChild("SwingSparks")
local tipDust = tip and tip:FindFirstChild("SwingDust")

if hum then
	local alive = true
	local drag = snd("ChainDrag")
	if drag then drag.Looped = true end
	-- 발소리 + 사슬 끌림
	task.spawn(function()
		local step = 0
		while alive do
			local root = model:FindFirstChild("HumanoidRootPart")
			local speed = root and (root.AssemblyLinearVelocity * Vector3.new(1, 0, 1)).Magnitude or 0
			local moving = hum.MoveDirection.Magnitude > 0.1 and speed > 1
			if drag then
				if moving and not drag.IsPlaying then drag:Play() elseif not moving and drag.IsPlaying then drag:Stop() end
				drag.PlaybackSpeed = math.clamp(0.7 + speed / 30, 0.7, 1.2)
			end
			if moving then
				step += 1
				play("Step", 0.55, 0.68, 0.6)
				if step % 3 == 0 then play("Jingle", 0.8, 1.05) end
				task.wait(math.clamp(5.0 / speed, 0.4, 0.95))
			else
				task.wait(0.2)
			end
		end
	end)
	-- 마스크 너머 숨소리·으르렁
	task.spawn(function()
		while alive do
			task.wait(hum.WalkSpeed > 8 and rng:NextNumber(3, 6) or rng:NextNumber(6, 12))
			if alive then play(rng:NextInteger(1, 2) == 1 and "Growl1" or "Growl2", 0.55, 0.7) end
		end
	end)
	-- 맞았을 때: 쇠 부딪힘 + 불티
	local lastHealth, lastHit = hum.Health, 0
	hum.HealthChanged:Connect(function(h)
		if h < lastHealth and h > 0 and os.clock() - lastHit > 0.15 then
			lastHit = os.clock()
			if sparks then sparks:Emit(12) end
			play("HitClang", 0.75, 0.95)
		end
		lastHealth = h
	end)
	-- 공격: 휘두르는 소리(타격 직전) + 타격 순간 쾅·불티·먼지
	local animator = hum:FindFirstChildOfClass("Animator") or hum:WaitForChild("Animator", 5)
	local hooked = {}
	if animator and attackAnim then
		animator.AnimationPlayed:Connect(function(track)
			if track.Animation and track.Animation.AnimationId == attackAnim then
				local sp = math.max(track.Speed, 0.05)
				task.delay(0.5 / sp, function() play("Swing", 0.55, 0.65, 0.9) end)
				if not hooked[track] then
					hooked[track] = true
					track:GetMarkerReachedSignal("Impact"):Connect(function()
						play("Impact", 0.8, 0.95)
						if tipSparks then tipSparks:Emit(20) end
						if tipDust then tipDust:Emit(8) end
					end)
				end
			end
		end)
	end
	hum.Died:Once(function()
		alive = false
		for _, s in torso:GetChildren() do if s:IsA("Sound") then s:Stop() end end
	end)
else
	-- 시체 복제본: 사슬과 손의 갈고리가 풀려 바닥에 떨어짐
	play("DeathChain", 0.85, 1.0)
	task.delay(0.9, function() play("DeathDrop", 0.8, 0.95) end)
	task.delay(0.8, function()
		for _, p in model:GetChildren() do
			if p:IsA("MeshPart") and (p.Name:match("__Rust$") and not p.Name:match("Foot") or p.Name == "RightHand__Paint") then
				local w = p:FindFirstChild("Attach")
				if w then w:Destroy() end
				p.Massless = false
				p.CanCollide = true
				p.Anchored = false
				p.AssemblyLinearVelocity = Vector3.new(rng:NextNumber(-2, 2), rng:NextNumber(0, 2), rng:NextNumber(-2, 2))
				p.AssemblyAngularVelocity = Vector3.new(rng:NextNumber(-3, 3), rng:NextNumber(-3, 3), rng:NextNumber(-3, 3))
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
	local o = model:FindFirstChild("HookFX"); if o then o:Destroy() end
	local torso, chainPart, hookPart = model.UpperTorso, model.UpperTorso__Rust, model.RightHand__Paint
	for _, p in { torso, chainPart, hookPart } do
		for _, c in p:GetChildren() do
			if c:IsA("ParticleEmitter") or c:IsA("Sound") or (c:IsA("Attachment") and c.Name == "HookTip") then c:Destroy() end
		end
	end
	local spark = {
		Texture = "rbxasset://textures/particles/sparkles_main.dds",
		Color = ColorSequence.new(Color3.fromRGB(255, 230, 170), Color3.fromRGB(255, 140, 50)), LightEmission = 1, LightInfluence = 0,
		Size = NumberSequence.new(0.12, 0), Lifetime = NumberRange.new(0.2, 0.5), Speed = NumberRange.new(8, 15),
		SpreadAngle = Vector2.new(70, 70), Acceleration = Vector3.new(0, -35, 0), Drag = 2, Enabled = false,
	}
	emitter(chainPart, "HitSparks", spark)
	local tip = Instance.new("Attachment")
	tip.Name = "HookTip"
	tip.Position = Vector3.new(0, -hookPart.Size.Y * 0.35, 0)
	tip.Parent = hookPart
	emitter(tip, "SwingSparks", spark)
	emitter(tip, "SwingDust", {
		Texture = "rbxasset://textures/particles/smoke_main.dds",
		Color = ColorSequence.new(Color3.fromRGB(90, 82, 74), Color3.fromRGB(65, 60, 55)),
		Transparency = NumberSequence.new(0.6, 1), Size = NumberSequence.new(0.6, 2.2), Lifetime = NumberRange.new(0.5, 1.0),
		Speed = NumberRange.new(2, 5), SpreadAngle = Vector2.new(60, 60), Drag = 4, Rotation = NumberRange.new(0, 360), Enabled = false,
	})
	local n = 0
	for name, d in SOUNDS do
		local s = Instance.new("Sound")
		s.Name = name
		s.SoundId = "rbxassetid://" .. d[1]
		s.Volume = d[2]
		s.RollOffMode = Enum.RollOffMode.InverseTapered
		s.RollOffMinDistance = 8
		s.RollOffMaxDistance = d[3]
		s.Parent = torso
		n += 1
	end
	local sc = Instance.new("Script")
	sc.Name = "HookFX"
	sc.Source = FX_SOURCE
	sc:SetAttribute("AttackAnim", ATTACK_ANIM)
	sc.Parent = model
	return n
end

return "installed sounds " .. install(game.ServerStorage.Assets.Enemies.HookHauler)
