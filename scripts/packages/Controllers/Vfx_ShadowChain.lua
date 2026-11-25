--!strict
-- 그림자 연쇄 연출 (Skills.shadow_chain, kind "chain", vfx = "ShadowChain"). 단검 색 = 흰 + 보라 + 검은 연기.
-- 원본: 저장소 scripts/packages/Controllers/Vfx_ShadowChain.lua (Controllers 패키지 SkillController.Vfx.ShadowChain)
-- 2026-11-26 1차 (임시 연출, 텍스처는 프로젝트 기존 것). 다음 단계에서 Python 붓질·잉크 연기 텍스처로 바꿀 예정.
--   사라짐  시전(phase 없음)   출발 자리: 어두운 잔상 + 발밑 검은 연기 고리 + 연기 덩이. 이때부터 끝날 때까지 몸·무기 빛을 모든 화면에서 숨김
--                              (사용자 결정: 벨 때도 캐릭터는 안 보이고 이펙트만)
--   벰      phase "strike"     서버가 고른 다음 적 뒤(origin = 도착 자리)로: 지나온 길에 그림자 궤적, 도착 자리 작은 연기,
--                              적 몸에 X 칼자국 + 불꽃, 그 적에 보라 표식(처형 때 같이 터짐). 내 캐릭터는 그 자리로 옮겨 고정
--   귀환    phase "return"     마지막 적 → 첫 대상 뒤로 궤적 + 모이는 연기
--   처형    phase "execute"    첫 대상에 큰 X + 섬광 + 표식들이 터짐 + 흔들림 → 몸이 다시 보임 (missing 이 클수록 크고 밝게)
--   끝      phase "finish"     처형 없이 끝 (첫 대상이 죽었음): 표식 거두고 몸이 다시 보임
-- 판정·대상·자리는 서버(Skill 서비스 chainHits)가 정한다. 이 모듈은 보이는 것과 내 캐릭터 이동만.
-- payload.timeScale 이면 개발 명령 /fx 미리보기 (몸 숨김·이동 없이, 앞쪽에 가짜 대상 자리로 이어서 재생).

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local RunService = game:GetService("RunService")

local T = require(ReplicatedStorage.Shared.Config.VfxConfig).TEXTURES :: any
local Skills = require(ReplicatedStorage.Shared.Data.Skills)
local CameraShake = require(ReplicatedStorage.Shared.Util.CameraShake)
local Kit = require(script.Parent.Parent.VfxKit)

local SKILL = Skills.shadow_chain
local seq = Kit.seq

local WHITE = Color3.new(1, 1, 1)
local PURPLE = Color3.fromRGB(110, 0, 230)
local LILAC = Color3.fromRGB(190, 130, 255)
local SHADOW = Color3.fromRGB(30, 8, 55)
local GHOST_COLOR = Color3.fromRGB(45, 10, 80)
local SMOKE = Color3.fromRGB(16, 10, 24)

local GHOST_LIFE = 0.35
local STREAK_LIFE = 0.28 -- 그림자 궤적이 남는 시간
local SLASH_LEN, SLASH_W = 7, 0.7 -- 칼자국 (스터드)
local SLASH_IN, SLASH_OUT = 0.05, 0.16
local EXEC_LEN, EXEC_W = 13, 1.4 -- 처형 X (missing 에 따라 최대 1.5배)
local REVEAL = 0.12 -- 끝나고 몸이 다시 보이는 시간

local SOUNDS = {
	vanish = { id = "rbxassetid://125132253621935", volume = 0.45, speed = 0.8 },
	hop = { id = "rbxassetid://9114159112", volume = 0.45, speed = 2.1, fadeAfter = 0.2 },
	cut = { id = "rbxassetid://9113450910", volume = 0.6, speed = 1.6 },
	hit = { id = "rbxassetid://9113567601", volume = 0.8, speed = 1.35 },
	gather = { id = "rbxassetid://125132253621935", volume = 0.5, speed = 0.65 },
	execute = { id = "rbxassetid://9116687945", volume = 0.9, speed = 1.1 },
	executeHit = { id = "rbxassetid://9118617342", volume = 0.7, speed = 1.3 },
}
Kit.preloadSounds(SOUNDS)

local ShadowChain = {}

