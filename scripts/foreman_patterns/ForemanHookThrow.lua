--!nonstrict
-- 패턴 (Foreman 전용): 갈고리 던지기. 몸을 돌려 대상을 조준하다가(windup, lockTime에 방향 고정) 붐 팔 끝의 갈고리를 직선으로 던진다
-- 갈고리에 맞은 플레이어는 피해를 입고 보스 앞(stopDistance)까지 끌려온다. 방향이 고정된 뒤 옆으로 피하면 된다
-- 끌려온 플레이어에게는 바로 갈고리 내려찍기가 이어진다(예고 없는 확정 연계, 패링으로만 막음). 내려찍기를 기다리는 동안 수평으로 붙잡혀 있다
-- 끝나면(recover) 빈틈: 모델 속성 Opening
-- 수치: anim, windup, lockTime, length, width, speed, damage, stopDistance, pullTime, comboWindup, comboDamage, recover
-- 높이 판정은 바닥 기준(보스 크기와 무관): 갈고리는 바닥 + FLY_HEIGHT 로 날아간다
-- 소리: 모델 UpperTorso 의 Sound "ThrowWhoosh", "ChainRattle", "HookHit" 가 있으면 낸다 (ForemanFX 설치 스크립트)

local Debris = game:GetService("Debris")

local Telegraph = require(script.Parent.Parent.Telegraph)

local HEIGHT_TOLERANCE = 7
local FLY_HEIGHT = 3.5 -- 바닥에서 갈고리가 나는 높이 (플레이어 몸통 높이)
local THROW_MARKER_TIME = 0.9 -- 애니메이션의 "Throw" 마커 시각

local tracks = setmetatable({}, { __mode = "k" })

local function anim(ctx, id: string?)
	if not id then
		return nil
	end
	local cache = tracks[ctx.humanoid]
	if not cache then
		cache = {}
		tracks[ctx.humanoid] = cache
	end
	if not cache[id] then
		local animator = ctx.humanoid:FindFirstChildOfClass("Animator")
		if not animator then
			return nil
		end
		local a = Instance.new("Animation")
		a.AnimationId = id
		local t = animator:LoadAnimation(a)
		t.Priority = Enum.AnimationPriority.Action
		t.Looped = false
		cache[id] = t
	end
	return cache[id]
end

local function sfx(ctx, name: string, pitch: number?)
	local torso = ctx.model:FindFirstChild("UpperTorso")
	local s = torso and torso:FindFirstChild(name)
	if s and s:IsA("Sound") then
		s.PlaybackSpeed = pitch or 1
		s:Play()
	end
end

local function flat(v: Vector3): Vector3
	local f = Vector3.new(v.X, 0, v.Z)
	return if f.Magnitude > 0.01 then f.Unit else Vector3.zAxis
end

-- 서버에서 플레이어 몸에 짧게 속도를 건다 (LinearVelocity 는 복제되어 소유 클라이언트가 계산)
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

-- 수평으로만 붙잡는다 (중력은 그대로). 연계 내려찍기 직전까지
local function pin(player: Player, duration: number)
	local character = player.Character
	local hrp = character and character:FindFirstChild("HumanoidRootPart")
	if not hrp then
		return
	end
	local att = Instance.new("Attachment")
	att.Name = "ForemanPin"
	att.Parent = hrp
	local lv = Instance.new("LinearVelocity")
	lv.Name = "ForemanPin"
	lv.Attachment0 = att
	lv.RelativeTo = Enum.ActuatorRelativeTo.World
	lv.VelocityConstraintMode = Enum.VelocityConstraintMode.Plane
	lv.PrimaryTangentAxis = Vector3.xAxis
	lv.SecondaryTangentAxis = Vector3.zAxis
	lv.PlaneVelocity = Vector2.zero
	lv.MaxForce = 4e5
	lv.Parent = hrp
	Debris:AddItem(lv, duration)
	Debris:AddItem(att, duration)
end

