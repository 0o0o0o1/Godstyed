--!strict
-- 그림자 발걸음 연출 (Skills.shadow_step, kind "blink", vfx = "ShadowStep"). 단검 색 = 보라 + 흰 + 검은 연기.
-- 원본: 저장소 scripts/packages/Controllers/Vfx_ShadowStep.lua (Controllers 패키지 SkillController.Vfx.ShadowStep)
--   사라짐  0                        출발 자리: 몸이 어두운 잔상으로 남아 흩어짐 + 발밑 검은 연기 고리(바깥으로) + 보라 알갱이 조금
--                                    시전자 몸·무기 빛을 castDelay 동안 숨김 (모든 화면에서)
--   도착    castDelay                도착 자리: 검은 연기·보라 알갱이가 안쪽으로 빨려 들며 모임 + 세로 보라 틈 번쩍 + 몸이 다시 보임
--                                    (내 캐릭터면) 실제로 dest로 옮기고 적을 보게 회전 고정, 단검 콤보 첫 타 모션 (기본 공격과 같은 타이밍)
--   찌르기  castDelay + stabDelay      찌르는 방향으로 보라 칼날 궤적이 짧게 지나가고 사라짐
--   맞음    phase "hit" (서버)        맞은 자리에 작은 보라·흰 불꽃 + 짧은 섬광, 타격음
-- 칼날 궤적: 이 모듈 아래에 MeshPart "BladeMesh" 가 있으면 그 메시를 쓰고, 없으면 Beam 3개로 만든 임시 칼날(마름모)을 쓴다.
--   BladeMesh 규격: 길이 = 앞(-Z, LookVector) 방향, 피벗 = 칼날 꼬리 가운데. 크기·색·투명도는 메시에 넣은 값 그대로 (아래 BLADE_* 로 움직임만)
--   지금 들어 있는 것 (2026-11-25): Blender scripts/shadow_step_blade.py, 모델 에셋 127313928571413. 보라 Neon 바깥 + 자식 "Core" 흰 심
-- 판정·이동 거리·무적은 서버(Skill 서비스 blinkTarget/blinkDest/blinkHits)가 정한다. 이 모듈은 보이는 것만.
-- payload.timeScale 이면 개발 명령 /fx 미리보기 (이동·모션 없이 연출만, 맞음 연출도 이어서).

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local RunService = game:GetService("RunService")

local T = require(ReplicatedStorage.Shared.Config.VfxConfig).TEXTURES
local Skills = require(ReplicatedStorage.Shared.Data.Skills)
local CombatConfig = require(ReplicatedStorage.Shared.Config.CombatConfig)
local CameraShake = require(ReplicatedStorage.Shared.Util.CameraShake)
local Kit = require(script.Parent.Parent.VfxKit)

local SKILL = Skills.shadow_step
local CAST_DELAY = SKILL.castDelay
local STAB_DELAY = SKILL.stabDelay or 0.27
local seq = Kit.seq

-- 색 (단검 = 보라, VfxConfig.WEAPON_COLORS.Dagger)
local WHITE = Color3.new(1, 1, 1)
local PURPLE = Color3.fromRGB(110, 0, 230)
local PURPLE_SOFT = Color3.fromRGB(190, 130, 255)
local GHOST_COLOR = Color3.fromRGB(45, 10, 80) -- 어두운 잔상
local SMOKE = Color3.fromRGB(16, 10, 24) -- 검은 연기 (살짝 보라 기운)

-- 조정용 상수
local GHOST_LIFE = 0.35 -- 잔상이 흩어지는 시간
local GHOST_DRIFT = 0.8 -- 잔상이 뒤로 밀리는 거리
local DEPART_SMOKE_RADIUS = 3.2
local ARRIVE_SMOKE_RADIUS = 2.2
local FADE_IN = 0.08 -- 도착해서 몸이 다시 보이는 시간
local BLADE_LENGTH = 6.5 -- 칼날 궤적 길이 (스터드)
local BLADE_WIDTH = 0.8 -- 임시 칼날 가장 넓은 곳 (스터드)
local BLADE_TIP = 0.72 -- 가장 넓은 곳 위치 (꼬리 0 ~ 끝 1)
local BLADE_IN = 0.06 -- 칼날이 뻗는 시간
local BLADE_OUT = 0.14 -- 칼날이 사라지는 시간
local HIT_SHAKE_TIME, HIT_SHAKE_AMOUNT = 0.07, 0.12