-- 시전 하나의 상태 (캐릭터별). 서버 phase 가 올 때마다 이어서 씀
type State = {
	ctx: Kit.Ctx,
	setHidden: ((number) -> ())?,
	unlock: (() -> ())?,
	pin: CFrame?,
	marks: { Instance },
	done: boolean,
	mine: boolean,
}
local active: { [Instance]: State } = {}

local function isMine(character: Instance?): boolean
	local lp = Players.LocalPlayer
	return character ~= nil and lp ~= nil and character == lp.Character
end

local function shakeCamera(time: number, amount: number)
	if not CameraShake.isEnabled() then
		return
	end
	local camera = workspace.CurrentCamera
	local name = "ShadowChainShake"
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

-- 몸 숨기기 (그림자 발걸음과 같음): 이 화면에서만 LocalTransparencyModifier, 무기 빛·파티클도 끔. set(0) 으로 되돌림
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

-- 어두운 잔상 (출발 자리)
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
		ctx:tween(p, GHOST_LIFE, { Transparency = 1, CFrame = part.CFrame + away * 0.8 }, Enum.EasingStyle.Quad, Enum.EasingDirection.Out)
	end
end

local function smokePuff(ctx: Kit.Ctx, at: Vector3, count: number, size: number, inward: boolean)
	local holder = Kit.holder(ctx, CFrame.new(at), "ChainSmoke")
	holder.Size = Vector3.new(size, size, size)
	Kit.emitter(ctx, holder, {
		Texture = T.FsSmokeDark,
		FlipbookLayout = Enum.ParticleFlipbookLayout.Grid4x4,
		FlipbookMode = Enum.ParticleFlipbookMode.OneShot,
		Color = ColorSequence.new(WHITE),
		LightEmission = 0,
		LightInfluence = 0.4,
		Size = if inward then seq({ { 0, size * 0.9 }, { 1, size * 0.3 } }) else seq({ { 0, size * 0.6 }, { 1, size * 1.1 } }),
		Transparency = seq({ { 0, 0.3 }, { 0.6, 0.5 }, { 1, 1 } }),
		Lifetime = NumberRange.new(0.3, 0.45),
		Speed = if inward then NumberRange.new(6, 9) else NumberRange.new(1.5, 3.5),
		Shape = Enum.ParticleEmitterShape.Sphere,
		ShapeInOut = if inward then Enum.ParticleEmitterShapeInOut.Inward else Enum.ParticleEmitterShapeInOut.Outward,
		ShapeStyle = Enum.ParticleEmitterShapeStyle.Surface,
		Rotation = NumberRange.new(0, 360),
		RotSpeed = NumberRange.new(-60, 60),
		Drag = 3,
	}):Emit(count)
end

local function sparks(ctx: Kit.Ctx, at: Vector3, dir: Vector3, count: number, speed: number)
	local holder = Kit.holder(ctx, CFrame.lookAt(at, at + dir), "ChainSparks")
	Kit.emitter(ctx, holder, {
		Texture = T.EbSpark,
		Color = ColorSequence.new(WHITE),
		LightEmission = 1,
		Brightness = 3,
		Orientation = Enum.ParticleOrientation.VelocityParallel,
		Size = seq({ { 0, 0.45 }, { 1, 0 } }),
		Transparency = seq({ { 0, 0 }, { 1, 0.6 } }),
		Lifetime = NumberRange.new(0.1, 0.2),
		Speed = NumberRange.new(speed * 0.6, speed),
		SpreadAngle = Vector2.new(40, 40),
		EmissionDirection = Enum.NormalId.Front,
		Drag = 6,
	}):Emit(count)
	Kit.emitter(ctx, holder, {
		Texture = T.EbSpark,
		Color = ColorSequence.new(LILAC, PURPLE),
		LightEmission = 1,
		Brightness = 2.5,
		Orientation = Enum.ParticleOrientation.VelocityParallel,
		Size = seq({ { 0, 0.55 }, { 1, 0 } }),
		Transparency = seq({ { 0, 0 }, { 1, 0.7 } }),
		Lifetime = NumberRange.new(0.15, 0.28),
		Speed = NumberRange.new(speed * 0.4, speed * 0.7),
		SpreadAngle = Vector2.new(80, 80),
		EmissionDirection = Enum.NormalId.Front,
		Acceleration = Vector3.new(0, -20, 0),
		Drag = 5,
	}):Emit(math.floor(count * 1.4))
