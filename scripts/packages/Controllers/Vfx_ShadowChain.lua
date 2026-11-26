--!strict
-- 그림자 연쇄 연출 (Skills.shadow_chain, kind "chain", vfx = "ShadowChain"). 단검 색 = 흰 + 보라 + 검은 연기.
-- 원본: 저장소 scripts/packages/Controllers/Vfx_ShadowChain.lua (Controllers 패키지 SkillController.Vfx.ShadowChain)
-- 2026-11-26 2차: 자체 텍스처 (저장소 scripts/vfx_shadow_chain_tex.py, Python numpy·Pillow — ID 는 exports/texture_ids.json VFX.ShadowChain)
--   잉크 연기 8x8 플립북(2D 흐름 계산) / 궤적 몸통·테두리 Beam / 칼자국 4x4 플립북 두 장 엇갈려 X / 표식 문양
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

-- 자체 텍스처 (흰색 + 알파, 색은 여기서 칠함)
local TEX = {
	ink = "rbxassetid://108787658210747", -- 잉크 연기 8x8 (64칸)
	streakBody = "rbxassetid://139998008469812", -- 궤적 몸통 (가로 0 출발 → 1 도착)
	streakEdge = "rbxassetid://95405263185689", -- 궤적 테두리 선 + 심
	slash = "rbxassetid://112085606213352", -- 칼자국 4x4 (16칸: 그어짐 → 머묾 → 갈라져 사라짐)
	mark = "rbxassetid://125070638939268", -- 표식 (끊긴 고리 + 네 갈래 가시)
	-- 2차 (같은 날): 플라즈마 구슬 (scripts/vfx_shadow_chain_plasma.py) — 넓게 퍼진 구름이 빠르게 압축 → 핵이 터짐
	plasmaOrb = "rbxassetid://93620747404382", -- 모임 4x4 (색 들어감, 압축 → 번개가 핵으로)
	plasmaPop = "rbxassetid://120435824829957", -- 핵 폭발 4x4 (섬광 → 충격파 → 껍질 찢어짐 → 잔광)
	burstGlow = "rbxassetid://96253058174530", -- 가운데 빛 구슬
}
task.spawn(function()
	local list = {}
	for _, id in TEX do
		local d = Instance.new("Decal")
		d.Texture = id
		table.insert(list, d)
	end
	pcall(function()
		game:GetService("ContentProvider"):PreloadAsync(list)
	end)
end)

local GHOST_LIFE = 0.35
local STREAK_LIFE = 0.28 -- 그림자 궤적이 남는 시간
local SLASH_SIZE, SLASH_LIFE = 9, 0.34 -- 칼자국 플립북 크기 (스터드)·재생 시간
local EXEC_SIZE = 11 -- 처형 X (missing 에 따라 최대 1.5배)
local MARK_SIZE = 4.2 -- 표식 지름
local DIM = { brightness = -0.14, saturation = -0.5, contrast = 0.15 } -- 처형 직전 내 화면 눌림
-- 플라즈마: 모임 크기 = Size 키 (크게 퍼진 구름 9.5 → 압축 4.2, 텍스처 ORB_SIZE_KEYS 와 같음), 폭발 = 캐릭터보다 조금 큼
local ORB_SIZE_KEYS = { { 0, 9.5 }, { 0.12, 8.2 }, { 0.3, 3.9 }, { 0.38, 4.5 }, { 0.48, 4.2 }, { 1, 4.2 } }
local POP_SIZE, POP_LIFE = 9, 0.55
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
	marks: { BillboardGui },
	done: boolean,
	mine: boolean,
	dim: ColorCorrectionEffect?,
	burst: { holder: BasePart, board: BillboardGui, core: ImageLabel, halo: ImageLabel, orb: ParticleEmitter, follow: BasePart? }?,
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

