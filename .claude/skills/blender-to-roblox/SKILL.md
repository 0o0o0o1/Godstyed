---
name: blender-to-roblox
description: Rules and workflow for building Roblox map assets in Blender (via the Blender MCP) and bringing them into Roblox Studio — scale (1 Blender unit = 1 stud, truck 28×11×12 reference), origin/pivot, FBX export settings, naming, collision fidelity, triangle budgets, and the post-apocalypse color palette. Use this whenever modeling any prop, container, crane, building or other asset in Blender that is meant for Roblox, exporting FBX for Studio, or fixing an imported mesh that came in at the wrong size, rotation, pivot, color or collision — even if the user only says "블렌더로 만들어줘", "컨테이너 모델링", "FBX 내보내기" or "Studio에 가져왔는데 크기가 이상해".
---

# Blender → Roblox 에셋 파이프라인

이 프로젝트(로블록스 포스트 아포칼립스 도시 맵, 플레이스 "도시")의 에셋을 Blender에서 만들어 Studio로 옮길 때의 규칙입니다.
목표는 **어떤 에셋이든 같은 기준**으로 만들어서, Studio에 넣었을 때 크기·방향·피벗·색·충돌을 다시 손볼 필요가 없게 하는 것입니다.

작업 흐름은 항상 이 순서입니다.

1. Blender에서 모델링 (규칙 1~5)
2. 내보내기 전 점검 → FBX 내보내기 (규칙 6)
3. **사용자가** Studio에서 `File → Import 3D`로 가져오기 (규칙 7)
4. Studio MCP로 후처리 스크립트 실행 (규칙 8)
5. 검사 & 보고

사용자는 단계마다 보고받고 확인하기를 원합니다. 에셋 하나를 끝낼 때마다 무엇을 만들었는지(크기, 삼각형 수, 파일 경로)를 짧게 보고하고 다음 단계로 넘어갈지 물어보세요.

---

## 1. 스케일: 1 Blender unit = 1 stud

- Blender 씬 단위는 `Unit System = None` 또는 `Metric, Unit Scale = 1.0`으로 두고, **Blender의 1 = Roblox의 1 스터드**로 생각하고 모델링합니다. 미터 감각으로 만들지 마세요. 이 맵은 자동차가 캐릭터에 비해 큰 스케일이라, 현실 비율로 만들면 어색해집니다.
- 기준 크기 (맵에 이미 있는 것):
  | 대상 | 크기 (X × Y높이 × Z, 스터드) |
  |---|---|
  | 캐릭터 | 약 4 × 5 × 1 (점프 높이 약 7) |
  | 세단 | 27 × 8 × 11 |
  | 트럭 | 28 × 11 × 12 |
  | 차선 1개 | 약 18 폭 |
- 이 프로젝트의 표준 에셋 크기:
  | 에셋 | 크기 (길이 × 높이 × 폭) |
  |---|---|
  | Container_40ft | 48 × 12 × 12 |
  | Container_20ft | 24 × 12 × 12 |
  | 문 높이 | 9 이상 (캐릭터가 여유 있게 지나가게) |
  | 통로 폭 | 16 ~ 20 |
  | 계단 한 단 | 높이 1, 깊이 2 |
- 실제로 Studio에 들어간 크기는 **보정 결과(아래 9장)**가 정답입니다. 보정 결과와 다르게 나오면 이 문서의 규칙보다 보정 결과를 따르세요.

## 2. 축과 원점(피벗)

- Blender는 Z가 위, Roblox는 Y가 위입니다. 내보내기 설정(규칙 6)이 이 변환을 처리하므로 Blender 안에서는 **Z = 위**로 정상적으로 모델링하세요.
- 길쭉한 에셋(컨테이너, 트럭, 크레인 붐)은 **긴 쪽을 Blender X축**에 맞춥니다. 앞쪽(컨테이너 문, 크레인 붐 끝)은 **Blender +X** 방향입니다. Studio에 들어오면 이 앞쪽이 **Roblox -X**를 향합니다 (9장 보정 결과). 맵에 배치할 때 이걸 기준으로 회전하세요.
- **원점 = 바닥 중앙 (0, 0, 0)**. 에셋의 바닥 면이 Z=0에 닿고, XY 중앙이 원점에 오게 합니다. 이렇게 하면 Studio에서 지면 높이 Y에 그대로 놓을 수 있습니다.
  - Studio의 MeshPart는 Blender 원점을 버리고 메쉬 바운딩박스 중심을 위치로 씁니다. 그래서 피벗은 후처리(규칙 8)에서 `PivotOffset`으로 바닥 중앙에 다시 맞춥니다.
