-- 신의 창(god_spear, kind "skyfall") — ServerScriptService.Services.Skill 에 넣을 수정 (2026-11-24, 아직 적용 안 함)
-- 다른 세션이 Studio 플레이 중이라 multi_edit 를 못 해서 여기 저장. 마을 place 편집 모드에서 아래 6곳을 multi_edit 로 적용.
-- (이미 적용됨: Shared.Data.Skills god_spear·kind 주석·warnTime/root 필드, PolearmRelics relic_god_spear,
--  StatusEffects rooted, Services.StatusEffect kind "root" → MoveSpeedMult 0 + Rooted 속성,
--  MovementController 대시·점프 막음, SkillController 이동 스킬 막음 + skyfall 조준 쪽으로 몸 돌림)

-- [1] 헤더 주석: "--   hook: castDelay에 창을 던져 ..." 줄 다음에
--   skyfall: 카메라 조준 바닥에 castDelay + warnTime 뒤 하늘에서 창이 꽂혀 반경 피해 + 속박(rooted). 맞은 대상 목록을 phase "pin" 으로 (신의 창)

-- [2] ECHO_EXCLUDED 끝 "spin = true }" → "spin = true, skyfall = true }" 그리고 바로 아래에:
-- 속박(Rooted) 중에 못 쓰는 kind (몸이 움직임). 클라이언트 SkillController.cast 와 같음
local ROOT_BLOCKED = { lunge = true, charge = true, leap = true }

-- [3] "-- aim: 클라이언트가 보낸 카메라 조준 방향" 주석(plan 위) 바로 앞에:
-- 신의 창 (kind "skyfall")
-- 꽂히는 자리: 가슴에서 카메라 조준(높낮이 ±maxPitch) 레이가 닿는 곳(최대 maxDistance)의 바닥.
-- 보정 aimAssist도: 조준선 안의 보이는 적이면 그 적 발밑. 바닥이 없으면(허공) 내 발 높이
-- 하늘에서 떨어지는 창이라 지붕·천장은 보지 않음 (실내에서도 꽂힘. 연출은 지붕을 뚫고 내려옴)
local function skyfallPlan(character: Model, root: BasePart, facing: Vector3, skill: Skills.SkillDef, aim: any): (any, Vector3)
	local humanoid = character:FindFirstChildOfClass("Humanoid")
	local foot = (if humanoid then humanoid.HipHeight else 2) + root.Size.Y / 2
	local chest = root.Position + Vector3.new(0, CAST_UP, 0)
	local range = skill.maxDistance or 40
	local params = terrainParams()
	local dir = hookAim(character, chest, facing, aim, { maxPitch = skill.maxPitch, aimAssist = 0, maxDistance = range } :: any)
	local hit = workspace:Raycast(chest, dir * range, params)
	local candidate = if hit then hit.Position - dir * 1 else chest + dir * range
	-- 약한 보정: 조준선에서 aimAssist도 안, 사거리 안, 가려지지 않은 적 발밑 (각도가 가장 가까운 적)
	local assist = skill.aimAssist or 0
	if assist > 0 then
		local bestDot = math.cos(math.rad(assist))
		for _, target in EnemyService.humanoidsInRadius(chest, range + 4, true) do
			local model = target.Parent :: Model
			local targetRoot = model and model:FindFirstChild("HumanoidRootPart")
			if not (targetRoot and targetRoot:IsA("BasePart") and hookable(target, character)) then
				continue
			end
			local v = targetRoot.Position - chest
			if v.Magnitude < 2 or v.Magnitude > range then
				continue
			end
			local dot = v.Unit:Dot(dir)
			if dot > bestDot and not workspace:Raycast(chest, v, params) then
				bestDot = dot
				candidate = targetRoot.Position
			end
		end
	end
	-- 수평 거리 제한
	local flat = (candidate - root.Position) * DamageDealer.HORIZONTAL
	if flat.Magnitude > range then
		candidate = Vector3.new(root.Position.X, candidate.Y, root.Position.Z) + flat.Unit * range
	end
	local down = workspace:Raycast(candidate + Vector3.new(0, 1, 0), Vector3.new(0, -80, 0), params)
	local center = if down then down.Position else Vector3.new(candidate.X, root.Position.Y - foot, candidate.Z)
	local look = if flat.Magnitude > 0.5 then flat.Unit else facing
	return {
		origin = CFrame.lookAt(root.Position, root.Position + look),
		center = center,
		radius = skill.radius,
		warnTime = skill.warnTime,
	}, center
