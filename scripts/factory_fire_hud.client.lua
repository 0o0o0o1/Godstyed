--!nonstrict
-- 화염 스택 표시 (공장 place 전용 LocalScript: StarterPlayerScripts.FactoryFireHud)
-- 원본: 저장소 scripts/factory_fire_hud.client.lua
-- 서버 FactoryHazards 가 캐릭터 속성 FireStacks(0~10)를 바꾸면 체력바 위에 불 아이콘 + 숫자, 화면 가장자리 붉은 열기.

local Players = game:GetService("Players")
local TweenService = game:GetService("TweenService")

local BURN_ICON = "rbxassetid://107925246224624" -- StatusEffects 정의 주석의 Burn 아이콘
local MAX_STACKS = 10

local player = Players.LocalPlayer

local gui = Instance.new("ScreenGui")
gui.Name = "FactoryFireHud"
gui.ResetOnSpawn = false
gui.IgnoreGuiInset = true
gui.DisplayOrder = 5
gui.Parent = player:WaitForChild("PlayerGui")

local holder = Instance.new("Frame")
holder.AnchorPoint = Vector2.new(0.5, 1)
holder.Position = UDim2.new(0.5, 0, 1, -255)
holder.Size = UDim2.fromOffset(62, 62)
holder.BackgroundColor3 = Color3.fromRGB(30, 14, 8)
holder.BackgroundTransparency = 0.25
holder.Visible = false
holder.Parent = gui
Instance.new("UICorner", holder).CornerRadius = UDim.new(1, 0)
local stroke = Instance.new("UIStroke", holder)
stroke.Color = Color3.fromRGB(255, 120, 35)
stroke.Thickness = 2

local icon = Instance.new("ImageLabel")
icon.BackgroundTransparency = 1
icon.Image = BURN_ICON
icon.Size = UDim2.fromScale(0.8, 0.8)
icon.AnchorPoint = Vector2.new(0.5, 0.5)
icon.Position = UDim2.fromScale(0.5, 0.5)
icon.ImageColor3 = Color3.fromRGB(255, 150, 60)
icon.Parent = holder

local count = Instance.new("TextLabel")
count.BackgroundTransparency = 1
count.AnchorPoint = Vector2.new(1, 1)
count.Position = UDim2.new(1, 4, 1, 4)
count.Size = UDim2.fromOffset(30, 24)
count.Font = Enum.Font.GothamBlack
count.TextScaled = true
count.TextColor3 = Color3.new(1, 1, 1)
count.TextStrokeTransparency = 0.2
count.TextXAlignment = Enum.TextXAlignment.Right
count.Parent = holder

-- 화면 가장자리 열기 (스택이 많을수록 진하게)
local vignette = Instance.new("ImageLabel")
vignette.BackgroundTransparency = 1
vignette.Size = UDim2.fromScale(1, 1)
vignette.Image = "rbxasset://textures/ui/TopBar/WhiteOverlay.png"
vignette.ImageTransparency = 1
vignette.ImageColor3 = Color3.fromRGB(255, 80, 20)
vignette.Parent = gui
local grad = Instance.new("UIGradient", vignette)
grad.Transparency = NumberSequence.new({
	NumberSequenceKeypoint.new(0, 0),
	NumberSequenceKeypoint.new(0.18, 1),
	NumberSequenceKeypoint.new(0.82, 1),
	NumberSequenceKeypoint.new(1, 0),
})

local function show(stacks: number)
	holder.Visible = stacks > 0
	count.Text = tostring(stacks)
	TweenService:Create(vignette, TweenInfo.new(0.3), { ImageTransparency = 1 - 0.45 * (stacks / MAX_STACKS) }):Play()
	if stacks > 0 then
		holder.Size = UDim2.fromOffset(70, 70)
		TweenService:Create(holder, TweenInfo.new(0.25, Enum.EasingStyle.Back), { Size = UDim2.fromOffset(62, 62) }):Play()
	end
end

local function watch(char: Model)
	show(char:GetAttribute("FireStacks") or 0)
	char:GetAttributeChangedSignal("FireStacks"):Connect(function()
		show(char:GetAttribute("FireStacks") or 0)
	end)
end

if player.Character then
	watch(player.Character)
end
player.CharacterAdded:Connect(watch)
