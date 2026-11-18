# 공장맵 — 이어서 할 일 (인수인계)

> 마지막 작업: 2026-11-18 · 계획서 작성까지 (Studio 변경 없음)
> 설계·구역·결정: `Factory_계획서.md`. 에셋 규칙: `.claude/skills/blender-to-roblox/`.

## 0. 꼭 알아야 할 것

1. 작업 place = **"공장"** (placeId 129022811153240, 같은 universe 10768843846). Studio MCP `list_roblox_studios`에서 이름 "공장".
2. 이 place는 도시 place 복사본 → 운하 창고 존·에셋 원본(`ServerStorage.Assets.CanalWarehouse`)·게임 스크립트가 다 들어 있음. **지우지 않고** 그 위에 공장 시설을 더함.
3. 운하 창고 존 규칙(그룹 소유 업로드, 축 매핑, CollisionFidelity 불가 → 투명 충돌, CorrodedMetal 분홍 문제, 보이는 수면 Y ≈ -1.75)은 `Zone_CanalWarehouse_이어서할일.md` 0장과 동일하게 적용.
4. 단계마다: 사용자에게 결정 질문 → 작업 → 한국어 보고 + 스크린샷 → 이 문서 갱신 → 커밋·푸시.

## 1. 현재 상태

- 계획서 완료 (중공업 단지, 공원·주차장 → 산업 부지, 계획서 → 블록아웃 → 랜드마크 순).
- Studio: 아직 아무것도 안 바꿈.

## 2. 다음 할 일

1. **블록아웃** (`Workspace.FactoryBlockout`): 계획서 3장 구역 A~H + 공통 배관 다리·굴뚝을 색 상자로. 전에 `Zone_Apartments` 처리 질문.
2. 위에서 본 스크린샷으로 사용자 확인.
3. 용광로(A) Blender 제작부터.