end

-- 꽂힘: castDelay + warnTime 에 center 반경 radius 안(높이 차 radius×0.6 안, 창이 꽂힌 자리에서 보이는) 대상에 피해
-- + 속박 root초 (보스·강철 의지 제외) + 짧은 경직. 맞은 대상은 phase "pin" 연출로 (사슬·빛 조각을 붙일 자리)
local SKYFALL_FLINCH = 0.25
local function skyfallHits(player: Player, character: Model, center: Vector3, skill: Skills.SkillDef, weaponDamage: number)
	task.delay(skill.castDelay + (skill.warnTime or 0.9), function()
		if not (player.Parent and character.Parent) then
			return
		end
		local radius = skill.radius or 18
		local damage = weaponDamage * skill.damage
		local eye = center + Vector3.new(0, 3, 0)
		local params = terrainParams()
		local pinned = {}
		for _, target in EnemyService.humanoidsInRadius(eye, radius + 3, true) do
			if not hookable(target, character) then
				continue
			end
			local model = target.Parent :: Model
			local targetRoot = model:FindFirstChild("HumanoidRootPart") :: BasePart?
			if not targetRoot then
				continue
			end
			local offset = (targetRoot.Position - center) * DamageDealer.HORIZONTAL
			if offset.Magnitude > radius + 1 or math.abs(targetRoot.Position.Y - center.Y) > radius * 0.6 then
				continue
			end
			if workspace:Raycast(eye, targetRoot.Position - eye, params) then
				continue -- 벽 너머
			end
			local crit = math.random() < CombatConfig.CRIT.CHANCE
			local dealt = DamageDealer.deal(player, target, if crit then damage * CombatConfig.CRIT.MULTIPLIER else damage, true, crit)
			if dealt > 0 and target.Health > 0 then
				local pin = (skill.root or 0) > 0 and not model:GetAttribute("Boss") and not model:GetAttribute("Unstoppable")
				if pin then
					StatusEffect.apply(target, "rooted", { source = player, stacks = 1, maxStacks = 1, duration = skill.root :: number, value = 0 })
				end
				DamageDealer.push(target, SKYFALL_FLINCH, Vector3.zero)
				table.insert(pinned, { model = model, pinned = pin })
			end
		end
		if #pinned > 0 then
			fxRemote:FireAllClients(skill.id, character, { origin = CFrame.new(center), phase = "pin", followup = true, targets = pinned, root = skill.root })
		end
	end)
end

-- [4] plan() 안 `if skill.kind == "hook" then` 바로 앞에:
--[[
	if skill.kind == "skyfall" then
		local payload, center = skyfallPlan(character, root, facing, skill, aim)
		return payload, function(weaponDamage)
			skyfallHits(player, character, center, skill, weaponDamage)
		end
	end
]]

-- [5] onCast 안 `local relic, skill = skillAt(...)` / `if not skill then return end` 바로 뒤에:
--[[
	if ROOT_BLOCKED[skill.kind] and character:GetAttribute("Rooted") then
		return -- 속박 중에는 몸이 움직이는 스킬 불가
	end
]]

-- [6] onCast 의 `if (skill.kind == "hook" or skill.kind == "leap") and typeof(claimedFacing) == "Vector3"`
--     → `(skill.kind == "hook" or skill.kind == "leap" or skill.kind == "skyfall")`
