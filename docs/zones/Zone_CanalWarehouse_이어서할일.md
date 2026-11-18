# Zone_CanalWarehouse — 이어서 할 일 (인수인계)

> **2026-11-18 방향 전환**: 도시 맵이 너무 커서 사용자가 새 place **"공장"**(placeId 129022811153240)을 도시 복사본으로 만들고, 맵 전체를 중공업 단지로 바꾸기로 함 → `Factory_계획서.md`, `Factory_이어서할일.md`. 이 존은 5단계까지 완성된 채 **보류**(7단계 태그부터 미진행). 공장 place 안에도 같은 존이 그대로 들어 있음.

> 마지막 작업: 2026-11-18 · Studio 저장 버전 **98** (게시 안 함) · 큰 에셋 전부 + 소품 묶음 1(창고 내부)·2(서쪽 강변)·3(크레인 부두) 완료 · FBX는 이제 자동 업로드(SKILL 7-A)
> 자세한 설계·결정·좌표는 같은 폴더의 `Zone_CanalWarehouse_계획서.md` (특히 9장 결정 결과, 9.5~9.7 결과 기록)
> 파이프라인 규칙은 `.claude/skills/blender-to-roblox/` (`SKILL.md`, `references/pbr_pipeline.md`, `scripts/`)

---

## 0. 꼭 알아야 할 규칙 (어기면 다시 해야 함)

1. **게임은 그룹 소유**(Group 597081155). 텍스처를 Studio MCP `upload_image`로 올리면 개인 소유라 안 보임.
   → 텍스처마다 2×2 판의 Base Color에 이미지를 연결한 **견본 FBX**(`TexUpload_<에셋>.fbx`, `path_mode='COPY', embed_textures=True`)를 만들고,
   사용자가 Import 3D → 각 `TexSwatch*` MeshPart의 `TextureID`를 읽음 → `GetProductInfo`로 Creator=Group 확인 → `exports/texture_ids.json`과 `studio_postimport.lua`의 `TEXTURES`에 기록.
2. **가져오기**: 기본은 자동(Open Cloud 업로드 + `insert_asset`, SKILL 7-A). 다른 PC에서 업로드 폴더 허용이 없으면 사용자가 Import 3D — 설정: File Dimensions = **Studs**, Anchored 켜기, Insert in Workspace + Insert Using Scene Position 켜기, Import Only As Model 켜기.
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

> 2026-11-18: 현재 Studio에 열리는 place 이름은 **'신이 머물렀다'**(placeId 133122559439695, universeId 10768843846). 사용자 확인 결과 "도시"와 **같은 게임** → 이 place에서 작업.

| 경로 | 내용 |
|---|---|
| `Workspace.ZoneContent.Zone_CanalWarehouse` | 존 콘텐츠 루트 (현재 BasePart 508개, 목표 신규 ≤ 3,500) |
| `.Blockout` | 남은 회색 블록아웃: RTG, 쓰러진 크레인(붐·잔해), 리치스태커, 트럭, 감시탑·연료탱크·정비고, 부두 사무소, 오두막, 골목 엄폐물, 창고 랙·잔해 계단·앞마당, 운하 얕은 바닥·경사로·바지선·폰툰, 상자 발판, STS 등반 마커 |
| `.A_CraneQuay` | `Crane_STS_01`(다른 세션), `Crane_Collapsed_01`(완성), `Containers` |
| `.B_ContainerYard/Crane_RTG_01` | **완성** RTG 갠트리 |
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
- 플레이 확인: 서쪽 끝 → 붐 끝(u 200)까지 걸어서 이동 OK. 창고 잔해 계단 맨 위(24)에서 붐까지는 남쪽 거더 윗면(≈31.8)이 너무 높아 못 올라가서 **잔해 계단 5번째 단 추가**(`Blockout/C_Warehouse/RubbleStep`, 7×30×7 @ (-416.5, 15, 909.2), 위면 30) → 바닥 → 계단 → 거더 → 붐 바닥 경로 확인. 소품 단계에서 잔해 더미로 교체할 때 이 높이(6/12/18/24/30) 유지.
- Studio 저장 버전 **83** (Team Create, 다른 세션 저장 포함). 존 BasePart 521.