local SOUNDS = {
	vanish = { id = "rbxassetid://125132253621935", volume = 0.45, speed = 0.8 }, -- Sword Whoosh Slash (낮게): 사라짐
	arrive = { id = "rbxassetid://125132253621935", volume = 0.5, speed = 1.35 }, -- 같은 소리 높게: 나타남
	stab = { id = "rbxassetid://9114159112", volume = 0.55, speed = 1.9, fadeAfter = 0.25 }, -- Doppler Whoosh (짧고 높게): 찌르기
	hit = { id = "rbxassetid://9113567601", volume = 0.85, speed = 1.3 }, -- Boxing Hits (Body Impact)
}
Kit.preloadSounds(SOUNDS)

local ShadowStep = {}

local function isMine(character: Instance?): boolean
	return character ~= nil and character == Players.LocalPlayer.Character
end

local function shakeCamera(time: number, amount: number)
	if not CameraShake.isEnabled() then
		return
	end
	local camera = workspace.CurrentCamera
	local name = "ShadowStepShake"
	pcall(function()
		RunService:UnbindFromRenderStep(name)
	end)
	local started = os.clock()
	RunService:BindToRenderStep(name, Enum.RenderPriority.Camera.Value + 1, function()
		local t = (os.clock() - started) / time
		if t >= 1 then
			RunService:UnbindFromRenderStep(name)
			return
		end
		local a = amount * (1 - t)
		camera.CFrame *= CFrame.new((math.random() - 0.5) * a, (math.random() - 0.5) * a, 0)
	end)
end

-- 단검 콤보 첫 타 (기본 공격과 같은 모션·타이밍). 없으면 기본 베기
local function animationId(character: Model): string?
	local anims = CombatConfig.ANIMATIONS.R15 :: any
	local weaponType = character:GetAttribute("HeldWeaponType")
	local list = weaponType and anims.combo[weaponType]
	if list and #list > 0 and list[1] ~= "" then
		return list[1]
	end
	return anims.slash
end

-- 몸 숨기기: 이 화면에서만 (LocalTransparencyModifier). 무기에 붙은 빛·파티클도 잠깐 끔.
-- 돌려준 함수(k: 0 = 다 보임, 1 = 숨김)로 다시 보이게 한다. 마지막에 꼭 0으로 부름
local function hideBody(character: Model): (number) -> ()
	local parts: { BasePart | Decal } = {}
	local paused: { Instance } = {}
	for _, d in character:GetDescendants() do
		if d:IsA("BasePart") or d:IsA("Decal") then
			table.insert(parts, d)
		elseif (d:IsA("ParticleEmitter") or d:IsA("Trail") or d:IsA("Beam") or d:IsA("Light")) and (d :: any).Enabled then
			(d :: any).Enabled = false
			table.insert(paused, d)
		end
	end
	local function set(k: number)
		for _, p in parts do
			if p.Parent then
				p.LocalTransparencyModifier = k
			end
		end
		if k <= 0 then
			for _, d in paused do
				if d.Parent then
					(d :: any).Enabled = true
				end
			end
			table.clear(paused)
		end
	end
	set(1)
	return set
end

-- 어두운 잔상: 지금 모습을 어두운 보라 복사본으로 남겨 뒤로 밀리며 흩어지게
local function ghost(ctx: Kit.Ctx, character: Model, away: Vector3)
	for _, part in character:GetDescendants() do
		if not part:IsA("BasePart") or part.Name == "HumanoidRootPart" or part.Transparency >= 0.9 then
			continue
		end
		local ok, copy = pcall(function()
			return part:Clone()
		end)
		if not ok or not copy then
			continue
		end
		local p = copy :: BasePart
		p:ClearAllChildren()
		Kit.decor(p)
		p.Massless = true
		p.Material = Enum.Material.Neon
		p.Color = GHOST_COLOR
		p.Transparency = 0.35
		p.LocalTransparencyModifier = 0
		if p:IsA("MeshPart") then
			p.TextureID = ""
		end
		p.CFrame = part.CFrame
		p.Parent = ctx.folder
		ctx:tween(p, GHOST_LIFE, { Transparency = 1, CFrame = part.CFrame + away * GHOST_DRIFT }, Enum.EasingStyle.Quad, Enum.EasingDirection.Out)
	end
end

