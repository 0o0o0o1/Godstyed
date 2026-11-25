--!strict
-- 칼날 회오리 연출 (Skills.blade_whirl, kind "whirl", vfx = "BladeWhirl"). 단검 색 = 어두운 보라 + 흰 심 + 검은 연기.
-- 원본: 저장소 scripts/packages/Controllers/Vfx_BladeWhirl.lua (Controllers 패키지 SkillController.Vfx.BladeWhirl)
--   발동    0 ~ castDelay                  발밑 검은 연기 고리 + 몸 둘레 보라 알갱이가 안쪽으로 모임 + 은은한 보라 빛
--   회전    castDelay ~ + spinTime          (내 캐릭터면) 몸을 왼쪽으로 turns 바퀴 돌림 + 단검 첫 타를 휘두른 자세로 멈춰 둠
--                                          몸 둘레(허리 높이)를 마주 보는 초승달 칼날 2장이 몸과 같은 속도로 돌며 감쌈 (등장: 작게→크게, 투명→보임)
--                                          칼날 끝에서 보라 불티가 조금씩 흩날려 원을 따라 꼬리를 남김
--   맞음    phase "hit" (서버, 적·타마다)    맞은 자리에 칼날이 지나가는 방향으로 흰·보라 불꽃 + 작은 섬광 (타격 횟수 = 연출 횟수)
--   끝      castDelay + spinTime            칼날이 조금 커지며 사라지고, 원을 따라 보라 잔광 알갱이 + 빛이 잠깐 남음
-- 칼날: 이 모듈 아래 MeshPart "WhirlBlade"(자식 "Core" 흰 심)가 있으면 그 메시, 없으면 Beam 곡선으로 만든 임시 초승달 2장.
--   WhirlBlade 규격: 수평 초승달 2장이 180° 마주 봄, 바운딩 중심 = 회전 중심, 회전 없는(identity) 자세에서 칼날 끝이
--   +Y 축 양의 회전 쪽(왼쪽으로 도는 방향)을 향함. Blender scripts/blade_whirl_arc.py
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

-- 색 (단검 = 보라)
local WHITE = Color3.new(1, 1, 1)
local PURPLE = Color3.fromRGB(110, 0, 230)
local PURPLE_SOFT = Color3.fromRGB(190, 130, 255)
local PURPLE_DIM = Color3.fromRGB(70, 20, 130)
local SMOKE = Color3.fromRGB(16, 10, 24)

-- 조정용 상수
local BLADE_HEIGHT = 0.1 -- 칼날 높이 (HumanoidRootPart 중심에서, 허리)
local BLADE_TILT = math.rad(5) -- 칼날 원판을 살짝 기울임 (평평하면 옆에서 선으로만 보임)
local R = 4.6 -- 칼날 바깥 반지름 (메시와 같게)
local ARC_FROM, ARC_TO = math.rad(35), math.rad(145) -- 칼날 하나가 차지하는 각 (꼬리 → 끝), 둘째 칼날은 +180°
local APPEAR = 0.1 -- 등장 시간 (회전 시작부터)
local VANISH = 0.18 -- 사라지는 시간
local HOLD_FRACTION = 0.55 -- 단검 첫 타를 휘두른 자세 (길이 대비)
local SMOKE_RADIUS = 2.6

local SOUNDS = {
	gather = { id = "rbxassetid://125132253621935", volume = 0.35, speed = 0.75 }, -- Sword Whoosh Slash (낮게)
	turn = { id = "rbxassetid://125132253621935", volume = 0.4, speed = 1.35 }, -- 바퀴마다 휙
	hit = { id = "rbxassetid://9113567601", volume = 0.6, speed = 1.4 }, -- Boxing Hits (Body Impact)
}
Kit.preloadSounds(SOUNDS)

local BladeWhirl = {}

local function isMine(character: Instance?): boolean
	return character ~= nil and character == Players.LocalPlayer.Character
end

local function yawOf(look: Vector3): number
	return math.atan2(-look.X, -look.Z)
end

-- 회전 중심(허리)에서 각 b(라디안, +Y 축 양의 회전 방향) 위의 점. 중심 CFrame 기준 로컬
local function onCircle(b: number, r: number): Vector3
	return Vector3.new(-math.sin(b) * r, 0, -math.cos(b) * r)
end

-- 단검 첫 타 (휘두른 자세로 멈춰 둠). 없으면 기본 베기
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

-- 칼날 2장. 반환: 매 프레임 자리 맞추기(centerCF, k = 크기 배율, fade = 0 보임 ~ 1 사라짐)
type Blades = { place: (CFrame, number, number) -> () }