**RTG 갠트리 `Crane_RTG` — 2026-11-18 제작**
- Blender 컬렉션 `Crane_RTG` (메쉬 7, 삼각형 4,560), FBX `exports/Crane_RTG.fbx`. 매핑: Blender (x,y,z) ↔ Roblox (-150 - x, z, 953 + y) → `PivotTo(CFrame.new(-150, 0, 953))`.
- 다리 4개 (X -172/-128 × Z 926/980, 통로 안), 높이 ~55 (트롤리 위 62). 고무 타이어 16개(1개 펑크), 바퀴 받침, 하부 빔은 **X 방향(통로를 따라)**으로 고침(블록아웃은 컨테이너를 관통했음) → 빔 양옆 약 7씩 통로 남음. 발전기실(남쪽), 트롤리+기계실, 운전실(유리), 스프레더, 상부 통로 난간, 부러진 무릎 버팀대, 늘어진 케이블, 떨어진 문짝.
- **등반 불가 유지**: 스프레더 바닥 Y 44.6 (3단 위면 36.5에서 +8.1 > 점프 7.2). 플레이 테스트에서 3단 위 점프 최고 발 높이 ≈ 40 확인. 상부 버팀대는 충돌 없음.
- 충돌: `Crane_RTG_01/Colliders` (다리 4, 바퀴 받침 4, 하부 빔 2, 상부 빔 4, 발전기실, 트롤리, 운전실, 스프레더). 컨테이너와 겹침 없음.
- 위치: `B_ContainerYard/Crane_RTG_01`, 원본 `ServerStorage.Assets.CanalWarehouse.Crane_RTG`. 블록아웃 `RTG_Blockout` 삭제.
- 플레이 확인: 두 통로 모두 빔 양옆으로 끝까지 걸어서 통과, Pathfinding(반경 2) 북→남 통로 Success.
- Studio 저장 버전 **85**. 존 BasePart 529.

**문 열린 컨테이너 `Container_40ft_Open` / `Container_20ft_Open` — 2026-11-18 제작**
- Blender 컬렉션 `Container_40ft_Open`, `Container_20ft_Open` (삼각형 3,060 / 2,482), FBX `exports/Container_*_Open.fbx`. 원점 = 바닥 중앙(원본 컨테이너와 같음), 문 = Blender +X → Roblox 로컬 -X.
- 원본 몸체에서 문짝 면을 잘라(y=0에서 bisect) 경첩 (±hx, ±5.62) 기준으로 왼쪽 -100°, 오른쪽 +72° 회전. 잠금 막대(HW)도 같이. 문짝 가운데 자른 면은 메우지 못함(얇은 틈, 거의 안 보임).
- 내부 새로 만듦: `_Interior`(안쪽 벽+세로 리브+천장 보+뒷벽, 색 = 변형 색을 어둡게, CorrodedMetal), `_Floor__Wood`(판자 7장, 바닥 위면 Y 1.0).
- 텍스처: 기존 `Container40`/`Container20` 아틀라스 그대로(이름 접두사 유지) → 변형별 SurfaceAppearance를 교체 시 붙임.
- 충돌(`Colliders`): 바닥, 양 벽, 지붕, 뒷벽, 문 위 헤더, 문짝 2(회전 상자).
- `Open=true` 컨테이너 **9개**(40ft 5, 20ft 4) 전부 교체, 속성(Variant, BlockoutSource, Open) 유지. 문 앞이 막힌 2개(Yard_South 40ft Olive (-128.4, 953), RustRed (-242.4, 995))는 180° 돌림 → 속성 `Flipped=true`.
- 템플릿: `ServerStorage.Assets.CanalWarehouse.Container_40ft_Open`, `Container_20ft_Open` (SurfaceAppearance 없음, 복제 후 변형별로 붙임).
- 플레이 확인: 9개 모두 문 앞 → 안쪽 뒷벽까지 걸어 들어갔다 나옴(발 높이 1.0). Pathfinding Success. → **7단계 `LootSpawn` 위치 후보**: 각 컨테이너 로컬 (hx - 4, 1, 0) 부근.
- 플레이 테스트 팁: MCP 재연결 뒤에는 클라이언트 물리가 멈춰 `MoveTo`가 안 먹음 → 서버에서 `HumanoidRootPart:SetNetworkOwner(nil)` 후 테스트. 긴 테스트는 `task.spawn` + 결과를 StringValue에 써 두고 나중에 읽기(호출이 길면 MCP 연결이 끊김).
- Studio 저장 버전 **89**. 존 BasePart 637.

