--!nonstrict
-- 클라이언트 시작 지점. Controllers 폴더의 모듈을 전부 불러와 init()을 호출한다.
-- 새 컨트롤러는 Controllers 폴더에 모듈을 추가하고 init 함수를 만들면 자동으로 시작된다.
-- 패키지가 아니라서 모든 place 에 같은 것을 하나씩 둔다 (서버 ServerScriptService.Main 과 짝).
-- [코드 불러오기] (2026-11-27): 서버가 최신 코드 패키지로 바꾼 뒤 ReplicatedStorage 속성 CodeReady 를 켜면 시작한다
--   (최대 READY_WAIT 초). 내 Controllers 가 예전 사본이면(서버가 바꾸기 전에 들어옴: 속성 LiveLoaded 없음)
--   ReplicatedStorage.LiveControllers(서버가 잠깐 두는 최신 복사본)를 쓴다.

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local READY_WAIT = 25
local deadline = os.clock() + READY_WAIT
while ReplicatedStorage:GetAttribute("CodeReady") ~= true and os.clock() < deadline do
	task.wait(0.1)
end

local controllersFolder = script.Parent:WaitForChild("Controllers")
if ReplicatedStorage:GetAttribute("CodeLive") == true and controllersFolder:GetAttribute("LiveLoaded") ~= true then
	local liveCopy = ReplicatedStorage:WaitForChild("LiveControllers", 10)
	if liveCopy then
		-- 내 쪽에 복사해서 쓴다 (서버가 잠시 뒤 LiveControllers 를 지워도 나중에 형제 모듈을 찾는 코드가 깨지지 않게)
		local fresh = liveCopy:Clone()
		controllersFolder:Destroy()
		fresh.Name = "Controllers"
		fresh.Parent = script.Parent
		controllersFolder = fresh
	else
		warn("[Main] 최신 컨트롤러를 못 받아 예전 사본으로 돈다")
	end
end


for _, module in controllersFolder:GetChildren() do
	if not module:IsA("ModuleScript") then
		continue
	end

	local loaded, controller = pcall(require, module)
	if not loaded then
		warn(("[Main] %s 로드 실패: %s"):format(module.Name, tostring(controller)))
		continue
	end

	if type(controller) == "table" and type(controller.init) == "function" then
		local started, err = pcall(controller.init)
		if started then
			print(("[Main] 컨트롤러 시작: %s"):format(module.Name))
		else
			warn(("[Main] %s 시작 실패: %s"):format(module.Name, tostring(err)))
		end
	end
end