local function meshBlades(ctx: Kit.Ctx, template: MeshPart): Blades
	local pieces: { { part: BasePart, size: Vector3, base: number, rel: CFrame } } = {}
	local function add(src: BasePart, copy: BasePart)
		Kit.decor(copy)
		copy.Parent = ctx.folder
		table.insert(pieces, { part = copy, size = src.Size, base = src.Transparency, rel = template.CFrame:ToObjectSpace(src.CFrame) })
	end
	local m = template:Clone()
	for _, c in template:GetChildren() do
		if c:IsA("BasePart") then
			add(c, m:FindFirstChild(c.Name) :: BasePart)
		end
	end
	add(template, m)
	return {
		place = function(center: CFrame, k: number, fade: number)
			for _, p in pieces do
				p.part.Size = p.size * k
				p.part.CFrame = center * CFrame.new(p.rel.Position * k) * p.rel.Rotation
				p.part.Transparency = p.base + (1 - p.base) * fade
			end
		end,
	}
end

-- 임시 칼날 (메시 없음): 꼬리·끝 두 점을 이은 Beam 곡선(호) 2장. 바깥 보라 + 안쪽 흰 심
local function beamBlades(ctx: Kit.Ctx): Blades
	local holder = Kit.holder(ctx, CFrame.new(), "WhirlBeams")
	local span = ARC_TO - ARC_FROM
	local beams: { { beam: Beam, base: number } } = {}
	local atts: { { a0: Attachment, a1: Attachment, from: number, to: number } } = {}
	for k = 0, 1 do
		local from, to = ARC_FROM + math.pi * k, ARC_TO + math.pi * k
		local a0, a1 = Instance.new("Attachment"), Instance.new("Attachment")
		a0.Parent, a1.Parent = holder, holder
		table.insert(atts, { a0 = a0, a1 = a1, from = from, to = to })
		for _, spec in { { PURPLE, 0.04, 0.5, 0.15 }, { WHITE, 0.02, 0.18, 0 } } do
			local b = Instance.new("Beam")
			b.Attachment0, b.Attachment1 = a0, a1
			b.Color = ColorSequence.new(spec[1] :: Color3)
			b.Width0, b.Width1 = spec[2] :: number, spec[3] :: number
			b.LightEmission, b.LightInfluence, b.Brightness = 1, 0, 2.5
			b.FaceCamera = true
			b.Segments = 20
			b.Transparency = NumberSequence.new(1)
			b.Parent = holder
			table.insert(beams, { beam = b, base = spec[4] :: number })
		end
	end
	local handle = 4 / 3 * math.tan(span / 4) -- 원호를 베지어로: 반지름 × 이 값
	return {
		place = function(center: CFrame, k: number, fade: number)
			holder.CFrame = center
			local r = R * k
			for _, a in atts do
				for i, b in { a.from, a.to } do
					local att = if i == 1 then a.a0 else a.a1
					local tangent = Vector3.new(-math.cos(b), 0, math.sin(b)) -- b 가 늘어나는 방향
					att.CFrame = CFrame.fromMatrix(onCircle(b, r), tangent, Vector3.yAxis)
				end
				for _, b in beams do
					if b.beam.Attachment0 == a.a0 then
						b.beam.CurveSize0 = r * handle
						b.beam.CurveSize1 = r * handle
					end
				end
			end
			for _, b in beams do
				b.beam.Transparency = NumberSequence.new(b.base + (1 - b.base) * fade)
			end
		end,
	}
end

