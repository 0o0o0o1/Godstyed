-- Roblox Studio post-import for Blender assets (run with Studio MCP execute_luau, Edit datamodel).
-- Set ASSET_NAME at the bottom. Finds the imported model in Workspace, applies naming rules,
-- sets bottom-center pivot, reports size, and moves it to ServerStorage.Assets.CanalWarehouse.

local PALETTE = {
	RustRed = {Color3.fromRGB(120, 55, 40), Enum.Material.CorrodedMetal},
	FadedBlue = {Color3.fromRGB(55, 80, 100), Enum.Material.CorrodedMetal},
	Olive = {Color3.fromRGB(85, 90, 60), Enum.Material.CorrodedMetal},
	DirtyWhite = {Color3.fromRGB(170, 165, 150), Enum.Material.Metal},
	CraneYellow = {Color3.fromRGB(175, 110, 40), Enum.Material.CorrodedMetal},
	DarkSteel = {Color3.fromRGB(60, 60, 62), Enum.Material.Metal},
	Rust = {Color3.fromRGB(105, 60, 40), Enum.Material.CorrodedMetal},
	Concrete = {Color3.fromRGB(95, 95, 90), Enum.Material.Concrete},
	DiamondPlate = {Color3.fromRGB(80, 80, 80), Enum.Material.DiamondPlate},
	Rubber = {Color3.fromRGB(30, 30, 30), Enum.Material.Plastic},
	Glass = {Color3.fromRGB(90, 105, 110), Enum.Material.Glass},
	Canvas = {Color3.fromRGB(90, 85, 65), Enum.Material.Fabric},
	Wood = {Color3.fromRGB(110, 85, 60), Enum.Material.WoodPlanks},
	Hazard = {Color3.fromRGB(190, 150, 40), Enum.Material.SmoothPlastic},
	-- texture-set variants (visuals come from SurfaceAppearance; color is the fallback)
	SidingTeal = {Color3.fromRGB(95, 115, 108), Enum.Material.CorrodedMetal},
	RoofZinc = {Color3.fromRGB(122, 124, 120), Enum.Material.CorrodedMetal},
	ShutterOrange = {Color3.fromRGB(158, 98, 50), Enum.Material.CorrodedMetal},
	SteelBlue = {Color3.fromRGB(60, 68, 78), Enum.Material.Metal},
}

local function parseName(name)
	local parts = string.split(name, "__")
	local opts = {}
	for i = 3, #parts do opts[parts[i]] = true end
	return parts[1], parts[2], opts
end

-- PBR texture sets (from exports/texture_ids.json). Key = asset prefix before the first "_" of the part name.
local TEXTURES = {
	Container40 = {
		Color = {
			RustRed = "rbxassetid://130510789441720",
			FadedBlue = "rbxassetid://107206467524502",
			Olive = "rbxassetid://91598772669186",
			DirtyWhite = "rbxassetid://135545618962984", -- v2: dark navy text (white text was invisible)
		},
		Normal = "rbxassetid://126151414262873",
		Roughness = "rbxassetid://136677513751331",
		Metalness = "rbxassetid://115530291617642",
	},
	Container20 = {
		Color = {
			RustRed = "rbxassetid://101783122966276",
			FadedBlue = "rbxassetid://72643923011469",
			Olive = "rbxassetid://125074963537265",
			DirtyWhite = "rbxassetid://135252773487669",
		},
		Normal = "rbxassetid://138452119007577",
		Roughness = "rbxassetid://79159293771381",
		Metalness = "rbxassetid://93220606877060",
	},
	-- Crane_STS: tileable maps (UV = world box projection, 20 studs per tile). Use VARIANT = "CraneYellow".
	CraneSTS = {
		Color = {
			CraneYellow = "rbxassetid://112714235470357",
		},
		Normal = "rbxassetid://81085273014661",
		Roughness = "rbxassetid://79409976353138",
		Metalness = "rbxassetid://127183483645771",
	},
	-- Warehouse_Main tileable sets. Color variant = the part's palette key (e.g. WhSiding_Roof__RoofZinc__TEX).
	WhSiding = {
		Color = {
			SidingTeal = "rbxassetid://126209095166827",
			RoofZinc = "rbxassetid://103975482907154",
			ShutterOrange = "rbxassetid://129767392683582",
		},
		Normal = "rbxassetid://134641190476675",
		Roughness = "rbxassetid://114139515165698",
		Metalness = "rbxassetid://106273879084217",
	},
	WhSteel = {
		Color = { SteelBlue = "rbxassetid://125962397461553" },
		Normal = "rbxassetid://99734605337204",
		Roughness = "rbxassetid://92645181061547",
		Metalness = "rbxassetid://122834005449657",
	},
}

-- Crane_Collapsed reuses the STS tile set (same 20-stud box-projection UVs)
TEXTURES.CraneCol = TEXTURES.CraneSTS
TEXTURES.RTG = TEXTURES.CraneSTS -- Crane_RTG uses the same tile set