-- 잉크 연기 (자체 8x8 플립북, 검게): inward 면 바깥에서 안으로 빨려 들며 작아짐 (도착), 아니면 퍼짐
local function smokePuff(ctx: Kit.Ctx, at: Vector3, count: number, size: number, inward: boolean)
	local holder = Kit.holder(ctx, CFrame.new(at), "ChainInk")
	holder.Size = Vector3.new(size * 0.5, size * 0.5, size * 0.5)
	local e = Kit.emitter(ctx, holder, {
		Texture = TEX.ink,
		FlipbookLayout = Enum.ParticleFlipbookLayout.Grid8x8,
		FlipbookMode = Enum.ParticleFlipbookMode.OneShot,
		Color = ColorSequence.new(SMOKE),
		LightEmission = 0,
		LightInfluence = 0.25,
		Size = if inward then seq({ { 0, size * 1.1 }, { 1, size * 0.5 } }) else seq({ { 0, size * 0.7 }, { 1, size * 1.3 } }),
		Transparency = seq({ { 0, 0.05 }, { 0.7, 0.25 }, { 1, 1 } }),
		Lifetime = NumberRange.new(0.45, 0.65),
		Speed = if inward then NumberRange.new(4, 7) else NumberRange.new(1, 3),
		Shape = Enum.ParticleEmitterShape.Sphere,
		ShapeInOut = if inward then Enum.ParticleEmitterShapeInOut.Inward else Enum.ParticleEmitterShapeInOut.Outward,
		ShapeStyle = Enum.ParticleEmitterShapeStyle.Surface,
		Rotation = NumberRange.new(0, 360),
		RotSpeed = NumberRange.new(-50, 50),
		Drag = 3,
		ZOffset = 0.5,
	})
	pcall(function()
		(e :: any).FlipbookStartRandom = false
	end)
	e:Emit(count)
	-- 잉크 가장자리에 옅은 보라 기운 (같은 그림, 빛남)
	Kit.emitter(ctx, holder, {
		Texture = TEX.ink,
		FlipbookLayout = Enum.ParticleFlipbookLayout.Grid8x8,
		FlipbookMode = Enum.ParticleFlipbookMode.OneShot,
		Color = ColorSequence.new(PURPLE),
		LightEmission = 0.8,
		LightInfluence = 0,
		Brightness = 1.5,
		Size = seq({ { 0, size * 0.9 }, { 1, size * 1.5 } }),
		Transparency = seq({ { 0, 0.75 }, { 1, 1 } }),
		Lifetime = NumberRange.new(0.35, 0.5),
		Speed = NumberRange.new(1, 2),
		Rotation = NumberRange.new(0, 360),
		ZOffset = 0.3,
	}):Emit(math.max(1, math.floor(count / 2)))
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

-- X 칼자국 (자체 4x4 플립북, 카메라를 봄): 두 장을 ±38° 로 엇갈려, 0.04초 차이. 바깥 보라 번짐 + 흰 심
local function slashX(ctx: Kit.Ctx, center: Vector3, size: number, brightness: number)
	local holder = Kit.holder(ctx, CFrame.new(center), "ChainSlash")
	local base = math.random(-15, 15)
	local function one(rot: number)
		for _, layer in { { color = PURPLE, scale = 1.18, tr = 0.15, b = brightness * 0.8, z = 1 }, { color = WHITE, scale = 1, tr = 0, b = brightness, z = 1.2 } } do
			local e = Kit.emitter(ctx, holder, {
				Texture = TEX.slash,
				FlipbookLayout = Enum.ParticleFlipbookLayout.Grid4x4,
				FlipbookMode = Enum.ParticleFlipbookMode.OneShot,
				Color = ColorSequence.new(layer.color),
				LightEmission = 1,
				LightInfluence = 0,
				Brightness = layer.b,
				Size = NumberSequence.new(size * layer.scale),
				Transparency = NumberSequence.new(layer.tr),
				Lifetime = NumberRange.new(SLASH_LIFE),
				Speed = NumberRange.new(0),
				Rotation = NumberRange.new(rot),
				ZOffset = layer.z,
			})
			pcall(function()
				(e :: any).FlipbookStartRandom = false
			end)
			e:Emit(1)
		end
	end
	one(base + 38)
	ctx:at(0.04, function()
		one(base - 38)
	end)
end

-- 그림자 궤적 (자체 텍스처 Beam 두 겹): 잉크 몸통(검은 보라 → 도착 쪽 보라) + 라일락 테두리 선, 출발 쪽부터 걷힘
local function streak(ctx: Kit.Ctx, from: Vector3, to: Vector3)
	local holder = Kit.holder(ctx, CFrame.new(from), "ChainStreak")
	local a0, a1 = Instance.new("Attachment"), Instance.new("Attachment")
	a0.Parent, a1.Parent = holder, holder
	a0.WorldPosition, a1.WorldPosition = from, to
	local function beam(texture: string, width: number, color: ColorSequence, brightness: number, emission: number): Beam
		local b = Instance.new("Beam")
		b.Attachment0, b.Attachment1 = a0, a1
		b.Texture = texture
		b.TextureMode = Enum.TextureMode.Stretch
		b.Width0, b.Width1 = width, width
		b.Color = color
		b.LightEmission, b.LightInfluence, b.Brightness = emission, 0, brightness
		b.FaceCamera = true
		b.Segments = 1
		b.Transparency = NumberSequence.new(0)
		b.Parent = holder
		return b
	end
	-- 화면 확인 뒤 (2026-11-26): 테두리가 넓고 밝아 흰 판처럼 보여서 좁고 어둡게, 몸통은 어두운 바닥에서 안 보여서 조금 빛나게
	local body = beam(TEX.streakBody, 3.4, ColorSequence.new(SHADOW, PURPLE), 1.6, 0.45)
	local edge = beam(TEX.streakEdge, 2.2, ColorSequence.new(PURPLE, LILAC), 1.6, 1)
	local t0 = ctx:clock()
	ctx:step(t0 + STREAK_LIFE, function(t)
		local k = math.clamp((t - t0) / STREAK_LIFE, 0, 1)
		body.Transparency = seq({ { 0, math.min(1, k * 1.8) }, { 1, k ^ 2 } })
		edge.Transparency = seq({ { 0, math.min(1, k * 2.4) }, { 1, k ^ 1.4 } })
	end)
	ctx:at(STREAK_LIFE + 0.03, function()
		holder:Destroy()
	end)
