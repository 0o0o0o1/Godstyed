-- Furnace Tender / Warden 소리·효과 설치 (Studio MCP execute_luau 로 실행). 공용 Services 코드는 건드리지 않음.
-- TenderFX 는 살아 있는 적(Humanoid 있음)과 시체 복제본(Humanoid 없음) 둘 다에서 돈다.
local ATTACK_ANIM = "rbxassetid://140592601845071"
local SOUNDS = { -- ProSoundEffects: id, 볼륨, 최대 거리
	Rustle = {9114576499, 0.22, 45},     -- 뻣뻣한 내열복 스침 (걸음마다)
	Step = {9113526269, 0.35, 55},       -- 발걸음 (낮은 음)
	Breath1 = {9114628818, 0.45, 70}, Breath2 = {9114628321, 0.45, 70}, -- 후드 안 거친 숨 (낮은 음)
	LanceHiss = {9119166195, 0.1, 30},   -- 달아오른 끝 지글거림 (반복)
	Thrust = {9119468100, 0.4, 55},      -- 찌르는 바람 소리
	Impact = {9119166424, 0.6, 70}, Clang = {9119072660, 0.4, 60},    -- 타격: 지글 + 쇠
	HitRip = {9113828720, 0.45, 55}, HitSizzle = {9119165650, 0.3, 50}, -- 맞을 때: 은박 찢김 + 지글
	DeathHiss = {9119166199, 0.55, 70}, DeathRip = {9113836270, 0.5, 60},
}

