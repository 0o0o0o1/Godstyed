# Godstyed

Roblox 플레이스 **"도시"** 의 포스트 아포칼립스 존을 Roblox Studio + Blender(둘 다 MCP)로 만드는 작업 저장소.
Claude Code로 작업하며, 어느 컴퓨터에서든 이 저장소를 받아 이어서 작업한다.

## 구조

```
Godstyed/
├─ CLAUDE.md                 Claude Code 작업 규칙 (시작/종료 시 할 일)
├─ README.md
├─ .mcp.json                 Blender MCP 서버 설정
├─ docs/
│  └─ zones/
│     ├─ Zone_CanalWarehouse_계획서.md      설계·좌표·결정 기록
│     └─ Zone_CanalWarehouse_이어서할일.md  현재 상태 + 남은 작업 (인수인계)
├─ .claude/skills/           프로젝트 스킬
│  ├─ blender-to-roblox/     Blender→Roblox 에셋 파이프라인 (스케일·FBX·PBR·Studio 후처리 스크립트)
│  ├─ roblox-building/  roblox-lighting/  roblox-studio-mcp/  level-design/
│  └─ find-skills/  session-metrics/  token-optimizer/
└─ exports/
   └─ texture_ids.json       그룹 소유 텍스처 ID (FBX·PNG는 저장소에 넣지 않음)
```

## 새 컴퓨터에서 시작하기

1. Git 설치 후 받기
   ```bash
   git clone https://github.com/0o0o0o1/Godstyed.git
   ```
2. [uv](https://docs.astral.sh/uv/) 설치 (`.mcp.json` 의 Blender MCP가 `uvx` 로 실행됨)
3. Blender에 MCP 애드온 설치 후 서버 시작: `uvx mcp-for-blender install-addon`
4. Roblox Studio에서 Studio MCP 켜고 "도시" 플레이스 열기
5. 이 폴더에서 Claude Code 실행 → "이어서 해줘"

작업 하나가 끝날 때마다 인수인계 문서를 갱신하고 커밋·푸시한다 (`CLAUDE.md` 참고).