**리치스태커 `ReachStacker` · 바지선 `Barge` — 2026-11-18 제작**
- 리치스태커: Blender 컬렉션 `ReachStacker` (삼각형 1,728), 로컬 원점 = (-120, 0.5, 790), 앞 = -X. 매핑 Blender (x,y,z) ↔ 로컬 (-x, z, y). 차체·평형추(경고 줄무늬)·엔진 덮개·배기구·운전실(+z로 치우침, 유리 반쯤 깨짐)·앞 이중 바퀴/뒤 조향 바퀴(1개 펑크)·2단 붐(피벗 (9, 10.8) → 끝 (-45, 34.6))·유압 실린더 2·회전 헤드·스프레더(들린 컨테이너 `RS_HeldContainer` 위면 Y 30.5에 맞춤). 텍스처 CraneSTS(`TEXTURES.RStack`).
  - **등반 불가**: 충돌 = 몸체 하나 32×14×16.8(위면 Y 14.4) + 붐 + 스프레더. 플레이 테스트 점프 최고 발 높이 ≈ 9.3.
  - 위치 `B_ContainerYard/ReachStacker_01`, 원본 `ServerStorage.Assets.CanalWarehouse.ReachStacker`. 블록아웃 `ReachStacker_Blockout` 삭제.
- 바지선: Blender 컬렉션 `Barge` (삼각형 2,212), 로컬 원점 = 블록아웃 `SunkenBarge` 중심(그 CFrame 그대로 `PivotTo`), 80×8×24, 갑판 위면 로컬 y 4. 선체(양 끝 경사, 옆구리 찢김), 갑판 판, 낮은 벽(서쪽 잠긴 끝 x < -27은 없음 → 물에서 걸어서 올라탐), 계류 기둥 6쌍, 밧줄 더미 2(1줄 물로 늘어짐), 기계실, 윈치, 타이어 방현재 6, 경고·흘수 표시. 선체 색은 더 어둡게 덮어씀(72, 42, 32), 갑판 (52, 50, 48) CorrodedMetal.
  - 충돌: 갑판(블록아웃 상자 그대로), 양옆 벽, 동쪽 벽, 기계실, 윈치. 갑판 위 컨테이너(`BargeContainer`)는 그대로.
  - 위치 `E_Canal/Barge_01`, 원본 `ServerStorage.Assets.CanalWarehouse.Barge`. 블록아웃 `SunkenBarge` 삭제.
  - 플레이 확인: 운하 바닥(-4.5) → 서쪽 잠긴 끝 → 갑판 동쪽 끝까지 걸어서 이동.
- Studio 저장 버전 **91**. 존 BasePart 654.

### 4단계 소품

**가져오기 방식 변경 (2026-11-18)**: `exports` 폴더를 Studio MCP 업로드 허용 폴더로 추가함 → FBX를 Open Cloud로 **그룹 소유 Model**로 올리고 `insert_asset`으로 넣음. 사용자에게 Import 3D 부탁 안 함. 절차는 `.claude/skills/blender-to-roblox/SKILL.md` 7-A.

**묶음 1: 창고 내부 `Warehouse_Props` — 완료** (asset 127864381341171)
- Blender 컬렉션 `Warehouse_Props` (메쉬 13, 삼각형 약 11,800). 매핑 Blender (x,y,z) ↔ Roblox (-410 - x, z, 870 + y). 기준: `WhRack_Uprights` 중심 = (-412, 8.5, 897).
- 팔레트 랙 4줄: 강철 파랑 기둥(SteelBlue)·주황 빔(ShutterOrange)·철망 선반·팔레트(Wood)·화물(Cardboard 색 125,100,70). (-398, 846) 랙 가운데 칸 무너짐 + 통로에 쏟아진 팔레트·상자(충돌 없음).
- 잔해 계단 5단: 콘크리트 판·나무 상자·팔레트를 층마다 엇갈려 쌓은 더미(생존자가 붐으로 오르려고 쌓은 것) + 기댄 지붕 철골 2 + 찢어진 지붕 판 + 철근. 5번째(30)는 **쓰러진 크레인에서 부러진 붐 끝이 세워진 것**(위에 철판, 찢긴 철판).
- 하역 앞마당: 깨진 콘크리트 판 + 경고 줄무늬 + 떨어진 조각.
- 충돌: 블록아웃 상자 10개를 그대로 투명하게 → `C_Warehouse_Main/Warehouse_Props/Colliders`. 랙은 통짜(등반 불가 유지). 블록아웃 `C_Warehouse` 폴더 삭제.
- 플레이 확인: 바닥 → 잔해 6/12/18/24/30 → 붐 바닥 경로 OK. 랙 사이 통로 가운데는 잔해 더미가 막지만 Pathfinding은 서쪽(x≈-427)·동쪽(x≈-387)으로 돌아감.
- Studio 저장 버전 **93**. 존 BasePart 667.