end

-- 칼자국 한 줄: center 를 지나 dir 방향으로 길이 len, 가운데 굵고 양 끝 바늘 (바깥 보라 + 흰 심). 순간 그어졌다 가늘어지며 사라짐
local function slashLine(ctx: Kit.Ctx, center: Vector3, dir: Vector3, len: number, width: number, brightness: number)
	local holder = Kit.holder(ctx, CFrame.new(center), "ChainSlash")
	local a, m, b = Instance.new("Attachment"), Instance.new("Attachment"), Instance.new("Attachment")
	a.Parent, m.Parent, b.Parent = holder, holder, holder
	local beams: { { beam: Beam, w: number, base: number } } = {}
	local function beam(p0: Attachment, p1: Attachment, w0: number, w1: number, color: Color3, base: number)
		local bm = Instance.new("Beam")
		bm.Attachment0, bm.Attachment1 = p0, p1
		bm.Width0, bm.Width1 = w0, w1
		bm.Color = ColorSequence.new(color)
		bm.LightEmission, bm.LightInfluence, bm.Brightness = 1, 0, brightness
		bm.FaceCamera = true
		bm.Segments = 1
		bm.Transparency = NumberSequence.new(1)
		bm.Parent = holder
		table.insert(beams, { beam = bm, w = math.max(w0, w1), base = base })
	end
	beam(a, m, 0, width, PURPLE, 0.15)
	beam(m, b, width, 0, PURPLE, 0.15)
	beam(a, m, 0, width * 0.32, WHITE, 0)
	beam(m, b, width * 0.32, 0, WHITE, 0)
	local t0 = ctx:clock()
	ctx:step(t0 + SLASH_IN + SLASH_OUT, function(t)
		local k = t - t0
		local draw = 1 - (1 - math.clamp(k / SLASH_IN, 0, 1)) ^ 3
		local fade = math.clamp((k - SLASH_IN) / SLASH_OUT, 0, 1)
		local half = len / 2
		a.WorldPosition = center - dir * half
		b.WorldPosition = center - dir * half + dir * len * draw
		m.WorldPosition = center - dir * half + dir * len * draw * 0.55
		for _, bb in beams do
			bb.beam.Transparency = NumberSequence.new(bb.base + (1 - bb.base) * fade)
			local thin = 1 - 0.7 * fade
			if bb.beam.Width0 > 0 then
				bb.beam.Width0 = bb.w * thin
			end
			if bb.beam.Width1 > 0 then
				bb.beam.Width1 = bb.w * thin
			end
		end
	end)
	ctx:at(SLASH_IN + SLASH_OUT + 0.03, function()
		holder:Destroy()
	end)
end

-- X 칼자국: 카메라를 향한 평면에서 두 대각선 (angle ± spread)
local function slashX(ctx: Kit.Ctx, center: Vector3, len: number, width: number, brightness: number)
	local cam = workspace.CurrentCamera
	local right = if cam then cam.CFrame.RightVector else Vector3.xAxis
	local up = if cam then cam.CFrame.UpVector else Vector3.yAxis
	local base = math.rad(math.random(-15, 15))
	for i, ang in { base + math.rad(38), base - math.rad(38) } do
		local dir = (right * math.cos(ang) + up * math.sin(ang)).Unit
		if i == 1 then
			slashLine(ctx, center, dir, len, width, brightness)
		else
			ctx:at(0.04, function()
				slashLine(ctx, center, -dir, len, width, brightness)
			end)
		end
	end
end