-- 맞음: 칼날이 지나가는 방향(접선)으로 흰·보라 불꽃 + 작은 섬광
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
		at = targetRoot.Position - dir * 0.8 -- 몸 겉 (내 쪽)
	end
	local hitAt = at :: Vector3
	local radial = (hitAt - center) * Vector3.new(1, 0, 1)
	radial = if radial.Magnitude > 0.1 then radial.Unit else Vector3.new(0, 0, -1)
	local tangent = Vector3.yAxis:Cross(radial) -- 왼쪽으로 도는 칼날의 진행 방향
	local holder = Kit.holder(ctx, CFrame.lookAt(hitAt, hitAt + tangent), "WhirlHit")
	Kit.emitter(ctx, holder, {
		Texture = T.EbSpark,
		Color = ColorSequence.new(WHITE),
		LightEmission = 1,
		Brightness = 3,
		Size = seq({ { 0, 0.4 }, { 1, 0 } }),
		Transparency = seq({ { 0, 0 }, { 1, 0.6 } }),
		Lifetime = NumberRange.new(0.08, 0.16),
		Speed = NumberRange.new(20, 30),
		SpreadAngle = Vector2.new(30, 30),
		EmissionDirection = Enum.NormalId.Front,
		Orientation = Enum.ParticleOrientation.VelocityParallel,
		Drag = 6,
	}):Emit(5)
	Kit.emitter(ctx, holder, {
		Texture = T.EbSpark,
		Color = ColorSequence.new(PURPLE_SOFT, PURPLE),
		LightEmission = 1,
		Brightness = 2.5,
		Size = seq({ { 0, 0.5 }, { 1, 0 } }),
		Transparency = seq({ { 0, 0 }, { 1, 0.7 } }),
		Lifetime = NumberRange.new(0.12, 0.24),
		Speed = NumberRange.new(10, 18),
		SpreadAngle = Vector2.new(60, 60),
		EmissionDirection = Enum.NormalId.Front,
		Orientation = Enum.ParticleOrientation.VelocityParallel,
		Acceleration = Vector3.new(0, -18, 0),
		Drag = 5,
	}):Emit(6)
	local flash = Instance.new("Part")
	flash.Name = "WhirlFlash"
	flash.Shape = Enum.PartType.Ball
	flash.Material = Enum.Material.Neon
	flash.Color = WHITE
	flash.Transparency = 0.15
	flash.Size = Vector3.new(0.3, 0.3, 0.3)
	Kit.decor(flash)
	flash.CFrame = CFrame.new(hitAt)
	flash.Parent = ctx.folder
	ctx:tween(flash, 0.1, { Size = Vector3.new(1.3, 1.3, 1.3), Transparency = 1, Color = PURPLE_SOFT })
	Kit.sound(SOUNDS.hit, if isMine(character) then nil else hitAt)
end

