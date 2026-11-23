--!strict
-- Spear of God 연출 (창 무기 스킬 신의 창, 흰 + 초록). 서버(Skill 서비스 kind "skyfall")가 정한 꽂히는 자리·시각에 맞춘다.
--   예고  0 ~ castDelay + warnTime   바닥 빛의 원(반경 radius) + 바깥에서 조여드는 고리, 하늘에서 내려오며 굵어지는 빛 기둥,
--                                    castDelay 부터 하늘 높이(SKY_HEIGHT)에 거대한 빛의 창이 빛 알갱이에서 맞춰지며 나타나 떠 있음
--   꽂힘  castDelay + warnTime       창이 내리꽂힘(DROP_TIME) → 섬광·충격파 시트·균열·흰 먼지 폭발·초록 불뛰·돌 파편·돌판·화면 흔들림·묵직한 소리
--   박힘  꽂힌 뒤 skill.root 초       창이 땅에 박혀 빛남 → 아래부터 투명해지며 빛 조각으로 흩어짐
--   속박  phase "pin" (서버, 꽂힌 순간)  맞은 대상마다 창 → 발밑까지 빛의 사슬 + 발밑 빛 고리 (root 초, 끝에 부서짐). 보스(pinned = false)는 반짝임만
-- 에셋: 창 메시 ReplicatedStorage.Assets.Vfx.GodSpear (scripts/vfx_god_spear.py, 피벗 = 창끝, +Y = 꼬리, 길이 40)
--   충격파·먼지·균열 시트는 도약 찌르기와 같은 Blender 시트 (exports/texture_ids.json VFX.LeapStrike), 돌판·돌은 Assets.Vfx.LeapStrike
-- 원본: 저장소 scripts/packages/Controllers/Vfx_GodSpear.lua (마을 place 에서 고친 뒤 이 파일도 같이)

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Debris = game:GetService("Debris")

local T = require(ReplicatedStorage.Shared.Config.VfxConfig).TEXTURES
local Skills = require(ReplicatedStorage.Shared.Data.Skills)
local Kit = require(script.Parent.Parent.VfxKit)
local PiercingLunge = require(script.Parent.PiercingLunge)

local SKILL = Skills.god_spear
local seq = Kit.seq
local WHITE = Color3.new(1, 1, 1)
local GREEN = Color3.fromRGB(70, 255, 110)
local GREEN_SOFT = Color3.fromRGB(170, 255, 185)
local GREEN_DEEP = Color3.fromRGB(20, 150, 55)

local SHEET = {
	dust = "rbxassetid://138956275728767",
	shock = "rbxassetid://139231006156621",
	crack = "rbxassetid://110852548933346",
}
local SHEET_GRID, SHEET_CELL = 8, 128

-- 조정용 상수
local SKY_HEIGHT = 70 -- 떠 있는 창의 창끝 높이 (꽂히는 바닥 기준)
local APPEAR_TIME = 0.35 -- 창이 맞춰지며 나타나는 시간
local DROP_TIME = 0.14 -- 내리꽂히는 시간 (꽂히는 시각에 끝남)
local SPEAR_SINK = 5 -- 창끝이 땅에 박히는 깊이
local SPEAR_TILT = 4 -- 박힐 때 기울기 (도, 방향은 무작위)
local PILLAR_TOP = 160 -- 빛 기둥이 시작되는 높이
local SHAKE_TIME, SHAKE_AMOUNT = 0.4, 0.9
local SHAKE_RANGE = 70 -- 내 캐릭터가 이 거리 안이면 (남이 써도) 화면 흔들림
local SHOCK_TIME = 0.85
local DUST_COUNT = 18
local ROCK_COUNT = 16
local CRACK_HOLD, CRACK_FADE = 2.6, 0.9
local SLAB_RISE, SLAB_HOLD, SLAB_SINK = 0.12, 1.6, 0.7
local LINK_LEN = 1.1 -- 빛의 사슬 고리 하나 길이
local DUST_COLOR = Color3.fromRGB(255, 255, 255)
local DUST_LIGHT_INFLUENCE = 0.1 -- 창·섬광의 초록 불빛에 먼지가 초록으로 물들지 않게 (0.35 에서 낮춤)

local SOUNDS = {
	call = { id = "rbxassetid://9113450910", volume = 0.6, speed = 0.75 }, -- 창을 치켜들며 부르는 쇠·유리 울림 (낮게)
	descend = { id = "rbxassetid://9114159112", volume = 0.9, speed = 0.65, fadeAfter = 1.1, range = 220 }, -- 하늘에서 내려오는 바람
	land = { id = "rbxassetid://9118617342", volume = 1, speed = 0.6, range = 260 }, -- 땅을 깨는 묵직한 충격 (낮게)
	stab = { id = "rbxassetid://9113567601", volume = 1, speed = 0.7, range = 220 }, -- 꽂히는 타격음
	chain = { id = "rbxassetid://9113450910", volume = 0.45, speed = 1.35 }, -- 사슬이 감기는 맑은 소리
	shatter = { id = "rbxassetid://9113450910", volume = 0.7, speed = 1.7 }, -- 결정이 부서지는 소리
}
Kit.preloadSounds(SOUNDS)
task.spawn(function()
	local list = {}
	for _, id in SHEET do
		local d = Instance.new("Decal")
		d.Texture = id
		table.insert(list, d)
	end
	pcall(function()
		game:GetService("ContentProvider"):PreloadAsync(list)
	end)
end)