- 내보내기 전에 모든 오브젝트에 `Apply All Transforms`(Ctrl+A)를 적용해서 회전 0, 스케일 1 상태로 만듭니다. 적용하지 않으면 Studio에서 크기나 회전이 틀어집니다.

## 3. 이름 규칙

Studio의 후처리 스크립트가 **이름을 보고** 색·재질·충돌을 자동으로 설정합니다. 그래서 이름이 곧 설정입니다.

```
<에셋이름>_<부품>__<팔레트키>[__<옵션>]
예) Container40_Body__RustRed
    Container40_Doors__RustRed
    Container40_Frame__DarkSteel__NoCollide
    CraneSTS_Cab__CraneYellow__TEX
```

- `<에셋이름>`: Studio 모델 이름이 됩니다 (`Container_40ft`, `Crane_STS` 등. 계획서 5장 이름 사용).
- `__<팔레트키>`: 4장 팔레트의 키. 색과 Roblox Material이 이걸로 정해집니다.
- 옵션 (여러 개 가능):
  - `__NoCollide` 충돌 없음 (장식, 작은 디테일)
  - `__Hull` / `__Box` / `__Precise` 충돌 정밀도 직접 지정 (기본값은 5장 참고)
  - `__TEX` 텍스처 사용 부품 (색을 덮어쓰지 않음)
- 부품 하나 = 머티리얼 하나. 한 메쉬에 머티리얼이 여러 개 있으면 Studio가 임의로 쪼개서 이름이 망가집니다. 색이 다른 부분은 **별도 오브젝트로 분리**하세요.

## 4. 색 & 재질 팔레트 (기본: 색 + Roblox Material)

기본은 **텍스처 없이** MeshPart.Color + Roblox Material로 표현합니다. 골판 무늬, 리브, 볼트 같은 형태는 텍스처가 아니라 **메쉬 모양**으로 만드세요. 이미지 업로드가 필요 없고, Studio에서 색을 바로 바꿔 변형을 만들 수 있습니다.

| 팔레트 키 | RGB | Roblox Material | 용도 |
|---|---|---|---|
| RustRed | 120, 55, 40 | CorrodedMetal | 녹슨 빨강 컨테이너 |
| FadedBlue | 55, 80, 100 | CorrodedMetal | 바랜 파랑 컨테이너 |
| Olive | 85, 90, 60 | CorrodedMetal | 올리브 컨테이너 |
| DirtyWhite | 170, 165, 150 | Metal | 냉동(Reefer) 컨테이너 |
| CraneYellow | 175, 110, 40 | CorrodedMetal | 크레인 본체 |
| DarkSteel | 60, 60, 62 | Metal | 프레임, 레일, 기계 부품 |
| Rust | 105, 60, 40 | CorrodedMetal | 녹 덩어리, 체인 |
| Concrete | 95, 95, 90 | Concrete | 바닥, 기초, 블록 |
| DiamondPlate | 80, 80, 80 | DiamondPlate | 철판 바닥, 발판 |
| Rubber | 30, 30, 30 | Plastic | 타이어, 펜더 |
| Glass | 90, 105, 110 | Glass | 운전실 창 (Transparency 0.4) |
| Canvas | 90, 85, 65 | Fabric | 방수포, 텐트 |
| Wood | 110, 85, 60 | WoodPlanks | 팔레트, 판자 |
| Hazard | 190, 150, 40 | SmoothPlastic | 경고 줄무늬 (바랜 노랑) |

- Blender 쪽 머티리얼도 같은 이름(`M_RustRed`)과 비슷한 색으로 만들어 두면 `look`으로 볼 때 결과를 미리 확인하기 좋습니다. 단, Studio로 넘어가는 건 **이름**이고 Blender 색은 참고용입니다.
- 팔레트에 없는 색이 필요하면 임의로 만들지 말고 사용자에게 물어본 뒤 이 표에 추가하세요.

