--!strict
-- 칼날 회오리 연출 v5 (Skills.blade_whirl, kind "whirl", vfx = "BladeWhirl"). 흰 + 선명한 보라 + 어두운 결.
-- 원본: 저장소 scripts/packages/Controllers/Vfx_BladeWhirl.lua (Controllers 패키지 SkillController.Vfx.BladeWhirl)
-- v5 (2026-11-25 사용자 "무료 Slash VFX System 기반으로 다시"): 베기 = Creator Store 무료 에셋 "Slash VFX System"
--   (MorphoTheNoob, 85889779196357, "Free to use")의 휘어진 텍스처 빔 초승달(빔 5겹) + 평면 초승달 플립북 + 불꽃·별·번개를
--   모듈 아래 Part "WhirlKit" 에 모아 둔 것(CrescentA/CrescentB 빔, Slash 플립북, Burst 터짐)을 복제해서 씀.
--   v3·v4 의 SurfaceAppearance 메시 칼날은 화면에서 거의 안 보여서(어둡고 투명) 버림. v1~v4 는 git 기록.
-- 2026-11-26: 키트 색 = 흰 + 단검 보라(110,0,230) + 라일락 규칙, 빔 3장·플립북 3장 텍스처는 자체 그림
--   (scripts/vfx_whirl_brush.py, Python 붓질)로 교체. 무료 키트 원래 텍스처는 각 빔·이미터 속성 OrigTexture. 터짐(Burst)은 키트 그대로.
--   발동      0                 가슴 앞 짧은 흰 섬광 + 반짝이, 플레이어 오라(테두리 빛·발밑 원·솟는 불티·빛기둥) 시작
--   연속 베기  castDelay ~ 0.85   보통 초승달 8개 (수평·대각·높낮이·크기·휘두르는 방향이 모두 다름), 각각 자기 평면 안에서 휘둘러지며 나타났다 사라짐
--   강조 베기  0.36 / 0.67        큰 초승달 2개 (서버 1·2타 0.4·0.7 직전) + 터짐 조금
--   마무리     1.0(서버 3타)       꽃잎 터짐 (2026-11-26 사용자: 마지막 X 베기를 빼고 꽃잎이 날리며 터지게 — 보라 + 흰 끝, 소용돌이쳐 퍼진 뒤 흩날림, 많고 작게)
--                                몸 둘레 18곳에서 회전 방향(접선)으로 비스듬히 바깥으로 꽃잎이 튀어 반경(16)까지 소용돌이치며 퍼지고, 느려진 뒤 천천히 흩날려 떨어짐
--                                + 천천히 떠도는 두 번째 꽃잎 + 몸 가까이 큰 꽃잎 몇 장 + 은은한 섬광. 꽃잎 = 자체 플립북 (scripts/vfx_whirl_petals*.py, Blender 렌더 + Python 빛 번짐)
--   맞음      phase "hit"        맞은 자리 흰·보라 불꽃 + 작은 섬광 (서버 타격 하나 = 연출 하나)
--   몸        (내 캐릭터) castDelay 부터 spinTime 동안 왼쪽 turns 바퀴, 단검 첫 타 휘두른 자세 멈춤
-- WhirlKit 초승달 규격: CrescentA(로컬 0,-7) → CrescentB(0,+7), 빔이 로컬 -Z 쪽으로 반지름 약 7 만큼 불룩 = 원점을 감싸는 반원,
--   평면 법선 = 로컬 X. 법선(X) 둘레로 돌리면 자기 평면 안에서 휘둘러짐
-- 판정·피해·타격 시각은 서버(Skill 서비스 whirlHits)가 정한다. 이 모듈은 보이는 것과 내 캐릭터 회전만.
-- payload.timeScale 이면 개발 명령 /fx 미리보기 (몸 회전·모션 없이, 맞음 연출은 타 시각마다 앞에 하나씩).

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local T = require(ReplicatedStorage.Shared.Config.VfxConfig).TEXTURES
local Skills = require(ReplicatedStorage.Shared.Data.Skills)
local CombatConfig = require(ReplicatedStorage.Shared.Config.CombatConfig)
local Kit = require(script.Parent.Parent.VfxKit)

local SKILL = Skills.blade_whirl
local seq = Kit.seq

local WHITE = Color3.new(1, 1, 1)
local PURPLE = Color3.fromRGB(140, 40, 255)
local PURPLE_SOFT = Color3.fromRGB(205, 160, 255)

