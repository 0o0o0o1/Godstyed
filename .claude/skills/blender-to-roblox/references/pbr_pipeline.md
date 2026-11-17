# PBR 텍스처 파이프라인 (Container_40ft에서 검증된 방법)

## 1. 작업용 오브젝트 구성
- 모든 부품을 **오브젝트 하나**로 만들고 머티리얼 슬롯으로 구분합니다 (예: 0 = 몸체, 1 = 철물). 같은 1024 아틀라스를 공유하도록 함께 UV를 펼치고 함께 굽습니다.
- 굽기가 끝나면 복사본을 `mesh.separate(type='MATERIAL')`로 나눠 내보내고, 원본은 `<에셋>_WORK` 컬렉션에 숨겨서 남겨 둡니다 (다시 구울 때 사용).
- 닫힌 내부처럼 **절대 안 보이는 면은 지웁니다** (UV 공간 낭비). 이때 찌그러짐(dent)으로 안쪽으로 밀린 면까지 지우지 않게 기준을 넉넉히 잡으세요. 실제로 `|y| < 5.5`로 지웠다가 옆벽에 구멍이 났고, `|y| < 5.2`로 고쳤습니다.

## 2. UV 전략 (해상도 = 1스터드당 픽셀)
1. `uv.smart_project(angle_limit=60°, island_margin=0.002)`
2. 바닥면처럼 거의 안 보이는 섬은 UV를 30%로 줄입니다.
3. **가장 크고 잘 보이는 면은 직접 배치합니다.** 양쪽 옆벽은 같은 UV 띠에 겹치게 놓고(바깥에서 봤을 때 글씨가 바로 읽히는 방향으로), 지붕은 그 위의 띠에 놓습니다.
4. 나머지 섬은 남은 영역에 넣고 `uv.pack_islands(shape_method='CONCAVE', scale=True, udim_source='ORIGINAL_AABB')`로 채웁니다. 직접 배치한 면은 `face.hide = True`로 숨겨서 pack에서 빠지게 합니다.
- 결과: 11.7 → 옆벽·지붕 22, 나머지 18 (픽셀/스터드). 목표는 18 이상입니다.
- 겹친 UV를 쓰는 면은 face 속성 `uvspace = 1`을 주고, 셰이더가 그 면에서 Object 좌표 대신 **UV에서 다시 계산한 좌표**를 쓰게 합니다. 그래야 겹친 두 면에서 같은 값이 나와 굽기 결과가 깨지지 않습니다.

## 3. 낡은 셰이더 레시피 (절차적, Object/UV 좌표 기반)
| 마스크 | 만드는 법 |
|---|---|
| 녹물 줄기 | Noise(좌표 × (1.8, 1.8, 0.07)) → 세로로 늘어진 줄. 높이가 높을수록 강하게 |
| 상단 녹 번짐 | 맨 위 레일 바로 아래 띠 × noise |
| 녹 얼룩 | 저주파 noise(0.12)와 중주파 noise(0.45)를 임계값으로 자름 |
| 페인트 벗겨짐 | 고주파 noise(0.85, detail 12)를 날카로운 임계값으로 자름 |
| 모서리 마모 | Bevel 노드 노멀과 원래 노멀의 dot → 모서리 마스크 × noise |
| 하단 때 | 높이 0~3.2 그라데이션 × noise |
| 틈새 그을음 | AO 노드(거리 1.2), 색에 곱하기 |
| 햇빛 바램 | 위를 향하는 면, 높은 곳일수록 바랜 베이지와 섞기 |
| 글씨 | Workbench로 흰 글씨/검은 배경 마스크를 렌더링(옆벽 공간 2048×461, 문 공간 1024²) → 벗겨짐·녹 부분을 빼고 noise로 군데군데 지움 |
- 회사명·번호는 **가상의 이름**만 씁니다 (현재: KESTREL LINES, KSTU 482019 4). 실제 선사 이름·로고는 쓰지 않습니다.
- Roughness: 페인트 0.58 → 녹 0.93. Metalness: 모서리 맨 금속만 약간(최대 0.55). 철물은 녹이 없는 곳 0.7.
- Normal: Bump(벗겨진 페인트 두께 + 녹 피팅 noise), strength 0.4.

## 4. 굽기
- Cycles, samples 32 (노멀 맵은 16), margin 8, 1024×1024.
- Color/Roughness/Metalness: 해당 값을 Emission에 연결하고 `bake(type='EMIT')`. Color 이미지는 sRGB, 나머지는 Non-Color.
- Normal: Principled(Bump 연결)을 출력에 연결하고 `bake(type='NORMAL', normal_space='TANGENT')`. OpenGL(Y+) 방식이라 Roblox와 맞습니다.
- 모든 머티리얼의 `BAKE_TARGET` 이미지 노드를 같은 이미지로 설정하고 active로 만든 뒤 굽습니다.
- 한 번의 MCP 호출에 2~3장씩 굽습니다 (7장을 한 번에 돌리면 연결이 끊김).

## 5. Roblox 업로드 — 반드시 "텍스처 견본 FBX" 방식

**이 게임("도시")은 그룹 소유(Group 597081155)입니다.** Roblox는 게임 소유자가 가진 이미지만 불러옵니다.
- ❌ Studio MCP `upload_image`는 **사용자 개인 소유**로 올라가서 이 게임에서 `AssetFetchStatus.Failure`가 나고 하얗게 보입니다. 쓰지 마세요.
  (참고: 이 도구는 http/https 주소만 받아서 로컬 서버가 필요하고, 그렇게 올려도 소유권 문제는 그대로입니다.)