**묶음 2: 서쪽 강변 `WestBank_Props` — 완료** (asset 74484859434017)
- Blender 컬렉션 `WestBank_Props` (메쉬 20, 삼각형 약 9,600). 매핑 Blender (x,y,z) ↔ Roblox (-630 - x, z, 870 + y). 기준: `WbTower_Steel` 중심 = (-628.97, 19.17, 759.70).
- 감시탑: 강철 다리 4 + X 버팀대 2단, 합판 바닥(Y 31.5), 모래주머니 4단 + 골판 뒷판(동쪽은 z 754..760만 → 사다리 도착 틈), 기둥 4 + 기울어진 골판 지붕, 찢어진 방수포, 부서진 탐조등, **케이지 사다리**(동쪽 면 x -623.3, z 762..764).
- 연료탱크 3: 바랜 흰색 원통 + 녹 띠·녹물 줄, 원뿔 지붕, 콘크리트 받침, 경고 판, 맨홀, 배관 → x -630 매니폴드, 밸브 핸들, 탱크 B 아래 기름 얼룩. 사다리 없음(등반 불가).
- 펜스 3줄: 기둥 4 간격, 위·아래 레일, 반투명 철망 판(Transparency 0.65), 가시철사 3줄, 남쪽 한 구간 기울어짐, 경고 판.
- 정비고: 벽·지붕 = 창고 텍스처 재사용(`WhSiding_Shed*` SidingTeal/RoofZinc/ShutterOrange, `WhSteel_ShedFrame`), 동쪽 셔터 반쯤 열림(아래 끝 Y 6.5), 북쪽 문. 내부: 작업대+공구, 선반, 드럼통 4(+1 넘어짐), 타이어 더미, 엔진 호이스트+엔진.
- 충돌(`D_WestBank/WestBank_Props/Colliders`, 33개): 블록아웃 그대로(탱크는 **Cylinder** 모양으로 바꿈) + 사다리 **TrussPart** 2×32×2 @ (-623.3, 16.5, 763) (속성 `ClimbPoint=true`) + 셔터·작업대·선반·드럼·타이어·호이스트.
- 플레이 확인: 사다리 → 감시탑 바닥(발 Y 31.5) OK, 정비고 동쪽 셔터 밑 → 안 → 북쪽 문 OK.
- Studio 저장 버전 **95**. 존 BasePart 694.

**묶음 3: 크레인 부두 `Quay_Props` — 완료** (asset 117280883930665, 사무소 철물 교체본 127392656967095)
- Blender 컬렉션 `Quay_Props` (메쉬 20, 삼각형 약 5,900). 매핑 Blender (x,y,z) ↔ Roblox (-400 - x, z, 620 + y). 기준: `QOffice_Walls` 중심 = (-422.1, 10.75, 643).
- 부두 사무소 (x -437..-407, z 630..656): 2단 컨테이너형 사무실. 1층 들어감(북쪽 문 열림, 깨진 창, 책상·의자·캐비닛·넘어진 캐비닛·흩어진 서류), 2층은 판자로 막힘. **동쪽 바깥 계단**(x -406.5..-402.5, z 656 → 634, 단 10) → 착지(z 632..636) → 발코니(x -411..-407, 바닥 Y 11). 지붕 실외기·안테나, 넘어진 간판. 벽 색 (138,134,122) Plastic(CorrodedMetal은 분홍, Metal은 하늘 반사가 심해서).
- 오두막 (x -655..-635, z 632..648): 판자 벽, 박공 함석 지붕, 경첩 하나로 매달린 문, 판자로 막은 창, 탁자·상자.
- 모래주머니 진지, 고철 더미(판·파이프·타이어·차 문·드럼), 볼라드 9(주철 + 노란 페인트 머리, 3개에 밧줄이 운하로), 크레인 레일 2줄(콘크리트 띠 + 레일 + 끝 차막이; STS 아래까지 이어짐 — 바닥 높이라 STS 세션 작업과 안 겹침).
- 충돌(`A_CraneQuay/Quay_Props/Colliders`, 44): 사무소 벽(문 구멍)·바닥·중간층·2층 상자·발코니 난간(동쪽 z 634..638.5 틈)·계단 경사판·계단 난간·착지, 오두막 벽(문 구멍)·바닥·지붕·탁자·상자, 볼라드(원통)·레일·모래주머니·고철은 블록아웃 그대로. STS 등반 마커 2개는 그대로 남김(다른 세션).
- 버그 수정: 계단 서쪽 손잡이가 착지 출구를 막음 → 메쉬를 다시 올려 `QOffice_Steel` 교체 + 충돌 단축.
- 플레이 확인: 사무소 문 → 안, 오두막 문 → 안, 계단 → 착지 → 발코니 끝까지(발 Y 11).
- Studio 저장 버전 **98**. 존 BasePart 743.

