# Godstyed — Roblox "도시" 존 제작 작업 폴더

Roblox Studio(MCP) + Blender(MCP)로 포스트 아포칼립스 맵 존을 만드는 작업 폴더.
여러 컴퓨터에서 이어서 작업하므로 이 저장소(https://github.com/0o0o0o1/Godstyed)가 기준이다.

## 시작할 때
1. `git pull` 로 최신 상태를 받는다.
2. 진행 중인 존의 인수인계 문서를 먼저 읽는다: `docs/zones/Zone_CanalWarehouse_이어서할일.md`
   (설계·좌표·결정은 같은 폴더의 `..._계획서.md`)
3. Blender→Roblox 에셋 작업은 `.claude/skills/blender-to-roblox/` 규칙을 따른다.

## 작업이 끝날 때마다 (필수)
- 한 단계(에셋 하나, 문서 수정 등)가 끝날 때마다 `docs/zones/..._이어서할일.md` 를 갱신하고
  **커밋 + `git push`** 한다. 다른 컴퓨터에서 바로 이어 할 수 있게 하기 위함.
- 커밋 메시지는 한국어로 짧게 (예: `쓰러진 크레인 에셋 추가, 인수인계 갱신`).
- `exports/` 의 FBX·PNG는 올리지 않는다(.gitignore). 텍스처 업로드 ID는 `exports/texture_ids.json` 에 기록해 올린다.
  다른 PC에서 원본 FBX/PNG가 필요하면 Blender에서 다시 굽거나 Studio의 `ServerStorage.Assets` 를 쓴다.

## 폴더 구조
| 경로 | 내용 |
|---|---|
| `docs/zones/` | 존별 계획서 · 인수인계(이어서 할 일) |
| `.claude/skills/` | 프로젝트 스킬 (blender-to-roblox, roblox-*, level-design, find-skills, session-metrics, token-optimizer) |
| `exports/` | Blender 내보내기 결과 (texture_ids.json만 저장소에 포함) |
| `.mcp.json` | Blender MCP 서버 설정 (uvx 필요) |

## 사용자 선호
- 한국어로 보고, 단계마다 결정 질문 → 작업 → 보고 + Studio 스크린샷.
- 품질 기준: "무조건 높은 퀄리티".