### PBR 텍스처를 쓰는 경우 (`__TEX`)

사용자는 **고품질**을 원합니다. 반복해서 많이 깔리는 주력 에셋(컨테이너, 크레인 등 랜드마크)과 형태로 표현할 수 없는 것(글씨, 녹물, 낙서)은 PBR 텍스처(SurfaceAppearance)로 만듭니다. 작은 소품은 계속 색+재질로 둡니다.
- 맵 4종(Color / Normal / Roughness / Metalness), 각 1024×1024 (Roblox 상한).
- 색 변형은 **Color 맵만 색마다 따로** 굽고, Normal/Roughness/Metalness는 공유합니다.
- 에셋 FBX에는 UV가 있는 메쉬와 **이미지 노드가 없는 단순 머티리얼**만 담습니다(텍스처 참조가 있으면 Importer가 엉뚱한 이미지로 SurfaceAppearance를 만들 수 있음).
- 텍스처는 별도의 **텍스처 견본 FBX**(`TexUpload_<에셋>.fbx`)로 사용자가 가져와서 **그룹 소유**로 올립니다. 게임이 그룹 소유라서, MCP `upload_image`(개인 소유)로 올린 이미지는 불러와지지 않습니다. 그다음 후처리 스크립트가 SurfaceAppearance를 붙입니다. 자세한 굽기·업로드 절차는 `references/pbr_pipeline.md`를 읽으세요.
- 업로드한 에셋 ID는 `exports/texture_ids.json`과 `scripts/studio_postimport.lua`의 `TEXTURES` 표에 같이 기록합니다.

## 5. 충돌 & 성능 규칙

**중요:** Studio에서 MeshPart의 `CollisionFidelity`는 스크립트(MCP 포함)로 바꿀 수 없습니다 (9장에서 확인). 그래서 충돌은 이렇게 처리합니다.

| 대상 | 방식 | 비고 |
|---|---|---|
| 상자형 (컨테이너 몸체, 벽, 바닥) — 기본값 | **충돌 프록시**: 후처리가 메쉬 크기와 같은 투명 Part(`<이름>_Collider`)를 만들고 메쉬는 CanCollide=false | 가장 가볍고 플레이어가 위에 올라서기 좋음 |
| 크레인 다리, 빔 같은 단순 볼록체 (`__Hull`) | 메쉬 충돌 유지, **사용자에게** Properties에서 CollisionFidelity=Hull 설정 부탁 | 여러 개 선택해서 한 번에 바꿀 수 있음 |
| 안으로 들어가는 것 (`__Precise`) | 가능하면 **벽·바닥을 별도 오브젝트로 분리**해서 각각 상자 프록시. 정말 필요할 때만 사용자에게 PreciseConvexDecomposition 설정 부탁 | |
| 작은 장식 (`__NoCollide`) | 충돌 없음 | CanCollide/CanTouch/CanQuery false, CastShadow false |

**겹침 금지 (사용자 지시 2026-11-18)**: 부재가 다른 부재를 뚫고 나오게 만들지 마세요(예: 서까래가 지붕판을 뚫음, 기둥이 벽을 관통, 파이프가 데크·난간을 관통). Roblox에서는 고칠 수 없습니다. 내보내기 전에 `mathutils.bvhtree.BVHTree.FromObject` + `overlap()`로 오브젝트 쌍별 겹침을 검사하고, 원래 붙는 접합부(파이프→밸브·탱크, 바닥 위 기둥)만 남기세요. 지붕·벽은 부재 꼭짓점이 지붕 밑면·벽 안쪽면을 넘는지 수치로도 확인하세요.

**텍스처 심의 함정**: Open Cloud로 올린 이미지를 심의(Approved) 전에 SurfaceAppearance에 붙이면 Studio가 그 ID를 실패로 캐시합니다. 붙이기 전에 `GET /assets/v1/assets/<이미지ID>`로 Approved 확인. 이미 꼬였으면 픽셀 1개를 바꿔 재업로드(같은 파일은 기존 ID로 합쳐짐).

