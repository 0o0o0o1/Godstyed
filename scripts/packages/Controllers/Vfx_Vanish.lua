--!strict
-- 은신 연출 (Skills.vanish, kind "stealth", vfx = "Vanish"). 단검 색 = 보라 + 검은 연기.
-- 원본: 저장소 scripts/packages/Controllers/Vfx_Vanish.lua (Controllers 패키지 SkillController.Vfx.Vanish)
--   시전 (phase 없음)  castDelay 뒤 몸을 숨김 — 남: 완전히 안 보임(이름표·무기 포함) / 파티원: 아주 흐린 윤곽 / 나: 반투명 + 검은 보라 실루엣
--                      나만: 발밑 검은 연기 + 화면이 살짝 어두워짐 + 작은 소리 (남에게는 이펙트·소리 없음, 분신만 보임 — 분신은 서버가 만듦)
--   분신 사라짐 "decoy"  분신 자리에 검은 연기 (모두에게, 맞았거나 은신이 끝남)
--   끝 "end"           몸이 다시 보임, 내 화면 효과 거둠
-- 숨김은 화면마다 LocalTransparencyModifier (매 프레임 다시 적용: 카메라 스크립트가 내 몸 값을 바꾸는 것을 덮음)

local Players = game:GetService("Players")
local Lighting = game:GetService("Lighting")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local RunService = game:GetService("RunService")
local TweenService = game:GetService("TweenService")

local Skills = require(ReplicatedStorage.Shared.Data.Skills)
local PartyUtil = require(ReplicatedStorage.Shared.Util.PartyUtil)
local Kit = require(script.Parent.Parent.VfxKit)

local SKILL = Skills.vanish
local seq = Kit.seq
local player = Players.LocalPlayer

local SMOKE = Color3.fromRGB(16, 10, 24)
local VEIL_FILL = Color3.fromRGB(40, 12, 75)
local VEIL_EDGE = Color3.fromRGB(170, 110, 255)
local INK = "rbxassetid://108787658210747" -- 그림자 연쇄 잉크 연기 8x8 (scripts/vfx_shadow_chain_tex.py)

-- 보이는 정도 (LocalTransparencyModifier)
local HIDE_MINE, HIDE_ALLY, HIDE_OTHER = 0.55, 0.9, 1
local DIM = { Brightness = -0.08, Saturation = -0.3, Contrast = 0.05, TintColor = Color3.fromRGB(232, 224, 255) }

local SOUNDS = {
	vanish = { id = "rbxassetid://125132253621935", volume = 0.3, speed = 1.1 }, -- 그림자 연쇄 사라짐과 같은 소리, 나한테만 작게
	reveal = { id = "rbxassetid://125132253621935", volume = 0.22, speed = 1.5 },
}
Kit.preloadSounds(SOUNDS)

type Veil = {
	token: {},
	character: Model,
	value: number,
	parts: { [Instance]: boolean },
	guis: { [LayerCollector]: boolean },
	conns: { RBXScriptConnection },
	highlight: Highlight?,
	dim: ColorCorrectionEffect?,
}
local veils: { [Model]: Veil } = {}

local Vanish = {}

local function ownerOf(character: Model): Player?
	return Players:GetPlayerFromCharacter(character)
end

local function track(v: Veil, d: Instance)
	if d:IsA("BasePart") or d:IsA("Decal") then
		v.parts[d] = true
	elseif d:IsA("BillboardGui") or d:IsA("SurfaceGui") then
		-- 남에게는 이름표·체력바도 숨김
		if v.value >= 1 and (d :: LayerCollector).Enabled then
			v.guis[d :: LayerCollector] = true
			(d :: LayerCollector).Enabled = false
		end
	end
end

local function smoke(ctx: Kit.Ctx, at: Vector3, count: number, size: number)
	local holder = Kit.holder(ctx, CFrame.new(at), "VanishInk")
	holder.Size = Vector3.new(size * 0.5, size * 0.3, size * 0.5)
	local e = Kit.emitter(ctx, holder, {
		Texture = INK,
		FlipbookLayout = Enum.ParticleFlipbookLayout.Grid8x8,
		FlipbookMode = Enum.ParticleFlipbookMode.OneShot,
		Color = ColorSequence.new(SMOKE),
		LightEmission = 0,
		LightInfluence = 0.25,
		Size = seq({ { 0, size * 0.6 }, { 1, size * 1.3 } }),
		Transparency = seq({ { 0, 0.1 }, { 0.6, 0.3 }, { 1, 1 } }),
		Lifetime = NumberRange.new(0.5, 0.75),
		Speed = NumberRange.new(1.5, 3.5),
		Shape = Enum.ParticleEmitterShape.Sphere,
		ShapeStyle = Enum.ParticleEmitterShapeStyle.Surface,
		Rotation = NumberRange.new(0, 360),
		RotSpeed = NumberRange.new(-40, 40),
		Drag = 3,
		Acceleration = Vector3.new(0, 2, 0),
	})
	pcall(function()
		(e :: any).FlipbookStartRandom = false
	end)
	e:Emit(count)
	-- 가장자리 옅은 보라 기운
	local glow = Kit.emitter(ctx, holder, {
		Texture = INK,
		FlipbookLayout = Enum.ParticleFlipbookLayout.Grid8x8,
		FlipbookMode = Enum.ParticleFlipbookMode.OneShot,
		Color = ColorSequence.new(VEIL_EDGE),
		LightEmission = 0.6,
		LightInfluence = 0,
		Brightness = 0.6,
		Size = seq({ { 0, size * 0.5 }, { 1, size * 1.1 } }),
		Transparency = seq({ { 0, 0.7 }, { 1, 1 } }),
		Lifetime = NumberRange.new(0.4, 0.6),
		Speed = NumberRange.new(1, 2.5),
		Shape = Enum.ParticleEmitterShape.Sphere,
		ShapeStyle = Enum.ParticleEmitterShapeStyle.Surface,
		Rotation = NumberRange.new(0, 360),
		Drag = 3,
	})
	pcall(function()
		(glow :: any).FlipbookStartRandom = false
	end)
	glow:Emit(math.ceil(count * 0.5))