**겹침(z-fighting)·사다리 정리 — 2026-11-18** (Studio 저장 버전 **102**)
- Blender 스캔: 같은 방향을 보는 면이 0.04 이내로 겹치는 곳을 12개 에셋 전부에서 찾음(약 1,600쌍) → 작은 쪽 면을 0.05 앞으로 밀어서 해결. 남은 것은 아래를 향한 숨은 면과 0.03㎡ 이하 접점뿐. 열린 컨테이너 내부는 바깥 벽 쪽을 향한(안 보이는) 면 삭제. 붐 끝 윗면 0.28 낮춤. 기름 얼룩은 같은 색이라 평평하게 되돌림.
- 고친 메쉬를 `exports/*_v2.fbx`로 다시 올려 맵·ServerStorage의 같은 이름 MeshPart 383개를 교체(색·재질·SurfaceAppearance 유지, 위치는 Blender 중심 차이만큼 보정). 컨테이너 몸체 색 변형(이름에 색 키)은 형태가 안 바뀌어 그대로.
- 판자: 부두 사무소 2층 창·문, 오두막 창 판자를 서로 안 겹치게 다시 만듦(기울기 ±0.05, 판마다 0.07씩 앞뒤로).
- 사다리: 감시탑 사다리가 바닥판 가장자리를 0.45 뚫고 있었음 → 메쉬 +X 0.75 이동, TrussPart 중심 (-622.3, 16.5, 763). 창고 지붕 사다리는 정상.
- **STS 크레인에는 실제 사다리가 없음**(파란 블록아웃 표시 2개뿐, 다른 세션 담당) → 사용자에게 내가 만들지 물어볼 것.
- 다음 작업자 주의: 같은 판 위 장식(줄무늬·종이·판자)은 바탕 면에서 최소 0.05 띄울 것.

**묶음 4: 야드 엄폐물 `Yard_Props` — 1차 완료 (2026-11-18)** (asset 114033981465355)
- Blender 컬렉션 `Yard_Props` (메쉬 32, 삼각형 4,380, 박스·원통 조합). 매핑 Blender (x,y,z) ↔ Roblox (-200 - x, z, 830 + y). 기준: `Yard_Crate1__Wood` 중심 = (-296, 3.615, 921).
- 등반 상자 3(나무 크레이트, 모서리 각재·대각 버팀·철 모서리), 트랙터 캡(FadedBlue → Plastic, 유리 반쯤 깨짐, 배기관·연료탱크·발판) + 스켈레톤 샤시(녹 가로대, 랜딩기어, 뒤 범퍼, 타이어 1개 빠져 휠만), 차단기(기울어 땅에 닿은 붐, 경고 줄무늬), 모래주머니 벽(4단 엇갈림 + 떨어진 2개), 불탄 차(Slate 어두운 갈색, 휠만, 떨어진 범퍼·문), 저지 방벽 2(1개 부서짐 + 철근).
- **CorrodedMetal은 이 place에서 주황/분홍 얼룩으로 보임** → 차는 Slate, 트럭 캡·차단기 빨강은 Plastic으로 바꿈.
- 충돌: 블록아웃 10개를 그대로 투명 복제 → `B_ContainerYard/Yard_Props/Colliders` (등반 상자는 속성 `ClimbPoint=true`). 블록아웃 `B_YardSouth/B_YardNorth/B_AlleyCover` 안의 파트 삭제(빈 폴더 남음). 충돌이 블록아웃과 같으므로 동선 변화 없음 — **플레이 테스트는 아직 안 함**.
- 원본 `ServerStorage.Assets.CanalWarehouse.Yard_Props`. Studio 저장 버전 **108**. 존 BasePart 775.
- **2차 보강(차·트럭) 완료** (asset 121293644087227, `exports/Yard_Vehicles_v2.fbx`, 정렬 기준으로 Crate1 포함 후 삭제): 측면 프로파일 압출 + 베벨로 차체 곡면·휠 아치. 불탄 세단 = 필러·벨트라인·문 틈·빠진 앞문 구멍·녹 패치·탄 시트 골조·운전대·열린 후드·휠(허브+러그). 트럭 = 캡 프로파일(펜더 아치·지붕 페어링), 창틀·선바이저·미러·그릴 살·헤드램프·범퍼·발판·경적·배기관 열차폐·연료탱크 띠·에어호스·I빔 프레임·타이어(사이드월+림+러그). 메쉬 이름 `Yard_Car<부품>__…`, `Yard_Truck<부품>__…`.
- 재질: 캡 Slate (56,72,84), 차체 Slate (70,46,34), 녹 패치 Slate (112,56,30), 그을음 Slate (24,22,21). 삼각형: 차 약 3,000, 트럭 약 9,000. Studio 저장 버전 **111**. 존 BasePart 785.