상자 프록시는 메쉬의 바운딩박스 그대로라서, 상자가 아닌 모양(L자, 경사)은 **부품을 나눠서** 각 부품이 상자에 가깝게 만드세요.

- 삼각형 예산 (Roblox MeshPart 상한은 20,000):
  | 에셋 | 목표 |
  |---|---|
  | 컨테이너 1개 (PBR 고품질) | 2,500 이하 (현재 Container_40ft: 2,288) |
  | 소품 | 500 이하 |
  | 크레인 1기 (전체) | 15,000 이하, 부품당 5,000 이하 |
- 보이지 않는 면(바닥 밑면, 다른 물체에 묻힌 면)은 지웁니다.
- 같은 모양은 **한 번만 만들고 Studio에서 복제**합니다 (예: 컨테이너는 색만 다르게 복제). 같은 MeshId를 쓰면 메모리를 공유합니다.

## 6. 내보내기 전 점검 & FBX 내보내기

`scripts/blender_helpers.py`에 점검·내보내기 함수가 있습니다.
Blender MCP는 **안전 모드**라서 `exec`/`open`/`os`가 막혀 있습니다. 파일을 Blender에서 불러오지 말고, Read 도구로 파일 내용을 읽은 뒤 **`execute_blender_code` 스크립트 맨 위에 전체를 붙여 넣고** 그 아래에 호출을 적으세요.

```python
# ... blender_helpers.py 전체 내용 ...
print(check_asset("Container_40ft"))       # 컬렉션 이름
print(export_asset("Container_40ft"))      # → exports\Container_40ft.fbx
```

내보내기 폴더 `C:\Users\CafeAlle\Desktop\god\exports`는 Blender가 만들 수 없으니 없으면 셸에서 먼저 만드세요.

**안전 모드에서 막히는 것** (실제로 겪은 것들. 미리 피하면 재시도가 줄어듭니다):
- `exec`, `eval`, `open`, `os`, `time` 등 import 불가 → 시간 측정·파일 읽기는 셸(PowerShell)에서
- `lambda`, 함수를 인자로 넘겨 호출하기 불가 → 문자열 `kind`로 분기하는 일반 `def` 사용
- `setattr(obj, 이름변수, 값)` 불가 → 속성을 하나씩 직접 대입
- 허용: bpy 연산자(렌더, 굽기 `object.bake`, FBX 내보내기, `image.save()`), bmesh, mathutils
- 오래 걸리는 작업(1024 굽기 여러 장)을 한 번에 돌리면 MCP 연결이 끊깁니다. 굽기는 **호출 하나에 2~3장**씩 나누세요.

- 에셋 하나 = Blender **컬렉션** 하나 (컬렉션 이름 = 에셋 이름). 컬렉션 안의 메쉬만 내보냅니다.
- `check_asset`이 확인하는 것: 이름 규칙, 미적용 트랜스폼, 원점/바닥 위치, 오브젝트당 머티리얼 수, 삼각형 수, n-gon, 크기. 문제가 있으면 내보내기 전에 고치세요.
- FBX 설정 (`export_asset` 안에 들어 있음): 선택 메쉬만, `apply_unit_scale=True`, `apply_scale_options='FBX_SCALE_ALL'`, `axis_forward='-Z'`, `axis_up='Y'`, 모디파이어 적용, 삼각화, 리프 본 없음, `__TEX` 부품이 있으면 텍스처 포함.
- 내보낸 파일 위치: `C:\Users\CafeAlle\Desktop\god\exports\<에셋이름>.fbx`
- 내보낸 뒤 `look`의 angles 모드로 에셋을 여러 방향에서 찍어 사용자에게 보여주세요.

## 7. Studio로 가져오기

### 7-A. 자동 (기본, 2026-11-18부터) — Open Cloud 업로드 + insert_asset
사용자가 `exports` 폴더를 Studio **Assistant Settings → MCP Permissions → 업로드 허용 폴더**에 추가해 둠. 그래서 사용자에게 Import 3D를 부탁하지 않고 직접 가져옵니다.
1. Studio MCP `open_cloud_invoke`: `POST /assets/v1/assets`, scopes `["asset:read","asset:write"]`,
   body `{"request":{"assetType":"Model","displayName":"<에셋>","description":"...","creationContext":{"creator":{"groupId":"597081155"}}}}`,
   files `[{"name":"fileContent","path":"C:\\Users\\CafeAlle\\Desktop\\god\\exports\\<에셋>.fbx"}]` → **그룹 소유** 모델(텍스처 소유권 문제 없음).