local HOLD_FRACTION = 0.55 -- 단검 첫 타를 휘두른 자세 (길이 대비)
local GROUND_IMAGE = "rbxassetid://88252622732116" -- 발밑 빛 원 (scripts/vfx_whirl_slash_tex.py WhirlGround)
local KIT = script:WaitForChild("WhirlKit") -- 무료 Slash VFX System 재료 (위 설명)
local ARC_R = 7 -- 키트 초승달 반지름 (스터드, 크기 1 기준)

-- 베기 배치표. t = 시전 후 시각, mesh = "SlashA" 보통 / "SlashB" 강조(크고 굵게), yaw = 그 순간 몸 방향에서 더 돌린 각(도),
-- tilt = 칼날 평면을 기울인 각(도, 0 = 수평), h = 허리에서 높이, k0→k1 = 크기(1 = 반지름 7), sweep = 휘두르는 각(도), dir = 1 왼쪽 / -1 반대, life = 보이는 시간
type SlashSpec = { t: number, mesh: string, yaw: number, tilt: number, h: number, k0: number, k1: number, sweep: number, dir: number, life: number }
local SLASHES: { SlashSpec } = {
	{ t = 0.10, mesh = "SlashA", yaw = 0, tilt = 0, h = 0.0, k0 = 0.85, k1 = 1.05, sweep = 110, dir = 1, life = 0.2 },
	{ t = 0.18, mesh = "SlashA", yaw = 150, tilt = 40, h = 0.7, k0 = 0.8, k1 = 1.0, sweep = 120, dir = -1, life = 0.2 },
	{ t = 0.26, mesh = "SlashA", yaw = 260, tilt = -35, h = -0.6, k0 = 0.9, k1 = 1.1, sweep = 110, dir = 1, life = 0.2 },
	{ t = 0.36, mesh = "SlashB", yaw = 30, tilt = 18, h = 0.2, k0 = 0.9, k1 = 1.15, sweep = 140, dir = 1, life = 0.28 },
	{ t = 0.46, mesh = "SlashA", yaw = 200, tilt = 60, h = 1.0, k0 = 0.8, k1 = 1.0, sweep = 120, dir = -1, life = 0.2 },
	{ t = 0.54, mesh = "SlashA", yaw = 310, tilt = -55, h = -0.4, k0 = 0.9, k1 = 1.1, sweep = 110, dir = 1, life = 0.2 },
	{ t = 0.62, mesh = "SlashA", yaw = 100, tilt = 5, h = -0.9, k0 = 0.95, k1 = 1.15, sweep = 110, dir = -1, life = 0.2 },
	{ t = 0.67, mesh = "SlashB", yaw = 230, tilt = -25, h = 0.5, k0 = 0.95, k1 = 1.2, sweep = 150, dir = -1, life = 0.28 },
	{ t = 0.76, mesh = "SlashA", yaw = 20, tilt = 75, h = 0.3, k0 = 0.85, k1 = 1.05, sweep = 120, dir = 1, life = 0.2 },
	{ t = 0.84, mesh = "SlashA", yaw = 170, tilt = -15, h = 0.8, k0 = 0.8, k1 = 1.0, sweep = 110, dir = -1, life = 0.2 },
}
-- 마무리 꽃잎 터짐 (서버 3타와 같은 시각)
local FINISH_FLASH = 1.0
-- 꽃잎 플립북 4x4 (16칸 = 기울어진 축으로 한 바퀴, 반복 재생). a = 끝이 둥근 잎, b = 가늘고 뾰족한 잎. 색이 들어 있어 Color 흰색
local PETALS = { "rbxassetid://79525251161536", "rbxassetid://78183119470395" }
local PETAL_LIFE = 4.2 -- 꽃잎이 다 사라질 때까지 (연출 폴더 수명에 더함, 가장 긴 꽃잎 수명 3.8 + 여유)
-- 꽃잎 투명도: 절반쯤부터 서서히 옅어져 끝에 사라짐 (사용자: 뚝 사라짐 → 70% 까지 불투명했다가 크기까지 0 으로 줄어 터지듯 사라졌음)
local PETAL_FADE = { { 0, 0 }, { 0.4, 0.04 }, { 0.75, 0.4 }, { 1, 1 } }

local SOUNDS = {
	flash = { id = "rbxassetid://125132253621935", volume = 0.4, speed = 1.1 }, -- Sword Whoosh Slash
	slashB = { id = "rbxassetid://125132253621935", volume = 0.5, speed = 1.45 },
	turn = { id = "rbxassetid://125132253621935", volume = 0.35, speed = 1.3 }, -- 바퀴마다
	finish = { id = "rbxassetid://9116687945", volume = 0.7, speed = 1.35 }, -- Metal Impacts 20: 맑은 쇠 울림
	hit = { id = "rbxassetid://9113567601", volume = 0.6, speed = 1.4 }, -- Boxing Hits (Body Impact)
}
Kit.preloadSounds(SOUNDS)