-- 그림자 궤적: from → to 를 잇는 어두운 보라 띠 + 가는 라일락 심, 끝(도착) 쪽부터 사라짐
local function streak(ctx: Kit.Ctx, from: Vector3, to: Vector3)
	local holder = Kit.holder(ctx, CFrame.new(from), "ChainStreak")
	local a0, a1 = Instance.new("Attachment"), Instance.new("Attachment")
	a0.Parent, a1.Parent = holder, holder
	a0.WorldPosition, a1.WorldPosition = from, to
	local function beam(width: number, color: ColorSequence, brightness: number, emission: number, base: number): Beam
		local b = Instance.new("Beam")
		b.Attachment0, b.Attachment1 = a0, a1
		b.Width0, b.Width1 = width * 0.4, width
		b.Color = color
		b.LightEmission, b.LightInfluence, b.Brightness = emission, 0, brightness
		b.FaceCamera = true
		b.Segments = 1
		b.Transparency = NumberSequence.new(base)
		b.Parent = holder
		return b
	end
	local body = beam(1.6, ColorSequence.new(SHADOW, PURPLE), 1, 0.3, 0.25)
	local core = beam(0.25, ColorSequence.new(PURPLE, LILAC), 3, 1, 0)
	local t0 = ctx:clock()
	ctx:step(t0 + STREAK_LIFE, function(t)
		local k = math.clamp((t - t0) / STREAK_LIFE, 0, 1)
		-- 출발 쪽부터 걷혀 도착 쪽으로 빨려 들어감
		body.Transparency = seq({ { 0, math.min(1, 0.25 + k * 1.6) }, { 1, 0.25 + 0.75 * k ^ 2 } })
		core.Transparency = seq({ { 0, math.min(1, k * 2) }, { 1, k ^ 1.5 } })
	end)
	ctx:at(STREAK_LIFE + 0.03, function()
		holder:Destroy()
	end)
end

-- 벤 적 표식: 몸 둘레를 맴도는 보라 알갱이 (처형·끝 때 거둠)
local function addMark(st: State, target: Instance?)
	local root = typeof(target) == "Instance" and target:FindFirstChild("HumanoidRootPart")
	if not (root and root:IsA("BasePart")) then
		return
	end
	local att = Instance.new("Attachment")
	att.Name = "ShadowChainMark"
	att.Parent = root
	local e = Instance.new("ParticleEmitter")
	e.Texture = T.HolySparkle
	e.Color = ColorSequence.new(LILAC, PURPLE)
	e.LightEmission = 1
	e.Brightness = 2
	e.Size = seq({ { 0, 0.35 }, { 1, 0 } })
	e.Transparency = seq({ { 0, 0.1 }, { 1, 1 } })
	e.Lifetime = NumberRange.new(0.4, 0.6)
	e.Speed = NumberRange.new(1, 2)
	e.SpreadAngle = Vector2.new(180, 180)
	e.Acceleration = Vector3.new(0, 3, 0)
	e.Rate = 25 / st.ctx.scale
	e.TimeScale = st.ctx.scale
	e.Shape = Enum.ParticleEmitterShape.Sphere
	e.ShapeStyle = Enum.ParticleEmitterShapeStyle.Surface
	e.Parent = att
	table.insert(st.marks, att)
end

local function clearMarks(st: State, burst: boolean)
	for _, att in st.marks do
		if att.Parent and burst then
			local pos = (att :: Attachment).WorldPosition
			sparks(st.ctx, pos, Vector3.yAxis, 5, 20)
		end
		att:Destroy()
	end
	table.clear(st.marks)
end

-- 끝: 몸이 다시 보이고 회전 잠금·고정 풂 (여러 번 불려도 한 번만)
local function finish(st: State)
	if st.done then
		return
	end
	st.done = true
	st.pin = nil
	local hide = st.setHidden
	if hide then
		local t0 = st.ctx:clock()
		st.ctx:step(t0 + REVEAL, function(t)
			hide(1 - math.clamp((t - t0) / REVEAL, 0, 1))
		end)
		task.delay(REVEAL / st.ctx.scale + 0.05, function()
			hide(0)
		end)
	end
	if st.unlock then
		st.unlock()
	end
end

local function moveTo(st: State, character: Model, dest: CFrame)
	if not st.mine then
		return
	end
	local root = character:FindFirstChild("HumanoidRootPart") :: BasePart?
	if root then
		root.AssemblyLinearVelocity = Vector3.zero
		character:PivotTo(dest)
	end
	st.pin = dest
end

