-- Slag Walker / Molten Walker 소리·효과 설치 (Studio MCP execute_luau 로 실행)
-- 모델 안에 파티클·빛·소리·스크립트(SlagFX)를 넣는다. 공용 Services 코드는 건드리지 않음.
-- SlagFX 는 살아 있는 적(Humanoid 있음)과 시체 복제본(Humanoid 없음, EnemyAI.spawnDeathCorpse) 둘 다에서 돈다.
local ATTACK_ANIM = "rbxassetid://89817274505362"
local SOUNDS = { -- ProSoundEffects (Roblox 라이선스 효과음)
	Step1 = {9118690418, 0.32, 60}, Step2 = {9116327660, 0.28, 60},
	Groan1 = {9114628818, 0.55, 90}, Groan2 = {9116305961, 0.5, 90},
	Hiss = {9119165650, 0.3, 50}, HitSizzle = {9119166424, 0.45, 60},
	Impact = {9118617342, 0.8, 80}, Death = {9118585250, 0.75, 90}, DeathHiss = {9119166195, 0.45, 60},
	Crackle = {9118030782, 0.1, 35}, -- 갓 굳은 형만 계속 재생
}

local FX_SOURCE = [==[
-- SlagFX: Slag Walker 소리·효과 (모델 안 스크립트, scripts/slag_walker_fx.lua 가 설치)
local TweenService = game:GetService("TweenService")
local model = script.Parent
local molten = script:GetAttribute("Molten") == true
local attackAnim = script:GetAttribute("AttackAnim")
local hum = model:FindFirstChildOfClass("Humanoid")
local torso = model:WaitForChild("UpperTorso", 5)
local slagTorso = model:FindFirstChild("UpperTorso__Slag")
local club = model:FindFirstChild("RightHand__Slag")
if not (torso and slagTorso and club) then return end
local rng = Random.new()

local function snd(name) return torso:FindFirstChild(name) end
local function play(name, pitchLo, pitchHi, stopAfter)
	local s = snd(name)
	if not s then return end
	s.PlaybackSpeed = rng:NextNumber(pitchLo or 1, pitchHi or 1)
	s:Play()
	if stopAfter then task.delay(stopAfter, function() s:Stop() end) end
end
local slagSA = {}
for _, p in model:GetChildren() do
	if p:IsA("MeshPart") and p.Name:match("__Slag$") then
		local sa = p:FindFirstChildOfClass("SurfaceAppearance")
		if sa then table.insert(slagSA, {sa, sa.EmissiveStrength}) end
	end
end
local light = slagTorso:FindFirstChild("SlagGlow")
local embers = { slagTorso:FindFirstChild("Embers"), club:FindFirstChild("Embers") }
local smoke = slagTorso:FindFirstChild("Smoke")
local sparks = slagTorso:FindFirstChild("HitSparks")
local chips = slagTorso:FindFirstChild("HitChips")
local tip = club:FindFirstChild("ClubTip")
local dust = tip and tip:FindFirstChild("SlamDust")
local slamSparks = tip and tip:FindFirstChild("SlamSparks")

if hum then
	---------------- 살아 있을 때 ----------------
	local alive = true
	if molten then local c = snd("Crackle"); if c then c:Play() end end
	-- 발소리: 이동 속도에 맞춘 보폭
	task.spawn(function()
		local step = 0
		while alive do
			local root = model:FindFirstChild("HumanoidRootPart")
			local speed = root and (root.AssemblyLinearVelocity * Vector3.new(1, 0, 1)).Magnitude or 0
			if hum.MoveDirection.Magnitude > 0.1 and speed > 1 then
				step += 1
				play(step % 2 == 0 and "Step1" or "Step2", 0.85, 1.15, 0.35)
				task.wait(math.clamp(4.2 / speed, 0.3, 0.8))
			else
				task.wait(0.2)
			end
		end
	end)
	-- 신음·식는 소리
	task.spawn(function()
		while alive do
			task.wait(hum.WalkSpeed > 10 and rng:NextNumber(4, 8) or rng:NextNumber(7, 15))
			if alive then play(rng:NextInteger(1, 2) == 1 and "Groan1" or "Groan2", 0.72, 0.88) end
		end
	end)
	task.spawn(function()
		while alive do
			task.wait(rng:NextNumber(8, 16))
			if alive then
				play("Hiss", 0.75, 0.95)
				if smoke then smoke:Emit(4) end
			end
		end
	end)
	-- 맞았을 때: 불티·껍질 조각·지글거림·균열 번쩍
	local lastHealth, lastHit = hum.Health, 0
	hum.HealthChanged:Connect(function(h)
		if h < lastHealth and h > 0 and os.clock() - lastHit > 0.12 then
			lastHit = os.clock()
			if sparks then sparks:Emit(14) end
			if chips then chips:Emit(6) end
			play("HitSizzle", 0.9, 1.2)
			for _, e in slagSA do
				e[1].EmissiveStrength = e[2] * 2
				TweenService:Create(e[1], TweenInfo.new(0.3), { EmissiveStrength = e[2] }):Play()
			end
			if light then
				local b = light.Brightness
				light.Brightness = b * 2.5
				TweenService:Create(light, TweenInfo.new(0.3), { Brightness = b }):Play()
			end
		end
		lastHealth = h
	end)
	-- 내려치기 타격 순간(애니메이션 마커 "Impact"): 쿵 소리·먼지·불티
	local animator = hum:FindFirstChildOfClass("Animator") or hum:WaitForChild("Animator", 5)
	local hooked = {}
	if animator and attackAnim then
		animator.AnimationPlayed:Connect(function(track)
			if track.Animation and track.Animation.AnimationId == attackAnim and not hooked[track] then
				hooked[track] = true
				track:GetMarkerReachedSignal("Impact"):Connect(function()
					play("Impact", 0.85, 1.0)
					if dust then dust:Emit(16) end
					if slamSparks then slamSparks:Emit(18) end
				end)
			end
		end)
	end
	hum.Died:Once(function()
		alive = false
		for _, e in embers do if e then e.Enabled = false end end
		if smoke then smoke.Enabled = false end
		if light then light.Enabled = false end
		for _, s in torso:GetChildren() do if s:IsA("Sound") then s:Stop() end end
	end)
else
	---------------- 시체 복제본: 빛이 꺼지며 부서짐 ----------------
	play("Death", 0.85, 1.0)
	task.delay(0.15, function() play("DeathHiss", 0.7, 0.85) end)
	if smoke then smoke:Emit(18) end
	local fade = TweenInfo.new(3, Enum.EasingStyle.Quad, Enum.EasingDirection.In)
	for _, e in slagSA do TweenService:Create(e[1], fade, { EmissiveStrength = 0 }):Play() end
	if light then TweenService:Create(light, fade, { Brightness = 0 }):Play() end
	task.delay(1.2, function()
		for _, e in embers do if e then e.Enabled = false end end
		if smoke then smoke.Enabled = false end
	end)
	-- 쓰러진 뒤 슬래그 껍질이 떨어져 나감
	task.delay(1.1, function()
		if chips then chips:Emit(25) end
		for _, p in model:GetChildren() do
			if p:IsA("MeshPart") and p.Name:match("__Slag$") and p.Parent then
				local w = p:FindFirstChild("Attach")
				if w then w:Destroy() end
				p.Massless = false
				p.CanCollide = true
				p.Anchored = false
				local out = (p.Position - model:GetPivot().Position) * Vector3.new(1, 0, 1)
				out = out.Magnitude > 0.01 and out.Unit or Vector3.xAxis
				p.AssemblyLinearVelocity = out * rng:NextNumber(2, 5) + Vector3.new(0, rng:NextNumber(2, 5), 0)
				p.AssemblyAngularVelocity = Vector3.new(rng:NextNumber(-4, 4), rng:NextNumber(-4, 4), rng:NextNumber(-4, 4))
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
local function seq(a, b) return NumberSequence.new(a, b) end
local function cseq(a, b) return ColorSequence.new(a, b) end

local function install(model, molten)
	for _, n in { "SlagFX" } do local o = model:FindFirstChild(n); if o then o:Destroy() end end
	local torso, slag, club = model.UpperTorso, model.UpperTorso__Slag, model.RightHand__Slag
	for _, p in { torso, slag, club } do
		for _, c in p:GetChildren() do
			if c:IsA("ParticleEmitter") or c:IsA("Light") or c:IsA("Sound") or (c:IsA("Attachment") and c.Name == "ClubTip") then c:Destroy() end
		end
	end
	local k = molten and 1 or 0
	local hot = Color3.fromRGB(255, 150, 60)
	local red = Color3.fromRGB(180, 40, 10)
	local light = Instance.new("PointLight")
	light.Name = "SlagGlow"; light.Color = Color3.fromRGB(255, 120, 40); light.Shadows = false
	light.Brightness = molten and 1.4 or 0.6; light.Range = molten and 10 or 6.5
	light.Parent = slag
	local emb = {
		Texture = "rbxasset://textures/particles/sparkles_main.dds", Color = cseq(hot, red), LightEmission = 1,
		Size = seq(0.09, 0), Lifetime = NumberRange.new(0.8, 1.6), Speed = NumberRange.new(0.8, 2.5),
		SpreadAngle = Vector2.new(40, 40), Acceleration = Vector3.new(0, 2.5, 0), Drag = 1,
		Rate = molten and 10 or 4, LightInfluence = 0,
	}
	emitter(slag, "Embers", emb)
	emb.Rate = molten and 6 or 2
	emitter(club, "Embers", emb)
	emitter(slag, "Smoke", {
		Texture = "rbxasset://textures/particles/smoke_main.dds", Color = cseq(Color3.fromRGB(60, 56, 52), Color3.fromRGB(40, 38, 36)),
		Transparency = seq(0.82, 1), Size = seq(0.5, 1.6), Lifetime = NumberRange.new(2, 3.2), Speed = NumberRange.new(0.4, 1.0),
		SpreadAngle = Vector2.new(25, 25), Acceleration = Vector3.new(0, 1.2, 0), Rate = molten and 4 or 1.5,
		Rotation = NumberRange.new(0, 360), RotSpeed = NumberRange.new(-20, 20),
	})
	emitter(slag, "HitSparks", {
		Texture = "rbxasset://textures/particles/sparkles_main.dds", Color = cseq(Color3.fromRGB(255, 210, 120), hot), LightEmission = 1,
		Size = seq(0.14, 0), Lifetime = NumberRange.new(0.25, 0.55), Speed = NumberRange.new(8, 14), SpreadAngle = Vector2.new(70, 70),
		Acceleration = Vector3.new(0, -30, 0), Drag = 2, Enabled = false, LightInfluence = 0,
	})
	emitter(slag, "HitChips", {
		Texture = "rbxasset://textures/particles/sparkles_main.dds", Color = cseq(Color3.fromRGB(40, 36, 34), Color3.fromRGB(25, 23, 22)),
		Size = seq(0.12, 0.08), Lifetime = NumberRange.new(0.5, 0.9), Speed = NumberRange.new(5, 9), SpreadAngle = Vector2.new(60, 60),
		Acceleration = Vector3.new(0, -40, 0), Rotation = NumberRange.new(0, 360), RotSpeed = NumberRange.new(-200, 200), Enabled = false,
	})
	-- 곤봉 아래 끝 (내려치기 먼지·불티 위치)
	local tip = Instance.new("Attachment")
	tip.Name = "ClubTip"
	tip.Position = Vector3.new(0, -club.Size.Y * 0.45, 0)
	tip.Parent = club
	emitter(tip, "SlamDust", {
		Texture = "rbxasset://textures/particles/smoke_main.dds", Color = cseq(Color3.fromRGB(95, 85, 75), Color3.fromRGB(70, 64, 58)),
		Transparency = seq(0.55, 1), Size = seq(0.8, 3), Lifetime = NumberRange.new(0.6, 1.2), Speed = NumberRange.new(4, 8),
		SpreadAngle = Vector2.new(80, 80), Drag = 4, Rotation = NumberRange.new(0, 360), Enabled = false,
	})
	emitter(tip, "SlamSparks", {
		Texture = "rbxasset://textures/particles/sparkles_main.dds", Color = cseq(Color3.fromRGB(255, 220, 140), hot), LightEmission = 1,
		Size = seq(0.16, 0), Lifetime = NumberRange.new(0.3, 0.7), Speed = NumberRange.new(10, 18), SpreadAngle = Vector2.new(85, 85),
		Acceleration = Vector3.new(0, -35, 0), Drag = 1.5, Enabled = false, LightInfluence = 0,
	})
	for name, d in SOUNDS do
		if name ~= "Crackle" or molten then
			local s = Instance.new("Sound")
			s.Name = name
			s.SoundId = "rbxassetid://" .. d[1]
			s.Volume = d[2]
			s.RollOffMode = Enum.RollOffMode.InverseTapered
			s.RollOffMinDistance = 8
			s.RollOffMaxDistance = d[3]
			s.Looped = name == "Crackle"
			s.Parent = torso
		end
	end
	local sc = Instance.new("Script")
	sc.Name = "SlagFX"
	sc.Source = FX_SOURCE
	sc:SetAttribute("Molten", molten)
	sc:SetAttribute("AttackAnim", ATTACK_ANIM)
	sc.Parent = model
	return k
end

local E = game.ServerStorage.Assets.Enemies
install(E.SlagWalker, false)
install(E.MoltenWalker, true)
return "installed"