local BladeWhirl = {}
local warned = false

local function isMine(character: Instance?): boolean
	local lp = Players.LocalPlayer -- 편집 화면 미리보기에서는 없음
	return character ~= nil and lp ~= nil and character == lp.Character
end

local function yawOf(look: Vector3): number
	return math.atan2(-look.X, -look.Z)
end

local function animationId(character: Model): string?
	local anims = CombatConfig.ANIMATIONS.R15 :: any
	local weaponType = character:GetAttribute("HeldWeaponType")
	local list = weaponType and anims.combo[weaponType]
	if list and #list > 0 and list[1] ~= "" then
		return list[1]
	end
	return anims.slash
end

local function holdPose(character: Model): AnimationTrack?
	local humanoid = character:FindFirstChildOfClass("Humanoid")
	local animator = humanoid and humanoid:FindFirstChildOfClass("Animator")
	local id = animationId(character)
	if not (animator and id) then
		return nil
	end
	local animation = Instance.new("Animation")
	animation.AnimationId = id
	local ok, track = pcall(animator.LoadAnimation, animator, animation)
	if not ok or not track then
		return nil
	end
	track.Priority = Enum.AnimationPriority.Action2
	track.Looped = false
	track:Play(0.06, 1, 0)
	task.spawn(function()
		local waited = os.clock()
		while track.Length == 0 and os.clock() - waited < 0.3 do
			task.wait()
		end
		if track.IsPlaying then
			track.TimePosition = track.Length * HOLD_FRACTION
		end
	end)
	return track
end

local function sparkProps(extra: { [string]: any }): { [string]: any }
	local props: { [string]: any } = {
		Texture = T.EbSpark,
		Color = ColorSequence.new(WHITE, PURPLE_SOFT),
		LightEmission = 1,
		Brightness = 3,
		Orientation = Enum.ParticleOrientation.VelocityParallel,
		Size = seq({ { 0, 0.45 }, { 1, 0 } }),
		Transparency = seq({ { 0, 0 }, { 1, 0.6 } }),
	}
	for k, v in extra do
		props[k] = v
	end
	return props
end

-- 흰 섬광 구 + 빛 (발동·마무리)
local function flash(ctx: Kit.Ctx, at: Vector3, size: number, time: number, brightness: number)
	local ball = Instance.new("Part")
	ball.Name = "WhirlFlash"
	ball.Shape = Enum.PartType.Ball
	ball.Material = Enum.Material.Neon
	ball.Color = WHITE
	ball.Transparency = 0.1
	ball.Size = Vector3.one * size * 0.2
	Kit.decor(ball)
	ball.CFrame = CFrame.new(at)
	ball.Parent = ctx.folder
	ctx:tween(ball, time, { Size = Vector3.one * size, Transparency = 1, Color = PURPLE_SOFT })
	local light = Instance.new("PointLight")
	light.Color, light.Range, light.Brightness, light.Shadows = PURPLE_SOFT, size * 6, brightness, false
	light.Parent = ball
	ctx:tween(light, time * 1.6, { Brightness = 0 })
end

-- 키트 터짐(불꽃·별·선·번개)을 at 에서 dir 쪽으로, 기본 개수 × mult
local function kitBurst(ctx: Kit.Ctx, at: Vector3, dir: Vector3, mult: number)
	local h = Kit.holder(ctx, CFrame.lookAt(at, at + dir), "KitBurst")
	local b = KIT.Burst:Clone()
	b.CFrame = CFrame.Angles(0, math.pi, 0) -- 키트 이미터는 Back 방향 → 몸 바깥(dir)으로
	b.Parent = h
	for _, e in b:GetChildren() do
		if e:IsA("ParticleEmitter") then
			e.TimeScale = ctx.scale
			e:Emit(math.max(1, math.floor((e:GetAttribute("EmitCount") or 5) * mult)))
		end
	end
end

type BeamInfo = { beam: Beam, w0: number, w1: number, c0: number, c1: number, tr: NumberSequence }

-- 투명도 시퀀스를 alive(0 안 보임 ~ 1 원래대로) 만큼 보이게
local function fadeSeq(src: NumberSequence, alive: number): NumberSequence
	local keys = {}
	for _, k in src.Keypoints do
		table.insert(keys, NumberSequenceKeypoint.new(k.Time, 1 - (1 - k.Value) * alive, k.Envelope))
	end
	return NumberSequence.new(keys)