**남은 묶음**: (완료됨) 야드 엄폐물 (블록아웃 확인함: 등반 상자 3 (-296,921)/(-274,910)/(-252,909) 6×6×6 높이 6/18/30, 트럭 캡 (-182,6,806)+샤시 (-182,2.5,832) yaw 90, 차단기 (-115,742), 모래주머니 벽 (-247,742), 불탄 차 (-250,869) yaw 20, 저지 방벽 2 (-160,868)/(-152,872))(등반 상자 3·트럭+샤시·차단기·모래주머니 벽·불탄 차·저지 방벽 2). 운하 폰툰·경사로·얕은 바닥은 5단계 운하 마감 때.

| 에셋 | 블록아웃 위치 / 크기 | 메모 |
|---|---|---|
| **쓰러진 크레인** `Crane_Collapsed` | 붐: (-622, 4, 908) → (-404, 28, 896), 폭 8, **위를 걸어 다니는 경사로**(약 6°). 받침 잔해는 Lot_040 (-632, 905) 부근 | 붐 윗면 = 걷는 길(충돌 상자 1개로 유지). 기존 `Crane_STS` 텍스처(CraneYellow 타일, `CraneSTS` 세트) 재사용 가능. 붐 옆에 매달린 컨테이너(현재 실제 컨테이너 모델) 유지 |
| **RTG 갠트리** `Crane_RTG` | 다리 X -172/-128 × Z 926/980, 상부 Y ≈ 50, 블록 S2(행 941~965) 위를 걸침 | 등반 불가. 다리는 통로 안. 타이어 바퀴 |
| **리치스태커** | (-120, 790) 본체 30×12×14, 붐이 컨테이너(-165, 18.5, 790)를 들고 정지 | 소품급 PBR 또는 색+재질 |
| **바지선** | 운하 (-95, ≈-3.3, 538), 80×8×24, 기울어짐 + 컨테이너 | 반쯤 가라앉음 |
| **문 열린 컨테이너** `Container_40ft_Open` | — | `Open=true` 6개 교체, 내부 진입 + 루트 지점 |
| **소품** | — | 팔레트 랙(창고 랙 4줄 교체), 잔해 더미(창고 내부 잔해 계단 교체: 바닥→붐 끝까지 6 높이 단위), 드럼통, 팔레트, 모래주머니, 철조망, 볼라드, 타이어 펜더, 연료탱크, 감시탑, 정비고, 부두 사무소, 텐트, 방수포, 경고 표지판, 꺼진 가로등, 트럭+샤시 |