local function playCast(payload: any, character: Model)
	local origin = payload.origin :: CFrame
	local castDelay = SKILL.castDelay
	local spinTime = if type(payload.spinTime) == "number" then payload.spinTime else (SKILL.spinTime or 0.9)
	local turns = if type(payload.turns) == "number" then payload.turns else (SKILL.turns or 3)
	local spinEnd = castDelay + spinTime
	local preview = payload.timeScale ~= nil
	local mine = isMine(character) and not preview
	local ctx = Kit.begin("BladeWhirl", spinEnd + VANISH + 0.8, payload.timeScale)
	local function atAbs(seconds: number, fn: () -> ())
		ctx:at(math.max(seconds - ctx:clock(), 0), fn)
	end
	local humanoid = character:FindFirstChildOfClass("Humanoid")
	local root = character:FindFirstChild("HumanoidRootPart") :: BasePart?
	local baseYaw = yawOf(origin.LookVector)
	local function centerPos(): Vector3
		local p = if root and root.Parent then root.Position else origin.Position
		return p + Vector3.new(0, BLADE_HEIGHT, 0)
	end
	local ground = Kit.ground(origin.Position, { character, ctx.folder })

	-- 1. 발동: 발밑 검은 연기 + 보라 기운이 몸 둘레로 모임
	Kit.smokeRing(ctx, ground, SMOKE_RADIUS, { duration = 0.6, count = 6, color = SMOKE, light = 0.6 })
	local shell = Kit.holder(ctx, CFrame.new(centerPos()), "WhirlGather")
	shell.Size = Vector3.new(7, 3, 7)
	Kit.emitter(ctx, shell, moteProps({
		Size = seq({ { 0, 0.3 }, { 1, 0.08 } }),
		Transparency = seq({ { 0, 0.4 }, { 0.5, 0.2 }, { 1, 1 } }),
		Lifetime = NumberRange.new(0.16, 0.22),
		Speed = NumberRange.new(10, 14),
		Shape = Enum.ParticleEmitterShape.Cylinder,
		ShapeInOut = Enum.ParticleEmitterShapeInOut.Inward,
		ShapeStyle = Enum.ParticleEmitterShapeStyle.Surface,
	})):Emit(16)
	local light = Instance.new("PointLight")
	light.Color, light.Range, light.Brightness, light.Shadows = PURPLE, 12, 0, false
	light.Parent = shell
	ctx:tween(light, castDelay, { Brightness = 1.6 })
	Kit.casterSound(SOUNDS.gather, character, origin.Position)

	-- 내 캐릭터: 회전 잠금 + 휘두른 자세 (무엇이 실패해도 끝나면 반드시 풀림)
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
			root.CFrame = CFrame.new(root.Position) * CFrame.Angles(0, baseYaw, 0) -- 처음 바라보던 쪽으로
		end
		if track and track.IsPlaying then
			track:Stop(0.2)
		end
		if unlock then
			unlock()
		end
	end
	task.delay((spinEnd + 0.4) / ctx.scale, release)

	-- 2. 회전: 칼날 2장이 몸 둘레를 감싸며 돎 (몸과 같은 각도, turns 바퀴)
	local template = script:FindFirstChild("WhirlBlade")
	local blades = if template and template:IsA("MeshPart") then meshBlades(ctx, template) else beamBlades(ctx)
	local tipHolders: { BasePart } = {}
	local tipEmitters: { ParticleEmitter } = {}
	for k = 1, 2 do
		local h = Kit.holder(ctx, CFrame.new(centerPos()), "WhirlTip" .. k)
		table.insert(tipHolders, h)
		table.insert(tipEmitters, Kit.emitter(ctx, h, moteProps({
			Rate = 0,
			Size = seq({ { 0, 0.22 }, { 1, 0 } }),
			Transparency = seq({ { 0, 0.1 }, { 1, 1 } }),
			Lifetime = NumberRange.new(0.18, 0.3),
			Speed = NumberRange.new(0.5, 1.5),
			SpreadAngle = Vector2.new(180, 180),
			Drag = 3,
		})))
	end
	local tilt = CFrame.Angles(BLADE_TILT, 0, 0)
	local function angleAt(t: number): number
		if t <= castDelay then
			return 0
		end
		if t <= spinEnd then
			return turns * math.pi * 2 * (t - castDelay) / spinTime
		end
		-- 끝난 뒤: 같은 속도에서 빠르게 느려짐
		local w = turns * math.pi * 2 / spinTime
		local e = t - spinEnd
		return turns * math.pi * 2 + w * VANISH * (1 - (1 - math.min(e / VANISH, 1)) ^ 2) / 2
	end
	blades.place(CFrame.new(centerPos()), 0.6, 1)
	atAbs(castDelay, function()
		light.Brightness = 1.2
		for _, e in tipEmitters do
			e.Rate = 45
		end
		for i = 0, turns - 1 do
			ctx:at(spinTime / turns * i, function()
				Kit.casterSound(SOUNDS.turn, character, origin.Position)
			end)
		end
	end)
	ctx:step(spinEnd + VANISH, function(t)
		local yaw = baseYaw + angleAt(t)
		local center = CFrame.new(centerPos()) * CFrame.Angles(0, yaw, 0) * tilt
		local k, fade = 0.6, 1
		if t >= castDelay and t < castDelay + APPEAR then
			local s = (t - castDelay) / APPEAR
			s = 1 - (1 - s) ^ 2
			k, fade = 0.6 + 0.4 * s, 1 - s
		elseif t >= castDelay + APPEAR and t < spinEnd then
			k, fade = 1, 0
		elseif t >= spinEnd then
			local s = math.min((t - spinEnd) / VANISH, 1)
			k, fade = 1 + 0.12 * s, s * s
		end
		blades.place(center, k, fade)
		for i, h in tipHolders do
			local b = ARC_TO + math.pi * (i - 1)
			h.CFrame = center * CFrame.new(onCircle(b, R * k - 0.25))
		end
		if mine and root and root.Parent and t >= castDelay and t < spinEnd and not released then
			root.CFrame = CFrame.new(root.Position) * CFrame.Angles(0, yaw, 0)
		end
	end)

	-- 미리보기: 서버 타격 대신 타 시각마다 앞쪽에 맞음 연출
	if preview then
		for _, ht in (if type(payload.hitTimes) == "table" then payload.hitTimes else {}) do
			atAbs(ht, function()
				local p = origin.Position + origin.LookVector * 5
				playHit({ origin = origin, timeScale = payload.timeScale }, character, p)
			end)
		end
	end

	-- 3. 끝: 칼날이 사라지고 원을 따라 보라 잔광
	atAbs(spinEnd, function()
		for _, e in tipEmitters do
			e.Rate = 0
		end
		release()
		local ring = Kit.holder(ctx, CFrame.new(centerPos()), "WhirlAfterglow")
		ring.Size = Vector3.new(R * 2, 0.2, R * 2)
		Kit.emitter(ctx, ring, moteProps({
			Color = ColorSequence.new(PURPLE_SOFT, PURPLE_DIM),
			Size = seq({ { 0, 0.28 }, { 1, 0 } }),
			Transparency = seq({ { 0, 0.2 }, { 1, 1 } }),
			Lifetime = NumberRange.new(0.35, 0.55),
			Speed = NumberRange.new(0.3, 1),
			Acceleration = Vector3.new(0, 1.5, 0),
			Shape = Enum.ParticleEmitterShape.Cylinder,
			ShapeStyle = Enum.ParticleEmitterShapeStyle.Surface,
			Drag = 2,
		})):Emit(22)
		ctx:tween(light, 0.4, { Brightness = 0 })
	end)
end

function BladeWhirl.play(payload: any, character: Model)
	if payload.phase == "hit" then
		playHit(payload, character)
		return
	end
	playCast(payload, character)
end

return BladeWhirl