end

-- 초승달 하나: 키트 빔 초승달(+ 평면 플립북)을 cf 자리에 두고, 평면 법선(로컬 X) 둘레로 sweep 만큼 휘두르며 나타났다 사라짐
-- cf: 원점 = 반원의 중심, 로컬 X = 평면 법선, 로컬 -Z = 불룩한 쪽. scale = 크기(1 = 반지름 7), widthMul = 굵기 배율
local function crescent(ctx: Kit.Ctx, cf: CFrame, scale0: number, scale1: number, life: number, sweepDeg: number, widthMul: number, flip: boolean)
	local holder = Kit.holder(ctx, cf, "Crescent")
	local a0, a1 = KIT.CrescentA:Clone(), KIT.CrescentB:Clone()
	local base0, base1 = a0.Position, a1.Position
	a0.Parent, a1.Parent = holder, holder
	local beams: { BeamInfo } = {}
	for _, b in a1:GetChildren() do
		if b:IsA("Beam") then
			b.Attachment0 = if b.Attachment0 and b.Attachment0.Name == "CrescentA" then a0 else a1
			b.Attachment1 = if b.Attachment1 and b.Attachment1.Name == "CrescentA" then a0 else a1
			table.insert(beams, { beam = b, w0 = b.Width0, w1 = b.Width1, c0 = b.CurveSize0, c1 = b.CurveSize1, tr = b.Transparency })
			b.Transparency = NumberSequence.new(1)
			b.Enabled = true
		end
	end
	-- 보조: 같은 평면에 눕는 초승달 플립북 (어두운 결 + 보라)
	local flat = KIT.Slash:Clone()
	flat.CFrame = CFrame.Angles(0, 0, -math.pi / 2) -- 플립북 축(Y) = 평면 법선(X)
	flat.Parent = holder
	for _, e in flat:GetChildren() do
		if e:IsA("ParticleEmitter") then
			e.TimeScale = ctx.scale
			e.Size = NumberSequence.new(e.Size.Keypoints[1].Value * scale1 * 1.4)
			e:Emit(e:GetAttribute("EmitCount") or 5)
		end
	end
	local sweep = math.rad(sweepDeg) * (if flip then -1 else 1)
	local t0 = ctx:clock()
	ctx:step(t0 + life, function(t)
		local s = math.clamp((t - t0) / life, 0, 1)
		local e = 1 - (1 - s) ^ 3
		local k = scale0 + (scale1 - scale0) * e
		holder.CFrame = cf * CFrame.Angles(-sweep / 2 + sweep * e, 0, 0)
		a0.Position, a1.Position = base0 * k, base1 * k
		local appear = math.clamp(s / 0.12, 0, 1)
		local alive = appear * (1 - (if s < 0.45 then 0 else ((s - 0.45) / 0.55) ^ 1.3))
		for _, b in beams do
			b.beam.Width0 = b.w0 * k * widthMul * (0.5 + 0.5 * appear)
			b.beam.Width1 = b.w1 * k * widthMul * (0.5 + 0.5 * appear)
			b.beam.CurveSize0, b.beam.CurveSize1 = b.c0 * k, b.c1 * k
			b.beam.Transparency = fadeSeq(b.tr, alive)
		end
	end)
	ctx:at(life + 0.05, function()
		holder:Destroy()
	end)
end

-- 보통·강조 베기: 허리 둘레, 지정한 평면에서 sweep 만큼 휘두름
local function spawnSlash(ctx: Kit.Ctx, center: Vector3, bodyYaw: number, spec: SlashSpec)
	local strong = spec.mesh == "SlashB"
	-- 수평(tilt 0) = 법선이 위: 키트 법선(X)을 위(Y)로 → Z 둘레 90°. 그 전에 몸 방향 yaw, 평면 기울임 tilt
	local cf = CFrame.new(center + Vector3.new(0, spec.h, 0))
		* CFrame.Angles(0, bodyYaw + math.rad(spec.yaw), 0)
		* CFrame.Angles(0, 0, math.rad(spec.tilt))
		* CFrame.Angles(0, 0, math.pi / 2)
	local k1 = spec.k1 * (if strong then 1.3 else 1)
	crescent(ctx, cf, spec.k0, k1, spec.life + (if strong then 0.06 else 0.04), spec.sweep, if strong then 1.6 else 1, spec.dir < 0)
	if strong then
		ctx:at(spec.life * 0.25, function()
			local out = cf.LookVector -- 로컬 -Z 의 반대 = 불룩한 쪽은 -LookVector
			kitBurst(ctx, cf.Position - out * ARC_R * k1, -out, 0.5)
		end)
	end