### 5단계 — 아포칼립스 디테일
- **생존자 캠프 — 완료 (2026-11-18, "버려진 캠프")** (asset 123927789000144, `B_ContainerYard/Survivor_Camp`, 원본 `ServerStorage.Assets.CanalWarehouse.Survivor_Camp`)
  - Blender 컬렉션 `Camp_Props` (메쉬 28, 삼각형 약 4,300). 매핑 Blender (x,y,z) ↔ Roblox (-200 - x, z, 790 + y). 기준: `Camp_Fire__Rust` 중심 = (-203, 26.0, 792.5). 지붕 위면 Y 24.5, 범위 X -206..-194, Z 766..814. 남쪽 끝(Z 806..814)은 경사로 도착 자리라 비워 둠.
  - 북쪽 끝: 기댄 골판 바람막이 + 모래주머니 2단. 파란 방수포 쉘터(기둥 하나 쓰러져 모서리가 지붕 밖으로 처짐, 찢어진 구멍) 아래 매트리스·침낭·베개·담요. A형 텐트(용마루 처짐, 한쪽 찢김, 나무 바닥판). 꺼진 드럼통 화로(재·석쇠·냄비) + 상자 의자·판자 벤치(하나 넘어짐). 빨랫줄(옷 3)·안테나 깃대(찢어진 흰 천). 지붕에 페인트 **SOS**(경사로에서 올라오면 바로 읽힘). 깡통·물통·배낭·타이어·지붕 밖으로 늘어진 담요.
  - 재질: 천은 Fabric, 녹 철은 Slate(CorrodedMetal 분홍 문제), 방수포 (46,78,112). `DoubleSided` 꺼짐(천은 solidify 두께 0.05~0.06이라 양면 보임).
  - 충돌(`Survivor_Camp/Colliders`): 드럼통(원통), 상자 의자 3, 모래주머니, 바람막이, 상자 더미. 텐트·쉘터는 충돌 없음(걸어 들어감).
  - 확인: Pathfinding(반경 2, 높이 5, 점프) 메인도로 (-182, 760) → 캠프 3지점 모두 Success. Studio 저장 버전 **115**.
- **바리케이드 — 완료 (2026-11-18)** (asset 114728492771937, `B_ContainerYard/Barricade`, 원본 `ServerStorage.Assets.CanalWarehouse.Barricade`)
  - Blender 컬렉션 `Barricade` (메쉬 22, 삼각형 약 17,000 — 대부분 철조망). 매핑 Blender (x,y,z) ↔ Roblox (-200 - x, z, 745 + y). 기준: `Bar_Sign__Wood` 중심 = (-259, 4.8, 733.4).
  - 컨테이너 벽(Z 739..751) 입구 2곳: **서쪽 X -268..-238 = 버티는 검문소** (도로 쪽 모래주머니 벽 A X -256..-238 + 안쪽 벽 B X -268..-250 → 지그재그 통로, 철조망, 대전차 장애물 3, 검문소 표지판(글씨 없음 → 낙서 단계에서 "CHECKPOINT" 데칼), 꺼진 투광등 기둥 + 늘어진 전선). **동쪽 X -138..-101 = 뚫린 입구** (가운데가 무너진 모래주머니, 흩어진 자루 16·터진 모래 더미, 넘어진 판자문 1(바닥)·경첩에 매달린 문 1(-138 컨테이너 끝), 끊긴 철조망, 쓰러진 장애물, 드럼통 2).
  - 벽: 컨테이너 위 도로 쪽 가장자리에 **콘서티나 철조망**(나선 리본, `DoubleSided=true`) 4구간. 컨테이너 사이 4칸 틈(X -190..-186)은 판자·골판·버팀대로 막음. **감시 발판**: -214 컨테이너 위(Y 12.5) 모래주머니 진지 + 함석 지붕 + 상자, 야드 쪽에 기댄 나무 사다리(충돌 = **TrussPart** (-215, 7.5, 752.2) 2×14×2, `ClimbPoint=true`).
  - 충돌(`Barricade/Colliders`): 서쪽 벽 A/B(높이 5 → 철조망까지 포함, 뛰어넘기 불가), 짧은 꺾임, 장애물 5(3×3×3), 동쪽 남은 자루 2, 드럼통, 틈 막이, 감시 진지 3, 사다리 Truss. 장애물은 도로 화단에 걸려 있어 Z +4 옮김.
  - 확인: Pathfinding 도로 → 야드 서쪽 입구(지그재그 통과)·동쪽 입구·캠프 Success. 플레이 테스트로 사다리 Truss 타고 감시 발판(발 Y 12.5)까지 올라감. (Pathfinding의 AgentCanClimb으로는 NoPath — 실제 플레이는 됨.) Studio 저장 버전 **119**.