-- 검은 연기 덩이 (Blender 렌더 플립북 FsSmokeDark)
local function smokeProps(extra: { [string]: any }): { [string]: any }
	local props: { [string]: any } = {
		Texture = T.FsSmokeDark,
		FlipbookLayout = Enum.ParticleFlipbookLayout.Grid4x4,
		FlipbookMode = Enum.ParticleFlipbookMode.OneShot,
		Color = ColorSequence.new(WHITE),
		LightEmission = 0,
		LightInfluence = 0.4,
		Rotation = NumberRange.new(0, 360),
		RotSpeed = NumberRange.new(-60, 60),
	}
	for k, v in extra do
		props[k] = v
	end
	return props
end

local function moteProps(extra: { [string]: any }): { [string]: any }
	local props: { [string]: any } = {
		Texture = T.HolySparkle,
		Color = ColorSequence.new(PURPLE_SOFT, PURPLE),
		LightEmission = 1,
		Brightness = 2,
		Rotation = NumberRange.new(0, 90),
	}
	for k, v in extra do
		props[k] = v
	end
	return props
end

-- 1. 사라짐 (출발 자리): 바깥으로 퍼지는 연기 + 잔상 + 위로 흩날리는 알갱이 조금
local function playVanish(ctx: Kit.Ctx, character: Model, origin: CFrame)
	local root = character:FindFirstChild("HumanoidRootPart")
	local at = if root and root:IsA("BasePart") then root.Position else origin.Position
	local ground = Kit.ground(at, { character, ctx.folder })
	ghost(ctx, character, -origin.LookVector)
	Kit.smokeRing(ctx, ground, DEPART_SMOKE_RADIUS, { duration = 0.75, count = 7, color = SMOKE, light = 0.6 })

	local holder = Kit.holder(ctx, CFrame.new(ground + Vector3.new(0, 1.2, 0)), "VanishSmoke")
	holder.Size = Vector3.new(2, 1.5, 2)
	local puff = Kit.emitter(ctx, holder, smokeProps({
		Size = seq({ { 0, 2.4 }, { 1, 4.2 } }),
		Transparency = seq({ { 0, 0.25 }, { 0.6, 0.5 }, { 1, 1 } }),
		Lifetime = NumberRange.new(0.45, 0.6),
		Speed = NumberRange.new(1.5, 3.5),
		SpreadAngle = Vector2.new(180, 180),
		Acceleration = Vector3.new(0, 2.5, 0),
		Drag = 3,
		Shape = Enum.ParticleEmitterShape.Box,
	}))
	puff:Emit(5)
	local motes = Kit.emitter(ctx, holder, moteProps({
		Size = seq({ { 0, 0.3 }, { 1, 0 } }),
		Transparency = seq({ { 0, 0 }, { 1, 1 } }),
		Lifetime = NumberRange.new(0.35, 0.6),
		Speed = NumberRange.new(3, 7),
		SpreadAngle = Vector2.new(180, 180),
		Acceleration = Vector3.new(0, 5, 0),
		Drag = 4,
		Shape = Enum.ParticleEmitterShape.Box,
	}))
	motes:Emit(9)
	Kit.casterSound(SOUNDS.vanish, character, at)
end