end

-- 마무리 베기 하나: 몸 앞 수직 평면(법선 = look)에서 대각선 큰 초승달. side = 기울기 방향(±1)
-- 마무리 꽃잎 터짐: center = 허리, spinYaw = 그 순간 몸 방향(회전 방향 = yaw 가 커지는 쪽), radius = 스킬 반경
local function petalEmitter(ctx: Kit.Ctx, parent: Instance, texture: string, props: { [string]: any }): ParticleEmitter
	local base = {
		Texture = texture,
		FlipbookLayout = Enum.ParticleFlipbookLayout.Grid4x4,
		FlipbookMode = Enum.ParticleFlipbookMode.Loop,
		Color = ColorSequence.new(WHITE),
		LightEmission = 0.2, -- 화면 확인: 0.35·밝기 1.7 은 로비 조명과 겹쳐 분홍빛 흰색으로 날아감 → 보라가 보이게 낮춤
		LightInfluence = 0.25,
		Brightness = 1.15,
		Rotation = NumberRange.new(0, 360),
		RotSpeed = NumberRange.new(-240, 240),
		EmissionDirection = Enum.NormalId.Front,
		ZOffset = 0.3,
	}
	for k, v in props do
		base[k] = v
	end
	local e = Kit.emitter(ctx, parent, base)
	pcall(function()
		(e :: any).FlipbookStartRandom = true -- 꽃잎마다 다른 각도에서 돌기 시작
		(e :: any).FlipbookFramerate = props.FlipbookFramerate or NumberRange.new(14, 26)
	end)
	return e
end

local function petalBurst(ctx: Kit.Ctx, center: Vector3, spinYaw: number, radius: number)
	local spots = 18
	-- 멈추는 거리 = 속도 / (Drag × ln2) ≈ 1.44 × 속도 / Drag (Roblox 파티클 Drag = 속도가 반으로 줄어드는 빈도). 가장 빠른 꽃잎도 반경의 약 0.8 에서 멈추게
	-- (처음엔 50 / 2.4 → 약 30 스터드로 반경 16 밖까지 날아감)
	local reach = radius / 16 -- 속도는 반경 16 기준
	for i = 0, spots - 1 do
		local a = spinYaw + (i + math.random() * 0.6) / spots * math.pi * 2
		-- yaw 가 커지는 회전(왼쪽)에서 점 (cos a, 0, -sin a) 의 진행 방향 = (-sin a, 0, -cos a)
		local out = Vector3.new(math.cos(a), 0, -math.sin(a))
		local tangent = Vector3.new(-math.sin(a), 0, -math.cos(a))
		local lift = (math.random() - 0.35) * 0.35
		local dir = (tangent * 0.8 + out * 0.6 + Vector3.new(0, lift, 0)).Unit
		local at = center + out * 1.4 + Vector3.new(0, -0.9 + math.random() * 2.6, 0)
		local holder = Kit.holder(ctx, CFrame.lookAt(at, at + dir), "WhirlPetals")
		local tex = PETALS[i % 2 + 1]
		-- 튀어 나가 소용돌이치며 퍼지는 꽃잎 (많고 작게)
		petalEmitter(ctx, holder, tex, {
			Size = seq({ { 0, 0.15 }, { 0.05, 0.55 }, { 1, 0.42 } }),
			Transparency = seq(PETAL_FADE),
			Lifetime = NumberRange.new(2.2, 3.2),
			Speed = NumberRange.new(17 * reach, 29 * reach), -- Drag 3.2 → 7.7 ~ 13 스터드에서 멈춤
			SpreadAngle = Vector2.new(16, 26),
			Drag = 3.2,
			Acceleration = Vector3.new(0, -3.2, 0),
		}):Emit(12)
		-- 천천히 떠도는 꽃잎 (흩날림)
		petalEmitter(ctx, holder, PETALS[(i + 1) % 2 + 1], {
			Size = seq({ { 0, 0.1 }, { 0.08, 0.42 }, { 1, 0.34 } }),
			Transparency = seq(PETAL_FADE),
			Lifetime = NumberRange.new(2.8, 3.8),
			Speed = NumberRange.new(6 * reach, 12 * reach), -- Drag 1.6 → 5.4 ~ 10.8 스터드
			SpreadAngle = Vector2.new(40, 55),
			Drag = 1.6,
			Acceleration = Vector3.new(0, -1.6, 0),
			FlipbookFramerate = NumberRange.new(9, 16),
			RotSpeed = NumberRange.new(-140, 140),
		}):Emit(5)
	end
	-- 몸 가까이 큰 꽃잎 몇 장
	local core = Kit.holder(ctx, CFrame.new(center + Vector3.new(0, 0.6, 0)), "WhirlPetalsCore")
	core.Size = Vector3.new(2.5, 2, 2.5)
	petalEmitter(ctx, core, PETALS[1], {
		Size = seq({ { 0, 0.3 }, { 0.06, 1.0 }, { 1, 0.8 } }),
		Transparency = seq(PETAL_FADE),
		Lifetime = NumberRange.new(2.0, 2.8),
		Speed = NumberRange.new(10, 18),
		Shape = Enum.ParticleEmitterShape.Sphere,
		ShapeStyle = Enum.ParticleEmitterShapeStyle.Volume,
		SpreadAngle = Vector2.new(180, 180),
		Drag = 2.2,
		Acceleration = Vector3.new(0, -2.4, 0),
		Brightness = 1.3,
		FlipbookFramerate = NumberRange.new(10, 18),
	}):Emit(10)
