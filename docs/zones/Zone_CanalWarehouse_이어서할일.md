# Zone_CanalWarehouse — 이어서 할 일 (인수인계)

> 마지막 작업: 2026-11-18 · Studio 저장 버전 **69** (게시 안 함)
> 자세한 설계·결정·좌표는 같은 폴더의 `Zone_CanalWarehouse_계획서.md` (특히 9장 결정 결과, 9.5~9.7 결과 기록)
> 파이프라인 규칙은 `.claude/skills/blender-to-roblox/` (`SKILL.md`, `references/pbr_pipeline.md`, `scripts/`)

---

## 0. 꼭 알아야 할 규칙 (어기면 다시 해야 함)

1. **게임은 그룹 소유**(Group 597081155). 텍스처를 Studio MCP `upload_image`로 올리면 개인 소유라 안 보임.
   → 텍스처마다 2×2 판의 Base Color에 이미지를 연결한 **견본 FBX**(`TexUpload_<에셋>.fbx`, `path_mode='COPY', embed_textures=True`)를 만들고,
   사용자가 Import 3D → 각 `TexSwatch*` MeshPart의 `TextureID`를 읽음 → `GetProductInfo`로 Creator=Group 확인 → `exports/texture_ids.json`과 `studio_postimport.lua`의 `TEXTURES`에 기록.
2. **Import 3D 설정**(사용자가 직접): File Dimensions = **Studs**, Anchored 켜기, Insert in Workspace + Insert Using Scene Position 켜기, Import Only As Model 켜기.
3. **축**: Blender +X → Roblox **-X**, Blender +Y → Roblox +Z, Blender +Z → Roblox +Y. 1 Blender unit = 1 stud.
   가져온 모델에서 Blender 점 (x,y,z) = 모델 로컬 (-x, z, y). 모델을 `CFrame.Angles(0, π/2, 0)`로 돌리면 Blender x → Roblox +Z.
4. **MeshPart CollisionFidelity는 스크립트로 못 바꿈** → 메쉬는 `__NoCollide`, 충돌은 투명 Part로 따로. 사다리는 투명 **TrussPart**.
5. **Blender MCP 안전 모드**: `exec/open/os/time/__import__`, `class` 정의, 람다/함수 인자, 계산된 이름 `setattr` 금지. 굽기는 호출 하나에 2~3장.
   에셋 FBX는 이미지 노드 없는 단순 머티리얼(`MX_Plain_<키>`)로 잠깐 바꿔서 내보냄.
6. **이름 규칙**: `<세트>_<부품>__<팔레트키>[__NoCollide][__TEX]`. 팔레트 표는 `SKILL.md` 4장(+ SidingTeal, RoofZinc, ShutterOrange, SteelBlue).
7. **실명 브랜드·실제 게임 재현 금지**. 회사명은 가상(현재 컨테이너: KESTREL LINES).
8. 사용자는 **단계마다 질문(결정) → 작업 → 한국어 보고 + Studio 스크린샷**을 원함. 품질 기준: "무조건 높은 퀄리티".
9. 스크린샷 찍을 때 `Workspace.Zones`의 존 볼륨(투명도 0.85)이 화면을 덮으므로 잠깐 Transparency=1 → 끝나면 원래 값으로 복구.
10. **STS 안벽 크레인은 다른 세션 담당**. `Crane_STS_01`(-220, 0, 603) 모델은 건드리지 말 것. 다리 주변 X -250..-190, Z 595..660 비워 두기.
11. **GitHub 동기화**: 작업 폴더 = 저장소 `0o0o0o1/Godstyed`. 단계가 끝날 때마다 이 문서 갱신 → 커밋 → `git push` (다른 PC에서 이어 하기 위함). `exports/`의 FBX·PNG는 올리지 않음(texture_ids.json만).

## 1. 현재 상태 (Studio "도시", placeId 76001235376585)

