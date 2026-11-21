--!nonstrict
-- 공장 조명 효과 (공용 패키지 Controllers 의 모듈 FactoryLightFXController, 공장 place 에서만 시작)
-- 태그별 깜빡임: FactoryFlicker = 고장 난 등(빛·렌즈 끊김), FactoryBlink = 항공 장애등 1초 켜짐/꺼짐,
-- FactoryPulse = 빛이 숨쉬듯, FactorySparks = 합선 불티(Emit + 소리 Zap). 카메라 260 안만 움직임.
-- 원본: 저장소 scripts/packages/Controllers/FactoryLightFXController.lua (패키지 코드는 마을 place 에서만 수정, CLAUDE.md)
-- (예전: 공장 place 의 StarterPlayerScripts.FactoryLightFX LocalScript)

local ReplicatedStorage = game:GetService("ReplicatedStorage")
local PlaceConfig = require(ReplicatedStorage:WaitForChild("Shared").Config.PlaceConfig)

local FactoryLightFXController = {}

local function run()
	local CS = game:GetService("CollectionService")
	local RunService = game:GetService("RunService")
	local NEAR = 260 -- only animate effects closer than this (studs)

	local function lightsOf(inst)
		local t = {}
		for _, d in ipairs(inst:GetDescendants()) do
			if d:IsA("Light") then table.insert(t, { d, d.Brightness }) end
		end
		if inst:IsA("Light") then table.insert(t, { inst, inst.Brightness }) end
		return t
	end
	local function lensOf(inst)
		local l = inst:FindFirstChild("Lens", true)
		return l, l and l.Color
	end
	local function posOf(inst)
		if inst:IsA("BasePart") then return inst.Position end
		return inst:GetPivot().Position
	end

	local items = {}
	local function add(inst, kind)
		local lens, col = lensOf(inst)
		table.insert(items, { inst = inst, kind = kind, lights = lightsOf(inst), lens = lens, col = col, pos = posOf(inst),
			t = math.random() * 10, next = 0, on = true })
	end
	for _, k in ipairs({ "FactoryFlicker", "FactoryBlink", "FactoryPulse", "FactorySparks" }) do
		for _, inst in ipairs(CS:GetTagged(k)) do add(inst, k) end
		CS:GetInstanceAddedSignal(k):Connect(function(inst) add(inst, k) end)
	end

	local function setOn(it, on, k)
		k = k or 1
		for _, l in ipairs(it.lights) do l[1].Brightness = on and l[2] * k or 0 end
		if it.lens then
			it.lens.Color = on and it.col or it.col:Lerp(Color3.new(0.15, 0.13, 0.12), 0.85)
		end
	end

	RunService.Heartbeat:Connect(function(dt)
		local cam = workspace.CurrentCamera
		if not cam then return end
		local cp = cam.CFrame.Position
		local now = os.clock()
		for _, it in ipairs(items) do
			if (it.pos - cp).Magnitude > NEAR then continue end
			it.t += dt
			if it.kind == "FactoryFlicker" then
				if now >= it.next then
					-- mostly on, with bursts of fast stutter and occasional long dropouts
					local r = math.random()
					if r < 0.55 then it.on = true; it.next = now + 0.4 + math.random() * 2.5
					elseif r < 0.9 then it.on = not it.on; it.next = now + 0.03 + math.random() * 0.09
					else it.on = false; it.next = now + 0.6 + math.random() * 1.6 end
					setOn(it, it.on, 0.75 + math.random() * 0.3)
				end
			elseif it.kind == "FactoryBlink" then
				local on = (it.t % 2) < 0.9
				if on ~= it.on then
					it.on = on
					for _, l in ipairs(it.lights) do l[1].Enabled = on end
					if it.inst:IsA("BasePart") then it.inst.Transparency = on and 0 or 0.6 end
				end
			elseif it.kind == "FactoryPulse" then
				local k = 0.8 + 0.2 * math.sin(it.t * 1.3) + 0.08 * math.sin(it.t * 5.7)
				for _, l in ipairs(it.lights) do l[1].Brightness = l[2] * k end
			elseif it.kind == "FactorySparks" then
				if now >= it.next then
					it.next = now + 1.5 + math.random() * 5
					local e = it.inst:FindFirstChildOfClass("ParticleEmitter")
					if e then e:Emit(math.random(8, 22)) end
					local s = it.inst:FindFirstChild("Zap")
					if s then s.PlaybackSpeed = 0.9 + math.random() * 0.3; s:Play() end
				end
			end
		end
	end)
end

function FactoryLightFXController.init()
	if game.PlaceId ~= PlaceConfig.FACTORY then
		return -- 공장 place 에서만
	end
	task.spawn(run)
end

return FactoryLightFXController