end

local function reveal(character: Model, token: {}?)
	local v = veils[character]
	if not v or (token and v.token ~= token) then
		return
	end
	veils[character] = nil
	for _, c in v.conns do
		c:Disconnect()
	end
	for part in v.parts do
		if part.Parent then
			(part :: any).LocalTransparencyModifier = 0
		end
	end
	for gui in v.guis do
		if gui.Parent then
			gui.Enabled = true
		end
	end
	if v.highlight then
		v.highlight:Destroy()
	end
	local dim = v.dim
	if dim then
		local tw = TweenService:Create(dim, TweenInfo.new(0.3, Enum.EasingStyle.Quad), { Brightness = 0, Saturation = 0, Contrast = 0, TintColor = Color3.new(1, 1, 1) })
		tw.Completed:Once(function()
			dim:Destroy()
		end)
		tw:Play()
	end
end

local function veil(character: Model, life: number)
	reveal(character, nil)
	local owner = ownerOf(character)
	local mine = owner == player
	local ally = not mine and owner ~= nil and PartyUtil.areAllies(player, owner)
	local value = if mine then HIDE_MINE elseif ally then HIDE_ALLY else HIDE_OTHER
	local token = {}
	local v: Veil = { token = token, character = character, value = value, parts = {}, guis = {}, conns = {} }
	veils[character] = v
	for _, d in character:GetDescendants() do
		track(v, d)
	end
	table.insert(v.conns, character.DescendantAdded:Connect(function(d)
		track(v, d)
	end))
	table.insert(v.conns, RunService.RenderStepped:Connect(function()
		for part in v.parts do
			if part.Parent then
				(part :: any).LocalTransparencyModifier = value
			else
				v.parts[part] = nil
			end
		end
	end))
	if mine or ally then
		local h = Instance.new("Highlight")
		h.Name = "VanishVeil"
		h.DepthMode = Enum.HighlightDepthMode.Occluded
		h.FillColor = VEIL_FILL
		h.OutlineColor = VEIL_EDGE
		h.FillTransparency = if mine then 0.45 else 1
		h.OutlineTransparency = if mine then 0.35 else 0.8
		h.Adornee = character
		h.Parent = character
		v.highlight = h
	end
	if mine then
		local cc = Instance.new("ColorCorrectionEffect")
		cc.Name = "VanishDim"
		cc.Parent = Lighting
		TweenService:Create(cc, TweenInfo.new(0.25, Enum.EasingStyle.Quad), DIM):Play()
		v.dim = cc
	end
	-- 끝 신호를 못 받아도 몸이 다시 보이게
	task.delay(life, function()
		reveal(character, token)
	end)
end

local function onCast(payload: any, character: Model)
	local owner = ownerOf(character)
	local mine = owner == player
	local scale = if type(payload.timeScale) == "number" and payload.timeScale > 0 then payload.timeScale else 1
	local delay = (SKILL.castDelay or 0) / scale
	local duration = (if type(payload.duration) == "number" then payload.duration else SKILL.duration or 4) / scale
	if mine then
		local ctx = Kit.begin("Vanish", 1.2, payload.timeScale)
		local root = character:FindFirstChild("HumanoidRootPart") :: BasePart?
		local at = if root then root.Position else payload.origin.Position
		smoke(ctx, Kit.ground(at, { character, ctx.folder }) + Vector3.new(0, 1.2, 0), 9, 4.5)
		Kit.sound(SOUNDS.vanish)
	end
	task.delay(delay, function()
		if character.Parent then
			veil(character, duration + 1)
		end
	end)
end

function Vanish.play(payload: any, character: Model)
	local phase = payload.phase
	if phase == nil then
		onCast(payload, character)
	elseif phase == "decoy" then
		-- 분신이 연기로 사라짐 (모두에게)
		local ctx = Kit.begin("VanishDecoy", 1.2)
		local at = payload.origin.Position
		smoke(ctx, at, 10, 5)
		Kit.smokeRing(ctx, Kit.ground(at, { ctx.folder }), 2.6, { duration = 0.6, count = 6, color = SMOKE, light = 0.6 })
	elseif phase == "end" then
		reveal(character, nil)
		if ownerOf(character) == player then
			Kit.sound(SOUNDS.reveal)
		end
	end
end

return Vanish