local FX_SOURCE = [==[
-- TenderFX: Furnace Tender / Warden 소리·효과 (모델 안 스크립트, scripts/furnace_tender_fx.lua 가 설치)
local TweenService = game:GetService("TweenService")
local model = script.Parent
local attackAnim = script:GetAttribute("AttackAnim")
local hum = model:FindFirstChildOfClass("Humanoid")
local torso = model:WaitForChild("UpperTorso", 5)
local hot = model:FindFirstChild("RightHand__Hot")
local glow = model:FindFirstChild("Head__Glow")
local suit = model:FindFirstChild("UpperTorso__Suit")
if not (torso and hot and glow and suit) then return end
local rng = Random.new()
local function snd(n) return torso:FindFirstChild(n) end
local function play(n, lo, hi, stopAfter)
	local s = snd(n)
	if not s then return end
	s.PlaybackSpeed = rng:NextNumber(lo or 1, hi or 1)
	s:Play()
	if stopAfter then task.delay(stopAfter, function() s:Stop() end) end
end
local tipLight = hot:FindFirstChild("TipGlow")
local visorLight = glow:FindFirstChild("VisorGlow")
local embers = hot:FindFirstChild("Embers")
local heat = hot:FindFirstChild("Heat")
local tip = hot:FindFirstChild("LanceTip")
local thrustSparks = tip and tip:FindFirstChild("ThrustSparks")
local hitSparks = suit:FindFirstChild("HitSparks")

if hum then
	local alive = true
	local hiss = snd("LanceHiss")
	if hiss then hiss.Looped = true; hiss:Play() end
	task.spawn(function()
		local step = 0
		while alive do
			local root = model:FindFirstChild("HumanoidRootPart")
			local speed = root and (root.AssemblyLinearVelocity * Vector3.new(1, 0, 1)).Magnitude or 0
			if hum.MoveDirection.Magnitude > 0.1 and speed > 1 then
				step += 1
				play("Step", 0.7, 0.82, 0.5)
				play("Rustle", 1.0, 1.25, 0.45)
				task.wait(math.clamp(4.6 / speed, 0.35, 0.9))
			else
				task.wait(0.2)
			end
		end
	end)
	task.spawn(function()
		while alive do
			task.wait(hum.WalkSpeed > 8 and rng:NextNumber(3.5, 7) or rng:NextNumber(6, 12))
			if alive then play(rng:NextInteger(1, 2) == 1 and "Breath1" or "Breath2", 0.5, 0.62) end
		end
	end)
	local lastHealth, lastHit = hum.Health, 0
	hum.HealthChanged:Connect(function(h)
		if h < lastHealth and h > 0 and os.clock() - lastHit > 0.15 then
			lastHit = os.clock()
			if hitSparks then hitSparks:Emit(12) end
			play("HitRip", 0.85, 1.1)
			play("HitSizzle", 0.9, 1.1)
		end
		lastHealth = h
	end)
	local animator = hum:FindFirstChildOfClass("Animator") or hum:WaitForChild("Animator", 5)
	local hooked = {}
	if animator and attackAnim then
		animator.AnimationPlayed:Connect(function(track)
			if track.Animation and track.Animation.AnimationId == attackAnim then
				local sp = math.max(track.Speed, 0.05)
				task.delay(0.42 / sp, function() play("Thrust", 0.7, 0.8, 0.6) end)
				if not hooked[track] then
					hooked[track] = true
					track:GetMarkerReachedSignal("Impact"):Connect(function()
						play("Impact", 0.9, 1.1)
						play("Clang", 0.8, 0.95)
						if thrustSparks then thrustSparks:Emit(22) end
						if tipLight then
							local b = tipLight.Brightness
							tipLight.Brightness = b * 3
							TweenService:Create(tipLight, TweenInfo.new(0.35), { Brightness = b }):Play()
						end
					end)
				end
			end
		end)
	end
	hum.Died:Once(function()
		alive = false
		for _, s in torso:GetChildren() do if s:IsA("Sound") then s:Stop() end end
		for _, e in { embers, heat } do if e then e.Enabled = false end end
		for _, l in { tipLight, visorLight } do if l then l.Enabled = false end end
	end)
else
	-- 시체 복제본: 후드 빛과 개공봉 열기가 식어 꺼지고, 개공봉(덩치는 방패도)이 떨어짐
	play("DeathRip", 0.8, 0.95)
	task.delay(0.2, function() play("DeathHiss", 0.6, 0.75) end)
	local fade = TweenInfo.new(3, Enum.EasingStyle.Quad, Enum.EasingDirection.In)
	TweenService:Create(glow, fade, { Color = Color3.fromRGB(20, 12, 8) }):Play()
	TweenService:Create(hot, TweenInfo.new(4, Enum.EasingStyle.Quad, Enum.EasingDirection.In), { Color = Color3.fromRGB(45, 25, 20) }):Play()
	for _, l in { tipLight, visorLight } do if l then TweenService:Create(l, fade, { Brightness = 0 }):Play() end end
	task.delay(1.5, function()
		glow.Material = Enum.Material.SmoothPlastic
		for _, e in { embers, heat } do if e then e.Enabled = false end end
	end)
	task.delay(4, function() hot.Material = Enum.Material.Metal end)
	task.delay(0.6, function()
		for _, p in model:GetChildren() do
			if p:IsA("MeshPart") and (p.Name:match("^RightHand__") and p.Name ~= "RightHand__Suit" or p.Name == "LeftLowerArm__Plate") then
				local w = p:FindFirstChild("Attach")
				if w then w:Destroy() end
				p.Massless = false
				p.CanCollide = true
				p.Anchored = false
				p.AssemblyLinearVelocity = Vector3.new(rng:NextNumber(-2, 2), rng:NextNumber(0, 2), rng:NextNumber(-2, 2))
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

local function install(model, big)
	local o = model:FindFirstChild("TenderFX"); if o then o:Destroy() end
	local torso, hot, glow, suit = model.UpperTorso, model.RightHand__Hot, model.Head__Glow, model.UpperTorso__Suit
	for _, p in { torso, hot, glow, suit } do
		for _, c in p:GetChildren() do
			if c:IsA("ParticleEmitter") or c:IsA("Sound") or c:IsA("Light") or (c:IsA("Attachment") and c.Name == "LanceTip") then c:Destroy() end
		end
	end
	local orange = Color3.fromRGB(255, 120, 40)
	local tl = Instance.new("PointLight"); tl.Name = "TipGlow"; tl.Color = orange; tl.Brightness = 1.0; tl.Range = big and 9 or 7; tl.Shadows = false; tl.Parent = hot
	local vl = Instance.new("PointLight"); vl.Name = "VisorGlow"; vl.Color = orange; vl.Brightness = 0.6; vl.Range = 4; vl.Shadows = false; vl.Parent = glow
	emitter(hot, "Embers", {
		Texture = "rbxasset://textures/particles/sparkles_main.dds",
		Color = ColorSequence.new(Color3.fromRGB(255, 180, 80), Color3.fromRGB(200, 50, 10)), LightEmission = 1, LightInfluence = 0,
		Size = NumberSequence.new(0.07, 0), Lifetime = NumberRange.new(0.5, 1.1), Speed = NumberRange.new(0.6, 1.8),
		SpreadAngle = Vector2.new(50, 50), Acceleration = Vector3.new(0, 3, 0), Drag = 1, Rate = 6,
	})
	emitter(hot, "Heat", {
		Texture = "rbxasset://textures/particles/smoke_main.dds",
		Color = ColorSequence.new(Color3.fromRGB(70, 66, 62), Color3.fromRGB(50, 48, 46)),
		Transparency = NumberSequence.new(0.88, 1), Size = NumberSequence.new(0.2, 0.9), Lifetime = NumberRange.new(1, 1.8),
		Speed = NumberRange.new(0.3, 0.7), Acceleration = Vector3.new(0, 1.5, 0), Rate = 2, Rotation = NumberRange.new(0, 360),
	})
	local spark = {
		Texture = "rbxasset://textures/particles/sparkles_main.dds",
		Color = ColorSequence.new(Color3.fromRGB(255, 225, 150), Color3.fromRGB(255, 120, 40)), LightEmission = 1, LightInfluence = 0,
		Size = NumberSequence.new(0.13, 0), Lifetime = NumberRange.new(0.25, 0.55), Speed = NumberRange.new(8, 15),
		SpreadAngle = Vector2.new(65, 65), Acceleration = Vector3.new(0, -30, 0), Drag = 2, Enabled = false,
	}
	emitter(suit, "HitSparks", spark)
	local tip = Instance.new("Attachment"); tip.Name = "LanceTip"; tip.Parent = hot
	emitter(tip, "ThrustSparks", spark)
	local n = 0
	for name, d in SOUNDS do
		local s = Instance.new("Sound")
		s.Name = name; s.SoundId = "rbxassetid://" .. d[1]; s.Volume = d[2]
		s.RollOffMode = Enum.RollOffMode.InverseTapered; s.RollOffMinDistance = 8; s.RollOffMaxDistance = d[3]
		s.Parent = torso
		n += 1
	end
	local sc = Instance.new("Script")
	sc.Name = "TenderFX"
	sc.Source = FX_SOURCE
	sc:SetAttribute("AttackAnim", ATTACK_ANIM)
	sc.Parent = model
	return n
end

local E = game.ServerStorage.Assets.Enemies
return "installed " .. install(E.FurnaceTender, false) .. " / " .. install(E.FurnaceWarden, true)
