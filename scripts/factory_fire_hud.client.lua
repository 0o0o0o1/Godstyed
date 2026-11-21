--!nonstrict
-- 화염 스택 표시 (공장 place 전용 LocalScript: StarterPlayerScripts.FactoryFireHud)
-- 원본: 저장소 scripts/factory_fire_hud.client.lua
-- 서버 FactoryHazards 가 캐릭터 속성 FireStacks(0~10)를 바꾸면 체력바 바로 위에 작은 띠로 표시한다.
-- 시야를 가리지 않게: 화면 가장자리 효과 없음, 작은 불 아이콘 + 칸 10개(쌓인 만큼 주황) + 숫자. 스택이 오를 때만 잠깐 밝아짐.

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

local function watch(char: Model)
	shown = 0
	show(char:GetAttribute("FireStacks") or 0)
	char:GetAttributeChangedSignal("FireStacks"):Connect(function()
		show(char:GetAttribute("FireStacks") or 0)
	end)
end

if player.Character then
	watch(player.Character)
end
player.CharacterAdded:Connect(watch)