-- Attach / replace a SurfaceAppearance on a __TEX MeshPart. variant picks the color map.
local function applySurface(p, variant)
	local prefix = string.split(p.Name, "_")[1]
	local set = TEXTURES[prefix]
	if not set then return false end
	local old = p:FindFirstChildOfClass("SurfaceAppearance")
	if old then old:Destroy() end -- recreate: an SA that once failed to load won't refresh in the viewport
	local sa = Instance.new("SurfaceAppearance")
	local fallback = set.Color.RustRed
	if not fallback then local _, v = next(set.Color); fallback = v end
	-- the part's own palette key wins when the set has a color map for it (multi-variant assets like Warehouse_Main)
	local pal = string.split(p.Name, "__")[2]
	sa.ColorMap = (pal and set.Color[pal]) or set.Color[variant] or fallback
	sa.NormalMap = set.Normal
	sa.RoughnessMap = set.Roughness
	sa.MetalnessMap = set.Metalness
	sa.Parent = p
	p.Material = Enum.Material.Metal -- footsteps/impact sound; visuals come from the SurfaceAppearance
	return true
end

local VARIANT = "RustRed"

local function process(ASSET_NAME, MOVE_TO_STORAGE)
	local model = workspace:FindFirstChild(ASSET_NAME)
	if not model then
		-- importer may name the model after the file; fall back to newest model containing a matching part
		for _, m in ipairs(workspace:GetChildren()) do
			if m:IsA("Model") and m:FindFirstChildWhichIsA("MeshPart", true) and string.find(m.Name, ASSET_NAME, 1, true) then
				model = m
			end
		end
	end
	if not model then return "ERROR: model '" .. ASSET_NAME .. "' not found in Workspace" end
	model.Name = ASSET_NAME

	local out, warn, count = {}, {}, 0
	local manual, colliders = {}, {}
	for _, p in ipairs(model:GetDescendants()) do
		if p:IsA("BasePart") and not p.Name:find("_Collider$") then
			count += 1
			p.Anchored = true
			local base, pal, opts = parseName(p.Name)
			local entry = pal and PALETTE[pal]
			if opts.TEX then
				if not (p:IsA("MeshPart") and applySurface(p, VARIANT)) then
					table.insert(warn, p.Name .. ": __TEX but no texture set in TEXTURES")
				end
			elseif entry then
				p.Color = entry[1]
				p.Material = entry[2]
				if pal == "Glass" then p.Transparency = 0.4 end
			else
				table.insert(warn, p.Name .. ": unknown/missing palette key")
			end
			-- CollisionFidelity cannot be changed from scripts in Studio, so:
			--   default  -> invisible box collider Part, mesh itself non-colliding
			--   Hull/Precise -> keep mesh collision, ask the user to set fidelity manually
			if opts.NoCollide then
				p.CanCollide = false; p.CanTouch = false; p.CanQuery = false; p.CastShadow = false
			elseif opts.Hull or opts.Precise then
				table.insert(manual, p.Name .. " -> " .. (opts.Hull and "Hull" or "PreciseConvexDecomposition"))
			elseif p:IsA("MeshPart") then
				local cname = base .. "_Collider"
				local old = p.Parent:FindFirstChild(cname)
				if old then old:Destroy() end
				local c = Instance.new("Part")
				c.Name = cname
				c.Size = p.Size
				c.CFrame = p.CFrame
				c.Anchored = true
				c.Transparency = 1
				c.CastShadow = false
				c.CanTouch = false
				table.insert(colliders, {c, p.Parent})
				p.CanCollide = false
				p.CanTouch = false
			end
		end
	end

	for _, pair in ipairs(colliders) do pair[1].Parent = pair[2] end

	-- bottom-center pivot
	local cf, size = model:GetBoundingBox()
	local bottom = CFrame.new(cf.Position - Vector3.new(0, size.Y / 2, 0))
	if model.PrimaryPart then model.PrimaryPart = nil end
	model.WorldPivot = bottom

	table.insert(out, string.format("%s: %d parts, size X=%.2f Y=%.2f Z=%.2f", ASSET_NAME, count, size.X, size.Y, size.Z))
	table.insert(out, string.format("  colliders created: %d", #colliders))
	for _, w in ipairs(warn) do table.insert(out, "  warn " .. w) end
	for _, m in ipairs(manual) do table.insert(out, "  ASK USER to set CollisionFidelity: " .. m) end

	if MOVE_TO_STORAGE then
		local ss = game:GetService("ServerStorage")
		local assets = ss:FindFirstChild("Assets") or Instance.new("Folder", ss)
		assets.Name = "Assets"
		local cw = assets:FindFirstChild("CanalWarehouse") or Instance.new("Folder", assets)
		cw.Name = "CanalWarehouse"
		local old = cw:FindFirstChild(ASSET_NAME)
		if old then old.Name = ASSET_NAME .. "_old" end
		model.Parent = cw
		table.insert(out, "  moved to ServerStorage.Assets.CanalWarehouse" .. (old and " (previous kept as _old)" or ""))
	end
	return table.concat(out, "\n")
end

-- EDIT HERE ---------------------------------------------------------------
return process("Container_40ft", true)
