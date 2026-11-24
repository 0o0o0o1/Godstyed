--!strict
-- Spear of God 연출 v2 (창 무기 스킬 신의 창, 흰·초록 + 청록·엷은 보라 오로라). 2026-11-24 사용자 피드백으로 새로 씀:
--   "밋밋함, 검이 몰아치듯 빠르게 떨어지게, 3번에 나눠서, 단색이 아니라 오로라치는 영롱하고 화려하지만 깔끔한 창"
-- 서버(Skill 서비스 kind "skyfall")가 정한 세 자리·시각(payload.strikes)에 맞춘다:
--   창마다  꽂히기 FALL_TIME 전  꽂힐 자리에 작은 빛 고리가 번쩍(예고) + 하늘에서 번개 같은 빛 줄기와 함께 창이 내리꽂힘
--           꽂힘                섬광·충격파 시트·빛 균열·연기 고리(Kit.smokeRing)·불뛰·돌 파편·화면 흔들림·소리 (마지막 큰 창은 더 크게 + 돌판)
--           박힘                창 속을 오로라 빛이 흐르고(AuroraFlow) 오로라 커튼 두 줄기가 창을 감아 돎(AuroraCurtain) → 빛 조각으로 흩어짐
--   속박  phase "pin" (서버, 큰 창이 꽂힌 순간)  맞은 대상마다 창 → 발밑 빛의 사슬 + 발밑 빛 고리 (root 초)
-- 에셋: 창 메시 ReplicatedStorage.Assets.Vfx.GodSpear (피벗 = 창끝, +Y = 꼬리, 길이 40) — 작은 창은 Model:ScaleTo
--   오로라 그림 scripts/vfx_aurora.py, 충격파·균열 시트는 도약 찌르기 것 (exports/texture_ids.json)
-- ⚠ HolyCircle·HaloRing·PillarCore·HolyFlare 텍스처는 금색 → GREEN 으로 물들일 것 (WHITE·연초록이면 금빛·노란빛)
-- 원본: 저장소 scripts/packages/Controllers/Vfx_GodSpear.lua

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
local MINT = Color3.fromRGB(190, 255, 215) -- 연초록 (금색이 아닌 텍스처·Neon 용)
local TEAL = Color3.fromRGB(90, 255, 215)
local VIOLET = Color3.fromRGB(190, 160, 255)
local GLASS = Color3.fromRGB(225, 255, 238)

local IMG = {
	auroraCurtain = "rbxassetid://128896189725887", -- 가로 반복, 아래 가장자리 밝은 띠 → 위로 청록·보라 빛살
	auroraFlow = "rbxassetid://115207308874249", -- 가로 반복, 가운데 흰빛 → 바깥 초록·청록
	lightning = { "rbxassetid://99501452920501", "rbxassetid://83874513440546", "rbxassetid://103476098391061", "rbxassetid://75288832809005" }, -- scripts/vfx_lightning.py
	shock = "rbxassetid://139231006156621",
	crack = "rbxassetid://110852548933346",
}
local SHEET_GRID, SHEET_CELL = 8, 128

-- 조정용 상수
local FALL_TIME = 0.12 -- 하늘에서 꽂히기까지 (번개처럼 빠르게)
local SKY_HEIGHT = 75 -- 떨어지기 시작하는 창끝 높이 (큰 창 기준, 작은 창은 크기 비율)
local SPEAR_SINK = 5 -- 창끝이 박히는 깊이 (큰 창 기준)
local SPEAR_TILT = 5 -- 박힐 때 기울기 (도)
local SMALL_LINGER = 0.7 -- 작은 창이 마지막 창 뒤 남아 있는 시간
local BOLT_TOP = 140 -- 빛 줄기 시작 높이
local BOLT_AFTER = 0.22 -- 꽂힌 뒤 빛 줄기가 남는 시간
local CURTAIN_SPIN = 1.1 -- 오로라 커튼 도는 속도 (라디안/초)
local SHAKE_RANGE = 70

-- AI티 줄이기 (사용자 2026-11-24): 값마다 ±k 비율로 흔들어 매번 조금씩 다르게
local function jitter(v: number, k: number): number
	return v * (1 + (math.random() * 2 - 1) * k)
end
-- 소리 높낮이를 매번 조금씩 다르게 (같은 소리가 세 번 반복돼 기계적으로 들리지 않게)
local function vary(def: any, k: number?): any
	local d = table.clone(def)
	d.speed = (def.speed or 1) * jitter(1, k or 0.06)
	return d