| 경로 | 내용 |
|---|---|
| `Workspace.ZoneContent.Zone_CanalWarehouse` | 존 콘텐츠 루트 (현재 BasePart 508개, 목표 신규 ≤ 3,500) |
| `.Blockout` | 남은 회색 블록아웃: RTG, 쓰러진 크레인(붐·잔해), 리치스태커, 트럭, 감시탑·연료탱크·정비고, 부두 사무소, 오두막, 골목 엄폐물, 창고 랙·잔해 계단·앞마당, 운하 얕은 바닥·경사로·바지선·폰툰, 상자 발판, STS 등반 마커 |
| `.A_CraneQuay` | `Crane_STS_01`(다른 세션), `Containers` |
| `.B_ContainerYard/Yard_South`, `Yard_North` | 실제 컨테이너 (속성 `Variant`, `BlockoutSource`, 열린 것은 `Open=true` 6개) |
| `.C_Warehouse_Main/Warehouse_Main` | **완성** 메인 창고 (13 MeshPart + 충돌 69 + 사다리 Truss) |
| `.E_Canal/Containers` | 운하 속 컨테이너 2개 |
| `ServerStorage.Assets.CanalWarehouse` | 원본: `Container_40ft`, `Container_20ft`, `Crane_STS`, `Warehouse_Main` |

결정 사항: STS만 등반 가능 / 운하 얕은 물(바닥 Y -4.5, 물 표면 ≈ -2.8, 다리 밑은 깊음) / 좀비·NPC 있음(통로 16~20, 막다른 길 최소화) / 열쇠 시스템 없음 / 존 전용 탈출 없음.

## 2. 남은 작업 (순서대로, 각 단계 전에 사용자에게 결정 질문)

### 4단계 나머지 — 에셋 (blender-to-roblox 파이프라인)

**쓰러진 크레인 `Crane_Collapsed` — 2026-11-18 제작 (STS형 박스 거더)**
- Blender 컬렉션 `Crane_Collapsed` (메쉬 10, 삼각형 7,006), FBX `exports/Crane_Collapsed.fbx`. 월드 좌표 그대로 모델링: Blender (x,y,z) ↔ Roblox (-513 - x, z, 902 + y) → Studio에서 모델 `PivotTo(CFrame.new(-513, 0, 902))`(가져온 직후 피벗 = Blender 원점).
- 붐 = 블록아웃 `Boom_Walkway` CFrame 그대로(서 (-622,4,908) → 동 (-404,28,896), 롤 약 5°). 거더 s ±4.5..8, w -6.2..+2 (w=0 = 걷는 바닥), 운하 서벽 위 u≈44에서 휨, 끝은 찢김. 트롤리+운전실이 u=150 아래 운하 위에 매달림. 서쪽 잔해: 쓰러진 다리·휜 다리(+바퀴)·받침 빔·기계실·윈치 드럼·지지봉·콘크리트.
- 텍스처: `CraneSTS` 타일 세트 재사용(`TEXTURES.CraneCol = TEXTURES.CraneSTS`), 새 업로드 없음. 모든 메쉬 `__NoCollide`, 큰 메쉬는 CastShadow 다시 켬.
- 충돌: `Crane_Collapsed_01/Colliders` = 붐 바닥(9×6×219.6) + 거더 2(3.5×8.2) + 블록아웃 4개(Base_Frame, Leg_Fallen, Leg_Bent, MachineHouse_Wreck) 위치 그대로.
- 위치: `A_CraneQuay/Crane_Collapsed_01`, 원본 `ServerStorage.Assets.CanalWarehouse.Crane_Collapsed`. 블록아웃 `A_CollapsedCrane` 삭제.
- ⚠ 배치 직후 Studio MCP 연결이 끊김 → **Studio 저장(버전 70) 여부 확인 필요**, 플레이 테스트(붐 위 걷기, 창고 잔해 계단 → 붐 끝) 아직 안 함. `Workspace.Zones` 투명도를 1로 바꿔 둔 상태일 수 있음(속성 `_SavedTransparency`로 복구).

다음 추천 에셋: RTG.