return {
	run = function(ctx, targetRoot: BasePart, p)
		local root, model = ctx.root, ctx.model
		ctx.stop()
		ctx.setGearState("Attacking", true)
		ctx.face(targetRoot.Position)
		local track = anim(ctx, p.anim)
		if track then
			track:Play(0.1, 1, THROW_MARKER_TIME / p.windup)
		end

		local function laneOrigin(): CFrame
			local g = Telegraph.ground(model, root.Position)
			return CFrame.lookAt(g, g + flat(root.CFrame.LookVector))
		end
		local lane = Telegraph.lane(laneOrigin(), p.length, p.width, p.windup)
		local started = os.clock()
		while os.clock() - started < p.windup do
			if not ctx.alive() or not targetRoot.Parent then
				lane.done(false)
				if track then track:Stop(0.2) end
				ctx.setGearState("Attacking", false)
				return
			end
			if os.clock() - started < p.lockTime then
				ctx.face(targetRoot.Position)
				lane.setOrigin(laneOrigin())
			end
			task.wait()
		end
		lane.done(true)

		-- 던지기: 손의 갈고리를 숨기고 같은 모양의 투사체를 날린다. 사슬은 Beam
		local hook = model:FindFirstChild("RightHand__Hook")
		local boom = model:FindFirstChild("RightHand__Paint")
		local dir = flat(root.CFrame.LookVector)
		local scale = model:GetScale()
		local from = if hook then hook.Position else root.Position + dir * 3
		local height = Telegraph.ground(model, root.Position).Y + FLY_HEIGHT
		local proj
		local beam
		if hook then
			proj = hook:Clone()
			proj:ClearAllChildren()
			local sa = hook:FindFirstChildOfClass("SurfaceAppearance")
			if sa then
				sa:Clone().Parent = proj
			end
			proj.Anchored = true
			proj.CanCollide = false
			proj.CanQuery = false
			proj.CanTouch = false
			proj.Name = "ForemanThrownHook"
			proj.Parent = workspace
			hook.Transparency = 1
			if boom then
				local a0 = Instance.new("Attachment")
				a0.Name = "ChainStart"
				a0.Position = Vector3.new(0, -boom.Size.Y * 0.45, 0)
				a0.Parent = boom
				local a1 = Instance.new("Attachment")
				a1.Name = "ChainEnd"
				a1.Position = Vector3.new(0, proj.Size.Y * 0.4, 0)
				a1.Parent = proj
				beam = Instance.new("Beam")
				beam.Attachment0 = a0
				beam.Attachment1 = a1
				beam.Width0 = 0.25 * scale
				beam.Width1 = 0.25 * scale
				beam.Color = ColorSequence.new(Color3.fromRGB(70, 45, 30))
				beam.LightInfluence = 1
				beam.FaceCamera = true
				beam.Segments = 1
				beam.Parent = boom
			end
		end
		sfx(ctx, "ThrowWhoosh", 0.7)
		sfx(ctx, "ChainRattle", 1.1)

		local hitPlayers = {}
		local already = {}
		local travelled = 0
		local last = os.clock()
		local pos = from -- 손 높이에서 출발해 금방 바닥 + FLY_HEIGHT 로 내려온다
		while travelled < p.length and ctx.alive() do
			local now = os.clock()
			local step = math.min(p.speed * (now - last), p.length - travelled)
			last = now
			travelled += step
			pos += dir * step
			pos = Vector3.new(pos.X, pos.Y + (height - pos.Y) * math.min(1, step / 6), pos.Z)
			if proj then
				proj.CFrame = CFrame.lookAt(pos, pos + dir)
			end
			local got = Telegraph.hit(model, function(r)
				local o = r.Position - pos
				return Vector3.new(o.X, 0, o.Z).Magnitude <= p.width / 2 + 1 and math.abs(r.Position.Y - height) <= HEIGHT_TOLERANCE
			end, p.damage, already)
			for _, pl in got do
				table.insert(hitPlayers, pl)
			end
			if #hitPlayers > 0 then
				break
			end
			task.wait()
		end
		ctx.setGearState("Attacking", false)

		-- 맞은 사람은 보스 앞으로 끌려온다
		if #hitPlayers > 0 then
			sfx(ctx, "HookHit", 0.9)
			for _, pl in hitPlayers do
				local hrp = pl.Character and pl.Character:FindFirstChild("HumanoidRootPart")
				if hrp then
					local to = root.Position + dir * p.stopDistance
					local off = Vector3.new(to.X - hrp.Position.X, 0, to.Z - hrp.Position.Z)
					if off.Magnitude > 1 then
						shove(pl, off / p.pullTime + Vector3.new(0, 6, 0), p.pullTime)
					end
				end
			end
		end

		-- 갈고리 회수
		sfx(ctx, "ChainRattle", 0.9)
		local pullTime = if #hitPlayers > 0 then p.pullTime else 0.4
		local t0 = os.clock()
		local startPos = pos
		while proj and os.clock() - t0 < pullTime do
			local a = (os.clock() - t0) / pullTime
			local hand = if hook then hook.Position else root.Position
			local cur = startPos:Lerp(hand, a)
			proj.CFrame = CFrame.lookAt(cur, cur + dir)
			task.wait()
		end
		if proj then
			proj:Destroy()
		end
		if beam then
			local a0 = beam.Attachment0
			beam:Destroy()
			if a0 then
				a0:Destroy()
			end
		end
		if hook then
			hook.Transparency = 0
		end
		if not ctx.alive() then
			return
		end

		-- 확정 연계: 끌려온 사람 위로 바로 내려찍기 (예고 없음, 피할 수 없음 — 패링만 됨)
		if #hitPlayers > 0 and p.comboDamage then
			local victims = {}
			local nearest
			for _, pl in hitPlayers do
				local hrp = pl.Character and pl.Character:FindFirstChild("HumanoidRootPart")
				if hrp then
					victims[pl.Character] = true
					pin(pl, p.comboWindup)
					nearest = nearest or hrp
				end
			end
			if nearest then
				ctx.face(nearest.Position)
				ctx.setGearState("Attacking", true)
				ctx.tracks.attack:Play(0.05, 1, ctx.hitTime / p.comboWindup)
				task.wait(p.comboWindup)
				ctx.setGearState("Attacking", false)
				if not ctx.alive() then
					return
				end
				Telegraph.hit(model, function(r)
					return victims[r.Parent] == true
				end, p.comboDamage)
			end
		end

		model:SetAttribute("Opening", true)
		task.wait(p.recover)
	end,
}