end

local SOUNDS = {
	call = { id = "rbxassetid://9113450910", volume = 0.55, speed = 0.75 },
	whoosh = { id = "rbxassetid://9114159112", volume = 0.7, speed = 1.3, fadeAfter = 0.35, range = 200 },
	land = { id = "rbxassetid://9118617342", volume = 0.9, speed = 0.75, range = 240 },
	landBig = { id = "rbxassetid://9118617342", volume = 1, speed = 0.55, range = 280 },
	stab = { id = "rbxassetid://9113567601", volume = 0.9, speed = 0.8, range = 220 },
	chain = { id = "rbxassetid://9113450910", volume = 0.45, speed = 1.35 },
	shatter = { id = "rbxassetid://9113450910", volume = 0.6, speed = 1.7 },
}
Kit.preloadSounds(SOUNDS)
task.spawn(function()
	local list = {}
	for _, id in IMG do
		for _, one in (if type(id) == "table" then id else { id }) do
			local d = Instance.new("Decal")
			d.Texture = one
			table.insert(list, d)
		end
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

local function playSheet(ctx: Kit.Ctx, gui: SurfaceGui, image: string, duration: number)
	local label = Instance.new("ImageLabel")
	label.BackgroundTransparency = 1
	label.Size = UDim2.fromScale(1, 1)
	label.Image = image
	label.ImageRectSize = Vector2.new(SHEET_CELL, SHEET_CELL)
	label.Parent = gui
	local start = ctx:clock()
	local frames = SHEET_GRID * SHEET_GRID
	ctx:step(start + duration + 0.05, function(t)
		local i = math.floor((t - start) / duration * frames)
		if i >= frames then
			label.Visible = false
			return
		end
		label.ImageRectOffset = Vector2.new((i % SHEET_GRID) * SHEET_CELL, math.floor(i / SHEET_GRID) * SHEET_CELL)
	end)
end

local function beam(a0: Attachment, a1: Attachment, props: { [string]: any }): Beam
	local b = Instance.new("Beam")
	b.Attachment0, b.Attachment1 = a0, a1
	b.LightInfluence = 0
	b.LightEmission = 1
	b.Segments = 12
	for k, v in props do
		(b :: any)[k] = v
	end
	b.Parent = a0.Parent
	return b
end

-- 오로라 창 하나: 메시 복제(크기 size) + 맑은 유리 + 날·자루 속 흐르는 오로라 + 감아 도는 커튼 두 줄기 + 끝 빛
-- rig = 모델 피벗에 놓인 투명 파트(모델 안이라 PivotTo 로 같이 움직임), 모든 효과의 Attachment 가 여기 달림
type Spear = {
	model: Model,
	rig: BasePart,
	size: number,
	light: PointLight,
	motes: ParticleEmitter,
	update: (t: number) -> (),
	fade: () -> (),
}
local function makeSpear(ctx: Kit.Ctx, size: number): Spear?
	local template = assets("GodSpear")
	if not (template and template:IsA("Model")) then
		return nil
	end
	local model = template:Clone()
	pcall(function()
		model:ScaleTo(size)
	end)
	local parts: { BasePart } = {}
	for _, d in model:GetDescendants() do
		if d:IsA("BasePart") then
			Kit.decor(d)
			if d.Name == "Core" then
				d.Transparency = 1 -- 심은 오로라 빛(Beam)이 대신함
			elseif d.Name == "Edge" then
				d.Color = MINT
			else
				d.Color = GLASS
				d.Transparency = 0.45 -- 더 맑게 (속 빛이 비침)
			end
			table.insert(parts, d)
		end
	end
	local rig = Instance.new("Part")
	rig.Name = "AuroraRig"
	rig.Size = Vector3.new(0.2, 0.2, 0.2)
	rig.Transparency = 1
	Kit.decor(rig)
	rig.CFrame = model:GetPivot()
	rig.Parent = model
	local function att(y: number): Attachment
		local a = Instance.new("Attachment")
		a.Position = Vector3.new(0, y * size, 0)
		a.Parent = rig
		return a
	end
	-- 날 속 흐르는 빛 (창끝 → 날 뿌리) + 자루 속 가는 빛
	local function flowBeam(a: number, b: number, w0: number, w1: number, len: number, bright: number)
		beam(att(a), att(b), {
			Texture = IMG.auroraFlow,
			TextureMode = Enum.TextureMode.Wrap,
			TextureLength = len * size,
			TextureSpeed = 0.9,
			FaceCamera = true,
			Brightness = bright,
			Color = ColorSequence.new(WHITE),
			Width0 = w0 * size,
			Width1 = w1 * size,
			Transparency = seq({ { 0, 1 }, { 0.08, 0.05 }, { 0.9, 0.1 }, { 1, 1 } }),
		})
	end
	flowBeam(0.6, 14.2, 1.2, 1.0, 9, 3)
	flowBeam(14, 39.5, 0.75, 0.55, 14, 2)
	-- 오로라 커튼 두 줄기: 나선 위 점 5개를 이은 Beam 4개. 점의 X축(Axis) = 나선 접선 → CurveSize 로 둥글게 이어짐
	local R = 2.6 * size
	local y0, y1 = 3, 34
	local turns = 1.15
	local steps = 5
	local curtains: { { atts: { Attachment }, phase: number } } = {}
	local curtainBeams: { Beam } = {}
	for c = 1, 2 do
		local atts = {}
		for i = 0, steps - 1 do
			table.insert(atts, att(y0 + (y1 - y0) * i / (steps - 1)))
		end
		for i = 1, steps - 1 do
			table.insert(curtainBeams, beam(atts[i], atts[i + 1], {
				Texture = IMG.auroraCurtain,
				TextureMode = Enum.TextureMode.Wrap,
				TextureLength = 16 * size,
				TextureSpeed = 0.35,
				FaceCamera = false, -- 나선을 따라 감기는 세로 띠 (true 면 카메라 쪽으로 펴져 톱니 조각처럼 보였음)
				Brightness = 2.2,
				Color = ColorSequence.new(WHITE),
				Width0 = 4 * size,
				Width1 = 4 * size,
				Transparency = seq({
					{ 0, if i == 1 then 1 else 0.25 },
					{ 0.5, 0.25 },
					{ 1, if i == steps - 1 then 1 else 0.25 },
				}),
			}))
		end
		table.insert(curtains, { atts = atts, phase = (c - 1) * math.pi })
	end
	local chord = 2 * R * math.sin(math.pi * turns / (steps - 1))
	for _, b in curtainBeams do
		b.CurveSize0 = chord * 0.36
		b.CurveSize1 = -chord * 0.36
	end
	local rise = (y1 - y0) * size / (turns * 2 * math.pi * R)
	local function update(t: number)
		for _, cur in curtains do
			for i, a in cur.atts do
				local k = (i - 1) / (steps - 1)
				local ang = cur.phase + k * turns * math.pi * 2 + t * CURTAIN_SPIN
				local p = Vector3.new(math.cos(ang) * R, (y0 + (y1 - y0) * k) * size, math.sin(ang) * R)
				local tangent = Vector3.new(-math.sin(ang), rise, math.cos(ang)).Unit
				-- Attachment.Axis(= X축)가 접선을 보게
				a.CFrame = CFrame.fromMatrix(p, tangent, Vector3.yAxis:Cross(tangent).Unit:Cross(tangent))
			end
		end
	end
	update(0)
	-- 창끝 흰빛 + 반짝임, 창 둘레 청록 불빛, 박힌 뒤 흘러나오는 오로라 알갱이
	local tip = att(0.8)
	local tipBoard = Kit.billboard(tip, 7 * size, 3)
	local tipImg = Kit.image(tipBoard, T.HolyFlare, 1, 1)
	tipImg.ImageColor3 = GREEN
	tipImg.ImageTransparency = 0.2
	local tipSparks = Kit.emitter(ctx, tip, {
		Texture = T.HolySparkle,
		Color = ColorSequence.new(WHITE, TEAL),
		LightEmission = 1,
		Brightness = 3,
		Size = seq({ { 0, 0.5 * size }, { 1, 0 } }),
		Lifetime = NumberRange.new(0.3, 0.6),
		Speed = NumberRange.new(1, 4),
		SpreadAngle = Vector2.new(180, 180),
		Rate = 0, -- 창끝 반짝이 분수는 뺌 (반짝이 남발이 AI티)
	})
	local motesAt = att(16)
	local motes = Kit.emitter(ctx, motesAt, {
		Texture = T.HolySparkle,
		Color = ColorSequence.new({ ColorSequenceKeypoint.new(0, MINT), ColorSequenceKeypoint.new(0.6, TEAL), ColorSequenceKeypoint.new(1, VIOLET) }),
		LightEmission = 1,
		Brightness = 2.5,
		Size = seq({ { 0, 0.35 * size + 0.15 }, { 1, 0 } }),
		Lifetime = NumberRange.new(0.6, 1.2),
		Speed = NumberRange.new(1, 4),
		SpreadAngle = Vector2.new(180, 180),
		Acceleration = Vector3.new(0, 4, 0),
		Rate = 0,
	})
	local mid = att(8)
	local light = Instance.new("PointLight")
	light.Color, light.Range, light.Brightness, light.Shadows = TEAL, 22 * size + 6, 0, false
	light.Parent = mid
	local function fade()
		motes.Rate = 0
		tipSparks.Enabled = false
		for _, p in parts do
			ctx:tween(p, 0.35, { Transparency = 1 }, Enum.EasingStyle.Quad, Enum.EasingDirection.In, math.random() * 0.1)
		end
		for _, d in rig:GetDescendants() do
			if d:IsA("Beam") then
				ctx:tween(d, 0.3, { Width0 = 0, Width1 = 0 })
			end
		end
		ctx:tween(tipImg, 0.2, { ImageTransparency = 1, Size = UDim2.fromScale(2, 2) })
		ctx:tween(light, 0.4, { Brightness = 0 })
	end
	model.Parent = ctx.folder
	return { model = model, rig = rig, size = size, light = light, motes = motes, update = update, fade = fade }
end

-- 번개 빛 줄기: 하늘(top) → 창 꼬리. Blender 번개 그림 4장(scripts/vfx_lightning.py, 가로 = 길이, 왼쪽 = 하늘)을
-- 카메라를 보는 넓은 Beam 두 겹에 씌우고 0.05초마다 그림을 바꿔 번쩍임 (사용자 2026-11-24: Neon 막대 번개는 "퀄리티가 떨어지고 너무 가늘다")
local function bolt(ctx: Kit.Ctx, top: Vector3, getBottom: () -> Vector3, startAt: number, endAt: number, width: number)
	local a0 = Instance.new("Attachment")
	local a1 = Instance.new("Attachment")
	local holder = Kit.holder(ctx, CFrame.new(), "Bolt")
	a0.Parent, a1.Parent = holder, holder
	local function layer(w: number, bright: number, alpha: number): Beam
		return beam(a0, a1, {
			Texture = IMG.lightning[1],
			TextureMode = Enum.TextureMode.Stretch,
			FaceCamera = true,
			Brightness = bright,
			Width0 = w,
			Width1 = w * 0.85,
			Segments = 2,
			Color = ColorSequence.new(WHITE),
			Transparency = seq({ { 0, 1 }, { 0.12, alpha }, { 1, alpha } }),
			Enabled = false,
		})
	end
	local main = layer(width, 3, 0)
	local back = layer(width * 1.35, 1.6, 0.45) -- 다른 그림을 한 겹 더 (가지가 많아 보이게)
	local nextSwap = -1
	local last = 1
	ctx:step(endAt, function(t)
		if t < startAt then
			return
		end
		if t >= endAt - 0.01 then
			main.Enabled, back.Enabled = false, false
			return
		end
		a0.WorldPosition, a1.WorldPosition = top, getBottom()
		if t < nextSwap then
			return
		end
		nextSwap = t + 0.05
		local i = (last + math.random(0, 2)) % #IMG.lightning + 1
		last = i
		main.Texture = IMG.lightning[i]
		back.Texture = IMG.lightning[(i + 1) % #IMG.lightning + 1]
		main.Enabled, back.Enabled = true, true
		main.Brightness = 2.4 + math.random() * 1.2 -- 깜빡임
		back.Brightness = 1.2 + math.random() * 0.8
	end)
end

local function rocks(ctx: Kit.Ctx, ground: Vector3, count: number, speed: number)
	local src = assets("LeapStrike")
	local folder = src and src:FindFirstChild("Rocks")
	local list = folder and folder:GetChildren() or {}
	if #list == 0 then
		return
	end
	for i = 1, count do
		local r = (list[math.random(1, #list)] :: BasePart):Clone()
		r.Size *= math.random(70, 170) / 100
		local ang = (i / count) * math.pi * 2 + math.random() * 0.5
		local dir = Vector3.new(math.cos(ang), 0, math.sin(ang))
		r.CFrame = CFrame.new(ground + dir * 1.5 + Vector3.new(0, 0.8, 0)) * CFrame.Angles(math.random() * 6, math.random() * 6, math.random() * 6)
		r.Anchored = false
		r.CanCollide = true
		r.Parent = ctx.folder
		r.AssemblyLinearVelocity = dir * math.random(14, 30) * speed + Vector3.new(0, math.random(18, 36) * speed, 0)
		r.AssemblyAngularVelocity = Vector3.new(math.random(-15, 15), math.random(-15, 15), math.random(-15, 15))
		ctx:tween(r, 0.4, { Transparency = 1 }, Enum.EasingStyle.Quad, Enum.EasingDirection.In, 1.1)
		Debris:AddItem(r, 1.6)
	end
end

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
		local up = CFrame.new(rest.Position + Vector3.new(0, math.random(30, 70) / 100 * scale, 0)) * CFrame.fromAxisAngle(axis, -math.rad(math.random(20, 36))) * rest.Rotation
		local sunk = rest - Vector3.new(0, p.Size.Y + 0.3, 0)
		p.CFrame = sunk
		ctx:tween(p, 0.12 + math.random() * 0.05, { CFrame = up }, Enum.EasingStyle.Back, Enum.EasingDirection.Out)
		ctx:at(1.8 + math.random() * 0.2, function()
			if p.Parent then
				ctx:tween(p, 0.7, { CFrame = sunk }, Enum.EasingStyle.Quad, Enum.EasingDirection.In)
			end
		end)
	end
	Debris:AddItem(ring, 3)
end

-- 꽂힘 충격 (big = 가운데 큰 창)
local function impactFx(ctx: Kit.Ctx, ground: Vector3, radius: number, big: boolean)
	local flashHolder = Kit.holder(ctx, CFrame.new(ground + Vector3.new(0, 3, 0)), "ImpactFlash")
	-- 주인공 = 큰 창. 작은 창은 섬광·충격파·불뛰·돌을 줄이고 균열은 뺌, 큰 창은 요소마다 시간차(0.02~0.06초)
	local board = Kit.billboard(flashHolder, radius * (if big then 2.6 else 1.6), 3)
	local flash = Kit.image(board, T.HolyFlare, 0.3, 1)
	flash.ImageColor3 = GREEN
	ctx:tween(flash, 0.04, { Size = UDim2.fromScale(1, 1) })
	ctx:tween(flash, 0.35, { ImageTransparency = 1 }, Enum.EasingStyle.Quad, Enum.EasingDirection.In, 0.04)
	local light = Instance.new("PointLight")
	light.Color, light.Range, light.Brightness, light.Shadows = TEAL, radius * 2, 3, false
	light.Parent = flashHolder
	ctx:tween(light, 0.3, { Brightness = 0 })
	-- 충격파 시트
	local _, shockGui = groundGui(ctx, ground, radius * (if big then 2.6 else 2.0), "ImpactShock", 0, 2.5, math.random() * math.pi * 2)
	playSheet(ctx, shockGui, IMG.shock, if big then 0.8 else 0.55)
	-- 빛 균열: 큰 창에만 (같은 균열 그림이 세 자리에 반복돼 보였음), 0.03초 뒤 / 어두운 선 + 청록 빛
	if big then ctx:at(0.03, function()
	local yaw = math.random() * math.pi * 2
	local _, lineGui = groundGui(ctx, ground, radius * 2.2, "ImpactCrack", 1, 1, yaw)
	local lines = Instance.new("ImageLabel")
	lines.BackgroundTransparency = 1
	lines.Image = IMG.crack
	lines.ImageRectSize = Vector2.new(512, 512)
	lines.ImageColor3 = Color3.fromRGB(28, 24, 20)
	lines.ImageTransparency = 0.1
	lines.Size = UDim2.fromScale(0.35, 0.35)
	lines.Position = UDim2.fromScale(0.325, 0.325)
	lines.Parent = lineGui
	local _, glowGui = groundGui(ctx, ground + Vector3.new(0, 0.02, 0), radius * 2.2, "ImpactCrackGlow", 0, 3.5, yaw)
	local glow = lines:Clone()
	glow.ImageRectOffset = Vector2.new(512, 0)
	glow.ImageColor3 = TEAL
	glow.ImageTransparency = 0
	glow.Parent = glowGui
	for _, l in { lines, glow } do
		ctx:tween(l, 0.12, { Size = UDim2.fromScale(1, 1), Position = UDim2.fromScale(0, 0) }, Enum.EasingStyle.Quart, Enum.EasingDirection.Out)
	end
	ctx:tween(glow, 1.2, { ImageTransparency = 1 }, Enum.EasingStyle.Quad, Enum.EasingDirection.In, if big then 1.4 else 0.5)
	ctx:tween(lines, 0.9, { ImageTransparency = 1 }, Enum.EasingStyle.Quad, Enum.EasingDirection.In, 2.6)
	end) end
	-- 연기 고리 (바닥에 낮게 깔려 바깥으로)
	ctx:at(0.06, function()
		Kit.smokeRing(ctx, ground, radius * jitter(1.1, 0.1), { duration = if big then 1.5 else 1.0, count = if big then 14 else 7 })
	end)
	-- 불뛰
	local at = Kit.holder(ctx, CFrame.new(ground + Vector3.new(0, 1, 0)), "ImpactSparks")
	at.Size = Vector3.new(radius * 0.3, 0.2, radius * 0.3)
	Kit.emitter(ctx, at, {
		Texture = "rbxasset://textures/particles/sparkles_main.dds",
		Color = ColorSequence.new({ ColorSequenceKeypoint.new(0, WHITE), ColorSequenceKeypoint.new(0.5, TEAL), ColorSequenceKeypoint.new(1, VIOLET) }),
		LightEmission = 1,
		Size = seq({ { 0, 0.45 }, { 1, 0 } }),
		Lifetime = NumberRange.new(0.3, 0.8),
		Speed = NumberRange.new(30, 60),
		SpreadAngle = Vector2.new(70, 70),
		EmissionDirection = Enum.NormalId.Top,
		Acceleration = Vector3.new(0, -60, 0),
		Drag = 2.5,
		Shape = Enum.ParticleEmitterShape.Box,
	}):Emit(if big then 40 else 12)
	ctx:at(0.02, function()
		rocks(ctx, ground, if big then 12 else 4, if big then 1 else 0.7)
	end)
	if big then
		ctx:at(0.04, function()
			slabs(ctx, ground, radius / 9)
		end)
	end
	Kit.sound(vary(if big then SOUNDS.landBig else SOUNDS.land), ground)
	Kit.sound(vary(SOUNDS.stab, 0.1), ground)
	local me = Players.LocalPlayer.Character
	local myRoot = me and me:FindFirstChild("HumanoidRootPart")
	if myRoot and myRoot:IsA("BasePart") then
		local d = (myRoot.Position - ground).Magnitude
		if d <= SHAKE_RANGE then
			local near = 1 - math.clamp(d / SHAKE_RANGE, 0, 1)
			PiercingLunge.shakeCamera(if big then 0.4 else 0.2, (if big then 1.0 else 0.45) * (0.4 + 0.6 * near))
		end
	end
end

-- 창 하나: hitAt 에 ground 에 꽂힘, removeAt 에 흩어짐 (시각은 연출 시작 기준)
local function strike(ctx: Kit.Ctx, ground: Vector3, radius: number, size: number, hitAt: number, removeAt: number, big: boolean)
	local startAt = math.max(hitAt - jitter(FALL_TIME, 0.15), 0)
	-- 예고: 꽂힐 자리에 빛 고리가 번쩍하며 조여듦
	ctx:at(math.max(startAt - 0.05, 0), function()
		local ring = Kit.holder(ctx, CFrame.new(ground + Vector3.new(0, 0.1, 0)), "StrikeMark")
		ring.Size = Vector3.new(radius * 2.4, 0.05, radius * 2.4)
		local img = Kit.surface(ring, { T.HaloRing }, 3, { Enum.NormalId.Top })[1][1]
		img.ImageColor3 = GREEN
		img.ImageTransparency = 0.1
		ctx:tween(ring, FALL_TIME + 0.05, { Size = Vector3.new(radius * 2, 0.05, radius * 2) }, Enum.EasingStyle.Quad, Enum.EasingDirection.In)
		ctx:tween(img, 0.25, { ImageTransparency = 1 }, Enum.EasingStyle.Quad, Enum.EasingDirection.In, FALL_TIME + 0.05)
	end)
	ctx:at(startAt, function()
		local spear = makeSpear(ctx, size)
		if not spear then
			return
		end
		local s = spear :: Spear
		local tilt = CFrame.Angles(0, math.random() * math.pi * 2, 0) * CFrame.Angles(math.rad(jitter(SPEAR_TILT, 0.6)), 0, 0)
		local rest = CFrame.new(ground - Vector3.new(0, SPEAR_SINK * size, 0)) * tilt
		local sky = rest + Vector3.new(0, (jitter(SKY_HEIGHT, 0.15) + SPEAR_SINK) * size, 0)
		s.model:PivotTo(sky)
		Kit.sound(vary(SOUNDS.whoosh, 0.1), ground + Vector3.new(0, 20, 0))
		local t0 = ctx:clock()
		local fall = hitAt - startAt
		-- 낙하(가속) + 오로라 커튼 회전
		ctx:step(t0 + (removeAt - startAt) + 0.5, function(t)
			local k = math.clamp((t - t0) / fall, 0, 1)
			s.model:PivotTo(sky:Lerp(rest, k * k * k))
			s.update(t - t0)
		end)
		-- 빛 줄기: 하늘에서 창 꼬리까지 (떨어지는 동안 + 꽂힌 뒤 잠깐)
		local topPoint = ground + Vector3.new(math.random(-6, 6), BOLT_TOP, math.random(-6, 6))
		bolt(ctx, topPoint, function()
			return s.model:GetPivot() * Vector3.new(0, 40 * size, 0)
		end, t0, t0 + fall + BOLT_AFTER, if big then 8 else 5)
		ctx:at(fall, function()
			s.light.Brightness = if big then 3 else 2
			s.motes.Rate = if big then 10 else 0 -- 박혀 있는 동안 주인공은 오로라 흐름, 반짝이는 조금만
			impactFx(ctx, ground, radius, big)
		end)
		-- 흩어짐: 창 길이를 따라 오로라 빛 알갱이로
		ctx:at(removeAt - startAt, function()
			if not s.model.Parent then
				return
			end
			Kit.sound(vary(SOUNDS.shatter, 0.1), ground + Vector3.new(0, 8, 0))
			s.fade()
			local burst = Kit.holder(ctx, rest * CFrame.new(0, (SPEAR_SINK + 16) * size, 0), "SpearBurst")
			burst.Size = Vector3.new(2 * size, 32 * size, 2 * size)
			Kit.emitter(ctx, burst, {
				Texture = T.HolySparkle,
				Color = ColorSequence.new({ ColorSequenceKeypoint.new(0, WHITE), ColorSequenceKeypoint.new(0.5, TEAL), ColorSequenceKeypoint.new(1, VIOLET) }),
				LightEmission = 1,
				Brightness = 3,
				Size = seq({ { 0, 0.6 * size + 0.2 }, { 1, 0 } }),
				Lifetime = NumberRange.new(0.4, 0.8),
				Speed = NumberRange.new(6, 18),
				SpreadAngle = Vector2.new(180, 180),
				Drag = 3,
				Shape = Enum.ParticleEmitterShape.Box,
			}):Emit(if big then 45 else 18)
			Debris:AddItem(s.model, 0.6)
		end)
	end)
end

-- 속박: 큰 창 아래 → 대상 발밑 빛의 사슬 + 발밑 빛 고리 (root 초 동안, 끝에 부서짐)
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
	local foot = Kit.holder(ctx, CFrame.new(footPos()), "PinRing")
	local ringSize = math.max(root.Size.X * 2.2, 4.5)
	foot.Size = Vector3.new(ringSize * 1.8, 0.05, ringSize * 1.8)
	local ringLayers = Kit.surface(foot, { T.HaloRing, T.HolyCircle_Core }, 2.6, { Enum.NormalId.Top })
	local ringImg, coreImg = ringLayers[1][1], ringLayers[2][1]
	ringImg.ImageColor3, coreImg.ImageColor3 = GREEN, GREEN
	ringImg.ImageTransparency, coreImg.ImageTransparency = 1, 1
	ctx:tween(foot, 0.15, { Size = Vector3.new(ringSize, 0.05, ringSize) }, Enum.EasingStyle.Back)
	ctx:tween(ringImg, 0.15, { ImageTransparency = 0.05 })
	ctx:tween(coreImg, 0.15, { ImageTransparency = 0.5 })
	local from = center + Vector3.new(0, 2, 0)
	local links: { BasePart } = {}
	local maxLinks = 30
	local LINK_LEN = 1.1
	for i = 1, maxLinks do
		local link = Instance.new("Part")
		link.Name = "LightLink"
		link.Size = Vector3.new(0.14, 0.5, LINK_LEN * 1.2)
		link.Material = Enum.Material.Neon
		link.Color = if i % 2 == 0 then MINT else TEAL
		link.Transparency = 0.1
		Kit.decor(link)
		link.CFrame = CFrame.new(from)
		link.Parent = ctx.folder
		links[i] = link
	end
	local a0 = Instance.new("Attachment")
	local a1 = Instance.new("Attachment")
	local beamHolder = Kit.holder(ctx, CFrame.new(), "PinBeam")
	a0.Parent, a1.Parent = beamHolder, beamHolder
	local glow = beam(a0, a1, {
		Texture = IMG.auroraFlow,
		TextureMode = Enum.TextureMode.Wrap,
		TextureLength = 6,
		TextureSpeed = 1.5,
		FaceCamera = true,
		Brightness = 2,
		Color = ColorSequence.new(WHITE),
		Width0 = 1.4,
		Width1 = 1.4,
		Transparency = seq({ { 0, 0.3 }, { 1, 0.3 } }),
	})
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
		local v = to - from
		local length = v.Magnitude * grow
		local dir = if v.Magnitude > 1e-3 then v.Unit else Vector3.xAxis
		local count = math.clamp(math.floor(length / LINK_LEN), 0, maxLinks)
		local parts, frames = {}, {}
		for i = 1, maxLinks do
			table.insert(parts, links[i])
			if i <= count then
				local k0 = (i - 0.5) * LINK_LEN / math.max(v.Magnitude, 1e-3)
				local p = from + v * k0 - Vector3.new(0, 0.6 * 4 * k0 * (1 - k0), 0)
				table.insert(frames, CFrame.lookAt(p, p + dir) * CFrame.Angles(0, 0, if i % 2 == 0 then math.pi / 2 else 0))
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
	ctx:at(duration, function()
		local mid = Kit.holder(ctx, CFrame.lookAt((from + footPos()) / 2, footPos()), "PinBreak")
		mid.Size = Vector3.new(1, 1, math.max((footPos() - from).Magnitude, 1))
		Kit.emitter(ctx, mid, {
			Texture = T.HolySparkle,
			Color = ColorSequence.new(WHITE, TEAL),
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
	end)
end

local function hitSpark(ctx: Kit.Ctx, model: Model)
	local root = model:FindFirstChild("HumanoidRootPart")
	if not (root and root:IsA("BasePart")) then
		return
	end
	local at = Kit.holder(ctx, root.CFrame, "PinSpark")
	Kit.emitter(ctx, at, {
		Texture = T.HolySparkle,
		Color = ColorSequence.new(WHITE, TEAL),
		LightEmission = 1,
		Brightness = 3,
		Size = seq({ { 0, 0.6 }, { 1, 0 } }),
		Lifetime = NumberRange.new(0.25, 0.5),
		Speed = NumberRange.new(6, 14),
		SpreadAngle = Vector2.new(180, 180),
		Drag = 4,
	}):Emit(30)
end

-- 시전: p = { origin: CFrame, center: 큰 창 자리, strikes = { { pos, time, radius, size } }, timeScale }
-- 속박: p = { phase = "pin", origin = CFrame.new(center), targets = { { model, pinned } }, root }
function GodSpear.play(p: any, character: Instance?)
	if p.phase == "pin" then
		if type(p.targets) ~= "table" or typeof(p.origin) ~= "CFrame" then
			return
		end
		local duration = if type(p.root) == "number" then p.root else 2
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
	if type(p.strikes) ~= "table" or #p.strikes == 0 then
		return
	end
	local rootTime = SKILL.root or 2
	local last = 0
	for _, s in p.strikes do
		last = math.max(last, s.time)
	end
	local ctx = Kit.begin("GodSpearFx", last + rootTime + 2.5, p.timeScale)
	local origin: CFrame = if typeof(p.origin) == "CFrame" then p.origin else CFrame.new(p.strikes[1].pos)
	Kit.casterSound(SOUNDS.call, character, origin.Position)
	for _, s in p.strikes do
		if typeof(s.pos) ~= "Vector3" then
			continue
		end
		local big = (s.size or 1) >= 0.99
		local removeAt = if big then s.time + rootTime else last + SMALL_LINGER
		strike(ctx, s.pos, s.radius or 9, s.size or 1, s.time, removeAt, big)
	end
end

return GodSpear