-- 2. 도착 (적 뒤): 안쪽으로 빨려 드는 연기·알갱이 + 세로 보라 틈 번쩍 (출발 자리와 반대 방향 움직임으로 구분)
local function playArrive(ctx: Kit.Ctx, character: Model, dest: CFrame)
	local ground = Kit.ground(dest.Position, { character, ctx.folder })
	local center = CFrame.new(dest.Position)
	local shell = Kit.holder(ctx, center, "ArriveShell")
	shell.Size = Vector3.new(5, 6, 5)
	local smoke = Kit.emitter(ctx, shell, smokeProps({
		Size = seq({ { 0, 2.2 }, { 1, 0.6 } }),
		Transparency = seq({ { 0, 0.6 }, { 0.3, 0.3 }, { 1, 1 } }),
		Lifetime = NumberRange.new(0.25, 0.32),
		Speed = NumberRange.new(8, 11),
		Shape = Enum.ParticleEmitterShape.Sphere,
		ShapeInOut = Enum.ParticleEmitterShapeInOut.Inward,
		ShapeStyle = Enum.ParticleEmitterShapeStyle.Surface,
	}))
	smoke:Emit(8)
	local motes = Kit.emitter(ctx, shell, moteProps({
		Size = seq({ { 0, 0.35 }, { 1, 0.05 } }),
		Transparency = seq({ { 0, 0.2 }, { 1, 0.8 } }),
		Lifetime = NumberRange.new(0.18, 0.26),
		Speed = NumberRange.new(13, 17),
		Shape = Enum.ParticleEmitterShape.Sphere,
		ShapeInOut = Enum.ParticleEmitterShapeInOut.Inward,
		ShapeStyle = Enum.ParticleEmitterShapeStyle.Surface,
	}))
	motes:Emit(14)
	Kit.smokeRing(ctx, ground, ARRIVE_SMOKE_RADIUS, { duration = 0.55, count = 5, color = SMOKE, light = 0.6 })

	-- 세로 틈: 가는 보라 막대가 위아래로 열렸다가 옆으로 닫히며 사라짐
	local rift = Instance.new("Part")
	rift.Name = "ArriveRift"
	rift.Material = Enum.Material.Neon
	rift.Color = PURPLE_SOFT
	rift.Transparency = 0.1
	rift.Size = Vector3.new(0.12, 0.2, 0.12)
	Kit.decor(rift)
	rift.CFrame = dest
	rift.Parent = ctx.folder
	ctx:tween(rift, 0.06, { Size = Vector3.new(0.12, 6, 0.12) }, Enum.EasingStyle.Quad, Enum.EasingDirection.Out)
	ctx:tween(rift, 0.14, { Size = Vector3.new(0.01, 6.5, 0.01), Transparency = 1 }, Enum.EasingStyle.Quad, Enum.EasingDirection.In, 0.06)
	local light = Instance.new("PointLight")
	light.Color, light.Range, light.Brightness, light.Shadows = PURPLE, 10, 3, false
	light.Parent = shell
	ctx:tween(light, 0.3, { Brightness = 0 })
	Kit.casterSound(SOUNDS.arrive, character, dest.Position)
end

-- 3. 찌르기 칼날 궤적: from 에서 dir 쪽으로 짧게 뻗었다 사라짐
local function playBlade(ctx: Kit.Ctx, from: Vector3, dir: Vector3)
	local template = script:FindFirstChild("BladeMesh")
	if template and template:IsA("MeshPart") then
		-- Blender 메시 (스킬 전용, 이 모듈 아래에 둠): 꼬리 피벗을 from 에 두고 앞으로 밀며 사라짐
		-- 자식 MeshPart(흰 심 "Core" 등)는 바깥 메시와의 상대 위치를 그대로 두고 같이 움직임
		local m = template:Clone()
		local pieces: { BasePart } = { m }
		for _, c in template:GetChildren() do
			if c:IsA("BasePart") then
				local copy = m:FindFirstChild(c.Name) :: BasePart
				copy.Parent = ctx.folder
				table.insert(pieces, copy)
			end
		end
		m:PivotTo(CFrame.lookAt(from, from + dir))
		local move = dir * (BLADE_LENGTH * 0.35)
		for i, p in pieces do
			Kit.decor(p)
			if i > 1 then
				p.CFrame = m.CFrame * template.CFrame:ToObjectSpace(template:FindFirstChild(p.Name).CFrame)
			end
			p.Parent = ctx.folder
			-- 찌르는 쪽으로 밀려나가며 BLADE_IN 뒤부터 사라짐
			ctx:tween(p, BLADE_IN + BLADE_OUT, { CFrame = p.CFrame + move }, Enum.EasingStyle.Quad, Enum.EasingDirection.Out)
			ctx:tween(p, BLADE_OUT, { Transparency = 1 }, Enum.EasingStyle.Quad, Enum.EasingDirection.In, BLADE_IN)
		end
		return
	end
	-- 임시 칼날 (메시 없음): 꼬리·넓은 곳·끝 세 점을 Beam 으로 이어 마름모 칼날. 바깥 보라 + 안쪽 흰 심
	local points = {}
	for i, name in { "Tail", "Mid", "Tip" } do
		local p = Kit.holder(ctx, CFrame.new(from), "Blade" .. name)
		local a = Instance.new("Attachment")
		a.Parent = p
		points[i] = { part = p, att = a }
	end
	local beams: { { beam: Beam, base: number } } = {}
	local function beam(a0: Attachment, a1: Attachment, w0: number, w1: number, color: Color3, base: number)
		local b = Instance.new("Beam")
		b.Attachment0, b.Attachment1 = a0, a1
		b.Width0, b.Width1 = w0, w1
		b.Color = ColorSequence.new(color)
		b.LightEmission = 1
		b.LightInfluence = 0
		b.Brightness = 3
		b.FaceCamera = true
		b.Segments = 1
		b.Transparency = NumberSequence.new(base)
		b.Parent = points[1].part
		table.insert(beams, { beam = b, base = base })
	end
	local tail, mid, tip = points[1].att, points[2].att, points[3].att
	beam(tail, mid, 0.04, BLADE_WIDTH, PURPLE, 0.1)
	beam(mid, tip, BLADE_WIDTH, 0, PURPLE, 0.1)
	beam(tail, mid, 0.02, BLADE_WIDTH * 0.3, WHITE, 0)
	beam(mid, tip, BLADE_WIDTH * 0.3, 0, WHITE, 0)
	local t0 = ctx:clock()
	ctx:step(t0 + BLADE_IN + BLADE_OUT, function(t)
		local k = t - t0
		-- 끝은 빠르게 뻗고, 꼬리는 늦게 따라와 칼날이 앞으로 빠져나감
		local head = math.clamp(k / BLADE_IN, 0, 1)
		head = 1 - (1 - head) ^ 3
		local back = math.clamp(k / (BLADE_IN + BLADE_OUT), 0, 1) ^ 1.6
		local tipAt = BLADE_LENGTH * head
		local tailAt = BLADE_LENGTH * 0.85 * back
		points[3].part.CFrame = CFrame.new(from + dir * tipAt)
		points[1].part.CFrame = CFrame.new(from + dir * tailAt)
		points[2].part.CFrame = CFrame.new(from + dir * (tailAt + (tipAt - tailAt) * BLADE_TIP))
		local fade = math.clamp((k - BLADE_IN) / BLADE_OUT, 0, 1)
		for _, b in beams do
			b.beam.Transparency = NumberSequence.new(b.base + (1 - b.base) * fade)
		end
	end)
