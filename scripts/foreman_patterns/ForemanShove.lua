--!nonstrict
-- 패턴 (Foreman 전용): 근접 밀치기. 붙어서 보스를 때리는 플레이어를 몸 주변 충격파로 밀어낸다
-- 조건(canUse): 대상이 maxRange 안 + 보스가 최근 hurtWindow 초 안에 피해를 입었음. 정의에서 priority = true 라 조건이 맞으면 먼저 고른다
-- 갈고리를 들었다가(windup, 보스 주변 원 예고) 바닥을 찍어 원 안 플레이어에게 피해 + 바깥으로 밀어냄. 예고 동안 원 밖으로 나가면 피함
-- 끝나면 짧은 빈틈(recover): 모델 속성 Opening
-- 수치: maxRange, hurtWindow, windup, radius, damage, push, lift, recover
-- 높이 판정은 바닥 기준(보스 크기와 무관)

local Debris = game:GetService("Debris")

local Telegraph = require(script.Parent.Parent.Telegraph)

local HEIGHT_TOLERANCE = 9

local lastHurt = setmetatable({}, { __mode = "k" }) -- [Humanoid] = os.clock()
local watching = setmetatable({}, { __mode = "k" })

local function watch(humanoid: Humanoid)
	if watching[humanoid] then
		return
	end
	watching[humanoid] = true
	local last = humanoid.Health
	humanoid.HealthChanged:Connect(function(h)
		if h < last then
			lastHurt[humanoid] = os.clock()
		end
		last = h
	end)
end

local function flat(v: Vector3): Vector3
	local f = Vector3.new(v.X, 0, v.Z)
	return if f.Magnitude > 0.01 then f.Unit else Vector3.zAxis
end

local function shove(player: Player, velocity: Vector3, duration: number)
	local character = player.Character
	local hrp = character and character:FindFirstChild("HumanoidRootPart")
	if not hrp then
		return
	end
	local att = Instance.new("Attachment")
	att.Name = "ForemanShove"
	att.Parent = hrp
	local lv = Instance.new("LinearVelocity")
	lv.Name = "ForemanShove"
	lv.Attachment0 = att
	lv.RelativeTo = Enum.ActuatorRelativeTo.World
	lv.VelocityConstraintMode = Enum.VelocityConstraintMode.Vector
	lv.MaxForce = 4e5
	lv.VectorVelocity = velocity
	lv.Parent = hrp
	Debris:AddItem(lv, duration)
	Debris:AddItem(att, duration)
end

return {
	canUse = function(ctx, p, distance: number): boolean
		watch(ctx.humanoid)
		local t = lastHurt[ctx.humanoid]
		return distance <= p.maxRange and t ~= nil and os.clock() - t <= p.hurtWindow
	end,

	run = function(ctx, targetRoot: BasePart, p)
		local root, model = ctx.root, ctx.model
		ctx.stop()
		ctx.face(targetRoot.Position)
		ctx.setGearState("Attacking", true)
		ctx.tracks.attack:Play(0.05, 1, ctx.hitTime / p.windup)
		local g = Telegraph.ground(model, root.Position)
		local done = Telegraph.circle(g, p.radius, p.windup, Color3.fromRGB(255, 120, 30))
		task.wait(p.windup)
		ctx.setGearState("Attacking", false)
		if not ctx.alive() then
			done(false)
			return
		end
		done(true)
		local got = Telegraph.hit(model, function(r)
			local o = r.Position - g
			return Vector3.new(o.X, 0, o.Z).Magnitude <= p.radius and o.Y <= HEIGHT_TOLERANCE and o.Y >= -3
		end, p.damage)
		for _, pl in got do
			local hrp = pl.Character and pl.Character:FindFirstChild("HumanoidRootPart")
			if hrp then
				shove(pl, flat(hrp.Position - g) * p.push + Vector3.new(0, p.lift or 20, 0), 0.3)
			end
		end
		lastHurt[ctx.humanoid] = nil -- 한 번 밀쳤으면 다시 맞아야 또 씀
		model:SetAttribute("Opening", true)
		task.wait(p.recover)
	end,
}
