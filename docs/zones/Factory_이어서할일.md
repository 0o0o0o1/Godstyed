# 공장맵 — 이어서 할 일 (인수인계)

> 마지막 작업: 2026-11-18 · **용광로(A) 실제 에셋 완료** (Studio "공장" 저장 버전 10)
> 설계·구역·결정: `Factory_계획서.md`. 에셋 규칙: `.claude/skills/blender-to-roblox/`.

## 0. 꼭 알아야 할 것

1. 작업 place = **"공장"** (placeId 129022811153240, 같은 universe 10768843846). Studio MCP `list_roblox_studios`에서 이름 "공장".
2. 이 place는 도시 place 복사본 → 운하 창고 존·에셋 원본(`ServerStorage.Assets.CanalWarehouse`)·게임 스크립트가 다 들어 있음. **지우지 않고** 그 위에 공장 시설을 더함.
3. 운하 창고 존 규칙(그룹 소유 업로드, 축 매핑, CollisionFidelity 불가 → 투명 충돌, CorrodedMetal 분홍 문제, 보이는 수면 Y ≈ -1.75)은 `Zone_CanalWarehouse_이어서할일.md` 0장과 동일하게 적용.
4. 단계마다: 사용자에게 결정 질문 → 작업 → 한국어 보고 + 스크린샷 → 이 문서 갱신 → 커밋·푸시.
5. **사용자 지시 (2026-11-18)**
   - 배치 수정(도로·나무·옛 LotDressing 손보기 포함)은 **알아서 결정**해도 됨. 목표는 맵 전체가 잘 어우러지는 것.
   - **Blender에서 부재끼리 겹치게(뚫고 나오게) 만들지 말 것** — Roblox에서는 못 고침. 지붕 밑 서까래가 지붕판을 뚫는 식의 실수 금지.
     → 만든 뒤 반드시 BVHTree `overlap` 검사(오브젝트 쌍별)로 확인하고, 접합부(파이프→밸브/탱크, 바닥 위 기둥)만 남길 것. 지붕·벽은 "부재 꼭짓점이 지붕 밑면/벽 안쪽면을 넘는지" 수치 검사.
6. **대각선 길 방향 주의**: 대각선 길(A 구역을 나누는 길)은 **X − Z ≈ −1811** 선을 따라 남서→북동으로 남. 길 양옆 보도 포함 폭 약 ±25. (이전 문서의 "x+z=0"은 삼각 부지의 대칭축이었고 길이 아님.) 남동쪽 삼각 부지 = `Lot_026` (꼭짓점 ≈ (-1015,739), (-739,739), (-739,1015)).
7. **텍스처 업로드 함정**: Open Cloud로 올린 이미지는 심의(Approved) 전에 SurfaceAppearance에 붙이면 Studio가 그 ID를 "실패"로 캐시해서 다시 붙여도 하얗게 나옴. 같은 파일을 다시 올리면 기존 ID로 합쳐짐 → **픽셀 1개 바꿔 재업로드**해야 새 ID가 나옴. 붙이기 전에 `GET /assets/v1/assets/<이미지ID>` 의 `moderationState: Approved` 확인할 것. (`PreloadAsync`는 편집 모드에서 정상 이미지도 Failure로 나와서 판단 기준으로 못 씀 → 화면으로 확인)
8. **플레이 테스트**: 이 게임은 스폰 위치가 없고 스크립트가 플레이어를 옮김 → 플레이어 캐릭터로 테스트하면 엉뚱한 데로 감. 서버에서 `Players:CreateHumanoidModelFromDescription`으로 **NPC를 만들어** `MoveTo` 경로 테스트. Pathfinding은 좁은 계단(폭 5.5)에서 NoPath가 나와 신뢰 불가.

## 1. 현재 상태

- 계획서 + 미리보기 이미지(`images/Factory_preview_*.png`).
- 블록아웃 `Workspace.FactoryBlockout` (구역 B~H, K_Common). **A_BlastFurnace 블록아웃은 삭제**(옛 위치 백업: `ServerStorage.A_BlastFurnace_OldBlockout`).
- `C_RawYard.Conveyor_ToFurnace2` 블록아웃 끝을 새 장입 피트 쪽 (-764, 18, 886)으로 옮김.