end

-- 4. 맞음: 작은 보라·흰 불꽃 + 짧은 섬광
local function playHit(payload: any, character: Model)
	local ctx = Kit.begin("ShadowStepHit", 0.8, payload.timeScale)
	local dest = payload.origin :: CFrame
	local point = if typeof(payload.point) == "Vector3" then payload.point else (dest * CFrame.new(0, 0, -(SKILL.behindDistance or 3.5))).Position
	local dir = (point - dest.Position) * Vector3.new(1, 0, 1)
	dir = if dir.Magnitude > 1e-3 then dir.Unit else dest.LookVector
	local holder = Kit.holder(ctx, CFrame.lookAt(point, point + dir), "HitSpark")
	local white = Kit.emitter(ctx, holder, {
		Texture = T.EbSpark,
		Color = ColorSequence.new(WHITE),
		LightEmission = 1,
		Brightness = 3,
		Size = seq({ { 0, 0.45 }, { 1, 0 } }),
		Transparency = seq({ { 0, 0 }, { 1, 0.6 } }),
		Lifetime = NumberRange.new(0.1, 0.2),
		Speed = NumberRange.new(22, 32),
		SpreadAngle = Vector2.new(35, 35),
		EmissionDirection = Enum.NormalId.Front,
		Orientation = Enum.ParticleOrientation.VelocityParallel,
		Drag = 6,
	})
	white:Emit(7)
	local purple = Kit.emitter(ctx, holder, {
		Texture = T.EbSpark,
		Color = ColorSequence.new(PURPLE_SOFT, PURPLE),
		LightEmission = 1,
		Brightness = 2.5,
		Size = seq({ { 0, 0.6 }, { 1, 0 } }),
		Transparency = seq({ { 0, 0 }, { 1, 0.7 } }),
		Lifetime = NumberRange.new(0.15, 0.28),
		Speed = NumberRange.new(12, 22),
		SpreadAngle = Vector2.new(70, 70),
		EmissionDirection = Enum.NormalId.Front,
		Orientation = Enum.ParticleOrientation.VelocityParallel,
		Acceleration = Vector3.new(0, -20, 0),
		Drag = 5,
	})
	purple:Emit(10)
	local flash = Instance.new("Part")
	flash.Name = "HitFlash"
	flash.Shape = Enum.PartType.Ball
	flash.Material = Enum.Material.Neon
	flash.Color = WHITE
	flash.Transparency = 0.1
	flash.Size = Vector3.new(0.4, 0.4, 0.4)
	Kit.decor(flash)
	flash.CFrame = CFrame.new(point)
	flash.Parent = ctx.folder
	ctx:tween(flash, 0.12, { Size = Vector3.new(1.8, 1.8, 1.8), Transparency = 1, Color = PURPLE_SOFT })
	local light = Instance.new("PointLight")
	light.Color, light.Range, light.Brightness, light.Shadows = PURPLE_SOFT, 9, 4, false
	light.Parent = holder
	ctx:tween(light, 0.18, { Brightness = 0 })
	Kit.sound(SOUNDS.hit, if isMine(character) then nil else point)
	if isMine(character) and payload.timeScale == nil then
		shakeCamera(HIT_SHAKE_TIME, HIT_SHAKE_AMOUNT)
	end