end

-- 벤 적 표식 (자체 문양, 몸 가운데 카메라를 봄): 확 커지며 나타나 천천히 돎. 처형 때 커지며 터지고, 끝이면 그냥 사라짐
local function addMark(st: State, target: Instance?)
	local root = typeof(target) == "Instance" and target:FindFirstChild("HumanoidRootPart")
	if not (root and root:IsA("BasePart")) then
		return
	end
	local board = Kit.billboard(st.ctx.folder, MARK_SIZE, 3)
	board.Name = "ShadowChainMark"
	board.Adornee = root
	board.AlwaysOnTop = false
	local image = Kit.image(board, TEX.mark, 0.2, 1)
	image.ImageColor3 = LILAC
	image.Rotation = math.random(0, 90)
	st.ctx:tween(image, 0.08, { Size = UDim2.fromScale(1.15, 1.15) }, Enum.EasingStyle.Quart)
	st.ctx:tween(image, 0.12, { Size = UDim2.fromScale(1, 1) }, Enum.EasingStyle.Quad, Enum.EasingDirection.Out, 0.08)
	local t0 = st.ctx:clock()
	st.ctx:step(t0 + 4, function()
		if image.Parent then
			image.Rotation += 1.2
		end
	end)
	table.insert(st.marks, board)
end

local function clearMarks(st: State, burst: boolean)
	for _, b in st.marks do
		local image = b:FindFirstChildOfClass("ImageLabel")
		if burst and image and b.Parent then
			local adornee = b.Adornee
			if adornee and adornee:IsA("BasePart") then
				sparks(st.ctx, adornee.Position, Vector3.yAxis, 5, 20)
			end
			image.ImageColor3 = WHITE
			st.ctx:tween(b, 0.25, { Size = UDim2.fromScale(MARK_SIZE * 2.4, MARK_SIZE * 2.4) }, Enum.EasingStyle.Quart)
			st.ctx:tween(image, 0.25, { ImageTransparency = 1, ImageColor3 = PURPLE }, Enum.EasingStyle.Quad, Enum.EasingDirection.In)
			task.delay(0.3 / st.ctx.scale, function()
				b:Destroy()
			end)
		elseif image then
			st.ctx:tween(image, 0.15, { ImageTransparency = 1 })
			task.delay(0.2 / st.ctx.scale, function()
				b:Destroy()
			end)
		else
			b:Destroy()
		end
	end
	table.clear(st.marks)
end

-- 처형 직전 내 화면 눌림 (ColorCorrection, 내 화면만)
local function dimStart(st: State, time: number)
	if not st.mine then
		return
	end
	local cc = Instance.new("ColorCorrectionEffect")
	cc.Name = "ShadowChainDim"
	cc.Parent = game:GetService("Lighting")
	st.dim = cc
	st.ctx:tween(cc, time, { Brightness = DIM.brightness, Saturation = DIM.saturation, Contrast = DIM.contrast })
end

local function dimRelease(st: State, flash: boolean)
	local cc = st.dim
	if not cc then
		return
	end
	st.dim = nil
	if flash then
		cc.Brightness, cc.Saturation, cc.Contrast = 0.18, -0.2, 0.1
	end
	game:GetService("TweenService"):Create(cc, TweenInfo.new(0.35 / st.ctx.scale), { Brightness = 0, Saturation = 0, Contrast = 0 }):Play()
	task.delay(0.4 / st.ctx.scale, function()
		cc:Destroy()
	end)
end