end

-- 맞음: 칼이 지나가는 방향(접선)으로 흰·보라 불꽃 + 작은 섬광
local function playHit(payload: any, character: Model, point: Vector3?)
	local ctx = Kit.begin("BladeWhirlHit", 0.6, payload.timeScale)
	local center = (payload.origin :: CFrame).Position
	local root = character:FindFirstChild("HumanoidRootPart")
	if root and root:IsA("BasePart") then
		center = root.Position
	end
	local at = point
	if not at then
		local target = payload.target
		local targetRoot = typeof(target) == "Instance" and target:FindFirstChild("HumanoidRootPart")
		if not (targetRoot and targetRoot:IsA("BasePart")) then
			ctx.folder:Destroy()
			return
		end
		local flat = (targetRoot.Position - center) * Vector3.new(1, 0, 1)
		local dir = if flat.Magnitude > 0.1 then flat.Unit else Vector3.new(0, 0, -1)
		at = targetRoot.Position - dir * 0.8
	end
	local hitAt = at :: Vector3
	local radial = (hitAt - center) * Vector3.new(1, 0, 1)
	radial = if radial.Magnitude > 0.1 then radial.Unit else Vector3.new(0, 0, -1)
	local tangent = Vector3.yAxis:Cross(radial)
	local holder = Kit.holder(ctx, CFrame.lookAt(hitAt, hitAt + tangent), "WhirlHit")
	Kit.emitter(ctx, holder, sparkProps({
		Color = ColorSequence.new(WHITE),
		Size = seq({ { 0, 0.4 }, { 1, 0 } }),
		Lifetime = NumberRange.new(0.08, 0.16),
		Speed = NumberRange.new(20, 30),
		SpreadAngle = Vector2.new(30, 30),
		EmissionDirection = Enum.NormalId.Front,
		Drag = 6,
	})):Emit(5)
	Kit.emitter(ctx, holder, sparkProps({
		Color = ColorSequence.new(PURPLE_SOFT, PURPLE),
		Brightness = 2.5,
		Size = seq({ { 0, 0.5 }, { 1, 0 } }),
		Transparency = seq({ { 0, 0 }, { 1, 0.7 } }),
		Lifetime = NumberRange.new(0.12, 0.24),
		Speed = NumberRange.new(10, 18),
		SpreadAngle = Vector2.new(60, 60),
		EmissionDirection = Enum.NormalId.Front,
		Acceleration = Vector3.new(0, -18, 0),
		Drag = 5,
	})):Emit(6)
	flash(ctx, hitAt, 1.3, 0.1, 2)
	Kit.sound(SOUNDS.hit, if isMine(character) then nil else hitAt)
end