2. `GET /assets/v1/operations/<id>`를 `done: true`가 될 때까지 (보통 15초) → `assetId`.
3. `insert_asset(assetId, assetType="Model")` → Workspace에 들어옴. **패키지로 들어오고 임의 위치·회전(예: Y -125°)으로 놓임** →
   `PackageLink` 삭제 후, 기준 MeshPart 하나의 원하는 CFrame(Blender 바운딩 중심을 매핑한 값, 회전 없음)으로
   `T = 원하는CF * ref.CFrame:Inverse(); model:PivotTo(T * model:GetPivot())`.
4. 그다음은 8장 후처리와 같음.

### 7-B. 수동 (폴더 허용이 없는 PC) — 사용자가 Import 3D

자동 업로드가 안 될 때만 이 단계를 사용자에게 부탁합니다. 매번 이 안내를 그대로 주세요.

1. Studio에서 **"도시"** 플레이스를 열고 `File → Import 3D` (또는 Avatar 탭 → Import 3D)
2. `exports\<에셋이름>.fbx` 선택
3. 가져오기 설정:
   - **File Dimensions: Studs** (9장 보정 결과에 다른 값이 적혀 있으면 그 값)
   - Anchored: 켜기
   - Insert in Workspace: 켜기, Insert Using Scene Position: 켜기
   - Import Only As Model: 켜기
4. `Import` 클릭 → 끝나면 "가져왔어" 라고 알려주기

## 8. 후처리 (Studio MCP)

사용자가 가져왔다고 하면 `scripts/studio_postimport.lua`의 내용을 읽어서 맨 아래의 `ASSET_NAME`(과 `__TEX` 에셋이면 `VARIANT` 색 변형)을 바꾼 뒤 Roblox Studio MCP의 `execute_luau`로 실행합니다 (studio_id는 `list_roblox_studios`에서 이름이 "도시"인 것).

이 스크립트가 하는 일:
- Workspace에서 가져온 모델을 찾아 이름 규칙대로 Color / Material / CanCollide / CastShadow 설정
- 상자형 부품에 투명 충돌 프록시 Part 생성, `__Hull`/`__Precise` 부품 목록은 사용자에게 수동 설정을 부탁하도록 출력
- 모든 파트 Anchored
- 모델 피벗을 바닥 중앙으로 맞춤
- 결과 크기·파트 수·삼각형 수를 출력
- `ServerStorage.Assets.CanalWarehouse`로 이동 (원본 보관용. 맵에는 여기서 복제해서 배치)

실행 후 출력된 크기를 Blender에서 만든 크기와 비교해 보고합니다. 다르면 9장 보정을 다시 확인하세요.

## 9. 보정 결과 (처음 한 번 측정 후 기록)

처음 파이프라인을 쓸 때 `make_calibration_cube()`로 48×12×12 상자(+X 쪽에 화살표 표시)를 만들어 위 과정을 그대로 거친 뒤, Studio에서 측정한 값을 여기 적습니다.

| 항목 | 값 |
|---|---|
| Studio에서 측정한 크기 | 48.00 × 12.00 × 12.00 (Blender와 정확히 일치) |
| 올바른 File Dimensions 설정 | **Studs** |
| Blender +Z (위) → Roblox | **+Y** (높이 그대로) |
| Blender +X (앞) → Roblox | **-X** (반대 방향으로 들어옴) |
| Blender +Y → Roblox | +Z (Y축 180° 회전으로 추정, 미측정) |
| 필요한 추가 회전 | 없음. Studio에서 "앞"은 -X라는 것만 기억하고 배치할 때 회전으로 맞추기 |
| 스크립트로 CollisionFidelity 변경 | **불가** (pcall은 성공하지만 값이 Default 그대로) → 5장의 충돌 프록시 방식 사용 |
| 측정 날짜 | 2026-11-17 |