-- 처형 대상 터짐 시작 (귀환 때): 대상 몸에서 그림자 리본이 말려 들며 빛 구슬을 감쌈 (처형 직후 플립북이 터지는 칸)
local function burstStart(st: State, at: Vector3, follow: BasePart?)
	local ctx = st.ctx
	local holder = Kit.holder(ctx, CFrame.new(at), "ExecuteBurst")
	local gather = SKILL.executeDelay or 0.3
	-- 플라즈마 구슬: 넓게 퍼진 구름이 앞 30% 동안 빠르게 압축, 처형 순간에 마지막 칸 (텍스처에 색이 들어 있어 Color 흰색)
	local orbKeys = {}
	for _, kv in ORB_SIZE_KEYS do
		table.insert(orbKeys, NumberSequenceKeypoint.new(kv[1], kv[2]))
	end
	local orb = Kit.emitter(ctx, holder, {
		Texture = TEX.plasmaOrb,
		FlipbookLayout = Enum.ParticleFlipbookLayout.Grid4x4,
		FlipbookMode = Enum.ParticleFlipbookMode.OneShot,
		Color = ColorSequence.new(WHITE),
		LightEmission = 1,
		LightInfluence = 0,
		Brightness = 1.2,
		Size = NumberSequence.new(orbKeys),
		Transparency = NumberSequence.new(0),
		Lifetime = NumberRange.new(gather + 0.08),
		Speed = NumberRange.new(0),
		Rotation = NumberRange.new(0, 360),
		RotSpeed = NumberRange.new(-40, -40),
		ZOffset = 2,
		LockedToPart = true,
	})
	pcall(function()
		(orb :: any).FlipbookStartRandom = false
	end)
	orb:Emit(1)
	-- 가운데 빛 구슬: 모이는 동안 커지며 밝아짐 (처형 때 번쩍 후 사라짐)
	local board = Kit.billboard(holder, 4.2 * 0.7, 4)
	local halo = Kit.image(board, TEX.burstGlow, 0.3, 1)
	halo.ImageColor3 = LILAC
	halo.ImageTransparency = 0.5
	local core = Kit.image(board, TEX.burstGlow, 0.15, 2)
	core.ImageTransparency = 0.4
	ctx:tween(halo, gather, { Size = UDim2.fromScale(1, 1), ImageTransparency = 0.6 })
	ctx:tween(core, gather, { Size = UDim2.fromScale(0.35, 0.35), ImageTransparency = 0.2 })
	local light = Instance.new("PointLight")
	light.Color, light.Range, light.Brightness, light.Shadows = LILAC, 14, 0, false
	light.Parent = holder
	ctx:tween(light, gather, { Brightness = 3 })
	st.burst = { holder = holder, board = board, core = core, halo = halo, orb = orb, follow = follow }
	-- 대상이 밀려도 따라감 (터지고 나면 그 자리에)
	local t0 = ctx:clock()
	ctx:step(t0 + gather + 0.05, function()
		if follow and follow.Parent and st.burst and st.burst.follow == follow then
			holder.CFrame = CFrame.new(follow.Position + Vector3.new(0, 0.3, 0))
		end
	end)
end