local GodSpear = {}

local function assets(name: string): Instance?
	local a = ReplicatedStorage:FindFirstChild("Assets")
	local v = a and a:FindFirstChild("Vfx")
	return v and v:FindFirstChild(name)
end

-- 바닥에 눕힌 판 + SurfaceGui (위를 봄)
local function groundGui(ctx: Kit.Ctx, at: Vector3, size: number, name: string, light: number, brightness: number, yaw: number): (BasePart, SurfaceGui)
	local part = Kit.holder(ctx, CFrame.new(at + Vector3.new(0, 0.06, 0)) * CFrame.Angles(0, yaw, 0), name)
	part.Size = Vector3.new(size, 0.05, size)
	local gui = Instance.new("SurfaceGui")
	gui.Face = Enum.NormalId.Top
	gui.LightInfluence = light
	gui.Brightness = brightness
	gui.SizingMode = Enum.SurfaceGuiSizingMode.PixelsPerStud
	gui.PixelsPerStud = 12
	gui.ClipsDescendants = true
	gui.ZOffset = 1
	gui.Parent = part
	return part, gui
end

local function sheetLabel(gui: SurfaceGui, image: string): ImageLabel
	local label = Instance.new("ImageLabel")
	label.BackgroundTransparency = 1
	label.Size = UDim2.fromScale(1, 1)
	label.Image = image
	label.ImageRectSize = Vector2.new(SHEET_CELL, SHEET_CELL)
	label.ImageRectOffset = Vector2.zero
	label.Parent = gui
	return label
end

local function playSheet(ctx: Kit.Ctx, label: ImageLabel, start: number, duration: number)
	label.Visible = false
	local frames = SHEET_GRID * SHEET_GRID
	ctx:step(start + duration + 0.05, function(t)
		if t < start then
			return
		end
		local i = math.floor((t - start) / duration * frames)
		if i >= frames then
			label.Visible = false
			return
		end
		label.Visible = true
		label.ImageRectOffset = Vector2.new((i % SHEET_GRID) * SHEET_CELL, math.floor(i / SHEET_GRID) * SHEET_CELL)
	end)
end

local function dustEmitter(ctx: Kit.Ctx, parent: Instance, life: number, size: NumberRange, speed: NumberRange): ParticleEmitter
	local e = Kit.emitter(ctx, parent, {
		Texture = SHEET.dust,
		FlipbookLayout = Enum.ParticleFlipbookLayout.Grid8x8,
		FlipbookMode = Enum.ParticleFlipbookMode.OneShot,
		Color = ColorSequence.new(DUST_COLOR),
		LightEmission = 0,
		LightInfluence = DUST_LIGHT_INFLUENCE,
		Size = seq({ { 0, size.Min }, { 1, size.Max } }),
		Transparency = seq({ { 0, 0.2 }, { 0.7, 0.4 }, { 1, 1 } }),
		Lifetime = NumberRange.new(life * 0.85, life * 1.15),
		Speed = speed,
		SpreadAngle = Vector2.new(85, 85),
		EmissionDirection = Enum.NormalId.Top,
		Acceleration = Vector3.new(0, 1.5, 0),
		Drag = 3,
		Rotation = NumberRange.new(0, 360),
		RotSpeed = NumberRange.new(-25, 25),
		ZOffset = 3,
	})
	pcall(function()
		(e :: any).FlipbookStartRandom = false
	end)
	return e
end

-- 창 모델의 부품과 원래 투명도 (나타남·사라짐 트윈용)
local function spearParts(model: Instance): { { part: BasePart, base: number } }
	local list = {}
	for _, d in model:GetDescendants() do
		if d:IsA("BasePart") then
			table.insert(list, { part = d, base = d.Transparency })
		end
	end
	return list
end