- ✅ **텍스처 견본 FBX**: 텍스처마다 작은 판(2×2)을 하나씩 만들고, 그 이미지를 판의 **Base Color**에 연결한 뒤 `path_mode='COPY', embed_textures=True`로 내보냅니다(`TexUpload_<에셋>.fbx`). 사용자가 Import 3D로 가져오면 Importer가 **게임 소유자(그룹)**로 업로드합니다.
  - 가져온 뒤 각 `TexSwatch_*` MeshPart의 `TextureID`가 그룹 소유 이미지 ID입니다. Roughness/Metalness/Normal도 Base Color로 실어 보내면 값이 그대로 올라가고, ID만 해당 맵에 쓰면 됩니다.
  - ID를 꺼낸 뒤 견본 모델은 Workspace에서 지웁니다.
  - `ContentProvider:PreloadAsync`로 `Success`를 확인하고, `MarketplaceService:GetProductInfo(id).Creator`가 Group인지 확인하세요.
- 반환된 ID를 `exports/texture_ids.json`과 `studio_postimport.lua`의 `TEXTURES`에 기록합니다.
- 스크립트로 `SurfaceAppearance.ColorMap/NormalMap/RoughnessMap/MetalnessMap` 설정이 가능합니다. 단, 이미 실패한 ID를 들고 있던 SurfaceAppearance는 ID를 바꿔도 화면이 갱신되지 않으니 **지우고 새로 만들어 붙이세요.**

## 5.5 건물용 타일 텍스처 (Warehouse_Main에서 검증)

큰 건물은 아틀라스 대신 **타일 텍스처 세트**를 굽고 여러 MeshPart가 같이 씁니다.
- 굽는 대상: UV 0..1인 평면 하나(`WhTex_SidingPlane` 24×30, `WhTex_SteelPlane` 8×8). 셰이더는 UV 좌표 기반.
- **한 방향만 이어지는 타일**(골판 외벽): U는 4D 노이즈 링(`(R·cos2πu, R·sin2πu, v·k, seed)`)으로 이어지게, V는 벽 높이 전체(30)에 그대로 매핑 → 아래쪽 때·물튀김, 고정 볼트 줄(1/3, 2/3 높이)에서 흘러내린 녹물, 판 이음선을 넣을 수 있음. 메쉬 UV는 `u = 가로/24, v = 높이/30`(박공벽 `높이/36`).
- **양방향 타일**(철골): `(Ru·cos2πu, Ru·sin2πu, Rv·cos2πv, Rv·sin2πv)` 4D 노이즈. 메쉬 UV는 박스 투영 8스터드/타일.
- 골 주름은 **노멀맵**으로 (Bump Distance 0.3). 0.02로 구우면 거의 평평하게 나옴 → 굽고 나서 R 채널 범위(0.15~0.85 정도)를 확인.
- 색 변형(외벽/지붕/셔터)은 `PAINT` RGB 노드 값만 바꿔 Color만 다시 굽고 Normal/Roughness/Metalness는 공유.
- 셔터처럼 골이 가로인 면은 UV를 돌려서(`u = 높이/9.6`) 같은 텍스처 사용.
- 큰 녹 얼룩은 타일 반복이 눈에 띄므로 임계값을 높여(0.6~0.69) 드물게.
- 텍스처 세트가 여러 개인 에셋은 부품 이름 접두사(`WhSiding_`, `WhSteel_`)로 세트를 고르고, **팔레트 키**(`SidingTeal`, `RoofZinc`, `ShutterOrange`, `SteelBlue`)로 Color 변형을 고름 (`studio_postimport.lua`의 `applySurface`).

### 큰 건물의 충돌
- 모든 메쉬는 `__NoCollide`로 내보내고, Studio에서 **Blender 좌표로 정의한 투명 Part**를 만들어 충돌을 맞춤 (벽은 개구부를 뺀 상자들, 지붕은 경사 판, 계단은 경사 판 1개, 난간은 얇은 판).
- 지붕 구멍처럼 랜덤으로 만든 모양은 Blender에서 마스크를 문자열로 출력해 Luau에 붙여 넣어 같은 모양의 충돌 판을 만듦.
- 사다리는 **투명 TrussPart**(2×N×2)로 → 걸어 들어가면 자동으로 오름 (확인됨).
- Blender 좌표 (x, y, z) → 가져온 모델 로컬 (-x, z, y). 모델을 `CFrame.Angles(0, π/2, 0)`로 돌리면 Blender x → Roblox +Z, Blender y → Roblox +X.
- 에셋 FBX를 내보낼 때는 이미지 노드가 없는 단순 머티리얼(`MX_Plain_<키>`)로 잠깐 바꿔서 내보내고 다시 미리보기 머티리얼로 돌려놓음.

## 6. 색 변형별 주의
- 밝은 바탕색(DirtyWhite 등)에는 **흰 글씨가 묻혀 안 보입니다.** 밝은 색 변형은 글씨를 짙은 남색(38, 46, 68)으로 바꿔서 굽습니다. 셰이더의 글씨 색 Mix 노드 이름은 `TEXTMIX`입니다.
- 굽는 오브젝트는 `hide_render = False`여야 합니다 (작업용 오브젝트를 숨길 때 `hide_set`만 쓰고 `hide_render`는 끄지 마세요).
