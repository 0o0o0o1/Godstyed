--!nonstrict
-- 공장 몬스터 몸 소리 (공용 패키지 Controllers 의 모듈 FactoryMonsterSoundController, 공장 place 에서만 시작)
-- 상가 Shutterback(GearSpinController)처럼 몬스터 몸에 늘 도는 반복 소리를 붙인다. 내 화면에서만 처리 (서버 부담 없음).
--   가만히 있을 때도 작게 들리고(idleVolume), 플레이어를 쫓기 시작하면 커지고 조금 높아진다(alertVolume, alertSpeed).
--   쫓는지는 Humanoid.WalkSpeed 가 적 정의의 walkSpeed 보다 빨라졌는지로 판단 (EnemyAI 가 추격 때 속도를 올림).
--   죽으면 줄어들며 꺼짐. 소리·크기는 SoundConfig.FACTORY_MONSTERS[적 id].
--   정신없지 않게 내 캐릭터에서 가까운 MAX_AUDIBLE(6) 마리만 소리를 내고 나머지는 0 으로 줄인다.
-- 원본: 저장소 scripts/packages/Controllers/FactoryMonsterSoundController.lua (패키지 코드는 마을 place 에서만 수정, CLAUDE.md)

local ReplicatedStorage = game:GetService("ReplicatedStorage")
local PlaceConfig = require(ReplicatedStorage:WaitForChild("Shared").Config.PlaceConfig)

local FactoryMonsterSoundController = {}

local function run()
	local RunService = game:GetService("RunService")
	local SOUNDS = require(ReplicatedStorage.Shared.Config.SoundConfig).FACTORY_MONSTERS
	local EnemyDatabase = require(ReplicatedStorage.Shared.Data.EnemyDatabase)
	if not SOUNDS then
		return
	end

	local CHANGE = 2.5 -- 크기·높이가 목표에 다가가는 빠르기 (갑자기 커지지 않게)
	local MAX_AUDIBLE = 6 -- 한 번에 소리를 내는 몬스터 수 (가까운 순). 공장은 몬스터가 많아 다 울리면 정신없음
	local Players = game:GetService("Players")
	local audible = {} -- [Model] = true (가까운 MAX_AUDIBLE 마리)
	local nextPick = 0
	local tracked = {} -- [Model] = { sound, def, walk, level }

	local function attach(model: Instance)
		if not model:IsA("Model") or tracked[model] then
			return
		end
		local id = model:GetAttribute("EnemyId")
		local def = id and SOUNDS[id]
		if not def then
			return
		end
		local root = model:WaitForChild("HumanoidRootPart", 5)
		local hum = model:FindFirstChildOfClass("Humanoid")
		if not root or not hum then
			return
		end
		local enemyDef = EnemyDatabase.get(id)
		local s = Instance.new("Sound")
		s.Name = "FactoryBodyLoop"
		s.SoundId = def.id
		s.Looped = true
		s.Volume = 0
		s.PlaybackSpeed = def.speed or 1
		s.RollOffMode = Enum.RollOffMode.InverseTapered
		s.RollOffMinDistance = 10
		s.RollOffMaxDistance = def.maxDistance or 70
		s.Parent = root
		s.TimePosition = math.random() * 2 -- 여러 마리가 같은 박자로 겹치지 않게
		s:Play()
		tracked[model] = { sound = s, def = def, hum = hum, walk = enemyDef and enemyDef.walkSpeed or hum.WalkSpeed, level = 0 }
	end

	-- 0.5초마다 가까운 MAX_AUDIBLE 마리를 고름 (살아 있고 maxDistance 안)
	local function pickAudible()
		local char = Players.LocalPlayer.Character
		local me = char and char:FindFirstChild("HumanoidRootPart")
		local list = {}
		if me then
			for model, e in tracked do
				local r = e.sound.Parent
				if r and e.hum.Health > 0 then
					local d = (r.Position - me.Position).Magnitude
					if d <= e.sound.RollOffMaxDistance then
						table.insert(list, { model = model, d = d })
					end
				end
			end
		end
		table.sort(list, function(a, b)
			return a.d < b.d
		end)
		audible = {}
		for i = 1, math.min(MAX_AUDIBLE, #list) do
			audible[list[i].model] = true
		end
	end

	RunService.Heartbeat:Connect(function(dt)
		local k = math.min(1, CHANGE * dt)
		if os.clock() >= nextPick then
			nextPick = os.clock() + 0.5
			pickAudible()
		end
		for model, e in tracked do
			if not model.Parent or not e.sound.Parent then
				tracked[model] = nil
				continue
			end
			local alive = e.hum.Health > 0
			local alerted = alive and e.hum.WalkSpeed > e.walk + 0.5
			local goal = if not alive then 0 elseif alerted then 1 else 0
			e.level += (goal - e.level) * k
			local d = e.def
			local target = if alive and audible[model] then d.idleVolume + (d.alertVolume - d.idleVolume) * e.level else 0
			local vol = e.sound.Volume + (target - e.sound.Volume) * k -- 6마리 안팎으로 바뀔 때도 부드럽게
			e.sound.Volume = vol
			e.sound.PlaybackSpeed = (d.speed or 1) * (1 + ((d.alertSpeed or 1) - 1) * e.level)
			if not alive and vol < 0.01 then
				e.sound:Destroy()
				tracked[model] = nil
			end
		end
	end)

	local enemies = workspace:WaitForChild("Enemies")
	enemies.ChildAdded:Connect(function(m)
		task.spawn(attach, m)
	end)
	for _, m in enemies:GetChildren() do
		task.spawn(attach, m)
	end
end

function FactoryMonsterSoundController.init()
	if game.PlaceId ~= PlaceConfig.FACTORY then
		return -- 공장 place 에서만
	end
	task.spawn(run)
end

return FactoryMonsterSoundController