local function onStrike(st: State, character: Model, payload: any)
	local dest = payload.origin :: CFrame
	local from = if typeof(payload.from) == "Vector3" then payload.from else dest.Position
	local target = payload.target
	local targetRoot = typeof(target) == "Instance" and target:FindFirstChild("HumanoidRootPart")
	local point = if typeof(payload.point) == "Vector3" then payload.point
		elseif targetRoot and targetRoot:IsA("BasePart") then targetRoot.Position
		else (dest * CFrame.new(0, 0, -3.5)).Position
	moveTo(st, character, dest)
	local ctx = st.ctx
	streak(ctx, from + Vector3.new(0, 0.5, 0), dest.Position + Vector3.new(0, 0.5, 0))
	smokePuff(ctx, dest.Position, 5, 3, true)
	slashX(ctx, point + Vector3.new(0, 0.4, 0), SLASH_LEN, SLASH_W, 3)
	local dir = (point - dest.Position) * Vector3.new(1, 0, 1)
	sparks(ctx, point, if dir.Magnitude > 0.1 then dir.Unit else dest.LookVector, 6, 26)
	addMark(st, target)
	Kit.casterSound(SOUNDS.hop, character, dest.Position)
	Kit.sound(SOUNDS.cut, if st.mine then nil else point)
	Kit.sound(SOUNDS.hit, if st.mine then nil else point)
	if st.mine and payload.timeScale == nil then
		shakeCamera(0.06, 0.12)
	end
end

local function onReturn(st: State, character: Model, payload: any)
	local dest = payload.origin :: CFrame
	local from = if typeof(payload.from) == "Vector3" then payload.from else dest.Position
	moveTo(st, character, dest)
	streak(st.ctx, from + Vector3.new(0, 0.5, 0), dest.Position + Vector3.new(0, 0.5, 0))
	smokePuff(st.ctx, dest.Position, 9, 4.5, true)
	local holder = Kit.holder(st.ctx, CFrame.new(dest.Position), "ChainGather")
	local light = Instance.new("PointLight")
	light.Color, light.Range, light.Brightness, light.Shadows = PURPLE, 12, 0, false
	light.Parent = holder
	st.ctx:tween(light, SKILL.executeDelay or 0.3, { Brightness = 3 })
	Kit.casterSound(SOUNDS.gather, character, dest.Position)
end

local function onExecute(st: State, character: Model, payload: any)
	local dest = payload.origin :: CFrame
	local target = payload.target
	local targetRoot = typeof(target) == "Instance" and target:FindFirstChild("HumanoidRootPart")
	local point = if typeof(payload.point) == "Vector3" then payload.point
		elseif targetRoot and targetRoot:IsA("BasePart") then targetRoot.Position
		else (dest * CFrame.new(0, 0, -3.5)).Position
	local missing = if type(payload.missing) == "number" then math.clamp(payload.missing, 0, 1) else 0.5
	local grow = 1 + 0.5 * missing -- 많이 잃었을수록 크게
	local ctx = st.ctx
	slashX(ctx, point + Vector3.new(0, 0.5, 0), EXEC_LEN * grow, EXEC_W * grow, 4 + 2 * missing)
	sparks(ctx, point, (point - dest.Position).Unit, 14, 40)
	-- 섬광 구
	local flash = Instance.new("Part")
	flash.Name = "ExecuteFlash"
	flash.Shape = Enum.PartType.Ball
	flash.Material = Enum.Material.Neon
	flash.Color = WHITE
	flash.Transparency = 0.1
	flash.Size = Vector3.one * 0.6
	Kit.decor(flash)
	flash.CFrame = CFrame.new(point)
	flash.Parent = ctx.folder
	ctx:tween(flash, 0.18, { Size = Vector3.one * 4 * grow, Transparency = 1, Color = LILAC })
	local light = Instance.new("PointLight")
	light.Color, light.Range, light.Brightness, light.Shadows = LILAC, 18 * grow, 6, false
	light.Parent = flash
	smokePuff(ctx, point, 10, 5 * grow, false)
	clearMarks(st, true)
	Kit.casterSound(SOUNDS.execute, character, point)
	Kit.sound(SOUNDS.executeHit, if st.mine then nil else point)
	if st.mine and payload.timeScale == nil then
		shakeCamera(0.18, 0.35 + 0.25 * missing)
	end
	finish(st)
end