end

local function playCast(payload: any, character: Model)
	local origin = payload.origin :: CFrame
	local dest = if typeof(payload.dest) == "CFrame" then payload.dest else origin
	local stabDelay = if type(payload.stabDelay) == "number" then payload.stabDelay else STAB_DELAY
	local preview = payload.timeScale ~= nil
	local mine = isMine(character) and not preview
	local ctx = Kit.begin("ShadowStep", CAST_DELAY + stabDelay + 1.2, payload.timeScale)
	-- 연출 시작 기준 시각에 실행 (잔상 복제 등 앞 작업이 걸린 시간만큼 밀리지 않게)
	local function atAbs(seconds: number, fn: () -> ())
		ctx:at(math.max(seconds - ctx:clock(), 0), fn)
	end
	local humanoid = character:FindFirstChildOfClass("Humanoid")
	local root = character:FindFirstChild("HumanoidRootPart") :: BasePart?

	-- 사라짐 → castDelay 동안 몸 숨김 (미리보기는 숨기지 않음)
	playVanish(ctx, character, origin)
	local setHidden: ((number) -> ())? = if preview then nil else hideBody(character)
	local unlock: (() -> ())? = nil
	if mine and humanoid then
		unlock = Kit.lockRotation(humanoid)
	end
	local restored = false
	local function restore()
		if restored then
			return
		end
		restored = true
		if setHidden then
			setHidden(0)
		end
		if unlock then
			unlock()
		end
	end
	-- 연출이 끝나기 전에 무엇이 실패해도 몸은 반드시 다시 보이게 (ctx 와 상관없이)
	task.delay((CAST_DELAY + stabDelay + 0.5) / ctx.scale, restore)

	atAbs(CAST_DELAY, function()
		-- 내 캐릭터: 서버가 정한 자리로 옮기고 적을 봄 + 단검 첫 타 모션 (기본 공격 windup 과 같아 stabDelay 에 찌름)
		if mine and root and humanoid and humanoid.Health > 0 then
			root.AssemblyLinearVelocity = Vector3.zero
			character:PivotTo(dest)
			local animator = humanoid:FindFirstChildOfClass("Animator")
			local id = animationId(character)
			if animator and id then
				local animation = Instance.new("Animation")
				animation.AnimationId = id
				local ok, track = pcall(animator.LoadAnimation, animator, animation)
				if ok and track then
					track.Priority = Enum.AnimationPriority.Action2
					track.Looped = false
					track:Play(0.05)
				end
			end
		end
		playArrive(ctx, character, dest)
		if setHidden then
			local hide = setHidden
			local t0 = ctx:clock()
			ctx:step(t0 + FADE_IN, function(t)
				hide(1 - math.clamp((t - t0) / FADE_IN, 0, 1))
			end)
			ctx:at(FADE_IN, function()
				hide(0)
			end)
		end
	end)

	atAbs(CAST_DELAY + stabDelay, function()
		local target = payload.target
		local targetRoot = typeof(target) == "Instance" and target:FindFirstChild("HumanoidRootPart")
		local from = dest.Position + Vector3.new(0, 0.3, 0) - dest.LookVector * 0.6
		local dir = dest.LookVector
		if targetRoot and targetRoot:IsA("BasePart") then
			local v = targetRoot.Position - from
			if v.Magnitude > 0.5 then
				dir = v.Unit
			end
		end
		playBlade(ctx, from, dir)
		Kit.casterSound(SOUNDS.stab, character, dest.Position)
		if preview then
			playHit({ origin = dest, timeScale = payload.timeScale, point = from + dir * (SKILL.behindDistance or 3.5) }, character)
		end
	end)
	atAbs(CAST_DELAY + stabDelay + 0.3, restore)
end

function ShadowStep.play(payload: any, character: Model)
	if payload.phase == "hit" then
		playHit(payload, character)
		return
	end
	playCast(payload, character)
end

return ShadowStep