-- 처형 순간: 빛 구슬이 번쩍 커졌다 사라지고 라일락 반짝이가 사방으로 (리본은 플립북이 이어서 터짐). 없으면 바로 만듦
local function burstPop(st: State, at: Vector3, grow: number)
	local b = st.burst
	if not b then
		burstStart(st, at, nil)
		b = st.burst
	end
	if not b then
		return
	end
	b.follow = nil
	local ctx = st.ctx
	-- 압축된 구슬을 거두고 같은 자리에서 핵 폭발 (캐릭터보다 조금 큼, missing 에 따라 최대 1.2배)
	b.orb:Clear()
	local popSize = POP_SIZE * math.min(grow, 1.2)
	local pop = Kit.emitter(ctx, b.holder, {
		Texture = TEX.plasmaPop,
		FlipbookLayout = Enum.ParticleFlipbookLayout.Grid4x4,
		FlipbookMode = Enum.ParticleFlipbookMode.OneShot,
		Color = ColorSequence.new(WHITE),
		LightEmission = 1,
		LightInfluence = 0,
		Brightness = 1.4,
		Size = NumberSequence.new(popSize),
		Transparency = NumberSequence.new(0),
		Lifetime = NumberRange.new(POP_LIFE),
		Speed = NumberRange.new(0),
		Rotation = NumberRange.new(0, 360),
		ZOffset = 2,
		LockedToPart = true,
	})
	pcall(function()
		(pop :: any).FlipbookStartRandom = false
	end)
	pop:Emit(1)
	b.board.Size = UDim2.fromScale(popSize * 0.5, popSize * 0.5)
	b.core.Size, b.core.ImageTransparency = UDim2.fromScale(0.5, 0.5), 0.1
	b.halo.Size, b.halo.ImageTransparency = UDim2.fromScale(1.1, 1.1), 0.45
	ctx:tween(b.core, 0.35, { Size = UDim2.fromScale(0.2, 0.2), ImageTransparency = 1 }, Enum.EasingStyle.Quad, Enum.EasingDirection.In, 0.05)
	ctx:tween(b.halo, 0.4, { Size = UDim2.fromScale(1.6, 1.6), ImageTransparency = 1 }, Enum.EasingStyle.Quad, Enum.EasingDirection.Out)
	local light = b.holder:FindFirstChildOfClass("PointLight")
	if light then
		light.Brightness, light.Range = 7, 20 * grow
		ctx:tween(light, 0.45, { Brightness = 0 })
	end
	Kit.emitter(ctx, b.holder, {
		Texture = T.HolySparkle,
		Color = ColorSequence.new(WHITE, LILAC),
		LightEmission = 1,
		Brightness = 3,
		Size = seq({ { 0, 0.45 }, { 1, 0 } }),
		Transparency = seq({ { 0, 0 }, { 1, 0.6 } }),
		Lifetime = NumberRange.new(0.35, 0.7),
		Speed = NumberRange.new(18, 32),
		SpreadAngle = Vector2.new(180, 180),
		Drag = 4,
		Shape = Enum.ParticleEmitterShape.Sphere,
		ShapeStyle = Enum.ParticleEmitterShapeStyle.Surface,
	}):Emit(26)
	st.burst = nil
end

-- 끝: 몸이 다시 보이고 회전 잠금·고정 풂 (여러 번 불려도 한 번만)
local function finish(st: State)
	if st.done then
		return
	end
	st.done = true
	st.pin = nil
	dimRelease(st, false)
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
	smokePuff(ctx, dest.Position, 3, 4, true)
	slashX(ctx, point + Vector3.new(0, 0.4, 0), SLASH_SIZE, 3)
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
	if payload.timeScale == nil then
		dimStart(st, SKILL.executeDelay or 0.3)
	end
	-- 처형 대상 몸에서 그림자 리본이 모이기 시작
	local target = payload.target
	local targetRoot = typeof(target) == "Instance" and target:FindFirstChild("HumanoidRootPart")
	if targetRoot and targetRoot:IsA("BasePart") then
		burstStart(st, targetRoot.Position + Vector3.new(0, 0.3, 0), targetRoot)
	elseif typeof(payload.point) == "Vector3" then
		burstStart(st, payload.point + Vector3.new(0, 0.3, 0), nil)
	end
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
	slashX(ctx, point + Vector3.new(0, 0.5, 0), EXEC_SIZE * grow, 2.2 + 1 * missing) -- 핵 폭발이 가려지지 않게 (원래 17·4+2m)
	sparks(ctx, point, (point - dest.Position).Unit, 14, 40)
	-- 처형 문양 충격: 표식 그림이 크게 퍼지며 사라짐 + 빛
	local shock = Kit.holder(ctx, CFrame.new(point), "ExecuteShock")
	local board = Kit.billboard(shock, 3, 4)
	local mark = Kit.image(board, TEX.mark, 1, 1)
	mark.ImageColor3 = WHITE
	ctx:tween(board, 0.3, { Size = UDim2.fromScale(11 * grow, 11 * grow) }, Enum.EasingStyle.Quart)
	ctx:tween(mark, 0.3, { ImageTransparency = 1, ImageColor3 = PURPLE, Rotation = 45 }, Enum.EasingStyle.Quad, Enum.EasingDirection.In)
	local light = Instance.new("PointLight")
	light.Color, light.Range, light.Brightness, light.Shadows = LILAC, 18 * grow, 6, false
	light.Parent = shock
	ctx:tween(light, 0.4, { Brightness = 0 })
	smokePuff(ctx, point, 6, 7 * grow, false)
	Kit.smokeRing(ctx, Kit.ground(point, { character, ctx.folder }), 4 * grow, { duration = 0.8, count = 9, color = SMOKE, light = 0.6 })
	burstPop(st, point + Vector3.new(0, 0.3, 0), grow)
	dimRelease(st, true)
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
	if st.burst then
		st.burst.holder:Destroy() -- 처형 없이 끝: 모이던 리본·빛 거둠
		st.burst = nil
	end
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
			onReturn(st, character, { origin = back, from = prev, point = first })
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
