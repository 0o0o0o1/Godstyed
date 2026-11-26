--!strict
-- 서버 시작 지점. 서비스 목록을 직접 적지 않고 Services 폴더를 읽어서 실행한다.
-- 새 서비스는 Services 폴더에 모듈을 추가하고 init 함수를 만들면 자동으로 시작된다.
-- 패키지가 아니라서 모든 place 에 같은 것을 하나씩 둔다 (클라이언트 StarterPlayerScripts.Main 과 짝).
--
-- [코드 불러오기] (2026-11-27, A안): 서버가 시작할 때 코드 패키지의 최신 게시 버전을 InsertService:LoadAsset 으로 받아
--   place 안의 사본과 바꾼다 -> 패키지만 게시하면 모든 place 의 새 서버에 반영 (place 는 다시 게시하지 않아도 됨).
--   대상: LIVE_PACKAGES (패키지 ID 는 각 사본의 PackageLink 에서 읽음). 게임과 패키지가 같은 그룹 소유라 LoadAsset 이 허용됨.
--   받기에 실패하거나 LOAD_TIMEOUT 안에 못 받은 패키지는 place 안의 사본(비상용)으로 돈다.
--   Studio 에서는 받지 않는다 (편집 중인 사본으로 테스트). Studio 에서 시험하려면 이 스크립트 속성 ForceLiveCode = true.
--   긴급 끄기: 이 스크립트 속성 UseEmbeddedCode = true (place 게시 필요). 보통은 패키지 버전을 되돌려 게시하는 쪽이 빠름.
--   끝나면 ReplicatedStorage 속성 CodeReady = true, CodeLive = (하나라도 받았는가). 클라 Main 이 이것을 기다린다.
--   Controllers: 받은 것에 속성 LiveLoaded 를 달아 StarterPlayerScripts 에 두고, 서버 시작 직후에 들어와
--   예전 사본을 받은 플레이어를 위해 ReplicatedStorage.LiveControllers 에도 LIVE_MIRROR_TIME 초 동안 복사본을 둔다.

local InsertService = game:GetService("InsertService")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local RunService = game:GetService("RunService")
local ServerScriptService = game:GetService("ServerScriptService")
local ServerStorage = game:GetService("ServerStorage")
local StarterPlayerScripts = game:GetService("StarterPlayer"):WaitForChild("StarterPlayerScripts")

local LOAD_TIMEOUT = 20
local LIVE_MIRROR_TIME = 90

-- [부모, 이름] : 최신 버전으로 바꿀 코드 패키지
local function livePackages(): { Instance }
	local list = {}
	local function add(parent: Instance?, name: string)
		local root = parent and parent:FindFirstChild(name)
		if root and root:FindFirstChildOfClass("PackageLink") then
			table.insert(list, root)
		end
	end
	add(ReplicatedStorage, "Shared")
	add(ReplicatedStorage, "Remotes")
	add(ReplicatedStorage, "Assets")
	add(ServerScriptService, "Services")
	add(StarterPlayerScripts, "Controllers")
	local serverAssets = ServerStorage:FindFirstChild("Assets")
	add(serverAssets, "Enemies")
	add(serverAssets, "EnemyAnimations")
	return list
end

local function loadLiveCode(): number
	local roots = livePackages()
	local results = {}
	local pending = #roots
	for i, root in roots do
		local link = root:FindFirstChildOfClass("PackageLink") :: PackageLink
		local id = tonumber(string.match(link.PackageId, "%d+") or "")
		task.spawn(function()
			if id then
				local ok, model = pcall(InsertService.LoadAsset, InsertService, id)
				if ok and model then
					results[i] = model
				else
					warn(("[Main] 코드 받기 실패 %s (%s): %s"):format(root.Name, tostring(id), tostring(model)))
				end
			end
			pending -= 1
		end)
	end
	local started = os.clock()
	while pending > 0 and os.clock() - started < LOAD_TIMEOUT do
		task.wait(0.05)
	end
	local swapped = 0
	for i, root in roots do
		local model = results[i]
		local fresh = model and model:FindFirstChild(root.Name)
		if fresh and fresh.ClassName == root.ClassName then
			local parent = root.Parent
			fresh:SetAttribute("LiveLoaded", true)
			root:Destroy()
			fresh.Parent = parent
			swapped += 1
			if root.Name == "Controllers" then
				local mirror = fresh:Clone()
				mirror.Name = "LiveControllers"
				mirror.Parent = ReplicatedStorage
				task.delay(LIVE_MIRROR_TIME, function()
					mirror:Destroy()
				end)
			end
		elseif model then
			warn(("[Main] 받은 코드에 %s 가 없음 — place 사본으로 돈다"):format(root.Name))
		end
		if model then
			model:Destroy()
		end
	end
	print(("[Main] 최신 코드 %d/%d 개 받음 (%.1f초)"):format(swapped, #roots, os.clock() - started))
	return swapped
end

local useLive = script:GetAttribute("UseEmbeddedCode") ~= true and (not RunService:IsStudio() or script:GetAttribute("ForceLiveCode") == true)
local live = if useLive then loadLiveCode() else 0
ReplicatedStorage:SetAttribute("CodeLive", live > 0)
ReplicatedStorage:SetAttribute("CodeReady", true)

local servicesFolder = ServerScriptService:WaitForChild("Services")
local PlaceConfig = require(ReplicatedStorage:WaitForChild("Shared").Config.PlaceConfig)

for _, module in servicesFolder:GetChildren() do
	if not module:IsA("ModuleScript") then
		continue
	end
	-- 다른 장소 전용 서비스는 건너뛴다 (마을과 던전이 같은 코드를 쓴다)
	local onlyIn = PlaceConfig.SERVICE_PLACE[module.Name]
	if onlyIn and onlyIn ~= game.PlaceId then
		continue
	end

	local loaded, service = pcall(require, module)
	if not loaded then
		warn(("[Main] %s 로드 실패: %s"):format(module.Name, tostring(service)))
		continue
	end

	if type(service) == "table" and type(service.init) == "function" then
		local started, err = pcall(service.init)
		if started then
			print(("[Main] 서비스 시작: %s"):format(module.Name))
		else
			warn(("[Main] %s 시작 실패: %s"):format(module.Name, tostring(err)))
		end
	end
end