-- 1. 예고: 바닥 빛의 원 + 조여드는 고리 + 하늘 빛 기둥
local function warning(ctx: Kit.Ctx, ground: Vector3, radius: number, impactAt: number)
	-- 빛의 원 (마법진 층 3장, 천천히 돎)
	local disc = Kit.holder(ctx, CFrame.new(ground + Vector3.new(0, 0.08, 0)), "WarnCircle")
	disc.Size = Vector3.new(radius * 2, 0.05, radius * 2)
	local layers = Kit.surface(disc, { T.HolyCircle_Outer, T.HolyCircle_Inner, T.HolyCircle_Core }, 2.2, { Enum.NormalId.Top })
	local labels: { ImageLabel } = {}
	for i, layer in layers do
		local l = layer[1]
		-- HolyCircle·HaloRing·PillarCore·HolyFlare 텍스처는 금색이라 WHITE 로 두면 금빛 → 초록으로 물들임
		l.ImageColor3 = GREEN
		l.ImageTransparency = 1
		l.Size = UDim2.fromScale(0.6, 0.6)
		ctx:tween(l, 0.18, { ImageTransparency = if i == 1 then 0.15 else 0.45, Size = UDim2.fromScale(1, 1) }, Enum.EasingStyle.Back)
		table.insert(labels, l)
	end
	-- 조여드는 고리: 반경 1.7배 → 반경, 꽂히는 순간 딱 맞음
	local ring = Kit.holder(ctx, CFrame.new(ground + Vector3.new(0, 0.12, 0)), "WarnRing")
	ring.Size = Vector3.new(radius * 2 * 1.7, 0.05, radius * 2 * 1.7)
	local ringImg = Kit.surface(ring, { T.HaloRing }, 3, { Enum.NormalId.Top })[1][1]
	ringImg.ImageColor3 = GREEN -- GREEN_SOFT 는 금색 텍스처와 섞여 노랗게 보였음
	ringImg.ImageTransparency = 1
	ctx:tween(ringImg, 0.15, { ImageTransparency = 0.1 })
	ctx:tween(ring, impactAt, { Size = Vector3.new(radius * 2.05, 0.05, radius * 2.05) }, Enum.EasingStyle.Quad, Enum.EasingDirection.In)
	ctx:step(impactAt, function(t)
		local k = t / impactAt
		disc.CFrame = CFrame.new(disc.Position) * CFrame.Angles(0, t * 0.6, 0)
		labels[2].Rotation = -t * 40
		labels[3].ImageTransparency = 0.45 - 0.35 * k + 0.1 * math.sin(t * 25)
	end)
	-- 꽂히면 원이 크게 번쩍하고 사라짐
	ctx:at(impactAt, function()
		for _, l in labels do
			ctx:tween(l, 0.08, { ImageTransparency = 0, Size = UDim2.fromScale(1.15, 1.15) })
			ctx:tween(l, 0.5, { ImageTransparency = 1 }, Enum.EasingStyle.Quad, Enum.EasingDirection.In, 0.1)
		end
		ctx:tween(ringImg, 0.2, { ImageTransparency = 1 })
	end)

	-- 하늘 빛 기둥: 위에서 내려오며(아랫끝이 내려옴) 굵어지고, 꽂히면 확 굵어졌다 사라짐
	local top = Instance.new("Attachment")
	local bottom = Instance.new("Attachment")
	local anchor = Kit.holder(ctx, CFrame.new(ground), "SkyPillar")
	top.Position = Vector3.new(0, PILLAR_TOP, 0)
	bottom.Position = Vector3.new(0, PILLAR_TOP - 1, 0)
	top.Parent, bottom.Parent = anchor, anchor
	local function beam(texture: string, width: number, color: Color3, brightness: number): Beam
		local b = Instance.new("Beam")
		b.Attachment0, b.Attachment1 = top, bottom
		b.Texture, b.TextureMode = texture, Enum.TextureMode.Stretch
		b.FaceCamera = true
		b.LightEmission, b.LightInfluence, b.Brightness = 1, 0, brightness
		b.Color = ColorSequence.new(color)
		b.Width0, b.Width1 = width, width
		b.Transparency = seq({ { 0, 1 }, { 0.15, 0.35 }, { 0.9, 0.2 }, { 1, 0.6 } })
		b.Segments = 1
		b.Parent = anchor
		return b
	end
	local core = beam(T.PillarCore, 0.6, GREEN_SOFT, 3)
	local halo = beam(T.PillarCore, 2, GREEN, 2)
	local descend = 0.35 -- 기둥 아랫끝이 바닥까지 내려오는 시간
	ctx:step(impactAt + 0.6, function(t)
		local k = math.clamp(t / descend, 0, 1)
		bottom.Position = Vector3.new(0, PILLAR_TOP * (1 - k * k), 0)
		if t < impactAt then
			local w = t / impactAt
			core.Width0, core.Width1 = 0.4 + 1.4 * w, 0.4 + 1.4 * w
			halo.Width0, halo.Width1 = 1.5 + 5 * w, 1.5 + 5 * w
		else
			local f = math.clamp((t - impactAt) / 0.6, 0, 1)
			local burst = (1 - f) * (1 - f)
			core.Width0, core.Width1 = 6 * burst, 6 * burst
			halo.Width0, halo.Width1 = 16 * burst, 16 * burst
		end
	end)
end

