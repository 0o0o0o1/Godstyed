--!nonstrict
-- 화염 스택 표시 (공용 패키지 Controllers 의 모듈 FactoryFireHudController, 공장 place 에서만 시작)
-- 서버 FactoryHazards 가 캐릭터 속성 FireStacks(0~10)를 바꾸면 체력바 바로 위에 작은 띠로 표시한다.
-- 시야를 가리지 않게: 화면 가장자리 효과 없음, 작은 불 아이콘 + 칸 10개(쌓인 만큼 주황) + 숫자. 스택이 오를 때만 잠깐 밝아짐.
-- 화면 효과: 스택 비례 주황 색보정 + 화염 피해 틱마다 짧게 붉게 번쩍 (Camera.FactoryHeat, 내 화면만).
-- Molten Walker 발밑 범위 원(HeatRing)은 가까이(28 안) 와야 보임.
-- 원본: 저장소 scripts/packages/Controllers/FactoryFireHudController.lua (패키지 코드는 마을 place 에서만 수정, CLAUDE.md)

local ReplicatedStorage = game:GetService("ReplicatedStorage")
local PlaceConfig = require(ReplicatedStorage:WaitForChild("Shared").Config.PlaceConfig)

local FactoryFireHudController = {}

local function run()
	local Players = game:GetService("Players")
	local TweenService = game:GetService("TweenService")

	local BURN_ICON = "rbxassetid://107925246224624" -- StatusEffects 정의 주석의 Burn 아이콘
	local MAX_STACKS = 10
	local FIRE = Color3.fromRGB(255, 130, 45)
	local HOT = Color3.fromRGB(255, 215, 120)
	local EMPTY = Color3.fromRGB(60, 40, 30)

	local player = Players.LocalPlayer

	local gui = Instance.new("ScreenGui")
	gui.Name = "FactoryFireHud"
	gui.ResetOnSpawn = false
	gui.DisplayOrder = 5
	gui.Parent = player:WaitForChild("PlayerGui")

	-- 체력바 위 가운데, 높이 18 띠 (StatsHud 를 찾으면 그 위로 옮겨 붙음, 아래 attach)
	local bar = Instance.new("Frame")
	bar.AnchorPoint = Vector2.new(0.5, 1)
	bar.Position = UDim2.new(0.5, 0, 1, -205)
	bar.Size = UDim2.fromOffset(150, 18)
	bar.BackgroundColor3 = Color3.fromRGB(20, 12, 8)
	bar.BackgroundTransparency = 0.45
	bar.Visible = false
	bar.Parent = gui
	Instance.new("UICorner", bar).CornerRadius = UDim.new(0, 5)

	local icon = Instance.new("ImageLabel")
	icon.BackgroundTransparency = 1
	icon.Image = BURN_ICON
	icon.ImageColor3 = FIRE
	icon.Size = UDim2.fromOffset(16, 16)
	icon.Position = UDim2.fromOffset(3, 1)
	icon.Parent = bar

	local pips = {}
	for i = 1, MAX_STACKS do
		local p = Instance.new("Frame")
		p.BorderSizePixel = 0
		p.Size = UDim2.fromOffset(8, 8)
		p.Position = UDim2.fromOffset(22 + (i - 1) * 10, 5)
		p.BackgroundColor3 = EMPTY
		p.Parent = bar
		Instance.new("UICorner", p).CornerRadius = UDim.new(0, 2)
		pips[i] = p
	end

	local count = Instance.new("TextLabel")
	count.BackgroundTransparency = 1
	count.Position = UDim2.fromOffset(122, 0)
	count.Size = UDim2.fromOffset(24, 18)
	count.Font = Enum.Font.GothamBold
	count.TextSize = 13
	count.TextColor3 = Color3.fromRGB(255, 235, 215)
	count.TextXAlignment = Enum.TextXAlignment.Right
	count.Parent = bar

	local scale = Instance.new("UIScale")
	scale.Parent = bar

	-- 체력바(PlayerGui.StatsHud.StatusHud)는 화면 크기에 따라 커지고 작아지므로 그 바로 위에 붙이고 크기도 맞춘다
	local function attach(hud: GuiObject)
		local function place()
			local pos, size = hud.AbsolutePosition, hud.AbsoluteSize
			scale.Scale = math.clamp(size.X / 420, 0.75, 1.6)
			bar.AnchorPoint = Vector2.new(0.5, 1)
			bar.Position = UDim2.fromOffset(pos.X + size.X / 2, pos.Y - 3)
		end
		hud:GetPropertyChangedSignal("AbsolutePosition"):Connect(place)
		hud:GetPropertyChangedSignal("AbsoluteSize"):Connect(place)
		place()
	end
	task.spawn(function()
		local stats = player.PlayerGui:WaitForChild("StatsHud", 30)
		local hud = stats and stats:WaitForChild("StatusHud", 10)
		if hud then
			gui.IgnoreGuiInset = stats.IgnoreGuiInset -- 같은 좌표계
			attach(hud)
		end
	end)

	local shown = 0
	local function show(stacks: number)
		bar.Visible = stacks > 0
		count.Text = tostring(stacks)
		for i, p in pips do
			p.BackgroundColor3 = if i <= stacks then (if stacks >= 7 then HOT else FIRE) else EMPTY
		end
		if stacks > shown then -- 오를 때만 아이콘이 잠깐 밝아짐 (크기는 그대로)
			icon.ImageColor3 = HOT
			TweenService:Create(icon, TweenInfo.new(0.35), { ImageColor3 = FIRE }):Play()
		end
		shown = stacks
	end

	---------------------------------------------------------------- 화면 효과 (불탈 때)
	-- 화면을 가리는 것 없이 색만: 스택에 비례해 따뜻한 주황 틴트 + 살짝 대비, 화염 피해 틱(스택이 있는 매초)마다 짧게 붉게 번쩍.
	-- 카메라 안에 두면 내 화면에만 적용되고, 조명 프리셋(LightingService)이 Lighting 을 바꿔도 안 지워짐
	local heat = Instance.new("ColorCorrectionEffect")
	heat.Name = "FactoryHeat"
	heat.Parent = workspace.CurrentCamera
	local HEAT_TINT = Color3.fromRGB(255, 226, 205) -- 10스택일 때 틴트 (옅게 — 맵이 이미 주황 안개라 강하면 화면이 다 주황)
	local FLASH_TINT = Color3.fromRGB(255, 170, 145)

	local function heatTint(stacks: number): Color3
		return Color3.new(1, 1, 1):Lerp(HEAT_TINT, stacks / MAX_STACKS)
	end
	local function screen(stacks: number)
		local k = stacks / MAX_STACKS
		TweenService:Create(heat, TweenInfo.new(0.4), {
			TintColor = heatTint(stacks),
			Contrast = 0.05 * k,
			Saturation = 0.05 * k,
		}):Play()
	end
	local function flash(stacks: number)
		heat.TintColor = heatTint(stacks):Lerp(FLASH_TINT, 0.25 + 0.25 * stacks / MAX_STACKS)
		TweenService:Create(heat, TweenInfo.new(0.35, Enum.EasingStyle.Quad), { TintColor = heatTint(stacks) }):Play()
	end

	---------------------------------------------------------------- 범위 원 (가까울 때만)
	-- 서버가 Molten Walker 발밑에 단 HeatRing 은 멀리서는 안 보이고, RING_SHOW 안으로 오면 서서히 나타남 (내 화면에서만)
	local RING_SHOW = 28 -- 이 거리부터 보이기 시작
	local RING_FULL = 18 -- 이 거리 안이면 완전히 보임
	local enemiesFolder = workspace:WaitForChild("Enemies", 30)
	task.spawn(function()
		while enemiesFolder do
			local char = player.Character
			local root = char and char:FindFirstChild("HumanoidRootPart")
			for _, m in enemiesFolder:GetChildren() do
				local ring = m:FindFirstChild("HeatRing")
				if ring and ring:IsA("BasePart") then
					local d = if root then (ring.Position - root.Position).Magnitude else math.huge
					ring.LocalTransparencyModifier = math.clamp((d - RING_FULL) / (RING_SHOW - RING_FULL), 0, 1)
				end
			end
			task.wait(0.15)
		end
	end)

	local function watch(char: Model)
		shown = 0
		local s0 = char:GetAttribute("FireStacks") or 0
		show(s0)
		screen(s0)
		char:GetAttributeChangedSignal("FireStacks"):Connect(function()
			local s = char:GetAttribute("FireStacks") or 0
			show(s)
			screen(s)
		end)
		-- 화염 피해 틱마다 번쩍 (서버 FactoryHazards 가 피해를 줄 때 BurnTick 을 올림 — 스택이 그대로여도)
		char:GetAttributeChangedSignal("BurnTick"):Connect(function()
			local s = char:GetAttribute("FireStacks") or 0
			if s > 0 then
				flash(s)
			end
		end)
	end

	if player.Character then
		watch(player.Character)
	end
	player.CharacterAdded:Connect(watch)
end

function FactoryFireHudController.init()
	if game.PlaceId ~= PlaceConfig.FACTORY then
		return -- 공장 place 에서만
	end
	task.spawn(run)
end

return FactoryFireHudController
