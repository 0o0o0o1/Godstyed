-- VfxKit 에 추가한 부분 (Controllers.SkillController.VfxKit, `return VfxKit` 바로 앞). 원본 기록용.
-- 착지 연기 고리 (신의 창·도약 찌르기 공용, 2026-11-24 사용자: 뭉게 덩이 먼지가 "방귀 같다" → 참고 그림처럼 바닥에 낮게 깔려 바깥으로 퍼지는 연기 고리)
-- 바닥: 위에서 본 연기 고리 시트(SmokeRing, 덩이가 고리를 따라 뭉게뭉게) / 테두리: 옆에서 본 낮은 연기 가닥 시트(SmokeWisp) 파티클을 원 둘레에서 바깥으로 뿌림
-- 시트: Blender scripts/vfx_smoke_ring.py (8x8, 칸 128, ID 는 exports/texture_ids.json VFX.SmokeRing)
-- radius = 다 퍼졌을 때 고리 반지름(스터드). opts: duration(고리 재생 초), count(가닥 수), color, light(주변 빛 영향)
VfxKit.SMOKE = {
	ring = "rbxassetid://124521428851491",
	wisp = "rbxassetid://89179403504248", -- v2: 아래가 부드럽게 옅어짐 (v1 72064605285438 은 바닥에서 뚝 끊겨 보였음)
}
function VfxKit.smokeRing(ctx: Ctx, ground: Vector3, radius: number, opts: { duration: number?, count: number?, color: Color3?, light: number? }?)
	local o = opts or {}
	local duration = o.duration or 1.4
	local color = o.color or Color3.new(1, 1, 1)
	local light = o.light or 0.3
	-- 1. 바닥 고리: 시트 끝 고리 반지름 = 칸 반지름의 0.9 → 판 크기 = radius * 2 / 0.9
	local size = radius * 2 / 0.9
	local part = VfxKit.holder(ctx, CFrame.new(ground + Vector3.new(0, 0.08, 0)) * CFrame.Angles(0, math.random() * math.pi * 2, 0), "SmokeRing")
	part.Size = Vector3.new(size, 0.05, size)
	local gui = Instance.new("SurfaceGui")
	gui.Face = Enum.NormalId.Top
	gui.LightInfluence = light
	gui.Brightness = 1.4
	gui.SizingMode = Enum.SurfaceGuiSizingMode.PixelsPerStud
	gui.PixelsPerStud = 10
	gui.ZOffset = 1
	gui.Parent = part
	local label = Instance.new("ImageLabel")
	label.BackgroundTransparency = 1
	label.Size = UDim2.fromScale(1, 1)
	label.Image = VfxKit.SMOKE.ring
	label.ImageColor3 = color
	label.ImageRectSize = Vector2.new(128, 128)
	label.ImageRectOffset = Vector2.zero
	label.Parent = gui
	local t0 = ctx:clock()
	ctx:step(t0 + duration, function(t)
		local i = math.floor((t - t0) / duration * 64)
		if i >= 64 then
			label.Visible = false
			return
		end
		label.ImageRectOffset = Vector2.new((i % 8) * 128, (i // 8) * 128)
	end)
	-- 2. 테두리 가닥: 원 둘레 count 곳에서 바깥으로 낮게. 빠르게 나갔다 느려짐(Drag) → 이동 거리 ≈ Speed / Drag ≈ radius
	-- 시트 칸 아래쪽이 바닥이라 파티클 중심을 크기의 0.42 위에 둠
	-- 개수·간격·크기·나오는 시각을 들쭉날쭉하게 (똑같은 가닥이 고른 간격으로 동시에 나오면 기계적이라고 해서, 2026-11-24)
	local count = math.max(3, (o.count or 14) + math.random(-2, 2))
	local wispSize = math.max(radius * 0.55, 3)
	for k = 1, count do
		local ang = (k + (math.random() - 0.5) * 0.9) / count * math.pi * 2
		local dir = Vector3.new(math.cos(ang), 0, math.sin(ang))
		local ws = wispSize * (0.7 + math.random() * 0.6)
		local from = ground + dir * radius * (0.1 + math.random() * 0.12) + Vector3.new(0, ws * 0.36, 0) -- 가닥 아래가 부드럽게 옅어져 조금 낮춤 (0.42 → 0.36)
		local holder = VfxKit.holder(ctx, CFrame.lookAt(from, from + dir), "SmokeWisp")
		local e = VfxKit.emitter(ctx, holder, {
			Texture = VfxKit.SMOKE.wisp,
			FlipbookLayout = Enum.ParticleFlipbookLayout.Grid8x8,
			FlipbookMode = Enum.ParticleFlipbookMode.OneShot,
			Color = ColorSequence.new(color),
			LightEmission = 0,
			LightInfluence = light,
			Size = VfxKit.seq({ { 0, ws * 0.7 }, { 1, ws * 1.15 } }),
			Transparency = VfxKit.seq({ { 0, 0.15 }, { 0.6, 0.35 }, { 1, 1 } }),
			Lifetime = NumberRange.new(duration * 0.9, duration * 1.1),
			Speed = NumberRange.new(radius * 2.2, radius * 2.8),
			Drag = 2.6,
			SpreadAngle = Vector2.new(8, 4),
			EmissionDirection = Enum.NormalId.Front,
			Rotation = NumberRange.new(-4, 4),
			ZOffset = 1,
		})
		pcall(function()
			(e :: any).FlipbookStartRandom = false
		end)
		task.delay(math.random() * 0.08 / ctx.scale, function()
			if e.Parent then
				e:Emit(1)
			end
		end)
	end
end