-- 2. 하늘 높이 나타나는 거대한 창 → 내리꽂힘 → 박혀 빛남 → 빛 조각으로 흩어짐
-- 반환 없음. 시각: appearAt(창이 나타나기 시작), impactAt(꽂힘), holdTime(박힌 채 있는 시간)
local function spear(ctx: Kit.Ctx, ground: Vector3, appearAt: number, impactAt: number, holdTime: number)
	local template = assets("GodSpear")
	if not template then
		return
	end
	local model = template:Clone()
	local parts = spearParts(model)
	for _, e in parts do
		Kit.decor(e.part)
		e.part.Transparency = 1
	end
	-- 박힌 자리: 창끝이 땅 속 SPEAR_SINK, 무작위 쪽으로 살짝 기울어짐
	local tiltDir = math.random() * math.pi * 2
	local rest = CFrame.new(ground - Vector3.new(0, SPEAR_SINK, 0)) * CFrame.Angles(0, tiltDir, 0) * CFrame.Angles(math.rad(SPEAR_TILT), 0, 0)
	local sky = CFrame.new(ground + Vector3.new(0, SKY_HEIGHT, 0)) * rest.Rotation
	model:PivotTo(sky)
	model.Parent = ctx.folder
	local blade = model:FindFirstChild("Blade") :: BasePart?

	-- 빛: 날 가운데 불빛 + 후광, 맞춰지는 동안 빛 알갱이가 안으로 모임
	local glowAt = Instance.new("Attachment")
	glowAt.Position = Vector3.new(0, 0, 0)
	glowAt.Parent = blade
	local light = Instance.new("PointLight")
	light.Color, light.Range, light.Brightness, light.Shadows = GREEN, 24, 0, false
	light.Parent = glowAt
	local board = Kit.billboard(glowAt, 26, 2)
	local flare = Kit.image(board, T.HolyFlare, 0.2, 1)
	flare.ImageColor3 = GREEN_SOFT
	flare.ImageTransparency = 1
	local gather = blade and Kit.emitter(ctx, blade, {
		Texture = T.HolySparkle,
		Color = ColorSequence.new(WHITE, GREEN),
		LightEmission = 1,
		Brightness = 3,
		Shape = Enum.ParticleEmitterShape.Sphere,
		ShapeStyle = Enum.ParticleEmitterShapeStyle.Surface,
		ShapeInOut = Enum.ParticleEmitterShapeInOut.Inward,
		Size = seq({ { 0, 0.3 }, { 0.6, 0.9 }, { 1, 0 } }),
		Lifetime = NumberRange.new(0.25, 0.35),
		Speed = NumberRange.new(14, 20),
		Rate = 0,
	})
	ctx:at(appearAt, function()
		Kit.sound(SOUNDS.descend, ground + Vector3.new(0, 30, 0))
		for _, e in parts do
			ctx:tween(e.part, APPEAR_TIME, { Transparency = e.base }, Enum.EasingStyle.Quad, Enum.EasingDirection.Out)
		end
		if gather then
			gather.Rate = 160
		end
		ctx:tween(flare, APPEAR_TIME, { ImageTransparency = 0.35, Size = UDim2.fromScale(1, 1) })
		ctx:tween(light, APPEAR_TIME, { Brightness = 2 })
	end)
	ctx:at(appearAt + APPEAR_TIME, function()
		if gather then
			gather.Rate = 0
		end
	end)
	-- 떠 있는 동안 살짝 떨림, 꽂히기 DROP_TIME 전부터 가속하며 내리꽂힘
	local dropStart = impactAt - DROP_TIME
	ctx:step(impactAt, function(t)
		if t < appearAt then
			return
		end
		if t < dropStart then
			local bob = math.sin((t - appearAt) * 9) * 0.25
			model:PivotTo(sky + Vector3.new(0, bob, 0))
		else
			local k = math.clamp((t - dropStart) / DROP_TIME, 0, 1)
			model:PivotTo(sky:Lerp(rest, k * k))
		end
	end)
	ctx:at(impactAt, function()
		model:PivotTo(rest)
	end)
	-- 박힌 채 빛남: 알갱이가 흘러나오고 불빛이 숨쉬듯
	local motes = blade and Kit.emitter(ctx, blade, {
		Texture = T.HolySparkle,
		Color = ColorSequence.new(GREEN_SOFT, GREEN),
		LightEmission = 1,
		Brightness = 2,
		Size = seq({ { 0, 0.4 }, { 1, 0 } }),
		Lifetime = NumberRange.new(0.6, 1.1),
		Speed = NumberRange.new(0.5, 2),
		SpreadAngle = Vector2.new(180, 180),
		Acceleration = Vector3.new(0, 3, 0),
		Rate = 0,
		Shape = Enum.ParticleEmitterShape.Box,
	})
	ctx:at(impactAt, function()
		if motes then
			motes.Rate = 40
		end
		ctx:tween(flare, 0.06, { ImageTransparency = 0, Size = UDim2.fromScale(1.6, 1.6) })
		ctx:tween(flare, 0.4, { ImageTransparency = 0.55, Size = UDim2.fromScale(0.8, 0.8) }, Enum.EasingStyle.Quad, Enum.EasingDirection.Out, 0.06)
	end)
	ctx:step(impactAt + holdTime, function(t)
		if t < impactAt + 0.3 then
			return
		end
		light.Brightness = 1.6 + 0.6 * math.sin((t - impactAt) * 6)
	end)
	-- 흩어짐: 아래(박힌 쪽)부터 투명해지며 빛 조각·알갱이로
	ctx:at(impactAt + holdTime, function()
		if not model.Parent then
			return
		end
		if motes then
			motes.Rate = 0
		end
		Kit.sound(SOUNDS.shatter, ground + Vector3.new(0, 8, 0))
		for _, e in parts do
			local y = (e.part.Position - ground).Y
			ctx:tween(e.part, 0.35, { Transparency = 1 }, Enum.EasingStyle.Quad, Enum.EasingDirection.In, math.clamp(y / 40, 0, 1) * 0.3)
		end
		ctx:tween(flare, 0.25, { ImageTransparency = 1, Size = UDim2.fromScale(2, 2) })
		ctx:tween(light, 0.5, { Brightness = 0 })
		-- 창 길이를 따라 빛 알갱이가 터짐
		local burst = Kit.holder(ctx, rest * CFrame.new(0, SPEAR_SINK + 16, 0), "SpearBurst")
		burst.Size = Vector3.new(2, 32, 2)
		Kit.emitter(ctx, burst, {
			Texture = T.HolySparkle,
			Color = ColorSequence.new(WHITE, GREEN),
			LightEmission = 1,
			Brightness = 3,
			Size = seq({ { 0, 0.7 }, { 1, 0 } }),
			Lifetime = NumberRange.new(0.4, 0.8),
			Speed = NumberRange.new(6, 18),
			SpreadAngle = Vector2.new(180, 180),
			Drag = 3,
			Shape = Enum.ParticleEmitterShape.Box,
		}):Emit(120)
		-- 결정 조각: 창 부품을 작게 복제해 튀김 (이 화면에서만 물리)
		local pieces = { model:FindFirstChild("Blade"), model:FindFirstChild("Collar"), model:FindFirstChild("Butt") }
		for _ = 1, 14 do
			local tpl = pieces[math.random(1, #pieces)]
			if not (tpl and tpl:IsA("BasePart")) then
				continue
			end
			local p = tpl:Clone()
			p:ClearAllChildren()
			p.Size *= math.random(12, 24) / 100
			p.Material = Enum.Material.Neon
			p.Color = GREEN_SOFT
			p.Transparency = 0.15
			local along = SPEAR_SINK + math.random() * 30
			p.CFrame = rest * CFrame.new(0, along, 0) * CFrame.Angles(math.random() * 6, math.random() * 6, math.random() * 6)
			p.Anchored = false
			p.Parent = ctx.folder
			local ang = math.random() * math.pi * 2
			p.AssemblyLinearVelocity = Vector3.new(math.cos(ang), 0, math.sin(ang)) * math.random(8, 20) + Vector3.new(0, math.random(4, 14), 0)
			p.AssemblyAngularVelocity = Vector3.new(math.random(-10, 10), math.random(-10, 10), math.random(-10, 10))
			ctx:tween(p, 0.6, { Transparency = 1 }, Enum.EasingStyle.Quad, Enum.EasingDirection.In, 0.15)
			Debris:AddItem(p, 1)
		end
		Debris:AddItem(model, 0.8)
	end)
end

-- 들린 돌판 (도약 찌르기 돌판 고리를 크게)
local function slabs(ctx: Kit.Ctx, ground: Vector3, scale: number)
	local src = assets("LeapStrike")
	local template = src and src:FindFirstChild("Slabs")
	if not (template and template:IsA("Model")) then
		return
	end
	local ring = template:Clone()
	pcall(function()
		ring:ScaleTo(scale)
	end)
	ring:PivotTo(CFrame.new(ground) * CFrame.Angles(0, math.random() * math.pi * 2, 0))
	ring.Parent = ctx.folder
	for _, p in ring:GetChildren() do
		if not p:IsA("BasePart") then
			continue
		end
		local rest = p.CFrame
		local outward = (rest.Position - ground) * Vector3.new(1, 0, 1)
		local dir = if outward.Magnitude > 0.1 then outward.Unit else Vector3.xAxis
		local axis = dir:Cross(Vector3.yAxis)
		local tilt = math.rad(math.random(20, 36))
		local up = CFrame.new(rest.Position + Vector3.new(0, math.random(30, 70) / 100 * scale, 0)) * CFrame.fromAxisAngle(axis, -tilt) * rest.Rotation
		local sunk = rest - Vector3.new(0, p.Size.Y + 0.3, 0)
		p.CFrame = sunk
		ctx:tween(p, SLAB_RISE + math.random() * 0.05, { CFrame = up }, Enum.EasingStyle.Back, Enum.EasingDirection.Out)
		ctx:at(SLAB_RISE + 0.06 + SLAB_HOLD + math.random() * 0.2, function()
			if p.Parent then
				ctx:tween(p, SLAB_SINK, { CFrame = sunk }, Enum.EasingStyle.Quad, Enum.EasingDirection.In)
			end
		end)
	end
	Debris:AddItem(ring, SLAB_RISE + SLAB_HOLD + SLAB_SINK + 0.5)
end

local function rocks(ctx: Kit.Ctx, ground: Vector3)
	local src = assets("LeapStrike")
	local folder = src and src:FindFirstChild("Rocks")
	local list = folder and folder:GetChildren() or {}
	if #list == 0 then
		return
	end
	for i = 1, ROCK_COUNT do
		local r = (list[math.random(1, #list)] :: BasePart):Clone()
		r.Size *= math.random(90, 200) / 100
		local ang = (i / ROCK_COUNT) * math.pi * 2 + math.random() * 0.4
		local dir = Vector3.new(math.cos(ang), 0, math.sin(ang))
		r.CFrame = CFrame.new(ground + dir * 2 + Vector3.new(0, 0.8, 0)) * CFrame.Angles(math.random() * 6, math.random() * 6, math.random() * 6)
		r.Anchored = false
		r.CanCollide = true
		r.Parent = ctx.folder
		r.AssemblyLinearVelocity = dir * math.random(18, 40) + Vector3.new(0, math.random(22, 42), 0)
		r.AssemblyAngularVelocity = Vector3.new(math.random(-15, 15), math.random(-15, 15), math.random(-15, 15))
		ctx:tween(r, 0.4, { Transparency = 1 }, Enum.EasingStyle.Quad, Enum.EasingDirection.In, 1.3)
		Debris:AddItem(r, 1.8)
	end
end

-- 3. 꽂힘 충격 (크고 화려하게)
local function impactFx(ctx: Kit.Ctx, ground: Vector3, radius: number)
	-- 섬광
	local flashHolder = Kit.holder(ctx, CFrame.new(ground + Vector3.new(0, 3, 0)), "ImpactFlash")
	local board = Kit.billboard(flashHolder, radius * 2.4, 3)
	local flash = Kit.image(board, T.HolyFlare, 0.3, 1)
	flash.ImageColor3 = GREEN_SOFT
	ctx:tween(flash, 0.05, { Size = UDim2.fromScale(1, 1) })
	ctx:tween(flash, 0.45, { ImageTransparency = 1, ImageColor3 = GREEN }, Enum.EasingStyle.Quad, Enum.EasingDirection.In, 0.05)
	local light = Instance.new("PointLight")
	light.Color, light.Range, light.Brightness, light.Shadows = GREEN_SOFT, radius * 2, 3, false
	light.Parent = flashHolder
	ctx:tween(light, 0.35, { Brightness = 0 })

	-- 바닥 충격파 시트 (두 겹: 큰 것 + 빠른 작은 것)
	local _, shockGui = groundGui(ctx, ground, radius * 2.6, "ImpactShock", 0, 2.5, math.random() * math.pi * 2)
	playSheet(ctx, sheetLabel(shockGui, SHEET.shock), ctx:clock(), SHOCK_TIME)
	local _, shockGui2 = groundGui(ctx, ground + Vector3.new(0, 0.03, 0), radius * 1.4, "ImpactShock2", 0, 3, math.random() * math.pi * 2)
	playSheet(ctx, sheetLabel(shockGui2, SHEET.shock), ctx:clock(), SHOCK_TIME * 0.6)
	-- 공중으로 퍼지는 빛 고리
	local ringPart = Kit.holder(ctx, CFrame.new(ground + Vector3.new(0, 1.5, 0)), "ImpactRing")
	ringPart.Size = Vector3.new(4, 0.05, 4)
	local ringImgs = Kit.surface(ringPart, { T.HolyShockRing }, 3, { Enum.NormalId.Top, Enum.NormalId.Bottom })[1]
	for _, l in ringImgs do
		l.ImageColor3 = GREEN_SOFT
	end
	ctx:tween(ringPart, 0.4, { Size = Vector3.new(radius * 3, 0.05, radius * 3) }, Enum.EasingStyle.Quart, Enum.EasingDirection.Out)
	for _, l in ringImgs do
		ctx:tween(l, 0.4, { ImageTransparency = 1 }, Enum.EasingStyle.Quad, Enum.EasingDirection.In)
	end

	-- 균열: 어두운 선 + 초록 빛
	local yaw = math.random() * math.pi * 2
	local _, lineGui = groundGui(ctx, ground, radius * 2.2, "ImpactCrack", 1, 1, yaw)
	local lines = Instance.new("ImageLabel")
	lines.BackgroundTransparency = 1
	lines.Image = SHEET.crack
	lines.ImageRectOffset = Vector2.zero
	lines.ImageRectSize = Vector2.new(512, 512)
	lines.ImageColor3 = Color3.fromRGB(28, 24, 20)
	lines.ImageTransparency = 0.1
	lines.Size = UDim2.fromScale(0.35, 0.35)
	lines.Position = UDim2.fromScale(0.325, 0.325)
	lines.Parent = lineGui
	local _, glowGui = groundGui(ctx, ground + Vector3.new(0, 0.02, 0), radius * 2.2, "ImpactCrackGlow", 0, 3, yaw)
	local glow = lines:Clone()
	glow.ImageRectOffset = Vector2.new(512, 0)
	glow.ImageColor3 = GREEN
	glow.ImageTransparency = 0
	glow.Parent = glowGui
	for _, l in { lines, glow } do
		ctx:tween(l, 0.14, { Size = UDim2.fromScale(1, 1), Position = UDim2.fromScale(0, 0) }, Enum.EasingStyle.Quart, Enum.EasingDirection.Out)
	end
	ctx:tween(glow, 1.2, { ImageTransparency = 1 }, Enum.EasingStyle.Quad, Enum.EasingDirection.In, 0.4)
	ctx:tween(lines, CRACK_FADE, { ImageTransparency = 1 }, Enum.EasingStyle.Quad, Enum.EasingDirection.In, CRACK_HOLD)

	-- 흰 먼지 폭발: 낮게 사방으로 + 창 둘레로 솟는 기둥
	local dustAt = Kit.holder(ctx, CFrame.new(ground + Vector3.new(0, 1.6, 0)), "ImpactDust")
	dustAt.Size = Vector3.new(radius * 0.45, 0.2, radius * 0.45)
	local ring = dustEmitter(ctx, dustAt, 1.5, NumberRange.new(4, 10), NumberRange.new(30, 46))
	ring.Shape = Enum.ParticleEmitterShape.Box
	ring.SpreadAngle = Vector2.new(82, 82)
	ring.Acceleration = Vector3.new(0, -5, 0)
	ring:Emit(DUST_COUNT)
	local column = dustEmitter(ctx, dustAt, 1.7, NumberRange.new(5, 11), NumberRange.new(5, 10))
	column.SpreadAngle = Vector2.new(35, 35)
	column:Emit(4)

	-- 초록 불뛰
	Kit.emitter(ctx, dustAt, {
		Texture = "rbxasset://textures/particles/sparkles_main.dds",
		Color = ColorSequence.new(GREEN_SOFT, GREEN_DEEP),
		LightEmission = 1,
		Size = seq({ { 0, 0.5 }, { 1, 0 } }),
		Lifetime = NumberRange.new(0.4, 0.9),
		Speed = NumberRange.new(35, 70),
		SpreadAngle = Vector2.new(70, 70),
		EmissionDirection = Enum.NormalId.Top,
		Acceleration = Vector3.new(0, -60, 0),
		Drag = 2.5,
	}):Emit(60)

	rocks(ctx, ground)
	slabs(ctx, ground, radius / 9)
	Kit.sound(SOUNDS.land, ground)
	Kit.sound(SOUNDS.stab, ground)
	local me = Players.LocalPlayer.Character
	local myRoot = me and me:FindFirstChild("HumanoidRootPart")
	if myRoot and myRoot:IsA("BasePart") and (myRoot.Position - ground).Magnitude <= SHAKE_RANGE then
		local near = 1 - math.clamp((myRoot.Position - ground).Magnitude / SHAKE_RANGE, 0, 1)
		PiercingLunge.shakeCamera(SHAKE_TIME, SHAKE_AMOUNT * (0.4 + 0.6 * near))
	end
end

-- 4. 속박: 창 아래쪽 → 대상 발밑 빛의 사슬 + 발밑 빛 고리 (root 초 동안, 끝에 부서짐)
local function pinTarget(ctx: Kit.Ctx, center: Vector3, model: Model, duration: number, index: number)
	local root = model:FindFirstChild("HumanoidRootPart") :: BasePart?
	local humanoid = model:FindFirstChildOfClass("Humanoid")
	if not (root and humanoid) then
		return
	end
	local function footPos(): Vector3
		local hip = humanoid.HipHeight + root.Size.Y / 2
		return root.Position - Vector3.new(0, hip - 0.3, 0)
	end
	-- 발밑 빛 고리
	local foot = Kit.holder(ctx, CFrame.new(footPos()), "PinRing")
	local ringSize = math.max(root.Size.X * 2.2, 4.5)
	foot.Size = Vector3.new(ringSize * 1.8, 0.05, ringSize * 1.8)
	local ringLayers = Kit.surface(foot, { T.HaloRing, T.HolyCircle_Core }, 2.6, { Enum.NormalId.Top })
	local ringImg, coreImg = ringLayers[1][1], ringLayers[2][1]
	ringImg.ImageColor3, coreImg.ImageColor3 = GREEN_SOFT, GREEN
	ringImg.ImageTransparency, coreImg.ImageTransparency = 1, 1
	ctx:tween(foot, 0.15, { Size = Vector3.new(ringSize, 0.05, ringSize) }, Enum.EasingStyle.Back)
	ctx:tween(ringImg, 0.15, { ImageTransparency = 0.05 })
	ctx:tween(coreImg, 0.15, { ImageTransparency = 0.5 })

	-- 사슬 고리: 창 아래쪽(바닥 위 2) → 발밑, 0.12초에 뻗어 나감. 고리는 90도씩 교차
	local from = center + Vector3.new(0, 2, 0)
	local links: { BasePart } = {}
	local maxLinks = 30
	for i = 1, maxLinks do
		local link = Instance.new("Part")
		link.Name = "LightLink"
		link.Size = Vector3.new(0.14, 0.5, LINK_LEN * 1.2)
		link.Material = Enum.Material.Neon
		link.Color = if i % 2 == 0 then GREEN_SOFT else GREEN
		link.Transparency = 0.1
		Kit.decor(link)
		link.CFrame = CFrame.new(from)
		link.Parent = ctx.folder
		links[i] = link
	end
	-- 사슬을 감싸는 빛 (Beam)
	local a0 = Instance.new("Attachment")
	local a1 = Instance.new("Attachment")
	local beamHolder = Kit.holder(ctx, CFrame.new(), "PinBeam")
	a0.Parent, a1.Parent = beamHolder, beamHolder
	local glow = Instance.new("Beam")
	glow.Attachment0, glow.Attachment1 = a0, a1
	glow.Texture, glow.TextureMode = T.HolyOrb_Trail, Enum.TextureMode.Stretch
	glow.FaceCamera = true
	glow.LightEmission, glow.LightInfluence, glow.Brightness = 1, 0, 2
	glow.Color = ColorSequence.new(GREEN)
	glow.Width0, glow.Width1 = 1.2, 1.2
	glow.Transparency = seq({ { 0, 0.4 }, { 1, 0.4 } })
	glow.Parent = beamHolder
	local hidden = CFrame.new(0, -1e4, 0)
	local started = ctx:clock()
	local shown = 0
	ctx:step(started + duration, function(t)
		if not root.Parent then
			return
		end
		local to = footPos()
		foot.CFrame = CFrame.new(to + Vector3.new(0, 0.1, 0))
		local grow = math.clamp((t - started) / 0.12, 0, 1)
		local v = (to - from)
		local length = v.Magnitude * grow
		local dir = if v.Magnitude > 1e-3 then v.Unit else Vector3.xAxis
		local count = math.clamp(math.floor(length / LINK_LEN), 0, maxLinks)
		-- 사슬이 살짝 처짐 (가운데가 0.6 아래)
		local parts, frames = {}, {}
		for i = 1, maxLinks do
			table.insert(parts, links[i])
			if i <= count then
				local k0 = (i - 0.5) * LINK_LEN / math.max(v.Magnitude, 1e-3)
				local p = from + v * k0 - Vector3.new(0, 0.6 * 4 * k0 * (1 - k0), 0)
				local twist = if i % 2 == 0 then math.pi / 2 else 0
				table.insert(frames, CFrame.lookAt(p, p + dir) * CFrame.Angles(0, 0, twist))
			else
				table.insert(frames, hidden)
			end
		end
		workspace:BulkMoveTo(parts, frames, Enum.BulkMoveMode.FireCFrameChanged)
		a0.WorldPosition = from
		a1.WorldPosition = from + dir * length
		shown = count
		ringImg.Rotation = t * 90
	end)
	ctx:at(0.02 * index, function()
		Kit.sound(SOUNDS.chain, footPos())
	end)
	-- 끝: 사슬·고리가 빛 조각으로 부서짐
	ctx:at(duration, function()
		local mid = Kit.holder(ctx, CFrame.new((from + footPos()) / 2), "PinBreak")
		mid.Size = Vector3.new(1, 1, math.max((footPos() - from).Magnitude, 1))
		mid.CFrame = CFrame.lookAt(mid.Position, footPos())
		Kit.emitter(ctx, mid, {
			Texture = T.HolySparkle,
			Color = ColorSequence.new(WHITE, GREEN),
			LightEmission = 1,
			Brightness = 3,
			Size = seq({ { 0, 0.4 }, { 1, 0 } }),
			Lifetime = NumberRange.new(0.25, 0.5),
			Speed = NumberRange.new(3, 9),
			SpreadAngle = Vector2.new(180, 180),
			Drag = 4,
			Shape = Enum.ParticleEmitterShape.Box,
		}):Emit(math.clamp(shown * 3, 10, 60))
		for _, l in links do
			ctx:tween(l, 0.15, { Transparency = 1 })
		end
		ctx:tween(glow, 0.15, { Width0 = 0, Width1 = 0 })
		ctx:tween(ringImg, 0.25, { ImageTransparency = 1 })
		ctx:tween(coreImg, 0.25, { ImageTransparency = 1 })
		ctx:tween(foot, 0.25, { Size = Vector3.new(ringSize * 1.6, 0.05, ringSize * 1.6) })
	end)
end

-- 보스 등 속박이 안 걸린 대상: 몸에 반짝임만
local function hitSpark(ctx: Kit.Ctx, model: Model)
	local root = model:FindFirstChild("HumanoidRootPart")
	if not (root and root:IsA("BasePart")) then
		return
	end
	local at = Kit.holder(ctx, root.CFrame, "PinSpark")
	Kit.emitter(ctx, at, {
		Texture = T.HolySparkle,
		Color = ColorSequence.new(WHITE, GREEN),
		LightEmission = 1,
		Brightness = 3,
		Size = seq({ { 0, 0.6 }, { 1, 0 } }),
		Lifetime = NumberRange.new(0.25, 0.5),
		Speed = NumberRange.new(6, 14),
		SpreadAngle = Vector2.new(180, 180),
		Drag = 4,
	}):Emit(30)
end

-- 시전: p = { origin: CFrame(시전 root·방향), center: 꽂히는 바닥 점, radius, warnTime, timeScale }
-- 속박: p = { phase = "pin", origin = CFrame.new(center), targets = { { model, pinned } }, root }
function GodSpear.play(p: any, character: Instance?)
	if p.phase == "pin" then
		if type(p.targets) ~= "table" or typeof(p.origin) ~= "CFrame" then
			return
		end
		local duration = if type(p.root) == "number" then p.root else (SKILL.root or 2)
		local ctx = Kit.begin("GodSpearPin", duration + 1, p.timeScale)
		local center = (p.origin :: CFrame).Position
		for i, t in p.targets do
			local model = t.model
			if typeof(model) == "Instance" and model:IsA("Model") and model.Parent then
				if t.pinned then
					pinTarget(ctx, center, model, duration, i)
				else
					hitSpark(ctx, model)
				end
			end
		end
		return
	end
	if typeof(p.center) ~= "Vector3" then
		return
	end
	local center: Vector3 = p.center
	local radius = if type(p.radius) == "number" then p.radius else (SKILL.radius or 18)
	local warnTime = if type(p.warnTime) == "number" then p.warnTime else (SKILL.warnTime or 0.9)
	local castDelay = SKILL.castDelay
	local impactAt = castDelay + warnTime
	local hold = SKILL.root or 2
	local ctx = Kit.begin("GodSpearFx", impactAt + hold + 2, p.timeScale)
	local origin: CFrame = if typeof(p.origin) == "CFrame" then p.origin else CFrame.new(center)

	Kit.casterSound(SOUNDS.call, character, origin.Position)
	warning(ctx, center, radius, impactAt)
	spear(ctx, center, castDelay, impactAt, hold)
	ctx:at(impactAt, function()
		impactFx(ctx, center, radius)
	end)
end

return GodSpear
