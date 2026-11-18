# 공장맵 — 이어서 할 일 (인수인계)

> 마지막 작업: 2026-11-18 · 블록아웃 완료 (Studio "공장" 저장 버전 5)
> 설계·구역·결정: `Factory_계획서.md`. 에셋 규칙: `.claude/skills/blender-to-roblox/`.

## 0. 꼭 알아야 할 것

1. 작업 place = **"공장"** (placeId 129022811153240, 같은 universe 10768843846). Studio MCP `list_roblox_studios`에서 이름 "공장".
2. 이 place는 도시 place 복사본 → 운하 창고 존·에셋 원본(`ServerStorage.Assets.CanalWarehouse`)·게임 스크립트가 다 들어 있음. **지우지 않고** 그 위에 공장 시설을 더함.
3. 운하 창고 존 규칙(그룹 소유 업로드, 축 매핑, CollisionFidelity 불가 → 투명 충돌, CorrodedMetal 분홍 문제, 보이는 수면 Y ≈ -1.75)은 `Zone_CanalWarehouse_이어서할일.md` 0장과 동일하게 적용.
4. 단계마다: 사용자에게 결정 질문 → 작업 → 한국어 보고 + 스크린샷 → 이 문서 갱신 → 커밋·푸시.

## 1. 현재 상태

- 계획서 완료 + 미리보기 이미지(`images/Factory_preview_*.png`).
- **블록아웃 완료 (2026-11-18)**: `Workspace.FactoryBlockout` (BasePart 약 164, SmoothPlastic 색 상자 + 구역 이름 BillboardGui `Label`). 폴더: `A_BlastFurnace`, `B_CokeOvens`, `C_RawYard`, `D_RollingMill`, `E_PowerPlant`, `F_GasHolder`, `F2_Weighbridge`, `G_SouthStrip`, `H_PipeRack`, `K_Common`(배관 다리 3, 굴뚝 2).
  - **용광로 중심 = (-800, 950)** (계획서의 -860,860에서 옮김: 대각선 길 x+z=0 위에 놓여 있었음). 열풍로 4기 (-844, 874..964), 장입 경사 컨베이어 피트 (-760, 1005), 출선장·집진기 동쪽. 대각선 길·연석과 겹침 없음.
  - 코크스로 배터리는 Spawn1 (-1200,1000)을 피하려고 Z 765..965로 줄임. 슬래그 더미는 Exit4 (-1220,400)에서 40 이상 떨어뜨림. 최근접 거리: Spawn1 34, Spawn2 22, Exit4 40.
  - 도로·운하·운하 창고 존과 겹침 없음. **겹치는 것은 옛 `LotDressing` 뿐** (Lot_057·053 공원 나무, Lot_037 주차 차량, Lot_023·043·011 잔해) → 바닥 마감 단계에서 치울지 사용자에게 물어볼 것.
  - `Zones/Zone_Apartments`는 손대지 않음 (사용자가 스크립트 확인을 원하지 않아 보류).
- Studio "공장" 저장 버전 **5**.

## 2. 다음 할 일

1. 사용자 블록아웃 확인 → 수정.
2. 용광로(A) Blender 제작 (계획서 6장 순서: 용광로 → 냉각탑 → 압연 공장동 → 코크스로).
3. 옛 LotDressing(공원 나무·주차 차량) 정리 여부 결정 → 산업 부지 바닥 마감.