### 용광로 `BlastFurnace` — 2026-11-18 완성
- 위치: `Workspace.FactoryContent.A_BlastFurnace.BlastFurnace_01`, 원본 `ServerStorage.Assets.Factory.BlastFurnace`. 그룹 소유 모델 assetId **119067813161619**.
- **배치 변경**: 원래 블록아웃(용광로 (-800,950))은 열풍로 3·4번이 대각선 길·보도 위였음 → 단지 전체를 남동 삼각 부지(Lot_026)로 옮김. 용광로 중심 **(-828.43, 0.5, 814.29)**.
- **좌표계**: 모델 속성 `BlenderFrame` (CFrame) = `fromMatrix(F, -eu, Y, ed)`, eu=(1,0,1)/√2(길 방향), ed=(1,0,-1)/√2(길에서 부지 안쪽). Blender 점 (x,y,z) → 월드 `BlenderFrame * Vector3.new(-x, z, y)`. 즉 Blender x = 길을 따라, y = 부지 안쪽, z = 위(지면 0 = Y 0.5).
- 구성 (Blender 좌표): 노체(높이 94, 노정 설비 상승관·블리더 ~127) + 환상관·풍구 16 / 철골탑 56×56 (작업대 z 62 원형 데크, 꼭대기 z 90 데크) / 열풍로 4기 (y −66, x −60·−34·−8·18, 높이 73) + 열풍 본관·냉풍 본관 / 집진기 (−74, −4) + 하강관 / 출선장 (x ±36, y 30..64, 처마 22·용마루 28.5, 지붕 구멍) 내부: 주상 바닥 높이 8 (계단 2곳), 주선(굳은 쇳물)·슬래그 주선·머드건·개공기, 천장 크레인, 래들카(토페도카) 선로 y 58 / 계단탑 (x −50..−38, y 8..22, 10구간) → 다리 → 62 작업대 / 스킵 경사로 (피트 하우스 x 90..108 → 노정) + A형 받침.
- 메쉬 37개, 삼각형 32,288. 모든 메쉬 `__NoCollide`, 충돌은 `BlastFurnace_01/Colliders` (투명 Part/원통 약 205개).
- 텍스처(그룹 소유, `exports/texture_ids.json`): **BfPlate** 리벳 철판 타일(16스터드/타일, FurnaceRust·StoveGrey, v2 ID), **BfSteel** 도장 강재 타일(8스터드/타일, SteelOxide·RailYellow), 출선장 벽·지붕은 기존 **WhSiding RoofZinc** 재사용. 원본 PNG `exports/textures/`(저장소 제외).
- 등반: 계단탑으로 **62 작업대까지만**. 꼭대기 90·스킵 경사로는 도달 불가(경로 테스트 NoPath, 점프로도 불가 높이).
- 플레이 확인(NPC): 지면 → 계단 10구간 → 다리 → 62 데크 한 바퀴 이동 OK. 출선장 바닥(계단)·래들카 구역 경로 Success.
- Blender: 씬 **FurnaceWork**, 컬렉션 `BlastFurnace`(에셋), `BF_TexBake`(굽기 판 + 머티리얼 `BAKE_BfPlate`/`BAKE_BfSteel`). **.blend 파일 저장 안 됨** → 다시 굽거나 고치려면 같은 PC의 열린 Blender가 필요(없으면 Studio 원본 사용).

## 2. 다음 할 일

1. 사용자 확인 → 수정.
2. 냉각탑(E) Blender 제작 (계획서 6장 순서: 용광로 ✔ → 냉각탑 → 압연 공장동 → 코크스로). 같은 BfPlate/BfSteel/WhSiding 텍스처 세트 재사용 가능.
3. 대각선 길 북서쪽 삼각 부지(Lot_025 쪽)는 비어 있음 → 가스 정제·펌프 시설 등으로 채울 것.
4. `K_Common.Chimney_A` (-760, 760) 블록아웃은 출선장 옆에 있음 — 굴뚝 에셋 만들 때 위치 재검토.
5. 옛 LotDressing(공원 나무·주차 차량) 정리 → 산업 부지 바닥 마감 (사용자가 알아서 정리해도 된다고 함).