local function onFinish(st: State, payload: any)
	clearMarks(st, false)
	if typeof(payload.origin) == "CFrame" then
		smokePuff(st.ctx, payload.origin.Position, 6, 3.5, false) -- 서버가 보낸 지금 자리 (마지막으로 벤 곳)
	end
	finish(st)
end

local function maxLife(): number
	return SKILL.castDelay + (SKILL.hopTime or 0.18) * ((SKILL.maxTargets or 6) - 1) + (SKILL.returnTime or 0.25) + (SKILL.executeDelay or 0.3) + 1.5
end

local function playCast(payload: any, character: Model)
	local origin = payload.origin :: CFrame
	local preview = payload.timeScale ~= nil
	local mine = isMine(character) and not preview
	local life = maxLife()
	local ctx = Kit.begin("ShadowChain", life + 0.8, payload.timeScale)
	local old = active[character]
	if old then
		clearMarks(old, false)
		finish(old)
	end
	local humanoid = character:FindFirstChildOfClass("Humanoid")
	local root = character:FindFirstChild("HumanoidRootPart") :: BasePart?
	local st: State = { ctx = ctx, marks = {}, done = false, mine = mine, pin = if mine and root then root.CFrame else nil }
	active[character] = st
	-- 사라짐
	local at = if root then root.Position else origin.Position
	ghost(ctx, character, -origin.LookVector)
	Kit.smokeRing(ctx, Kit.ground(at, { character, ctx.folder }), 3.2, { duration = 0.75, count = 7, color = SMOKE, light = 0.6 })
	smokePuff(ctx, at, 5, 3, false)
	Kit.casterSound(SOUNDS.vanish, character, at)
	if not preview then
		st.setHidden = hideBody(character)
	end
	if mine and humanoid then
		st.unlock = Kit.lockRotation(humanoid)
		-- 숨어 있는 동안 서버가 정한 자리에 고정 (입력·중력으로 움직이지 않게)
		ctx:step(life, function()
			if st.pin and root and root.Parent then
				root.AssemblyLinearVelocity = Vector3.zero
				root.CFrame = st.pin
			end
		end)
	end
	-- 무엇이 실패해도 몸은 반드시 다시 보이게
	task.delay(life / ctx.scale, function()
		if active[character] == st then
			active[character] = nil
		end
		clearMarks(st, false)
		finish(st)
	end)
	-- 미리보기: 서버 신호 대신 앞쪽 가짜 자리 4곳 → 귀환 → 처형
	if preview then
		local hop = SKILL.hopTime or 0.18
		local spots = { Vector3.new(0, 0, -8), Vector3.new(6, 0, -14), Vector3.new(-4, 0, -19), Vector3.new(-9, 0, -12) }
		local prev = at
		for i, off in spots do
			local p = (origin * CFrame.new(off)).Position
			local dest = CFrame.lookAt(p + (prev - p).Unit * 3.5, p)
			local from = prev
			ctx:at(SKILL.castDelay + hop * (i - 1), function()
				onStrike(st, character, { origin = dest, from = from, point = p, timeScale = payload.timeScale })
			end)
			prev = dest.Position
		end
		local first = (origin * CFrame.new(spots[1])).Position
		local back = CFrame.lookAt(first + (first - at).Unit * 3.5, first)
		local tReturn = SKILL.castDelay + hop * (#spots - 1) + (SKILL.returnTime or 0.25)
		ctx:at(tReturn, function()
			onReturn(st, character, { origin = back, from = prev })
		end)
		ctx:at(tReturn + (SKILL.executeDelay or 0.3), function()
			onExecute(st, character, { origin = back, point = first, missing = 0.6, timeScale = payload.timeScale })
		end)
	end
end

function ShadowChain.play(payload: any, character: Model)
	local phase = payload.phase
	if phase == nil then
		playCast(payload, character)
		return
	end
	local st = active[character]
	if not st then
		return -- 시전 연출을 못 받은 화면 (늦게 들어옴 등): 이후 신호는 무시
	end
	if phase == "strike" then
		onStrike(st, character, payload)
	elseif phase == "return" then
		onReturn(st, character, payload)
	elseif phase == "execute" then
		onExecute(st, character, payload)
		active[character] = nil
	elseif phase == "finish" then
		onFinish(st, payload)
		active[character] = nil
	end
end

return ShadowChain
