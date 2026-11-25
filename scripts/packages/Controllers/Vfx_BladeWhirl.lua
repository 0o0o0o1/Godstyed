--!strict
-- 칼날 회오리 연출 v4 (Skills.blade_whirl, kind "whirl", vfx = "BladeWhirl"). 흰 + 선명한 보라.
-- 원본: 저장소 scripts/packages/Controllers/Vfx_BladeWhirl.lua (Controllers 패키지 SkillController.Vfx.BladeWhirl)
-- v3 (2026-11-25, 사용자 참고 그림): 메시에 SurfaceAppearance 그라데이션(흰 앞날 → 보라 → 어두운 꼬리, 투명도) + 발광 마스크,
--   베기마다 앞머리 보라 빛(PointLight) + 불티, 강조·마무리 베기는 접선 방향 빛줄기. 텍스처 scripts/vfx_whirl_slash_tex.py
-- v4 (2026-11-25 사용자): 범위 10→16 에 맞춰 넓은 띠 메시(A 반지름 7·폭 2.2 / B 9·3.4 / C 11·2.0), 플레이어 오라(테두리 빛·발밑 원·솟는 불티·빛기둥)
-- v1(원형 궤도 칼날 2장 + 검은 연기)은 git 기록. v2 = 개별 초승달 베기 메시를 여러 평면·높이·각도로 시간 차를 두고 교차시킴
--   발동      0                 가슴 앞 짧은 흰 섬광 + 빛 + 반짝이 몇 개
--   연속 베기  castDelay ~ 0.85   SlashA 8개 (수평·대각·높낮이·크기·휘두르는 방향이 모두 다름), 하나씩 0.2초 동안 나타나 휘둘러지고 사라짐
--   강조 베기  0.36 / 0.67        SlashB 2개 (더 크고 넓음, 다른 방향으로 교차) — 서버 1·2타(0.4·0.7) 직전
--   마무리     0.92 / 0.97        SlashC 2개가 몸 앞 수직 평면에서 X 자로 교차 → 1.0(서버 3타) 흰 섬광 + 바깥으로 튀는 불꽃(보조 충격파)
--   맞음      phase "hit"        맞은 자리 흰·보라 불꽃 + 작은 섬광 (서버 타격 하나 = 연출 하나)
--   몸        (내 캐릭터) 기존과 같음: castDelay 부터 spinTime 동안 왼쪽 turns 바퀴, 단검 첫 타 휘두른 자세 멈춤
-- 메시: 이 모듈 아래 MeshPart SlashA / SlashB / SlashC (SurfaceAppearance, v3 는 흰 심 Core 없음 — 자식 MeshPart 가 있으면 같이 움직임). Blender scripts/blade_whirl_slashes.py
--   규격: 호(arc) 모양 칼날, PivotOffset = 호의 중심(휘두르는 축), 칼날 가운데 = 피벗 로컬 -X, 칼날 평면 법선 = 로컬 Y,
--   로컬 +Y 축 양의 회전 = 칼날 끝(앞) 쪽으로 휘두름. 메시가 없으면 그 베기는 건너뜀 (경고 한 번)
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
local C_RADIUS = 11 -- SlashC 호 반지름 (메시와 같게, v4 범위 16)
-- 베기 메시마다 앞머리(빛·불티를 붙일 자리) = 피벗 로컬. 호 반지름 r, 호 각 span 의 끝 쪽 85% 지점
-- (Blender (r cos a, r sin a) → Roblox 로컬 (-r cos a, 0, r sin a))
local function headOf(r: number, spanDeg: number): Vector3
	local a = math.rad(spanDeg / 2 * 0.85)
	return Vector3.new(-r * math.cos(a), 0, r * math.sin(a))
end
local HEADS = { SlashA = headOf(7.0, 150), SlashB = headOf(9.0, 170), SlashC = headOf(11.0, 72) } -- v4 넓은 띠 메시
local GROUND_IMAGE = "rbxassetid://88252622732116" -- 발밑 빛 원 (scripts/vfx_whirl_slash_tex.py WhirlGround)
local STREAK_TEXTURE = T.FsSlashLine -- 가는 흰 선 (Beam 색으로 물들임)

