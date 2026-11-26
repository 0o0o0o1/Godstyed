# Godstyed — Roblox "도시" 존 제작 작업 폴더

Roblox Studio(MCP) + Blender(MCP)로 포스트 아포칼립스 맵 존을 만드는 작업 폴더.
여러 컴퓨터에서 이어서 작업하므로 이 저장소(https://github.com/0o0o0o1/Godstyed)가 기준이다.

## 시작할 때
1. `git pull` 로 최신 상태를 받는다.
2. 진행 중인 작업의 인수인계 문서를 먼저 읽는다: **`docs/zones/Factory_이어서할일.md`** (공장 place, 2026-11-18부터)
   (설계·결정은 `Factory_계획서.md`. 이전 운하 창고 존은 `Zone_CanalWarehouse_이어서할일.md` — 보류 중, 규칙 참고용)
3. Blender→Roblox 에셋 작업은 `.claude/skills/blender-to-roblox/` 규칙을 따른다. 공장 에셋 생성 함수(배관·트러스·타워·갤러리 등)는 `scripts/factory_kit.py` 를 Blender 세션마다 한 번 붙여 넣어 쓴다.

## 작업이 끝날 때마다 (필수)
- 한 단계(에셋 하나, 문서 수정 등)가 끝날 때마다 `docs/zones/..._이어서할일.md` 를 갱신하고
  **커밋 + `git push`** 한다. 다른 컴퓨터에서 바로 이어 할 수 있게 하기 위함.
- 커밋 메시지는 한국어로 짧게 (예: `쓰러진 크레인 에셋 추가, 인수인계 갱신`).
- `exports/` 의 FBX·PNG는 올리지 않는다(.gitignore). 텍스처 업로드 ID는 `exports/texture_ids.json` 에 기록해 올린다.
  다른 PC에서 원본 FBX/PNG가 필요하면 Blender에서 다시 굽거나 Studio의 `ServerStorage.Assets` 를 쓴다.

## Roblox 패키지 스크립트 수정 규칙 (2026-11-21 사용자 지시)
- 패키지 코드는 **마을 플레이스(Godstayed, 133122559439695)에서만** 수정하고, 게시는 사용자가 직접 한다.
- 수정은 `multi_edit` 으로 하고, 끝나면 `execute_luau` 로 Source 를 한 번 다시 써서(내용 + `"\n"` 후 원래 내용) 패키지 수정 표시를 띄운다.
- 그 스크립트 탭이 Studio 에 열려 있으면 Source 수정이 되돌아가고, "자동 업데이트 비활성화" 확인 창이 뜨면 Studio 가 응답하지 않으니 사용자에게 확인을 눌러 달라고 한다.
- 작업이 끝나면 게시할 패키지 이름을 알려 준다.
- **코드 실행 시 불러오기 (2026-11-27)**: 각 place 의 서버/클라 `Main`(원본 `scripts/start/ServerMain.lua`·`ClientMain.lua`)이 서버 시작 때 코드 패키지 최신 게시 버전을 `InsertService:LoadAsset` 으로 받는다 → 코드 수정은 **패키지 게시만** 하면 모든 place 의 새 서버에 반영 (place 재게시 불필요, 맵을 바꿀 때만 place 게시). Studio 에서는 받지 않음(시험: Main 속성 ForceLiveCode). 새 place 를 만들면 이 두 Main 을 넣는다.
- 공장 전용 코드도 패키지 안에 있다 (2026-11-21 옮김): Services `FactoryRaid`·`FactoryHazards` (Shared `PlaceConfig.SERVICE_PLACE` 로 공장에서만 시작), Controllers `FactoryCrateOutlineController`·`FactoryFireHudController`·`FactoryLightFXController` (init 에서 공장 place 가 아니면 바로 끝). 원본은 저장소 `scripts/packages/<패키지>/<이름>.lua` — 마을 place 에서 고친 뒤 이 파일도 같이 고친다.

## 폴더 구조
| 경로 | 내용 |
|---|---|
| `docs/zones/` | 존별 계획서 · 인수인계(이어서 할 일) |
| `.claude/skills/` | 프로젝트 스킬 (blender-to-roblox, roblox-*, level-design, find-skills, session-metrics, token-optimizer) + 외부 스킬 (2026-11-18 추가, MIT): roblox-performance (TabooHarmony/roblox-brain), roblox-world-building (EL4CTEO/roblox-skills), blender-game-optimization·blender-texture-baking·blender-hardsurface-modeling·blender-environment-kits (EL4CTEO/blender-skills). 외부 Blender 스킬의 `scripts/*.py`는 명령줄 Blender용이라 내용을 참고만 하고(실행하지 않음), 규칙은 blender-to-roblox가 우선. 스킬 작성용 (2026-11-23 추가, MIT): writing-for-agents (mattpocock/skills), writing-skills (obra/superpowers — 본문이 말하는 superpowers:test-driven-development 는 설치 안 함). 모델링·이펙트용 (2026-11-24 추가, MIT): reference-modeling·game-asset-modeling (colinurbs/claude-modeling-skills — 스크립트 경로는 `D:\god\.claude\skills
eference-modeling\scripts`, game-asset-modeling 의 glTF/Babylon 기준은 참고만, Roblox 규칙은 blender-to-roblox 우선), blender-modeling (roble3/cc-blender-skill, 공용 참고 `text-to-blender/references/mcp-backends.md` 같이 복사), roblox-animation-vfx (TabooHarmony/roblox-brain), roblox-vfx (nonlooped/roblox-suite) |
| `scripts/` | 몬스터 등 에셋 생성 스크립트. **Blender MCP 안전 모드는 2026-11-20부터 끔** → `exec(open(r"<저장소>\scripts\...py", encoding="utf-8").read())` 한 줄로 실행 (붙여 넣기 금지, 비용 절약) |
| `exports/` | Blender 내보내기 결과 (texture_ids.json만 저장소에 포함) |
| `.mcp.json` | Blender MCP 서버 설정 (uvx 필요) |

## 사용자 선호
- 한국어로 보고, 단계마다 결정 질문 → 작업 → 보고. **보고용 Studio 스크린샷은 찍지 않음** (2026-11-18 사용자 지시). 텍스처 로드 등 문제가 의심될 때만 확인용으로 찍음.
- 품질 기준: "무조건 높은 퀄리티".