| 에셋 | 블록아웃 위치 / 크기 | 메모 |
|---|---|---|
| **쓰러진 크레인** `Crane_Collapsed` | 붐: (-622, 4, 908) → (-404, 28, 896), 폭 8, **위를 걸어 다니는 경사로**(약 6°). 받침 잔해는 Lot_040 (-632, 905) 부근 | 붐 윗면 = 걷는 길(충돌 상자 1개로 유지). 기존 `Crane_STS` 텍스처(CraneYellow 타일, `CraneSTS` 세트) 재사용 가능. 붐 옆에 매달린 컨테이너(현재 실제 컨테이너 모델) 유지 |
| **RTG 갠트리** `Crane_RTG` | 다리 X -172/-128 × Z 926/980, 상부 Y ≈ 50, 블록 S2(행 941~965) 위를 걸침 | 등반 불가. 다리는 통로 안. 타이어 바퀴 |
| **리치스태커** | (-120, 790) 본체 30×12×14, 붐이 컨테이너(-165, 18.5, 790)를 들고 정지 | 소품급 PBR 또는 색+재질 |
| **바지선** | 운하 (-95, ≈-3.3, 538), 80×8×24, 기울어짐 + 컨테이너 | 반쯤 가라앉음 |
| **문 열린 컨테이너** `Container_40ft_Open` | — | `Open=true` 6개 교체, 내부 진입 + 루트 지점 |
| **소품** | — | 팔레트 랙(창고 랙 4줄 교체), 잔해 더미(창고 내부 잔해 계단 교체: 바닥→붐 끝까지 6 높이 단위), 드럼통, 팔레트, 모래주머니, 철조망, 볼라드, 타이어 펜더, 연료탱크, 감시탑, 정비고, 부두 사무소, 텐트, 방수포, 경고 표지판, 꺼진 가로등, 트럭+샤시 |

### 5단계 — 아포칼립스 디테일
- 컨테이너 위 생존자 캠프: `Yard_North`의 2단 스택(-200, 790, 위면 Y 24.5), 기댄 컨테이너 경사로로 올라감
- 바리케이드(메인도로 쪽 컨테이너 벽 + 모래주머니 + 철조망), 잔해, 운하 부유물·기름막
- 낙서(Decal): "NO SHIP COMING", 날짜 카운트(////), 창고 벽 구호물자 배급 안내판
- 운하 얕은 바닥 Part(`Blockout/E_Canal/ShallowFloor`)를 진흙/잔해 느낌으로 마감 후 Blockout 밖으로 이동

### 6단계 — 조명·분위기
- 흐림, 옅은 안개, 녹 톤. **Lighting은 도시 전체 공용** → 반드시 사용자에게 먼저 물어볼 것 (플레이 중 게임 자체 조명 스크립트가 따뜻한 톤으로 바꾸는 것 확인됨 → 그 스크립트부터 확인)
- 창고 내부 빛줄기, 깜빡이는 작업등 (`roblox-lighting` 스킬)

### 7단계 — 게임플레이 태그
- CollectionService `LootSpawn` (열린 컨테이너 내부 8~12, 창고 랙, 창고 2층 사무실, STS 운전실 = 고급)
- 등반 지점 `ClimbPoint` (창고 사다리 TrussPart에 속성만 있음 → 태그로), STS 사다리(다른 세션과 맞춤)
- 운하 "물속 느림": 실제로 느려지는지 플레이로 재확인 (서버 측정이 들쭉날쭉했음). 안 느리면 WalkSpeed 조절 영역 필요
- NPC용: 운하 경사로 4곳 난간은 이미 잘라 둠

### 8단계 — 테스트·최적화
- 신규 파트 ≤ 3,500, StreamingEnabled 확인(크레인 `ModelStreamingMode` 검토), 끼임·빠짐(운하 벽, 바지선 주변), 장식 파트 CanCollide/CastShadow off
- PathfindingService(반경 2, 높이 5, 점프 허용)로 메인도로 → 주요 지점 경로 재확인

## 3. 주의 / 미해결
- **Blender 파일이 저장된 적 없음**(공유 Blender, STS 세션과 함께 사용). 작업용 셰이더 `MW_Siding_Bake`, `MW_Steel_Bake`, 컬렉션 `Warehouse_Main`, `Warehouse_WORK`가 메모리에만 있음. 구운 PNG/FBX는 `exports/`에 있음.
- STS 등반 루트: 파란 마커 `ClimbMarker_STS_Ladder1` (Leg2 안쪽 (-236.2, Y 0.5~61.5, 602)), `Ladder2` (-214, 61.5~88, 604.6). STS 세션이 실제 사다리를 넣어야 함.
- 창고 지붕 충돌은 구멍 마스크 문자열로 만든 경사 판(`Warehouse_Main/Colliders/Roof`). 지붕 메쉬를 다시 만들면 마스크도 다시 뽑을 것(Blender `random.seed(11)`).