-- 베기 배치표. t = 시전 후 시각, yaw = 그 순간 몸 방향에서 더 돌린 각(도), tilt = 칼날 평면을 기울인 각(도, 0 = 수평),
-- h = 허리에서 높이, k0→k1 = 크기, sweep = 휘두르는 각(도), dir = 1 왼쪽으로 / -1 반대로, life = 보이는 시간
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
-- 마무리 X: 시각, 몸 앞 평면에서 칼날이 불룩한 쪽(오른쪽 +1 / 왼쪽 -1)
local FINISH = { { t = 0.92, side = 1 }, { t = 0.97, side = -1 } }
local FINISH_FLASH = 1.0 -- 서버 3타와 같은 시각
local FINISH_FORWARD, FINISH_UP = 5, 0.5 -- X 교차점: 몸 앞·위 (v4: 칼날이 커져 앞으로)
local FINISH_SCALE = 1 -- 마무리 베기 크기 (v4 메시가 이미 큼)

local SOUNDS = {
	flash = { id = "rbxassetid://125132253621935", volume = 0.4, speed = 1.1 }, -- Sword Whoosh Slash
	slashB = { id = "rbxassetid://125132253621935", volume = 0.5, speed = 1.45 },
	turn = { id = "rbxassetid://125132253621935", volume = 0.35, speed = 1.3 }, -- 바퀴마다
	finish = { id = "rbxassetid://9116687945", volume = 0.7, speed = 1.35 }, -- Metal Impacts 20: 맑은 쇠 울림
	finishCut = { id = "rbxassetid://9114159112", volume = 0.6, speed = 1.7, fadeAfter = 0.3 }, -- Doppler Whoosh
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

type Piece = { part: BasePart, size: Vector3, base: number, off: Vector3 }

-- 베기 하나: 템플릿(바깥 + 자식 Core)을 복제해 pivot(호 중심) 둘레로 휘두르며 크기·투명도를 바꾸고 끝나면 지움
-- pivotAt(s): s = 0 ~ 1 진행도의 피벗 CFrame, scale(s), fade(s) (0 보임 ~ 1 사라짐)
local function swing(ctx: Kit.Ctx, mesh: string, life: number, pivotAt: (number) -> CFrame, scale: (number) -> number, fade: (number) -> number)
	local template = script:FindFirstChild(mesh)
	if not (template and template:IsA("MeshPart")) then
		if not warned then
			warned = true
			warn("[BladeWhirl] 베기 메시 " .. mesh .. " 없음 (모듈 아래 SlashA/B/C 필요)")
		end
		return
	end
	local pieces: { Piece } = {}
	local function add(src: MeshPart, copy: BasePart)
		Kit.decor(copy)
		copy.Transparency = 1
		copy.Parent = ctx.folder
		table.insert(pieces, { part = copy, size = src.Size, base = src.Transparency, off = src.PivotOffset.Position })
	end
	local m = template:Clone()
	for _, c in template:GetChildren() do
		if c:IsA("MeshPart") then
			add(c, m:FindFirstChild(c.Name) :: BasePart)
		end
	end
	add(template, m)
	-- 앞머리: 보라 빛(바닥·몸을 물들임) + 흩날리는 불티
	local headLocal = HEADS[mesh] or Vector3.new(-3, 0, 0)
	local head = Kit.holder(ctx, pivotAt(0), "SlashHead")
	local light = Instance.new("PointLight")
	light.Color, light.Range, light.Brightness, light.Shadows = PURPLE_SOFT, if mesh == "SlashA" then 14 else 20, 0, false
	light.Parent = head
	local sparks = Kit.emitter(ctx, head, sparkProps({
		Rate = if mesh == "SlashA" then 60 else 100,
		Color = ColorSequence.new(WHITE, PURPLE),
		Size = seq({ { 0, 0.28 }, { 1, 0 } }),
		Lifetime = NumberRange.new(0.12, 0.3),
		Speed = NumberRange.new(4, 12),
		SpreadAngle = Vector2.new(70, 70),
		Acceleration = Vector3.new(0, -8, 0),
		Drag = 4,
	}))
	local t0 = ctx:clock()
	local function place(s: number)
		local pivot = pivotAt(s)
		local k = scale(s)
		local f = fade(s)
		for _, p in pieces do
			p.part.Size = p.size * k
			p.part.CFrame = pivot * CFrame.new(-p.off * k)
			p.part.Transparency = p.base + (1 - p.base) * f
		end
		head.CFrame = pivot * CFrame.new(headLocal * k)
		light.Brightness = (1 - f) * (if mesh == "SlashA" then 2.2 else 3.5)
		sparks.Enabled = f < 0.6
	end
	place(0)
	ctx:step(t0 + life, function(t)
		place(math.clamp((t - t0) / life, 0, 1))
	end)
	ctx:at(life + 0.02, function()
		for _, p in pieces do
			p.part:Destroy()
		end
		sparks.Enabled = false
		light.Brightness = 0
	end)
end

-- 빛줄기: 한 점에서 dir 방향으로 길게 뻗는 가는 흰·보라 선이 번쩍 (강조·마무리 베기)
local function streak(ctx: Kit.Ctx, at: Vector3, dir: Vector3, length: number, width: number)
	local a0 = Kit.holder(ctx, CFrame.new(at - dir * length * 0.5), "StreakA")
	local a1 = Kit.holder(ctx, CFrame.new(at + dir * length * 0.5), "StreakB")
	local att0, att1 = Instance.new("Attachment"), Instance.new("Attachment")
	att0.Parent, att1.Parent = a0, a1
	local b = Instance.new("Beam")
	b.Attachment0, b.Attachment1 = att0, att1
	b.Texture = STREAK_TEXTURE
	b.TextureMode = Enum.TextureMode.Stretch
	b.Color = ColorSequence.new({ ColorSequenceKeypoint.new(0, PURPLE), ColorSequenceKeypoint.new(0.5, WHITE), ColorSequenceKeypoint.new(1, PURPLE) })
	b.Transparency = seq({ { 0, 1 }, { 0.35, 0.2 }, { 0.5, 0 }, { 0.65, 0.2 }, { 1, 1 } })
	b.Width0, b.Width1 = width, width
	b.LightEmission, b.LightInfluence, b.Brightness = 1, 0, 6
	b.FaceCamera = true
	b.Segments = 1
	b.Parent = a0
	local t0 = ctx:clock()
	ctx:step(t0 + 0.16, function(t)
		local k = math.clamp((t - t0) / 0.16, 0, 1)
		b.Width0 = width * (1 - k)
		b.Width1 = width * (1 - k)
		att0.WorldPosition = at - dir * length * (0.3 + 0.25 * k)
		att1.WorldPosition = at + dir * length * (0.3 + 0.25 * k)
	end)
end

local function easeOut(s: number): number
	return 1 - (1 - s) ^ 3
end

-- 보통·강조 베기: 허리 둘레, 지정한 평면에서 sweep 만큼 휘두름. 나타남 15% → 유지 → 뒤 55% 동안 사라짐
local function spawnSlash(ctx: Kit.Ctx, center: Vector3, bodyYaw: number, spec: SlashSpec)
	local base = CFrame.new(center + Vector3.new(0, spec.h, 0))
		* CFrame.Angles(0, bodyYaw + math.rad(spec.yaw), 0)
		* CFrame.Angles(0, -math.pi / 2, 0) -- 칼날 가운데(-X) = 이 방향 앞
		* CFrame.Angles(math.rad(spec.tilt), 0, 0) -- 칼날 평면 기울임 (가운데 방향 축)
	if spec.dir < 0 then
		base *= CFrame.Angles(math.pi, 0, 0) -- 뒤집어 반대로 휘두름
	end
	local sweep = math.rad(spec.sweep)
	if spec.mesh == "SlashB" then
		-- 강조: 휘두름이 가장 빠른 순간 앞머리에서 접선 방향 빛줄기
		ctx:at(spec.life * 0.18, function()
			local mid = base * CFrame.Angles(0, -sweep / 2 + sweep * easeOut(0.18), 0)
			local headAt = (mid * CFrame.new(HEADS.SlashB * spec.k1)).Position
			local tangent = (mid * CFrame.Angles(0, 0.05, 0) * CFrame.new(HEADS.SlashB * spec.k1)).Position - headAt
			if tangent.Magnitude > 1e-3 then
				streak(ctx, headAt, tangent.Unit, 16, 0.45)
			end
		end)
	end
	swing(ctx, spec.mesh, spec.life, function(s)
		return base * CFrame.Angles(0, -sweep / 2 + sweep * easeOut(s), 0)
	end, function(s)
		return spec.k0 + (spec.k1 - spec.k0) * easeOut(s)
	end, function(s)
		if s < 0.15 then
			return 1 - s / 0.15
		elseif s < 0.45 then
			return 0
		end
		return ((s - 0.45) / 0.55) ^ 1.5
	end)
end

-- 마무리 베기 하나: 몸 앞 수직 평면(법선 = look)에서 대각선으로. side = 칼날이 불룩한 쪽
local function spawnFinish(ctx: Kit.Ctx, cross: Vector3, look: Vector3, side: number)
	local right = look:Cross(Vector3.yAxis).Unit
	local d = (right * side - Vector3.yAxis).Unit -- 호 중심 → 칼날 가운데 (불룩한 쪽, 아래 대각)
	local life = 0.4
	ctx:at(0.05, function()
		streak(ctx, cross, (right * side + Vector3.yAxis).Unit, 18, 0.5) -- 칼날이 그어지는 대각 방향
	end)
	swing(ctx, "SlashC", life, function(s)
		-- 0.09초(전체의 22%) 안에 빠르게 그어지고 멈춤
		local p = easeOut(math.min(s / 0.22, 1))
		local k = FINISH_SCALE + 0.08 * s
		local center = cross - d * C_RADIUS * k
		local pivot = CFrame.fromMatrix(center, -d, look)
		return pivot * CFrame.Angles(0, math.rad(-24 + 30 * p), 0)
	end, function(s)
		return FINISH_SCALE + 0.08 * s
	end, function(s)
		if s < 0.08 then
			return 1 - s / 0.08
		elseif s < 0.5 then
			return 0
		end
		return ((s - 0.5) / 0.5) ^ 1.4
	end)
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
	local spinEnd = castDelay + spinTime
	local preview = payload.timeScale ~= nil
	local mine = isMine(character) and not preview
	local ctx = Kit.begin("BladeWhirl", math.max(spinEnd, FINISH_FLASH) + 0.8, payload.timeScale)
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

	-- 마무리 X 교차 (몸이 3바퀴 돌아 처음 방향을 볼 때)
	local look = (origin.LookVector * Vector3.new(1, 0, 1)).Unit
	for _, f in FINISH do
		atAbs(f.t, function()
			local cross = centerPos() + look * FINISH_FORWARD + Vector3.new(0, FINISH_UP, 0)
			spawnFinish(ctx, cross, look, f.side)
		end)
	end
	atAbs(FINISH[1].t, function()
		Kit.casterSound(SOUNDS.finishCut, character, origin.Position)
	end)
	atAbs(FINISH_FLASH, function()
		local cross = centerPos() + look * FINISH_FORWARD + Vector3.new(0, FINISH_UP, 0)
		flash(ctx, cross, 2.4, 0.12, 5)
		-- 보조 충격파: 허리 높이에서 바깥으로 튀는 짧은 불꽃
		local ring = Kit.holder(ctx, CFrame.new(centerPos()), "WhirlShock")
		ring.Size = Vector3.new(1.5, 0.1, 1.5)
		Kit.emitter(ctx, ring, sparkProps({
			Lifetime = NumberRange.new(0.14, 0.22),
			Speed = NumberRange.new(28, 36),
			Shape = Enum.ParticleEmitterShape.Cylinder,
			ShapeInOut = Enum.ParticleEmitterShapeInOut.Outward,
			ShapeStyle = Enum.ParticleEmitterShapeStyle.Surface,
			Drag = 7,
		})):Emit(24)
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