-- 플레이어 오라 (v4, 사용자 참고 그림 3): 스킬 동안 몸에 보라 테두리 빛 + 발밑 빛 원 + 몸 둘레로 솟는 불티 + 은은한 빛기둥.
-- 몸을 따라다니고 untilT(연출 시각)에 0.35초 동안 사라짐
local function playerAura(ctx: Kit.Ctx, character: Model, root: BasePart?, untilT: number)
	if not root then
		return
	end
	local glow = Instance.new("Highlight")
	glow.FillColor, glow.OutlineColor = PURPLE, PURPLE_SOFT
	glow.FillTransparency, glow.OutlineTransparency = 1, 1
	glow.DepthMode = Enum.HighlightDepthMode.Occluded
	glow.Adornee = character
	glow.Parent = ctx.folder
	ctx:tween(glow, 0.12, { FillTransparency = 0.72, OutlineTransparency = 0.25 })
	ctx:tween(glow, 0.35, { FillTransparency = 1, OutlineTransparency = 1 }, nil, nil, untilT)
	-- 발밑 빛 원 (천천히 돌며 커졌다 사라짐)
	local disc = Kit.holder(ctx, CFrame.new(root.Position), "AuraGround")
	disc.Size = Vector3.new(3, 0.05, 3)
	local gui = Instance.new("SurfaceGui")
	gui.Face = Enum.NormalId.Top
	gui.LightInfluence = 0
	gui.Brightness = 2.5
	gui.SizingMode = Enum.SurfaceGuiSizingMode.PixelsPerStud
	gui.PixelsPerStud = 40
	gui.Parent = disc
	local img = Instance.new("ImageLabel")
	img.BackgroundTransparency = 1
	img.Size = UDim2.fromScale(1, 1)
	img.Image = GROUND_IMAGE
	img.ImageTransparency = 1
	img.Parent = gui
	-- 솟는 불티 (몸 둘레 원기둥 안에서)
	local column = Kit.holder(ctx, CFrame.new(root.Position), "AuraColumn")
	column.Size = Vector3.new(4.5, 5, 4.5)
	local embers = Kit.emitter(ctx, column, sparkProps({
		Texture = T.HolySparkle,
		Orientation = Enum.ParticleOrientation.FacingCamera,
		Rate = 80,
		Color = ColorSequence.new(WHITE, PURPLE),
		Size = seq({ { 0, 0.3 }, { 0.5, 0.22 }, { 1, 0 } }),
		Transparency = seq({ { 0, 0.1 }, { 1, 1 } }),
		Lifetime = NumberRange.new(0.5, 0.9),
		Speed = NumberRange.new(2, 6),
		EmissionDirection = Enum.NormalId.Top,
		SpreadAngle = Vector2.new(20, 20),
		Acceleration = Vector3.new(0, 4, 0),
		Shape = Enum.ParticleEmitterShape.Cylinder,
		ShapeStyle = Enum.ParticleEmitterShapeStyle.Volume,
		Drag = 1,
	}))
	-- 은은한 빛기둥 (발에서 위로, 카메라를 봄)
	local a0, a1 = Instance.new("Attachment"), Instance.new("Attachment")
	a0.Parent, a1.Parent = column, column
	local pillar = Instance.new("Beam")
	pillar.Attachment0, pillar.Attachment1 = a0, a1
	pillar.Texture = T.PillarCore
	pillar.Color = ColorSequence.new(PURPLE_SOFT, PURPLE)
	pillar.Transparency = seq({ { 0, 0.55 }, { 0.6, 0.75 }, { 1, 1 } })
	pillar.Width0, pillar.Width1 = 3.6, 2
	pillar.LightEmission, pillar.LightInfluence, pillar.Brightness = 1, 0, 2
	pillar.FaceCamera = true
	pillar.Parent = column
	local light = Instance.new("PointLight")
	light.Color, light.Range, light.Brightness, light.Shadows = PURPLE, 16, 0, false
	light.Parent = column
	ctx:tween(light, 0.15, { Brightness = 2.2 })
	local t0 = ctx:clock()
	ctx:step(untilT + 0.35, function(t)
		local e = t - t0
		local out = math.clamp((t - untilT) / 0.35, 0, 1)
		local inn = math.clamp(e / 0.15, 0, 1)
		local alive = inn * (1 - out)
		local pos = if root.Parent then root.Position else column.Position
		local feet = Kit.ground(pos, { character, ctx.folder })
		local d = 3 + 5 * (1 - (1 - inn) ^ 2) + 0.8 * out
		disc.Size = Vector3.new(d, 0.05, d)
		disc.CFrame = CFrame.new(feet + Vector3.new(0, 0.06, 0)) * CFrame.Angles(0, e * 1.5, 0)
		img.ImageTransparency = 1 - alive
		column.CFrame = CFrame.new(feet + Vector3.new(0, 2.5, 0))
		a0.Position, a1.Position = Vector3.new(0, -2.5, 0), Vector3.new(0, 5.5, 0)
		pillar.Transparency = seq({ { 0, 1 - 0.45 * alive }, { 0.6, 1 - 0.25 * alive }, { 1, 1 } })
		embers.Enabled = out <= 0
		if out > 0 then
			light.Brightness = 2.2 * (1 - out)
		end
	end)
end