- **낙서·안내판 — 완료 (2026-11-18, 영어)** (`Zone_CanalWarehouse/Graffiti`, 원본 `ServerStorage.Assets.CanalWarehouse.Graffiti`)
  - 이미지 6장: Blender 별도 씬 `DecalStudio`(직교 카메라, 투명 배경, Emission + 노이즈 알파로 벗겨진 페인트)에서 렌더 → `exports/decals/*.png`. 폰트 Impact/Arial Bold. 이미지 ID는 `exports/texture_ids.json` → `Graffiti`.
  - **업로드 방법**: Open Cloud `assetType: "Decal"` + groupId → 결과 assetId는 *Decal* ID라 `Decal.Texture`로 안 불러와짐(PreloadAsync Failure). 업로드 operation의 `childOperations` 를 GET 하면 `ModerationPending ids` 에 **이미지 ID**가 나옴 → 그걸 Texture로 씀(바로 로드 Success).
  - 배치(투명 판 Part + Decal Front, 벽에서 0.06): 창고 동쪽 벽 (-381, 10.2, 846) "NO SHIP COMING" 24×9 / 셔터 옆 (-381, 5.8, 829.6) 구호물자 배급 안내판 4×5.5(찢긴 종이 + "LIES" 스프레이) / 캠프 스택 위 컨테이너 동쪽 면 (-194, 19, 786) 날짜 카운트 DAY 37, Decal.Color3 어둡게(흰 컨테이너라) / 캠프 스택 아래 컨테이너 **서쪽** 면 (-206, 6.5, 806) "CAMP ↑"(동쪽 면은 트럭에 가려짐) / 벽 줄 컨테이너 야드 쪽 (-152, 6.2, 751) "DEAD INSIDE / DO NOT OPEN" 15×7.5 / 검문소 표지판 앞면 (-259, 4.8, 733.18) "CHECKPOINT / STOP / SHOW YOUR HANDS".
  - Studio 저장 버전 **125**. 남은 아쉬움: DEAD INSIDE 흘러내림이 글자에서 살짝 떨어져 있음, 날짜 카운트가 작은 편.
- **운하 마감 — 완료 (2026-11-18, "적당하게 너무 정신없지 않게")**
  - 얕은 바닥 4개 → Material Mud (64,57,44), `E_Canal/CanalFloor`로 이동. 블록아웃 `E_Canal` 비워짐.
  - `E_Canal/CanalDebris` (asset 132710927934464, 메쉬 12, 삼각형 약 3,300; 매핑 Blender (x,y,z) ↔ Roblox (-500 - x, z, 750 + y)): 바닥 잔해 묶음 7곳(타이어·드럼통·콘크리트 덩이+철근·파이프·판자·가라앉은 철판) + 따로 놓인 타이어 4. 떠 있는 것(판자·병·스티로폼·비닐) 6곳은 동쪽 둑(X≈-462)과 남북 운하 북쪽 벽(Z≈578)에 몰아 둠. 모두 충돌 없음.
  - 기름막 3곳 = `CanalDebris/OilSlicks` 얇은 원통 Part 5개씩 (28,26,30), Y ≈ -1.65. **평면 메쉬·반투명 Part는 물 위에서 파랗게 보임** → 불투명 + 두께 있는 Part로 바꿈.
  - **실제로 보이는 물 표면은 약 Y -1.75** (레이캐스트는 -2.98을 줌). 떠 있는 물건은 -1.7 근처에 둘 것.
  - 경사로 4곳: `E_Canal/Ramps/Ramp_1..4` (asset 94885248972212) — 콘크리트 경사판 + 미끄럼 방지 홈 + 아래쪽 이끼 띠 + 한쪽 난간. 기존 WedgePart를 투명 충돌(`Ramp_Col`)로 유지(높은 쪽 = 로컬 +Z).
  - 폰툰: `E_Canal/Pontoon_01` (asset 134278906305610) — 판자 데크(한 장 빠짐, 한 장 짧음) + 각재 틀 + 파란 드럼 부표 9 + 타이어 방현재 4 + 클리트 + 밧줄. 충돌 = 기존 블록아웃 상자(`Colliders/Deck_Col`).
  - 확인: Pathfinding 도로 → 경사로 → 운하 바닥 2곳, 폰툰 → 바닥 Success. Studio 저장 버전 **128**.
  - 참고(이번에 고치지 않음): 부두 고철 더미 일부가 분홍색으로 보임(CorrodedMetal 문제) → 8단계에서 Slate로 바꿀 것.

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