local function playCast(payload: any, character: Model)
	local origin = payload.origin :: CFrame
	local castDelay = SKILL.castDelay
	local spinTime = if type(payload.spinTime) == "number" then payload.spinTime else (SKILL.spinTime or 0.9)
	local turns = if type(payload.turns) == "number" then payload.turns else (SKILL.turns or 3)
	local radius = if type(payload.radius) == "number" then payload.radius else (SKILL.radius or 16) -- 꽃잎이 퍼지는 거리
	local spinEnd = castDelay + spinTime
	local preview = payload.timeScale ~= nil
	local mine = isMine(character) and not preview
	local ctx = Kit.begin("BladeWhirl", math.max(spinEnd, FINISH_FLASH) + PETAL_LIFE, payload.timeScale)
	local function atAbs(seconds: number, fn: () -> ())
		ctx:at(math.max(seconds - ctx:clock(), 0), fn)
	end
	local humanoid = character:FindFirstChildOfClass("Humanoid")
	local root = character:FindFirstChild("HumanoidRootPart") :: BasePart?
	local baseYaw = yawOf(origin.LookVector)
	local function centerPos(): Vector3
		return if root and root.Parent then root.Position else origin.Position
	end
	local function spinAngle(t: number): number
		if t <= castDelay then
			return 0
		end
		return turns * math.pi * 2 * math.min((t - castDelay) / spinTime, 1)
	end

	-- 발동: 가슴 앞 짧은 흰 섬광 + 반짝이
	local chest = centerPos() + Vector3.new(0, 0.6, 0) + origin.LookVector * 0.6
	flash(ctx, chest, 2.4, 0.14, 3)
	local burst = Kit.holder(ctx, CFrame.new(chest), "WhirlStart")
	Kit.emitter(ctx, burst, sparkProps({
		Lifetime = NumberRange.new(0.1, 0.2),
		Speed = NumberRange.new(12, 20),
		SpreadAngle = Vector2.new(180, 180),
		Drag = 6,
	})):Emit(8)
	Kit.casterSound(SOUNDS.flash, character, origin.Position)
	playerAura(ctx, character, root, spinEnd)

	-- 내 캐릭터: 기존과 같은 회전·자세 (무엇이 실패해도 끝나면 반드시 풀림)
	local unlock: (() -> ())? = nil
	local track: AnimationTrack? = nil
	if mine and humanoid then
		unlock = Kit.lockRotation(humanoid)
		track = holdPose(character)
	end
	local released = false
	local function release()
		if released then
			return
		end
		released = true
		if mine and root and root.Parent then
			root.CFrame = CFrame.new(root.Position) * CFrame.Angles(0, baseYaw, 0)
		end
		if track and track.IsPlaying then
			track:Stop(0.2)
		end
		if unlock then
			unlock()
		end
	end
	task.delay((spinEnd + 0.4) / ctx.scale, release)
	if mine then
		ctx:step(spinEnd, function(t)
			if not released and root and root.Parent and t >= castDelay then
				root.CFrame = CFrame.new(root.Position) * CFrame.Angles(0, baseYaw + spinAngle(t), 0)
			end
		end)
	end
	atAbs(spinEnd, release)
	for i = 0, turns - 1 do
		atAbs(castDelay + spinTime / turns * i, function()
			Kit.casterSound(SOUNDS.turn, character, origin.Position)
		end)
	end

	-- 연속 베기 + 강조 베기: 그 순간 몸 방향 기준으로 하나씩
	for _, spec in SLASHES do
		atAbs(spec.t, function()
			spawnSlash(ctx, centerPos(), baseYaw + spinAngle(spec.t), spec)
			if spec.mesh == "SlashB" then
				Kit.casterSound(SOUNDS.slashB, character, origin.Position)
			end
		end)
	end

	-- 마무리: 꽃잎이 소용돌이치며 터짐 (서버 3타 순간)
	atAbs(FINISH_FLASH, function()
		local c = centerPos()
		flash(ctx, c + Vector3.new(0, 0.6, 0), 3.2, 0.16, 1.6) -- 은은한 섬광 (꽃잎이 주인공)
		petalBurst(ctx, c, baseYaw + spinAngle(FINISH_FLASH), radius)
		Kit.casterSound(SOUNDS.finish, character, origin.Position)
	end)

	-- 미리보기: 서버 타격 대신 타 시각마다 앞쪽에 맞음 연출
	if preview then
		for _, ht in (if type(payload.hitTimes) == "table" then payload.hitTimes else {}) do
			atAbs(ht, function()
				playHit({ origin = origin, timeScale = payload.timeScale }, character, origin.Position + origin.LookVector * 5)
			end)
		end
	end
end

function BladeWhirl.play(payload: any, character: Model)
	if payload.phase == "hit" then
		playHit(payload, character)
		return
	end
	playCast(payload, character)
end

return BladeWhirl
