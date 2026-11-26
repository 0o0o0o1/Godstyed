# 공장맵 — 이어서 할 일 (인수인계)

> 마지막 작업: 2026-11-26 · **공장 복귀 포탈(템플릿 없던 것)·도착 자리 몬스터/보스 회피·물 속 이동 −15% — 공장 place 게시 + Shared·Services·Controllers 게시 대기** · **핑을 M 지도에서만(탈출구 핑) + 튜토리얼 '탈출구에 핑' 완료 — Shared·Services·Controllers 게시 대기** · **핑(파티원에게만, 자동+휠, 월드 표시·M 지도) + 튜토리얼 핑 단계 — Shared·Services·Controllers 게시 대기** · **모바일 버튼 배치 설정(끌어서 옮기기·전체/버튼별 크기, 서버 저장) — Shared·Services·Controllers 게시 대기** · **튜토리얼 지도 단계(레이드 도착 → M으로 지도 열기) + 모바일 지도 버튼 — Shared·Services·Controllers 게시 대기** · **한국어 언어 전환(설정 창 Language: English/한국어) — Shared·Services·Controllers 게시 대기** · **단검 은신(Vanish) 1차 완성 — Shared·Services·Controllers 게시 대기** · **그림자 연쇄 처형 = 플라즈마 구슬 압축 → 핵 폭발(Controllers 게시 대기)** · 2026-11-21 · **공장만 배경음악 70%(PLACE_VOLUME, Shared·Controllers 게시 대기)** · **몬스터 몸 소리(가까운 6마리)·공격 소리·체력바 피격 강조 — Shared·Controllers·Enemies 게시 대기** · **화염·폭발 옥상 관통 버그 수정(Services 게시 대기)** · **공장 배경음악 3곡 + 보스전 음악 Ground Zero A(167.4초에서 자름) — Shared·Controllers 게시 대기** · **화염 피해 틱 화면 흔들림·지글 소리(Controllers 게시 대기)** · **공장 전용 스크립트 5개를 패키지(Services·Controllers)로 옮김 완료 — Shared v103·Services v63·Controllers v89, 공장 place 게시 필요** · **습격 상자 닫힘 경고(상자 깜빡임·마지막 5초 빠르게·틱 소리, Studio 버전 125)** · **Hook Hauler 등 약점 앞 50%·뒤 150%(Studio 버전 122)** · **열기 범위 원 가까울 때만·화염 화면 효과(Studio 버전 121)** · **화염 스택 표시를 체력바 위 작은 띠로(Studio 버전 119)** · **Slag Walker 폭발 소리·싱크 수정(Studio 버전 118)** · **화염 스택 마리 수만큼·5초 초기화, 야외 Molten/Slag 반반(Studio 버전 113)** · **Slag Walker 체력 비례 균열 빛·폭발 예고(Studio 버전 112)** · **Molten Walker 화염 스택 오라 + Slag Walker 죽음 폭발(Studio 버전 111)** · **상자 등급별 경비 몬스터 + 습격 적 수 증가(Studio 버전 110)** · **공장 적 거대화 진짜 원인(Humanoid 자동 크기 조정) 고침, Studio 버전 109, Enemies 게시 필요** · **공장 습격(셔터 없는 상가 습격) + 등급 상자 테두리 빛·자동 흡수(Studio 버전 108)** · **보스 Foreman 메쉬 3.5배 버그 고침(Studio 버전 107, Enemies 패키지 게시 필요)** · **몬스터 1번 Slag Walker 완료(외형·소리·효과·공격 애니·정의·배치, Studio 버전 68), 몬스터 2번 Hook Hauler 완료(Studio 버전 72), 몬스터 3번 Furnace Tender 완료(Studio 버전 75), 몬스터 디자인 1~4번 모두 완료(보스 The Foreman, Studio 버전 79) — 남은 것: 능력치·게시·플레이 확인** · **보스 Gear Head + 일반 몬스터 31지점(67마리) 배치** (Studio 버전 58) · **8단계 자동 검사·최적화 완료 — 계획서 전 단계 끝** (Studio 버전 56) · **7단계 상자·등반 태그 완료** (공장 25 + 운하 11 상자) · **6단계 조명·연기 완료** (Studio "공장" 저장 버전 54, 공용 패키지 Shared·Services 게시 필요) · **5단계 소품·표지·낙서 완료** (버전 51) · 2026-11-19 · **4단계 바닥 마감 완료 + 슬래그장 Exit4 수정** (Studio "공장" 저장 버전 49) · G 남쪽 띠(슬래그장·고철장·측선·침전조) 완성 → 블록아웃 전부 에셋화 · F2 계량소 + 광석 덤프트럭 완성 · E 발전소(터빈홀·개폐소) 완성 · 굴뚝 3기 완성(중간 에셋 단계 끝) · 컨베이어 갤러리(원료 야적장 → 용광로) 완성 · 배관 다리 키트 4노선 + H 배관 회랑 완성 · 원료 야적장(C) 완성 (Studio "공장" 저장 버전 33) · 가스 홀더(F) · 철도 야드(Lot_058) + 작업자 배랭(Lot_060) · 보스 마당 `BossYard` 완성 · 북쪽 확장 땅 · 낙하 문제 수정(스폰·경계벽) · 코크스로(B) 완료 · 압연 공장동(D)+야적장·냉각탑(E)·용광로(A) 완료
> 설계·구역·결정: `Factory_계획서.md`. 에셋 규칙: `.claude/skills/blender-to-roblox/`.

### 몬스터 디자인 (진행 중, 2026-11-20 시작)
- 사용자 지시: "몬스터 디자인을 하나하나 차근차근 순서대로, 단계마다 보고, 궁금한 건 무조건 물어보기."
- 결정(사용자): **공장 전용 새 몬스터**(기존 적은 다른 맵과 공유라 안 건드림) / 몬스터마다 **컨셉·설정 + 외형(3D, Blender) + 소리·효과·애니메이션** (능력치·공격 패턴은 범위 밖 — 기존 적 수치 쓸지 물어볼 것) / 순서 **약한 적부터 → 보스 마지막**: 야외 기본 적 → 실내 작업자형 → 보스 마당 경비 → 보스.
- 능력치(사용자 결정 2026-11-20): **사용자가 직접 정함 — 그전까지 임시로 Ashen Husk 수치**(체력 150, 걷기 6 / 추격 20, 어그로 50, 공격 피해 8·사거리 5·windup 0.5·cooldown 1.6, xp 25, 금화 1~5, scrap_metal 2개 60%).
- **1번 야외 기본 적 = Slag Walker (컨셉 확정 2026-11-20)**
  - 설정: 출선 사고 날 출선장에서 일하던 작업자들. 쏟아진 슬래그를 뒤집어쓰고 굳었지만 속은 아직 식지 않았다. 'STILL INSIDE' 낙서처럼 공장 밖을 맴돌며 출구를 찾는다.
  - 외형: 녹아 붙은 작업복·안전모 위로 몸 절반 이상이 검회색 슬래그 껍질이고, 갈라진 틈에서 주황 빛. 한쪽 팔은 굳은 슬래그 덩어리가 곤봉처럼 커짐. 키는 일반 R15.
  - 소리·효과: 걸을 때 껍질 갈리는 소리, 식는 '쉭' 소리, 낮은 신음. 몸에서 잔불과 옅은 연기. 맞으면 껍질 조각과 불티, 죽으면 빛이 꺼지며 부서짐.
  - 애니메이션: 걷기·추격은 공통 좀비 동작(EnemyConfig.ZOMBIE_ANIMATIONS), 공격은 곤봉 팔 내려치기를 새로 만듦.
  - **변형 2종**(메쉬·리그는 같고 껍질 양·색·빛만 다름): `slag_walker` 식은 형(껍질 두꺼운 검회색, 틈 빛 약함) → Ashen Husk 자리 26마리 / `molten_walker` Molten Walker 갓 굳은 형(껍질 얇고 틈 넓음, 밝은 주황 빛, 연기 많음) → Toothed Revenant 자리 26마리. (어느 쪽이 어느 자리인지는 바꿔도 됨)
  - **외형 완료 (2026-11-20, Studio 저장 버전 60)**: `ServerStorage.Assets.Enemies.SlagWalker`(식은 형, 메쉬 33) / `MoltenWalker`(갓 굳은 형, 30 — LeftUpperArm·LeftLowerLeg·LowerTorso 슬래그 뺌). 속성 `Variant` = Cooled / Molten.
    - 구조: AshenHusk R15 리그 복제(얼굴 데칼·FaceControls 삭제, 몸 파트 Transparency 1) + `<부위>__<재질>` MeshPart 를 Weld "Attach"로 부위에 용접(Massless, 충돌·쿼리·터치 끔). 기존 적(ToothedRevenant 등)과 같은 방식.
    - 재질: Slag/Cloth/Skin = SurfaceAppearance(타일 텍스처), Slag 는 **EmissiveMaskContent**(균열 발광) — 식은 형 Strength 2.5 / Tint (255,120,40), 갓 굳은 형 ColorB·EmitB, Strength 4 / Tint (255,135,45). 작업복·피부는 사진보다 밝게 나와 SA.Color 틴트(Cloth 135,135,140 / Skin 150,118,110). Helmet = Plastic (128,96,34), Boot = Leather, Dark = Plastic, Glow(눈) = Neon.
    - 텍스처 ID: `exports/texture_ids.json` → `SlagWalker`. 메쉬 모델 assetId 87082938518749(그룹 소유).
    - Blender: 씬 `SlagWalker`, 컬렉션 `SlagWalker`(메쉬, Decimate 수정자: 슬래그 0.55·큰 옷 0.7), `SW_RigRef`(R15 상자 와이어), `SW_TexBake`(굽기 판). 재현 스크립트 `scripts/slag_walker_build.py`(메쉬) → `slag_walker_tex.py`(굽기 셰이더) → `slag_walker_uv_export.py`(UV·FBX). 좌표 = Roblox HRP 기준 (-X, Z, Y), 앞 = -y. 삼각형 13,478.
    - **Blender MCP 안전 모드 끔 (2026-11-20, 사용자 지시)**: `.mcp.json`에서 `BLENDER_MCP_SAFE_MODE` 삭제 → Claude Code 세션을 다시 시작해야 적용. 이후 스크립트는 `exec(open(r"D:\god\scripts\slag_walker_build.py", encoding="utf-8").read())`처럼 파일로 실행.
    - **Blender `look`은 이 PC에서 하얗게 나옴 → Cycles CPU 렌더를 PNG로 저장해 Read 로 확인**(`exports/_preview/`).
    - 겹침(BVH): 껍질↔옷 접합부와 관절(목·어깨·팔꿈치·무릎)만 남음. 곤봉 손↔오른 허벅지 겹침은 곤봉을 바깥으로 0.12 옮겨 해결.
    - **주의: `ServerStorage.Assets.Enemies` 폴더도 패키지(PackageLink)라 새 모델 2개를 넣었으니 사용자가 게시해야 함.**
  - **소리·효과·애니메이션·정의·배치 완료 (2026-11-20, Studio 버전 68) → 1번 몬스터 끝 (능력치만 임시)**
    - 결정(사용자): 모델 안 스크립트 / 크리에이터 스토어 무료 효과음 / 공격 키프레임 직접 제작.
    - **공격 애니메이션** `SlagWalkerAttack` assetId **89817274505362**(그룹 소유, Open Cloud에 `.rbxmx` KeyframeSequence 업로드). 생성 `scripts/slag_walker_anim.py` → `exports/anims/`. 0 → 0.40 들어 올림 → 0.46 멈춤 → **0.58 내려침(마커 "Impact")** → 0.82 → 1.35 복귀. Studio FK 계산으로 확인: 타격 때 곤봉 끝 땅 위 약 0.2, 발 땅에 붙음(±0.1). 걷기·추격·피격·사망은 공통 좀비 동작.
    - **소리·효과**: `scripts/slag_walker_fx.lua`가 두 모델에 설치. UpperTorso 에 Sound(ProSoundEffects: 발소리 2, 신음 2, 식는 소리, 피격 지글거림, 내려치기 쿵, 사망 균열·쉭, 갓 굳은 형만 Crackle 반복), UpperTorso__Slag 에 PointLight `SlagGlow` + ParticleEmitter(Embers·Smoke·HitSparks·HitChips), 곤봉 `ClubTip` 첨부점에 SlamDust·SlamSparks. 텍스처는 Roblox 내장 `rbxasset://textures/particles/*`. 효과음 10개 PreloadAsync Success 확인.
    - **SlagFX 스크립트**(모델 안 Script, 속성 Molten·AttackAnim): 살아 있을 때 발소리(속도 맞춘 보폭)·신음(추격 중 더 자주)·식는 소리, 피격 시 불티·껍질 조각·지글거림·균열 번쩍, 공격 마커 "Impact"에서 쿵·먼지·불티, 사망 시 효과 끔. **시체 복제본(EnemyAI.spawnDeathCorpse, Humanoid 없음)에서도 실행** → 균열 빛 3초에 걸쳐 꺼짐 + 1.1초에 슬래그 조각이 떨어져 나감(4초 뒤 고정).
    - 이전 메모의 "drip 노멀 뒤집힘"은 DoubleSided 로 처리됨(메쉬 재제작 시 수정).
    - **적 정의**: `ReplicatedStorage.Shared.Data.Enemies.Factory` 새 모듈 — `slag_walker`, `molten_walker` (attackHitTime 0.58, animations.attack). 능력치 = Ashen Husk 임시값.
    - **배치**: `FactoryEnemies.EnemySpawns` 22지점 EnemyId 교체 (ashen_husk→slag_walker 26마리, toothed_revenant→molten_walker 26마리). 원래 값은 각 지점 속성 `OldEnemyId`.
    - **게시 필요(사용자)**: 공용 패키지 Shared(새 모듈 Factory) + `ServerStorage.Assets.Enemies`(SlagWalker·MoltenWalker 모델).
    - 플레이 테스트 안 함(사용자 지시). 실제 게임에서 소리 크기·효과 양은 아직 확인 안 됨.
    - Studio MCP 주의: 스크립트 소스를 바이트 위치로 잘라 돌려받으면 한글 중간이 잘려 **응답이 시간 초과**됨 → `utf8.len` 으로 경계 맞춰 자를 것.
- **2번 실내 작업자형 = Hook Hauler (컨셉 확정 2026-11-20)** — stockroom_brute 자리 4지점 8마리(압연 공장동 2곳 (-899,1131)·(-937,1177), 용광로 출선장 (-776,863), 발전소 터빈홀 (-89,1228)). **한 종류만**(변형 없음).
  - 설정: 천장 크레인을 몰던 작업자. 사고 날 떨어진 갈고리가 등에 박혔고, 그 뒤로 쇠사슬을 몸에 감은 채 실내를 돌며 아직도 '짐'을 옮긴다.
  - 외형: 일반 적의 1.5배 거구(scale 1.5). 찢어진 작업 조끼·기름 밴 작업복, 어깨·팔에 감긴 굵은 쇠사슬, 등에 박힌 녹슨 크레인 갈고리, 한 손에 쇠사슬 끝의 큰 갈고리(무기), 얼굴은 용접 마스크.
  - 소리·효과: 쇠사슬 끌리는 소리, 무거운 발소리, 급한 숨소리. 피격 시 쇠 부딪힘·불티, 사망 시 쇠사슬이 풀려 바닥에 떨어짐.
  - 공격: 갈고리를 옆으로 크게 휘두르기(1번 내려치기와 다르게).
  - 능력치: 사용자가 정할 때까지 Stockroom Brute 임시값(scale 1.5, 체력 320, 걷기 5/추격 15, 어그로 45, 피해 17·사거리 9·windup 0.8·cooldown 2.2, xp 55, knockbackResist 0.6, leash 220, 금화 2~6).
  - **외형 완료 (2026-11-20, Studio 버전 71)**: `ServerStorage.Assets.Enemies.HookHauler` (메쉬 33, 삼각형 약 18,000). 1번과 같은 구조(AshenHusk R15 복제 + `<부위>__<재질>` MeshPart Weld "Attach"). 메쉬 모델 assetId 137332056598079.
    - 구성: 두꺼운 몸·팔다리, 찢긴 형광 조끼(앞 틈·팔 구멍·찢긴 아랫단·구멍) + 반사 띠 2줄, 용접 마스크 + 보안경(한쪽 깨져 눈빛), 머리끈, 벨트·공구 주머니, 강철 앞코 장화, 가죽 장갑(왼손 벌림·오른손 주먹). 쇠사슬: 몸 대각선으로 한 바퀴(등 쪽은 갈고리 위로), 왼 팔뚝 나선, 오른 손목, 주먹 → 무기 갈고리, 등 갈고리 눈의 끊어진 사슬, 허리 뒤에서 바닥에 끌리는 사슬. 갈고리 2개(오른손 무기 = RightHand__Paint, 등에 박힌 것 = UpperTorso__Paint).
    - 재질: Cloth·Skin = Slag Walker 텍스처 재사용(같은 틴트), Vest = 새 컬러(형광 주황, 기름·그을음) + Cloth 노멀·거칠기, Rust(사슬·앞코)·Paint(갈고리, 노랑 도장 벗겨짐) = 새 PBR(금속성 포함). Boot = Leather, Strip = SmoothPlastic 밝은 회색, Mask = Plastic, Dark(보안경) = Glass 0.15, Glow = Neon. ID → `exports/texture_ids.json` `HookHauler`.
    - **공용 키트 분리**: `scripts/monster_kit.py`(loft·blob·box·tube·finger·torus·chain·hook·shell(cut 함수)·finalize·uv_box·export_fbx·bbox_table·overlaps·shot), `scripts/tex_kit.py`(4D 타일 셰이더 도우미, cloth_mat·rust_mat(paint)·bake_jobs). **loft 면 뒤집힘 수정 + finalize 에서 덩어리별 부호 부피로 면 방향 자동 교정** (이번 메쉬 뒤집힌 덩어리 0).
    - 실행: Blender에서 `exec(open(r"D:\god\scripts\monster_kit.py", encoding="utf-8").read()); exec(open(r"D:\god\scripts\hook_hauler_build.py", encoding="utf-8").read())`. Blender 시작 장면의 기본 Cube·Light·Camera 는 빌드 스크립트가 지움.
    - 겹침(BVH): 조끼↔몸, 마스크↔머리, 관절, 등에 박힌 갈고리(의도), 사슬이 몸에 닿는 접촉만 남음. 사슬이 팔·갈고리를 관통하던 5곳은 경로를 옮겨 해결.
  - **소리·효과·공격 애니·정의·배치 완료 (2026-11-20, Studio 버전 72) → 2번 몬스터 끝 (능력치만 임시)**
    - **공격 애니메이션** `HookHaulerAttack` assetId **129093537179092**: 0 → 0.50 오른쪽 뒤로 들어 올림 → 0.58 멈춤 → **0.70 앞으로 휘둘러 타격(마커 "Impact")** → 0.92 왼쪽으로 따라 휘두름 → 1.50 복귀. 생성 `scripts/hook_hauler_anim.py` + 공용 `scripts/anim_kit.py`(1번 애니 스크립트에서 분리). FK 확인: 타격 때 갈고리가 몸 앞 3.2·왼쪽 0.9, 땅 위 3.6(가슴 높이), 발 땅에 붙음.
    - **소리·효과** `scripts/hook_hauler_fx.lua`: UpperTorso 에 Sound 10개(ProSoundEffects — 사슬 끌림 반복(움직일 때), 무거운 발소리, 사슬 짤랑, 마스크 너머 으르렁 2, 휘두르는 바람(0.9초에서 끊음), 타격 쇠 부딪힘, 피격 쇠 소리, 사망 사슬·떨어지는 쇠), UpperTorso__Rust 에 HitSparks, 무기 갈고리 `HookTip` 첨부점에 SwingSparks·SwingDust. 효과음 10개 PreloadAsync Success.
    - **HookFX 스크립트**(모델 안): 이동 속도 맞춘 발소리·사슬 끌림, 추격 중 더 잦은 으르렁, 피격 불티·쇠 소리, 공격 시 휘두르는 소리 → "Impact"에 쾅·불티·먼지. 시체 복제본에서 사슬(앞코 제외)과 손 갈고리가 풀려 바닥에 떨어짐(4초 뒤 고정). 등 갈고리는 그대로 박혀 있음.
    - **적 정의**: Factory 모듈에 `hook_hauler` 추가(scale 1.5, attackHitTime 0.70, 능력치 = Stockroom Brute 임시값).
    - **배치**: stockroom_brute 4지점(8마리) → hook_hauler, 원래 값은 `OldEnemyId`.
    - 게시 필요(사용자): Shared(Factory 모듈) + `ServerStorage.Assets.Enemies`(HookHauler 추가). 플레이 테스트 안 함.
- **3번 보스 마당 경비 = Furnace Tender (컨셉 확정 2026-11-20)** — 보스 마당: lab_subject 2지점×2 (-960,1400)·(-800,1400) → `furnace_tender`, bloated_husk 2지점×1 (-882,1528)·(-887,1310) → `furnace_warden`(덩치 변형). 보스 Gear Head (-879,1450).
  - 설정: 사고 날 마지막 쇳물을 뽑으려고 출선장에 남았던 작업자들. 은빛 내열복이 몸에 녹아 붙었고, 지금은 보스 마당을 지키며 아무도 북쪽으로 못 가게 막는다('DON'T GO NORTH' 낙서).
  - 외형: 그을리고 찢긴 은빛 내열복(알루미늄 코팅) + 후드, 녹아 흘러내린 금빛 방열 유리창 안에서 주황 빛. 무기 = 끝이 달아오른 긴 개공봉(쇠막대). 덩치 변형 = 같은 메쉬, 더 크고 팔에 방열판 방패·어깨 보호대 추가.
  - 소리·효과: 내열복 스치는 소리, 후드 안 거친 숨, 개공봉 끝 불티·열기. 피격 시 은박 찢기는 소리·불티, 사망 시 후드 안 빛 꺼짐.
  - 공격: 개공봉으로 앞 찌르기.
  - 능력치(임시): 경비 = Lab Subject(scale 1.5, 체력 280, 걷기 5/추격 18, 피해 16·사거리 8·windup 0.6·cooldown 1.6, xp 40, lvl 4), 덩치 = Bloated Husk(체력 3000, 6/16, 피해 10·사거리 6·windup 0.6·cooldown 1.8, xp 60, lvl 3) 단 scale 1.8.
  - **외형 완료 (2026-11-20, Studio 버전 74)**: `ServerStorage.Assets.Enemies.FurnaceWarden`(메쉬 32) / `FurnaceTender`(30 — `__Plate` 2개 뺌). 속성 Variant = Warden / Tender. 메쉬 모델 assetId 118317063967066, 삼각형 12,210.
    - 구성: 넉넉한 은박 코트(앞 여밈 띠·버클, 무릎까지 자락 + 앞트임 + 찢겨 늘어진 끝), 벨트·주머니, 후드(머리 + 어깨 덮개, 안쪽 Dark 마개), 금빛 방열 유리창(Glass 0.35) + 흘러내린 방울 4 + 유리 뒤 주황 빛(Neon), 넓은 소매(안쪽 Dark), 벙어리 장갑, 덧신 + 고무 밑창, 등 공기통(노랑 Paint) + 밸브 + 등·어깨끈 + 후드로 가는 호스. 개공봉: 오른손에서 앞으로 약간 들어 겨눈 자세(방향 (0,-0.90,0.44)), 손잡이 천, 끝 0.45 달아오름(Neon). Warden 전용 Plate: 왼팔 방열판 방패(리벳·손잡이), 가슴판(리벳).
    - 재질: Suit = 새 은박 PBR(구김·세로 누빔·그을음·열 변색·찢긴 속감, 금속성 0.85). **첫 업로드는 얼룩이 잘고 진해 위장복처럼 보여서** 그을음·변색 노이즈를 크고 옅게 바꿔 Color·Rough·Metal 다시 올림(Normal 은 그대로). Rod·Plate(틴트 150) = Hook Hauler Rust, Tank = Hook Hauler Paint. ID → `exports/texture_ids.json` `FurnaceTender`.
    - 스크립트: `scripts/furnace_tender_build.py`, `tex_kit.foil_mat`. 키트 보강: `monster_kit.reset` 이 다른 몬스터의 `__` 메쉬도 지움(이름 충돌로 `.001` 붙던 문제), `drip`·`rod` 추가.
    - 겹침: 개공봉↔소매(각도 조정)·공기통↔등(뒤로 뺌)·어깨 보호대↔팔/후드(가슴판으로 교체) 해결. 남은 것은 손잡이·끈·가슴판 가장자리 접촉, 코트 안쪽 마개↔다리(속, 안 보임).
  - **소리·효과·공격 애니·정의·배치 완료 (2026-11-20, Studio 버전 75) → 3번 몬스터 끝 (능력치만 임시)**
    - **공격 애니메이션** `FurnaceTenderAttack` assetId **140592601845071** (두 변형 공용): 0 → 0.35 당김 → 0.45 멈춤 → **0.55 찌름(마커 "Impact")** → 0.78 → 1.25 복귀. `scripts/furnace_tender_anim.py`. FK: 찌를 때 끝이 몸 앞 4.6·땅 위 2.7, 거의 수평(팔을 뻗으면 막대가 들려서 손목 -62°로 보정). 첫 시도는 너무 높고(3.4) 왼쪽으로 비껴서 몸 비틀기를 줄임.
    - **소리·효과** `scripts/furnace_tender_fx.lua` (두 모델): Sound 12(ProSoundEffects — 내열복 스침(마른 잎 소리 대체)·발소리, 숨 2(낮은 음), 개공봉 지글 반복, 찌르는 바람, 타격 지글+쇠, 피격 은박 찢김+지글, 사망 찢김+긴 식는 소리), 개공봉 끝 PointLight TipGlow(경비 7·덩치 9) + Embers + Heat 연기 + `LanceTip` ThrustSparks, 유리창 뒤 VisorGlow, 코트 HitSparks. 효과음 12개 PreloadAsync Success.
    - **TenderFX 스크립트**: 걸음 소리, 숨소리(추격 중 더 자주), 피격 불티·찢김, 공격 시 바람 → "Impact"에 지글·쇠·불티·끝 빛 번쩍. 시체 복제본: 유리창 빛·끝 열기가 3~4초에 식어 꺼지고(Neon → 플라스틱/금속) 개공봉·손잡이(덩치는 방패도)가 떨어짐.
    - **적 정의**: Factory 모듈에 `furnace_tender`(scale 1.5, attackHitTime 0.55, Lab Subject 임시값), `furnace_warden`(scale 1.8, Bloated Husk 임시값) 추가 → 모듈 항목 5개.
    - **Warden 수정 (2026-11-21, Studio 버전 80, 사용자 지시 "경비답게 낮추고 활동범위를 그 건물 전체 수준으로")**: Bloated Husk 값(체력 3000 — 원래 스킬 훈련용)이라 보스(2500)보다 단단했음 → 체력 900, 피해 18·사거리 7·windup 0.65·cooldown 1.8, 걷기 6/추격 16, lvl 5, xp 80, knockbackResist 0.5. **aggroRange 75, leashDistance 250**(스폰이 건물 북·남 끝이라 건물 286×287 거의 전체를 쫓음, 먼 반대편 모서리 일부(~277)만 밖). 대상 없을 때 어슬렁거리는 범위(WANDER_RADIUS 12)는 공용 EnemyConfig 전체값이라 안 바꿈.
    - **순찰 추가 (2026-11-21, Studio 버전 81, 사용자 지시)**: 공용 코드 2곳을 최소 수정 — `Services.Enemy` spawnAt 이 스폰 지점 속성 `WanderCenter`(Vector3)·`WanderRadius` 를 모델 속성으로 복사, `EnemyAI` 배회가 그 속성이 있으면 그 중심·반경에서 목적지를 고름(없으면 기존대로 home 주변 12 → **다른 적 동작 변화 없음**). 두 파일 require 문법 확인 OK. Warden 2지점에 WanderCenter (-881, y, 1433)·WanderRadius 85 설정. 순찰 지점 ↔ 집 거리 최대 208 < leash 250. 보스 마당 바닥 격자 레이캐스트: 중심 ±90 대부분 빈 바닥, 북·남 끝은 벽(남쪽 가운데 정문만 열림), 중심 북쪽 +30 줄에 높은 구조물 띠(양 끝만 통과) → 그쪽 목적지면 잠깐 막혔다가 다음 배회로 넘어감. MoveTo 8초 제한·걷기 6 때문에 한 번에 약 48씩 끊어 걸음. **Services 패키지도 게시 필요.** 플레이 확인 안 함.
    - **배치**: 보스 마당 lab_subject 2지점(4마리) → furnace_tender, bloated_husk 2지점(2마리) → furnace_warden. 원래 값 `OldEnemyId`.
    - 게시 필요(사용자): Shared(Factory 모듈) + `ServerStorage.Assets.Enemies`(FurnaceTender·FurnaceWarden). 플레이 테스트 안 함.
- **4번 보스 = The Foreman (새 보스, 컨셉 확정 2026-11-20)** — Gear Head 자리(Boss_GearHead (-879,1450)) 1마리. 기존 Gear Head(다른 맵 공유)는 안 건드림.
  - 설정: 사고 날 공장 문을 잠그고 작업자들을 안에 가둔 현장 반장. 무너진 천장 크레인 운전실과 하나로 용접된 채 확성기로 '작업 재개'를 외침('STILL INSIDE'·'DAY 112' 낙서의 원인). 1~3번 몬스터는 모두 그가 가둔 작업자.
  - 외형: 일반 적의 약 2배(scale 2). 하얀 반장 안전모, 찢긴 반장 조끼, 등에 박힌 깨진 크레인 운전실(벽에 날짜 센 빗금), 오른팔 = 크레인 붐 팔 + 쇠사슬 끝 거대 갈고리, 왼손에 녹아 붙은 확성기.
  - 패턴(사용자 결정: 새 패턴도 만들기 + 졸개 소환 추가): 재사용 KnuckleSmash(갈고리 내려찍기)·GrinderCharge(돌진). **새 모듈(공용 Services EnemyAI.Patterns 에 파일 추가만, 기존 패턴 수정 없음)**: ① 갈고리 던지기(직선, 맞으면 끌어당김, 옆으로 피함) ② 확성기 사이렌(2페이즈, 앞 부채꼴 음파로 밀쳐냄 + **Slag Walker 2마리 소환**, 동시 졸개 수 제한) ③ 짐 낙하(분노, 강철 코일이 표시 자리에 떨어짐, 빈칸으로 피함).
  - 페이즈: 2페이즈 60% 운전실 유리 깨짐, 분노 25% 확성기 떨어져 나감(사이렌 대신 짐 낙하).
  - 능력치(임시): Gear Head 값(체력 2500, 걷기 8/추격 16, 어그로 60, 공격 30·사거리 14·windup 0.8·cooldown 2, slam, xp 800, 보스 드랍) 단 scale 2.
  - 게시 필요: Services(새 패턴 모듈), Shared(정의), Assets.Enemies(모델).
  - **외형 완료 (2026-11-20, Studio 버전 76)**: `ServerStorage.Assets.Enemies.Foreman` (메쉬 39, 삼각형 16,268, scale 1 기준 3.9×5.8×2.8 → 게임 scale 2). 메쉬 모델 assetId 79783467643444. `scripts/foreman_build.py`.
    - 구성: 배 나온 거구 + 작업복, 반장 조끼(앞 열림)·반사 띠·흰 명찰, 벨트·버클·**열쇠 꾸러미(문을 잠근 열쇠)**, 불독 턱·찌푸린 이마·벌린 입·눈빛, 하얀 반장 안전모(SmoothPlastic). 왼팔: 사람 팔 + 주먹에 녹아 붙은 빨간 확성기(`LeftHand__Mega`, 나팔 안 Dark, 테두리·용접 슬래그 Rust). 오른팔: 위팔 + 용접 고리(볼트) → 팔꿈치 아래 크레인 붐 트러스(노랑 Paint, 지그재그 가새) → 도르래 블록·도르래 → 사슬 → 거대 갈고리(`RightHand__Hook`, scale 1.5). 등: 박힌 크레인 운전실(노랑 판·창 기둥·지붕, 옆·뒤 유리 `UpperTorso__Glass` Glass 0.45, 왼쪽 옆판에 날짜 센 빗금 5개 묶음×15, 안에 의자·레버, 레일 바퀴 2, 용접 받침).
    - 부위 파괴용 이름: 2페이즈 `UpperTorso__Glass`, 분노 `LeftHand__Mega`(+ LeftHand__Dark, LeftHand__Rust).
    - 재질은 전부 기존 텍스처 재사용(Cloth·Skin = Slag Walker, Vest·Rust·Paint = Hook Hauler) → 새 업로드 없음.
    - 겹침: 운전실 앞판↔등(박힌 것, 의도), 붐↔용접 고리(팔꿈치), 확성기↔손, 사슬↔도르래·갈고리 접합만.
    - **확인용 캡처 실패**: Studio 뷰포트가 검은 화면만 찍힘(창이 안 그려지는 상태) → 외형은 Blender 렌더(`exports/_preview/fm_*.png`)로만 확인, Studio 화면 확인은 다음에.
  - **패턴·애니·소리·정의·배치 완료 (2026-11-20, Studio 버전 79) → 4번 보스 끝 (능력치·패턴 수치는 임시, 플레이 확인 전)**
    - **동작 3종** (`scripts/foreman_anim.py`, FK 확인): `ForemanSmash` **121917648178069** (갈고리 머리 위 → 0.80 "Impact" 내려찍기, 갈고리 땅 위 0.15·앞 2.9; 기본 attack + KnuckleSmash + CoilDrop 시작), `ForemanThrow` **120213273357659** (0.90 "Throw", 1.75 "Pull"), `ForemanSiren` **118908082714018** (확성기 앞으로 겨눔, 0.90 "Siren", 2.4까지 유지). 쉬는 자세에서 갈고리가 땅을 0.36 뚫어서 `RightHand__Hook` 용접 C0 를 +0.45 올림(모델 속성 HookLifted).
    - **새 패턴 모듈 3개** — 공용 `ServerScriptService.Services.Enemy.EnemyAI.Patterns` 에 **파일만 추가**(기존 패턴·BossBrain 수정 없음). 원본 `scripts/foreman_patterns/*.lua`:
      - `ForemanHookThrow`: GrinderCharge 처럼 lane 예고로 조준(lockTime 고정) → 손 갈고리 숨기고 복제 투사체 + Beam 사슬로 직선 비행 → 맞은 플레이어 피해 + 보스 앞(stopDistance)까지 끌어당김 → 회수 → Opening.
      - `ForemanSiren` (2페이즈만, forced 20초): 앞 넓은 lane 예고 → 피해 + 밀쳐냄 + 모델 속성 Siren → `Enemy.spawnTemporary("slag_walker")` 2마리(보스가 부른 졸개 살아 있는 수 최대 4, `SummonedBy` 속성). Enemy 는 순환 require 를 피하려고 run 안에서 불러옴. 확성기가 떨어져 나가면 스스로 안 씀.
      - `ForemanCoilDrop` (분노, forced 13초): 내려찍기 → 범위 32 안 플레이어 발밑 + 보스 주변에 6곳, 주황 원 예고 1.3초(0.15초 간격) → 강철 코일(원통+구멍+띠) 낙하·피해·먼지·소리 → 6초 장애물 후 사라짐.
      - **플레이어 밀기/당기기**는 기존 시스템에 없어서 패턴 안에서 플레이어 HumanoidRootPart 에 서버가 `LinearVelocity`(이름 ForemanShove)를 짧게 붙이는 방식. **실제 게임에서 클라이언트에 잘 먹히는지는 플레이 확인 필요.**
      - 편집 모드에서 가짜 ctx 로 3개 패턴 run 을 끝까지 실행 → 오류 없음, 갈고리 복원·투사체/코일 정리 확인(사이렌 소환은 편집 모드라 빼고 실행). 플레이 테스트 안 함.
    - **소리·효과** `scripts/foreman_fx.lua`: Sound 15(ProSoundEffects 위주 + 사이렌 106098533112635 "T1300 Siren Slow", 유리 6737581507 "Glass Break 2" — 이 둘은 일반 사용자 업로드), 확성기 입 `MegaMouth` SoundWave·WaveDust, 운전실 `CabLight`(2페이즈 주황, 분노 빨강 깜빡임), 갈고리 `HookTip` SmashSparks·SmashDust, 사슬 HitSparks. `ForemanFX` 스크립트: 쿵 발소리+사슬, 확성기 지직+으르렁, 피격 쇠 소리, Impact 쾅·먼지·불티, Siren 속성 → 사이렌·음파, Phase 2 유리 깨짐 / Phase 3 확성기 뜯김. 시체: 큰 쇳소리, 갈고리·사슬 떨어짐. 15개 PreloadAsync Success.
    - **정의** Factory 모듈 `foreman` (boss, scale 2, Gear Head 임시 능력치·드랍, phases 0.6/0.25, groggy, breakParts [2] 유리 / [3] 확성기, patterns 5개: KnuckleSmash·ForemanHookThrow·GrinderCharge·ForemanSiren·ForemanCoilDrop). 그로기 전용 동작은 없음.
    - **배치**: `Boss_GearHead` → 이름 `Boss_Foreman`, EnemyId foreman (OldEnemyId gear_head).
    - **게시 필요(사용자)**: Services(패턴 3개), Shared(Factory 모듈), Assets.Enemies(Foreman 외 1~3번 모델).
  - **보스 수정 (2026-11-21, Studio 버전 82, 사용자 지시)**: "밀기는 근접해서 공격하면, 당기기는 당긴 다음 확정 공격 연계, 당기기는 빨간 표시 이후 더 빠르게, 보스 사이즈 훨씬 크게"
    - **크기**: scale 2 → **3.5** (키 약 19.1, 폭 13.8, HRP 바닥 위 11.2). 거리·범위 수치 ×1.75 — attack.range 24, KnuckleSmash maxRange 28·reach 16·radius 13, GrinderCharge 24~60·length 60·width 13·speed 48, Siren length 42·width 26, CoilDrop area 40·minDistance 14(코일 반경 5 그대로).
    - **근접 밀치기 새 패턴 `ForemanShove`** (`scripts/foreman_patterns/ForemanShove.lua`): 대상이 20 안 + 보스가 최근 1.5초 안에 피해를 입었으면 **먼저** 씀(priority). 보스 주변 주황 원(반경 16) 0.5초 예고 → 피해 15 + 바깥으로 75 밀어냄(위로 22). 쿨다운 5, 빈틈 0.6. 한 번 쓰면 피격 기록을 지워 다시 맞아야 또 씀. 동작은 내려찍기 재사용.
    - **사이렌 밀쳐내기 뺌**: 정의에서 push 삭제 → 피해 + 소환만. 패턴은 push 가 있을 때만 밀어냄.
    - **갈고리 던지기**: 빨간 예고 0.9 → **0.55초**(lockTime 0.6 → 0.3), 갈고리 속도 80 → 140, 끌기 피해 12. **확정 연계**: 끌려온 플레이어를 수평으로 붙잡고(LinearVelocity Plane `ForemanPin`) 0.45초 뒤 예고 없는 내려찍기 피해 35 (그 플레이어만, 패링으로만 막힘). stopDistance 10 = 내려찍기 갈고리가 닿는 거리.
    - 보스 크기와 상관없게 **높이 판정을 바닥 기준**으로 바꿈(갈고리는 바닥 + 3.5 높이로 날아감, 사이렌·밀치기도 바닥 기준). 공용 GrinderCharge 는 HRP 기준(허용 10)인데 scale 3.5 에서 차이 약 8.2라 평지에선 맞음.
    - **공용 BossBrain 최소 수정**: 패턴 모듈에 `canUse(ctx, p, distance)` 가 있으면 그것도 통과해야 고르고, 정의에 `priority = true` 면 조건이 맞을 때 weight 보다 먼저 고름. 둘 다 없으면 기존과 같음(다른 보스 영향 없음).
    - 편집 모드 가짜 ctx 확인: choose(10) 피격 전 KnuckleSmash / 피격 후 ForemanShove / choose(40) ForemanHookThrow, Shove·HookThrow run 오류 없음, 갈고리 복원·투사체·예고 정리 확인. 플레이어가 없어 연계 피해·밀기·붙잡기는 **플레이 확인 필요**. 스폰 위 20 이내 낮은 천장 없음(동쪽 50 원통 콜라이더만).
    - 게시 필요: Services(BossBrain + 패턴 4개), Shared(Factory 모듈).
  - **사이렌 소환 고침 (2026-11-21, Studio 버전 84, 사용자: "사이렌 때 몬스터가 안 나옴, 사방에서 종류별 2마리씩 6마리")**: 정의 `summons = { slag_walker 2, molten_walker 2, hook_hauler 2 }`, summonRadius 20, maxSummons 6. 종류를 섞어 보스 둘레 6방향에 고르게(벽이 있으면 벽 앞 3, 최소 4). 이전 코드는 실패해도 조용히 넘어가서(pcall require 결과를 안 봄) 원인을 못 찾음 — 플레이 Output 에 오류 기록 없음. 이제 실패하면 `[ForemanSiren] ...` 경고가 뜸 → **다음 플레이에서 안 나오면 Output 확인**. 보스 자리 기준 6지점 모두 빈 평지 확인.
  - **보스 외형 문제 (사용자: "그냥 네모난 자동차 같음")**: Studio 캡처로 확인(이번엔 캡처 됨) — 메쉬는 제대로 로드됨(RenderFidelity Precise 로 바꿔도 같음). 몸이 R15 상자 비율(네모난 어깨·몸통·다리) + 등의 노란 상자 운전실 때문에 상자 덩어리처럼 보였음.
  - **보스 외형 재제작 v2 (2026-11-21, Studio 버전 86, 사용자 선택 "괴물 실루엣으로 재제작")**: `scripts/foreman_build.py` 다시 씀(git 이전 버전 = v1). 메쉬 모델 assetId **97537500825700**, 40조각, 삼각형 약 21,000, scale 1 기준 3.95×5.97×3.19.
    - 실루엣: 앞으로 숙인 가슴 + 머리 뒤로 솟은 둥근 혹 등(단면 expo 1로 둥글게), 오른쪽이 더 큰 승모근(비대칭), 머리는 리그 Head 보다 낮고 앞(HZ -0.22, HY -0.30)에 파묻힘 + 튀어나온 아래턱·송곳니(`Head__Helmet` 안), 우그러진 안전모. 팔·허벅지 훨씬 굵게.
    - 운전실: 작게(0.66×0.46×0.52 반치수) 만들어 노이즈로 우그러뜨리고 -38°/22°/-14° 기울여 혹 왼쪽 뒤에 반쯤 파묻음, 가장자리를 살(`UpperTorso__Skin`)이 덮음. 혹에서 파이프·철근 6개(끝 뭉툭), 혹을 가로지르는 사슬, 어깨 슬래그 껍질. 붐 팔엔 유압 호스 `RightLowerArm__Rust` (새 조각, Rust SA 복사).
    - 갈고리·붐·확성기 위치는 v1과 같음 → 동작 3종 그대로 씀. 갈고리 용접 C0 +0.45(HookLifted) 다시 적용.
    - Studio 교체: v1 모델을 복제해 리그·Humanoid·소리 15·ForemanFX 유지, `__` 메쉬만 새것으로(재질·SA·색 이름별 복사, MegaMouth·HookTip·CabLight·HitSparks 옮김, MegaMouth/HookTip 위치 새 크기로 다시 계산). **운전실만 어둡게**: `UpperTorso__Paint` SA.Color (115,92,72), `UpperTorso__Glass` (70,60,50) 투명 0.25 (밝은 노란 상자 → 녹슨 잔해).
    - 이전 모델 백업: `ServerStorage.Foreman_v1_backup` (패키지 밖, 확인 후 지워도 됨).
    - 편집 모드 가짜 ctx 로 ForemanShove·ForemanHookThrow 다시 실행 → 오류 없음.
    - 게시 필요: `ServerStorage.Assets.Enemies`(Foreman v2).
  - **보스 거대 덩어리 버그 고침 (2026-11-21, Studio 버전 107, 사용자 플레이 스크린샷: 보스 마당이 검은 덩어리로 뒤덮임)**: v2 교체 때 `__` 메쉬 40조각이 모두 **MeshSize × 3.5** 크기로 들어가 있었음(리그는 정상 → 메쉬가 몸의 2.4배, 게임 scale 2 에서 약 19×22×15). 이 상태로 Enemies 패키지 v5 에 게시돼 실제 게임에 나옴. → 40조각 Size = MeshSize, 메쉬 안 첨부점도 같은 비율로 줄임(MegaMouth z −1.46 → −0.42, HookTip y −2.90 → −0.83). 모델 크기 3.95×5.97×3.19 (v2 설계값과 같음). 모델 속성 `MeshSizeFixed`. `foreman_build.py` 1줄 주석의 "게임에서 scale 3.5"는 틀림 — 게임 scale 은 정의의 2, Studio 에 넣을 때 메쉬는 MeshSize 그대로.
    - **사용자 할 일: 공장 place 에서 `ServerStorage.Assets.Enemies` 패키지 게시 (v6)**, 마을 place 는 "최신 패키지 가져오기"만.
  - **진짜 원인 = Humanoid 자동 크기 조정 (2026-11-21, Studio 플레이로 확인)**: 위 수정 뒤에도 플레이에서 보스가 덩어리 + Furnace Warden 이 커 보임. 서버에서 재 보니 `Enemy.create` 의 `model:ScaleTo(scale)` 뒤 workspace 에 넣는 순간 **Humanoid.AutomaticScalingEnabled 가 `__` 메쉬(Weld "Attach" 로 붙은 비신체 파트)만 scale 배 한 번 더 키움** (리그 파트는 그대로). scale ≠ 1 인 공장 적만 해당: hook_hauler 1.5 (8.2 → 9.5), furnace_tender 1.5, furnace_warden 1.8 (9.8 → 11.3), foreman 3.5 (20.9 → 39.4). v2 템플릿 메쉬가 3.5배로 들어가 있던 것도 아마 같은 현상을 템플릿에 구워 넣은 것.
    - 고침: 공장 적 템플릿 6개(SlagWalker·MoltenWalker·HookHauler·FurnaceTender·FurnaceWarden·Foreman) Humanoid **AutomaticScalingEnabled = false**. 플레이 확인: foreman 15×22.5×11.8, furnace_warden 7.7×10, furnace_tender 6.4×8.4. Studio 저장 버전 109. **새 적을 scale ≠ 1 로 만들 때 꼭 끌 것.**
    - 기존 적(GearHead 등, 다른 맵 공유)은 안 건드림.
- **능력치 확정 (2026-11-21, Studio 버전 98, 사용자 선택 "추천안(보통)")** — 레벨 8 맵 Steelworks 기준, 갓운드 중간 난이도. Factory 모듈의 "임시값" 경고 삭제.
  | 적 | Lv | 체력 | 걸음/추격 | 피해·사거리·windup·cooldown | 경험치 | 금화 | 넉백 저항 |
  |---|---|---|---|---|---|---|---|
  | slag_walker | 7 | 260 | 5/17 | 13·5.5·0.58·1.8 | 45 | 3~9 | 0.2 |
  | molten_walker | 8 | 210 | 6/21 | 15·5.5·0.58·1.5 | 48 | 3~9 | 0 |
  | hook_hauler | 10 | 560 | 5/15 | 26·9·0.8·2.3 | 90 | 5~14 | 0.6 |
  | furnace_tender | 10 | 420 | 5/18 | 22·8.5·0.6·1.7 | 75 | 5~14 | 0.3 |
  | furnace_warden | 12 | 900 | 6/16 | 24·7·0.65·1.8 | 140 | 8~20 | 0.5 |
  | foreman (보스) | 14 | 6000 | 8/16 | 34 (근접 기준) | 1500 | 250~420 | 1 |
  - 보스 패턴 피해: 내려찍기 34, 갈고리 끌기 14 + 확정 연계 40, 돌진 40, 밀치기 18, 사이렌 15, 코일 45. 아이템 드랍은 그대로. Slag·Molten 의 windup 을 동작 타격 순간(0.58)에 맞춤. 게시 필요: Shared.
- **몬스터 디자인 1~4번 모두 끝 (2026-11-20).** 남은 것: 사용자 능력치 결정, 패키지 게시, 실제 플레이 확인(소리 크기·효과 양·보스 패턴 난이도·플레이어 밀기 동작).
- 기존 적 구조(참고): 모델 = `ServerStorage.Assets.Enemies.<Model>` R15 Humanoid 리그 + 몸에 용접한 MeshPart(SurfaceAppearance), 정의 = `ReplicatedStorage.Shared.Data.Enemies` 모듈(id, name, model, scale, level, maxHealth, walkSpeed, chaseSpeed, aggroRange, attack{damage,range,windup,cooldown}, xp, drops, animations, gearSpin 등). 공통 좀비 애니메이션 = EnemyConfig.ZOMBIE_ANIMATIONS. 새 적 정의 추가 = 공용 패키지(Shared) 수정 → 사용자 게시 필요. 보스 Gear Head(gear_head) 모델 = Motor6D 리그 + 파티클 7·PointLight 2.
- 새 적이 생기면 `Workspace.FactoryEnemies.EnemySpawns`의 해당 지점 `EnemyId`를 바꾼다.

## 0. 꼭 알아야 할 것

1. 작업 place = **"공장"** (placeId 129022811153240, 같은 universe 10768843846). Studio MCP `list_roblox_studios`에서 이름 "공장".
2. 이 place는 도시 place 복사본 → 운하 창고 존·에셋 원본(`ServerStorage.Assets.CanalWarehouse`)·게임 스크립트가 다 들어 있음. **지우지 않고** 그 위에 공장 시설을 더함.
3. 운하 창고 존 규칙(그룹 소유 업로드, 축 매핑, CollisionFidelity 불가 → 투명 충돌, CorrodedMetal 분홍 문제, 보이는 수면 Y ≈ -1.75)은 `Zone_CanalWarehouse_이어서할일.md` 0장과 동일하게 적용.
4. 단계마다: 사용자에게 결정 질문 → 작업 → 한국어 보고(보고용 스크린샷 없음, 문제 의심 시에만 확인용) → 이 문서 갱신 → 커밋·푸시.
5. **사용자 지시 (2026-11-18)**
   - 배치 수정(도로·나무·옛 LotDressing 손보기 포함)은 **알아서 결정**해도 됨. 목표는 맵 전체가 잘 어우러지는 것.
   - **Blender에서 부재끼리 겹치게(뚫고 나오게) 만들지 말 것** — Roblox에서는 못 고침. 지붕 밑 서까래가 지붕판을 뚫는 식의 실수 금지.
     → 만든 뒤 반드시 BVHTree `overlap` 검사(오브젝트 쌍별)로 확인하고, 접합부(파이프→밸브/탱크, 바닥 위 기둥)만 남길 것. 지붕·벽은 "부재 꼭짓점이 지붕 밑면/벽 안쪽면을 넘는지" 수치 검사.
6. **대각선 길 방향 주의**: 대각선 길(A 구역을 나누는 길)은 **X − Z ≈ −1811** 선을 따라 남서→북동으로 남. 길 양옆 보도 포함 폭 약 ±25. (이전 문서의 "x+z=0"은 삼각 부지의 대칭축이었고 길이 아님.) 남동쪽 삼각 부지 = `Lot_026` (꼭짓점 ≈ (-1015,739), (-739,739), (-739,1015)).
7. **텍스처 업로드 함정**: Open Cloud로 올린 이미지는 심의(Approved) 전에 SurfaceAppearance에 붙이면 Studio가 그 ID를 "실패"로 캐시해서 다시 붙여도 하얗게 나옴. 같은 파일을 다시 올리면 기존 ID로 합쳐짐 → **픽셀 1개 바꿔 재업로드**해야 새 ID가 나옴. 붙이기 전에 `GET /assets/v1/assets/<이미지ID>` 의 `moderationState: Approved` 확인할 것. (`PreloadAsync`는 편집 모드에서 정상 이미지도 Failure로 나와서 판단 기준으로 못 씀 → 화면으로 확인)
8. **사용자 지시: Studio에서 직접 플레이(캐릭터/NPC 걷기) 테스트는 하지 말 것** (2026-11-18). 경로·충돌은 편집 모드 레이캐스트·충돌 파트 수치로 확인하고 "플레이 테스트 안 함"이라고 보고.
   (참고 기록) 이 게임은 스폰 위치가 없고 스크립트가 플레이어를 옮김 → 플레이어 캐릭터로 테스트하면 엉뚱한 데로 감. 서버에서 `Players:CreateHumanoidModelFromDescription`으로 **NPC를 만들어** `MoveTo` 경로 테스트. Pathfinding은 좁은 계단(폭 5.5)에서 NoPath가 나와 신뢰 불가.

## 1. 현재 상태

- 계획서 + 미리보기 이미지(`images/Factory_preview_*.png`).
- 블록아웃 `Workspace.FactoryBlockout` (구역 C, E 나머지, F~H, K_Common). D(2026-11-18)·B(2026-11-19)는 삭제(실제 에셋으로 교체). **A_BlastFurnace 블록아웃은 삭제**(옛 위치 백업: `ServerStorage.A_BlastFurnace_OldBlockout`).
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

### 용광로 1차 수정 — 2026-11-18 (사용자 요청 순서 1→2→3)
1. **버려진 연출**: 열풍 본관을 x −19..−10 구간에서 끊어 찢어진 끝 2개 + 바닥에 떨어진 토막(`BfPlate_FallenMain`, 충돌 원통 `FallenMain`). 본관을 x 22까지 늘려 4번 열풍로 출구관이 허공에서 끝나던 문제 수정, 받침 포털 x 12 추가(`BfSteel_Supports2`). 바닥 잔해: 슬래그 덩어리 7, 출선장 +x 문 밖 굳은 쇳물 웅덩이, 드럼통 4(1개 넘어짐), 끊어진 작은 배관 2, 콘크리트 조각 3, 안전모 4. 큰 것만 충돌(슬래그·드럼·조각). 패치 모델 assetId 82155023500304 (메쉬는 `BlastFurnace_01`에 합침). Blender 컬렉션 `BF_Patch1`.
2. **텍스처 색 v3**: 열풍로(StoveGrey) 녹 얼룩 약하게 + 이음매에서 흘러내린 녹물·때 줄기, 노란 난간(RailYellow) 큰 얼룩 → 작은 칩·옅은 녹, 본체(FurnaceRust) 푸른 열변색·그을음 추가. 컬러맵만 교체(노멀/거칠기/금속은 그대로). 굽기 머티리얼 `BAKE2_BfPlate`/`BAKE2_BfSteel`.
3. **블록아웃 정리**: `K_Common.Chimney_A`를 출선장 옆에서 열풍로 1번 서쪽 (-934.5, 793.1)로 이동. `FactoryBlockout` 파트 전부 투명도 0.55·그림자 끔(자리 표시로만 보이게). 하늘의 색깔 공(빨강·초록·파랑)은 블록아웃이 아니라 게임 쪽 표시라 건드리지 않음.
4. 출선장 내부 조명·바닥 얼룩은 **조명 단계(계획서 6장 6단계)**로 미룸.
- 플레이 테스트 안 함(사용자 지시). 새 잔해·배관은 Blender BVH 겹침 검사로 접합부 외 겹침 없음 확인.
- 아직 없음: 대피 안내판·경고 표지(데칼 업로드 필요) → 소품 단계.

### 냉각탑 `CoolingTowers` — 2026-11-18 완성 (구역 E, 옛 공원 Lot_057)
- 결정(사용자): 1기 온전 + 1기 부분 붕괴 / 높이 ~110, 밑동 지름 ~76 / 밑동 다리 사이로 진입(등반 불가) / 이번 범위는 냉각탑만(발전동·변압기·굴뚝은 중간 에셋 단계).
- 위치: `Workspace.FactoryContent.E_PowerPlant.CoolingTowers_01`, 원본 `ServerStorage.Assets.Factory.CoolingTowers`. 그룹 소유 모델 assetId **133122925803824**. 블록아웃 냉각탑 삭제.
- 좌표계: `BlenderFrame` = `CFrame.new(-200, 0.5, 1157)` (회전 없음). Blender (x,y,z) → 월드 `(-200 - x, 0.5 + z, 1157 + y)`. 서쪽 탑(온전) Blender (50,0) = 월드 (-250, 1157), 동쪽 탑(붕괴) Blender (-50,0) = 월드 (-150, 1157).
- 형상: 쌍곡선 셸 `r(z) = 24·√(1+((z−80)/54.6)²)` (z 13 r 38 → 목 z 80 r 24 → 꼭대기 z 110 r 27.4), 두께 0.8, 64분할×22단. 밑동: 고리보(z 11.4..13) + X자 대각 기둥 48개(발 24곳, 다리 사이 입구 폭: 지면 ~9, 머리 높이 ~4.9) + 기초 고리. 내부: 마른 수조 바닥, 8스터드 격자 기둥 숲(높이 13.4) 위 냉각 충전재 판(z 13.4..16.4, 일부 빠져 바닥에 떨어짐) + 살수 배관.
- 붕괴 탑: 남서쪽(Blender −45°, 월드 기준 남서) 약 156° 범위가 높이 17~110으로 들쭉날쭉 무너짐 + 철근 노출, 그쪽 다리·고리보·기초 일부 없음, 안쪽·바깥쪽 잔해 더미(높이 6.25 / 8.5), 바깥에 셸 조각 3. 붕괴 쪽 충전재·기둥 제거(부러진 기둥 1개).
- 급수 배관(BfPlate FurnaceRust) 2줄: 동쪽 탑 → 발전동 블록아웃, 서쪽 탑 → 남쪽 둘레(y −70) → 발전동. 높이 2.6, 반지름 1.8, 콘크리트 받침.
- 텍스처: 새 **CtConcrete** 타일 (16스터드/타일, 빗물 자국·거푸집 줄 4스터드 간격·이끼·박리). 셸 UV = 원주 14타일 × 높이/16. MetalnessMap 없음(전부 0이라 기존 검은 이미지와 합쳐져 ID가 안 나옴 → 생략). 충전재 FillPack(52,54,52) Plastic.
- 메쉬 15개, 삼각형 약 20,600. 충돌 600개 (`CoolingTowers_01/Colliders`): 셸 띠(32분할×4단, 붕괴 높이 반영), 다리, 고리보, 기초, 바닥, 기둥, 충전재, 잔해(계단식 원통), 조각, 배관.
- 확인(플레이 테스트 안 함): 레이캐스트로 다리 사이 입구 서쪽 23/24, 동쪽 22/24 통과(막힌 곳 = 배관 앞·잔해 더미). Spawn2 (-300,1200)과 실제 거리 약 28.
- 부지 정리: `LotDressing.Lot_057`의 초록 나무·덤불·탑 근처 풀 74개 삭제(백업 `ServerStorage.LotDressing_Lot057_Backup`), 마른 나무·가장자리 풀 64개 남김. `Lot_057` 재질 LeafyGrass → Concrete, 색 (128,126,118) (Lot_026 색은 이 부지에서 너무 하얗게 보여서 어둡게).
- Blender: 씬 FurnaceWork, 컬렉션 `CoolingTowers`, 굽기 머티리얼 `BAKE_CtConcrete`. 붕괴 높이 배열은 씬 속성 `CT_HBRK`.
- 남은 것: 안쪽 잔해 더미가 밝게 떠 보임(텍스처 대비 부족) → 소품·마감 단계에서 색 낮추기 검토.

### 압연 공장동 `RollingMill` — 2026-11-18 완성 (구역 D, Lot_027)
- 결정(사용자): 본동 240×56(처마 31.5, 용마루 38, 천장 크레인) + 북쪽 보조동 240×24(모터실·제어실·창고) / 실내 압연 라인 + 엄폐물 많이, 입구 3곳 이상 / 제어실 2층(바닥 10, 유리창, 계단) + 크레인 점검 통로(높이 20) / 동쪽 끝 40스터드 지붕 붕괴. 지붕·크레인 위 등반 불가.
- 위치: `Workspace.FactoryContent.D_RollingMill.RollingMill_01`, 원본 `ServerStorage.Assets.Factory.RollingMill`. 그룹 소유 모델 assetId **81148178409570**. 블록아웃 `FactoryBlockout.D_RollingMill` 삭제. Studio 저장 버전 19.
- **좌표계**: `BlenderFrame` = `CFrame.new(-881, 0.5, 1157)` (회전 없음). Blender (x,y,z) → 월드 `(-881 - x, 0.5 + z, 1157 + y)`. Blender x = 동서(+x = 서쪽, x −120 = 동쪽 끝 = 월드 X −761), y = 남북(+y = 북쪽). 본동 y −40..16(월드 Z 1117..1173), 보조동 y 16..40(Z 1173..1197). 부지 여백: 남북 각 40, 동서 각 22. 배관 다리 기둥(`K_Common.PipeBridge_AtoD_PostB`, Z 1080)과 겹치지 않음(건물 남쪽 벽에서 37 떨어짐).
- 구성 (Blender 좌표):
  - 본동: 기둥 H형 x = −117.8, −100..100(20 간격), 117.8 / 남 y −35..−32.6, 북 8.6..11. 벽 = 콘크리트 기초벽(z 0..4) + 골판 외벽(SidingTeal) + 샛기둥·띠장(z 8.5/16/28.7), 창 띠(남 z 21..27, 북 23..27.5, 깨진 유리 30~35%). 트러스 11개(Pratt) + 도리 + 지붕판(RoofZinc, 채광판 일부, 빠진 판 12장) + 물받이·선홈통.
  - 주행보(판형 거더) z 23..26.6, 레일 y −31.1 / 7.1, x −101.2..119. 천장 크레인(RailYellow) x 35, 훅 z 13..19.5 (스탠드 사이 위).
  - 점검 통로: 남 y −38.2..−35, 북 y 11..14.2, 바닥 z 20, x −84..118.2, 안쪽 난간(높이 3.5). 올라가는 길: 남쪽 사다리 x 90(바닥→20), 북쪽은 계단 → 층계참(z 10) → 사다리 x −30(10→20), 붕괴부 남쪽 통로가 꺾여 내려온 경사판(잔해 더미 M5에서 20까지).
  - 계단: x −51.6..−35.6, y 3..8 (단 높이 1, 디딤 1.6) → 층계참 x −35.6..−26, y 3..15.7, z 10 → 제어실 문 x −32..−28.
  - 압연 라인 y −12: 스탠드 5기 x 60/44/28/12/−4 (하우징 높이 16 + 스크루다운 19.5, 4단 롤), 스핀들 → 피니언 → 모터(y 0..8.2). 롤러 테이블 상면 4.7: 입측 x 64..84, 90..110(사이 84..90 건너는 틈), 스탠드 사이 4개, 출측 x −8..−40, −46..−66(−46..−40 틈). 코일러 x −78..−67.
  - 엄폐물: 코일 피라미드(남 x 30..42, x −48..−42 / 북 x 97, 높이 11.4), 세운 코일 6개(높이 4), 슬래브 더미 4곳(높이 2.5~6), 나무상자·공구함. 떨어진 훅 블록 + 와이어 로프 (x −86 근처).
  - 보조동(CtConcrete 벽, 지붕 z 22 + 난간벽 23.2): 모터실 x 0..120(MG 세트 3, 변압기 2), 배전반실 x −60..0(1층, 캐비닛 2열) / 제어실 x −60..0 2층(바닥 z 10, 본동 쪽 유리창 z 10.5..15.5, 콘솔·의자·캐비닛), 창고 x −120..−60(선반 4, 드럼, 상자). 칸막이 x 0, −60(문 y 18..22).
  - 붕괴부 x −120..−84: 지붕판 가장자리 들쭉날쭉(−84..−79.5), 휜 트러스(x −100, 기둥 머리에서 잔해 위로 기울어짐), 쓰러진 트러스 반쪽(바닥에 눕힘), 떨어진 남쪽 주행보, 늘어진 도리 3·지붕판 3, 벽 윗부분 찢김(남 11~31.5, 북 23.2~31.5, 동쪽 박공 10.5~21 + 큰 구멍 y −30..−8). 잔해 더미 M1 (−98,−14) 높이 6.5 / M2 (−108,9) / M3 (−112,−20) / M4 건물 밖 (−125,−19) / M5 (−92,−35.5).
- 입구: 남쪽 큰 문 x 2..18(셔터가 z 9에 걸림, 아래로 통과), 남쪽 쪽문 x −52..−48, 서쪽 박공 큰 문 y −34..−16(높이 15.5), 동쪽 붕괴 구멍, 보조동 북쪽 3곳(x 77..83 셔터 6.5, x −40..−36, x −96..−90) → 보조동-본동 문 x 26..34, x −76..−70.
- 메쉬 38개(전부 `__NoCollide`), 삼각형 37,582. 텍스처는 새로 올리지 않고 기존 승인 세트 복제: `RmSiding_`→WhSiding(SidingTeal/RoofZinc), `RmSteel_`→BfSteel(SteelOxide/RailYellow), `RmPlate_`→BfPlate(FurnaceRust/StoveGrey), `RmConc_`→CtConcrete. 나머지(`RmMisc_`/`RmGlass_`)는 색+재질(DarkSteel Metal, DiamondPlate, Glass 0.4, 채광판 0.35, FadedBlue/Olive/ShutterOrange Metal, Wood WoodPlanks, Hazard). CorrodedMetal 없음.
- 충돌 `RollingMill_01/Colliders` 333개(투명 Part/원통, 사다리 TrussPart 2개). **`NoClimbCeiling`** = 본동 전체 z 27..27.5 투명 판 → 통로(20)에서 크레인·주행보·트러스·지붕으로 못 올라감 (CanCollide라 레이캐스트에도 걸림 — 실내에서 위로 쏘면 27에서 막힘). 휜 트러스·늘어진 지붕판·도리는 충돌 없음(장식).
- 확인(플레이 테스트 안 함): 겹침 검사 = 면을 0.03 줄인 BVH 쌍별 검사 → 트러스-기둥 머리, 꺾인 도리·통로 끝(같은 부재가 휘는 곳), 계단 난간 기둥-측판, 잔해 더미 속 조각만 남김(그 외 5건 수정). Studio 레이캐스트: 입구 9곳 통과, 벽 막힘, 통로 면 z 20, 계단 면 경사(x −43.6에서 5.0), 층계참 10, 제어실 바닥 10, 붕괴 경사판, 천장 27, 지붕 36.6, 보조동 지붕 22.
- Blender: 씬 FurnaceWork, 컬렉션 `RollingMill`. 충돌 정의는 씬 속성 `RMC_A/B/C/D/E/G`(행 = 종류, 중심, 반크기, 축), 메쉬 바운딩 `RM_bbox`. 스크립트는 모듈별(A 벽·골조, B 지붕, C 통로·계단, D 보조동, E 라인·크레인·코일, G 붕괴)로 다시 만들 수 있게 짜 놓았지만 .blend 저장은 안 됨.
- 남은 것(마감 단계): 실내 조명(주황 작업등)·먼지, 바닥 기름 얼룩 데칼, 안전 표지. 남쪽 큰 문 셔터 색이 텍스처 없는 단색이라 필요하면 WhSiding ShutterOrange UV로 교체 검토.

### 압연 공장동 주변 야적장 `RollingMillYard` — 2026-11-19 (사용자: "건물 말고 도로 전까지 주변이 비어 보임")
- 위치: `Workspace.FactoryContent.D_RollingMill.RollingMillYard_01` (+ `GeneratorContainer`), 원본 `ServerStorage.Assets.Factory.RollingMillYard`. 그룹 소유 모델 assetId **128051664628393**. 좌표계는 본동과 같음(`BlenderFrame` = `CFrame.new(-881, 0.5, 1157)`). Studio 저장 버전 21.
- 구성 (Blender 좌표, 부지 x −142..142, y −80..80):
  - 바닥: 건물 남·북 콘크리트 앞마당(y ±40..46), 정문 앞 아스팔트 진입로 x 0..20(노란 차선·중앙 점선·문 앞 빗금), 보수 패치 6, 기름 얼룩 7. `Lot_027` 색을 (128,126,118)로 어둡게(냉각탑 부지와 같은 톤).
  - 남쪽: 배관 랙(포털 3개 y −71/−59/−47, x −9/−1) — 배관 3줄(z 18.35)이 배관 다리 블록아웃 기둥(y −75.5)에서 남쪽 벽(y −40)까지, 밸브 1. 경비 초소 x 23..29, y −77..−71(서쪽 문, 깨진 창) + 차단기(팔 떨어짐). 방호벽 5(진입로 안 1개는 지그재그용). 가로등 5 + 쓰러진 가로등 1. 볼라드 4, 드럼 5. 야외 코일 야적장 x −110..−62(눕힌 코일 2줄, 피라미드 높이 11.3, 세운 코일 3, 나무 굄목). 코일 3개 실은 평판 트레일러 x 30..70, y −69..−61(높이 10.6). 슬래브 더미 3(받침목 포함, 높이 2.8~6).
  - 북쪽: 변압기 야드(팔리세이드 울타리 x 30..96, y 50..78, 높이 8, 남쪽 문 x 74..86 열림) 안에 변압기 3기(방열판·부싱·컨서베이터), 케이블 덮개. 물탱크 2기 (−12,64)/(6,64) r 6 높이 17.6 + 보조동 북벽으로 들어가는 배관. 고철 스킵 2. 팔레트·드럼·IBC 탱크(창고 문 옆). 강제통풍 냉각탑 x 100..132, y 52..76(높이 15.7, 팬 스택 2) + 보조동으로 가는 배관(z 1.2).
  - 서쪽: 서쪽 큰 문에서 나오는 철도 인입선(레일 y −27.3/−22.7, x 120.2..141.6) + 차막이 + 슬래브 2장 실은 평판 화차 x 120.8..139.2(문 남쪽 y −34..−28.6, 북쪽 −21.4..−16로 드나듦). 공기 탱크 (132,44).
  - 동쪽: 20ft 컨테이너(기존 `CanalWarehouse.Container_20ft` 복제, x −140..−128, y 15..39), 떨어진 지붕판 3, 고철 더미 (−132,−67).
  - 건물 북쪽 앞마당(y 40..46)은 동서로 막힘 없이 통하는 통로 → 모터실 문(x 77..83)은 이 통로로 들어감.
- 메쉬 44개(전부 `__NoCollide`), 삼각형 21,664. 텍스처는 기존 승인 세트 복제(`Ry` 접두사: RySiding→WhSiding, RySteel→BfSteel, RyPlate→BfPlate, RyConc→CtConcrete). 새 단색 키: Asphalt(Asphalt 재질), Oil, Paint, Insulator, Fence, Plastic. 바닥 판(앞마당·아스팔트·차선·기름)은 그림자 끔.
- 충돌 `RollingMillYard_01/Colliders` 87개 (컨테이너는 원본 충돌 파트 그대로).
- 확인(플레이 테스트 안 함): 겹침 검사 = 줄인 BVH 쌍별(본동 포함) → 배관→탱크, 밸브→탱크, 차단기 팔→기둥, 스킵 안 고철끼리만 남김(드럼·패치·냉각기 배관·차막이·고철 조각 수정). 레이캐스트: 정문 진입로, 쪽문, 서쪽 문(화차 양옆), 북쪽 통로 전체, 모터실·배전반실·창고 문, 동쪽 붕괴 구멍 모두 통과.
- Blender 컬렉션 `RollingMillYard`, 충돌 정의 씬 속성 `RMY_1..4`, 바운딩 `RMY_bbox`.
- 주의: 이번 작업 중 Studio에서 `FactoryContent.D_RollingMill` 폴더와 `ServerStorage.Assets.Factory.RollingMill` 사본이 사라져 `RollingMill_01`이 Workspace 바로 아래에 있었음(Team Create 저장 버전 20이 끼어 있음 — 다른 세션/되돌리기 추정). 모델 자체는 온전해서 폴더·사본을 다시 만듦. 다른 세션에서 같은 place를 만질 때 주의.
- 배관 랙의 배관 3줄 중 2줄은 남쪽 끝이 블록아웃 배관 다리(폭 5) 옆에서 끝남 → 배관 다리 키트 만들 때 이어 붙일 것.

### 코크스로 `CokeOvens` — 2026-11-19 완성 (구역 B, Lot_012)
- 결정(사용자): 블록아웃대로 배터리 1기 / 배터리 위 통로는 양 끝 계단 2곳 / 부분 파손 / 배터리·기계·탑·컨베이어 + 주변 부지까지 전부.
- 위치: `Workspace.FactoryContent.B_CokeOvens.CokeOvens_01`, 원본 `ServerStorage.Assets.Factory.CokeOvens`. 그룹 소유 모델 assetId **74375219503174**. 블록아웃 `B_CokeOvens` 삭제. `Lot_012` 색 (96,92,86)(석탄 먼지 톤). Studio 저장 버전 22.
- **좌표계 (회전 있음)**: `BlenderFrame` = `CFrame.new(-1157, 0.5, 881) * CFrame.Angles(0, π/2, 0)`. Blender (x,y,z) → 월드 `(-1157 + y, 0.5 + z, 881 + x)`. 즉 Blender **+x = 북쪽(+Z)**, **+y = 동쪽(+X)**. 부지 = x −142..142, y −80..80. Spawn1 = Blender (119, −43) → 반경 20 안에 충돌 파트 0.
- 구성 (Blender 좌표):
  - 배터리: 오븐 40칸 (피치 4.5, 중심 x = −101 + 4.5(i+0.5)), 본체 x −101..79 + 끝벽 x −105..−101 / 79..83, 폭 y ±13(문·버크스테이까지 ±14.2), 기초 z 0..4(콘크리트), 오븐 z 4..17(Brick 재질), 문 2.2×10(StoveGrey) + 걸쇠, 버크스테이(SteelOxide) z 4..18.5. 상부 덱 z 17: 장입구 뚜껑 3열, 장입차 레일 y ±6(x −103..112.8), 상승관 80개 + 구즈넥, 가스 집합관 2줄(y ±10.8, z 19.6, r 1.6), 덱 가장자리 난간. 남쪽 끝 크로스오버 → 가스관(z 25)이 동쪽 부지 끝(y 80)까지, 받침대 y 30/50/70.
  - 벤치: 압출기 쪽 y −18..−13, 코크스 쪽 y 13..18, 높이 4(점프로 오를 수 있음). 압출기 선로 y −27.5/−22.5(x −112..95), 가이드카 레일(코크스 벤치 위), 소화차 선로 y 22.5/27.5(x −138..95, 소화탑 안까지).
  - **파손 연출 = 13번 오븐(x −40.25)에서 압출 중 멈춤**: 압출기 램이 오븐 안 y −9까지 들어가 있고 반대편 문이 열린 채 가이드카 슈트로 코크스가 쏟아져 땅에 더미(높이 3). 압출기 쪽 문은 벤치에 떨어져 있음. 소화차(x −67..−49)는 북쪽 대차만 레일 위, 남쪽 대차는 탈선해 침목 위로 빠짐(9° 틀어짐). 5번 오븐(코크스 쪽)·28번 오븐(압출기 쪽) 문도 떨어짐(열린 오븐 안에 코크스 덩어리).
  - 장입차(x 25..37) 상부 레일 위 정지 — **상부 덱을 남/북 두 구역으로 나눔**(옆으로 지나갈 틈 없음, 각 구역은 그쪽 계단으로).
  - 계단탑: 남쪽 x −121..−105, y −10..−2 / 북쪽 x 83..96, y 9..17 (2구간 스위치백, 층계참 z 8.5, 끝 z 17 → 끝벽 위로 연결).
  - 석탄탑: 기둥 4 (x 96..98/110..112, y ±8.5..10.5), 벙커 z 26..40, 헤드하우스 z 40..47.4(RoofZinc). 장입차 레일 다리 x 83..113(z 15.4..17, 난간) + 포털 x 90. 컨베이어 갤러리: 헤드하우스(110, 0, 44) → 부지 북쪽 끝(142, 0, 36), 받침 x 128, 옆판 일부 떨어짐 → 원료 야적장(C) 컨베이어 만들 때 여기서 이어 붙일 것.
  - 소화탑: x −140..−124, y 17..33, 높이 44 + 벽돌 굴뚝 52. 북쪽 면에 소화차 입구(y 20..30, 높이 12), 높이 30..40 루버(나무 배플, 일부 빠짐), 북동 모서리 윗부분 무너짐.
  - 주변: 코크스 와프(y 31..42 경사, 위에 코크스 층) + 벨트 컨베이어(y 43..46, x −98..63), 코크스 더미 4(높이 3~6), 문 수리 창고(x −70..−30, y −72..−52, 지붕 13.5, 예비 문 더미), 예비 버크스테이, 사무동(x 20..36, y 52..64, 높이 8.5, 문·깨진 창), 드럼·가스병, 가로등 6, 코크스 먼지 바닥 패치.
- 메쉬 40개(전부 `__NoCollide`), 삼각형 40,930. 텍스처는 기존 승인 세트 복제(`Ck` 접두사: CkSiding→WhSiding RoofZinc, CkSteel→BfSteel, CkPlate→BfPlate, CkConc→CtConcrete). 새 단색 키: **Brick**(Brick 재질 96,62,50), **Coke**/CokeDust(Slate 40,38,37 / 48,45,43).
- 충돌 `CokeOvens_01/Colliders` 167개. `NoClimbCeiling` = 배터리·레일 다리 위 z 26..26.5 (덱 17에서 장입차·가스관·석탄탑으로 못 올라감).
- 확인(플레이 테스트 안 함): 줄인 BVH 쌍별 검사 → 남긴 것은 코크스 더미가 레일·침목을 덮은 곳, 램 머리-램, 계단 난간 기둥-측판, 갤러리 프레임-지붕, 탈선 대차가 레일 머리에 얹힌 곳(0.06). 레이캐스트: 덱 17, 천장 26, 계단 각 구간·층계참·끝 층계참, 레일 다리, 양 벤치 4, 와프 경사, 석탄탑 밑 통과.
- Blender: 컬렉션 `CokeOvens`, 충돌 정의 씬 속성 `CKC_1..4`, 바운딩 `CK_bbox`.
- 작업 중 실수 기록: 정점 범위 선택으로 부재를 지울 때 이웃 부재(가스 받침대, 포털 면)가 같이 지워짐 → 지운 뒤 `is_boundary` 검사로 열린 면이 없는지 꼭 확인할 것.

### 맵 밖으로 떨어지는 문제 수정 — 2026-11-19 (Studio 저장 버전 24)
- 원인: "공장" placeId(129022811153240)가 `ReplicatedStorage.Shared.Config.PlaceConfig`/`RaidConfig.MAPS`에 없어서 **Raid 서비스의 도착 배치(RaidSpawns로 옮기기)가 돌지 않음** + Workspace에 SpawnLocation이 하나도 없음 → 캐릭터가 원점(0,0) 근처에 생기는데 거기는 땅이 없는 허공. 추가로 맵 가장자리(땅 X −1252..52, Z 323..1252) 밖이 허공인데 막는 벽이 없었음.
- 수정 (게임 코드는 건드리지 않음):
  - `Workspace.FactorySpawns`: 투명 SpawnLocation 18개(Neutral, 6×1×6, CanCollide 끔, 보호막 없음). 구역별 빈 땅 자동 탐색(땅 높이 0.5인 CityRoadNetwork 위 + 16×12×16 안에 충돌 파트 없음 + 서로 60 이상 떨어짐). Roblox가 이 중 무작위로 골라 스폰 = 랜덤 스폰.
  - `Workspace.RaidSpawns`에도 같은 16곳 추가(Spawn1·Spawn2 포함 총 18) → 나중에 이 place를 레이드 맵으로 등록하면 Raid 서비스가 그대로 씀.
  - `Workspace.MapBoundary`: 투명 경계벽 4개(땅 끝에서 1 바깥, 높이 300, Y −20..280).
- 확인: 스폰 18곳 모두 아래 땅(Y 0.5) 레이캐스트 OK, 경계벽은 다른 파트와 겹침 0. 플레이 테스트는 안 함(사용자가 테스트).
- **남은 결정(사용자)**: 레이드 맵으로 정식 등록하려면 `PlaceConfig`에 FACTORY id, `RaidConfig.MAPS`에 이름·lifetime·maxPlayers·보스·탈출구 등을 넣어야 함 → 게임 코드 변경이라 따로 결정 필요. 등록 전까지 이 place에는 레이드 타이머·도착 연출·탈출구가 없음.
- 사용자 참고(2026-11-19): 랜덤 스폰이라 스폰 고정 위치 없음 / **보스전용으로 넓지만 실내이거나 건물로 둘러싸인 공간 필요** → 후보: 가스 홀더(F) 내부, Lot_025 둘러싸인 마당.

### 북쪽 확장 땅 + 보스 마당 블록아웃 — 2026-11-19 (Studio 저장 버전 25)
- 사용자: 가스 홀더(F)는 보스전에 너무 좁음 → **최소 3~4배**, 건물로 둘러싼 마당 방식, 북쪽 새 땅으로 결정. 가스 홀더는 일반 랜드마크로 유지.
- **새 땅** (X −1250..−584, Z 1250..1588, 운하 서쪽만): 기존 도로·보도·연석·부지 부품을 복제해 만듦(속성 `NorthExt=true`, `CityRoadNetwork` 각 폴더 안).
  - 동서 골목 Z 1250..1278 (X −1250..−585) — 기존 남북 길 끝(Z 1250)과 T자로 이어짐. 남북 길 연장: 골목 X −1064..−1036, 큰길 X −726..−674 → Z 1588까지(막다른 길).
  - 새 부지: `Lot_058` X −1237..−1077 (빈 땅), **`Lot_059` X −1023..−739 (보스 마당)**, `Lot_060` X −661..−597 (빈 땅), 모두 Z 1291..1576, 둘레 보도 12 + 연석. 차선 점선 추가.
  - 경계벽: `North` 를 X −581..57 (Z 1255)로 줄이고 `North_Ext` (Z 1593, X −1257..−577), `East_ExtJog` (X −579, Z 1253..1595) 추가, `West` 를 Z 1595까지 늘림.
  - 스폰 3곳 추가(`FactorySpawns.FSpawn_N1..3`, `RaidSpawns.Spawn_N1..3`): (−1157,1433), (−629,1433), (−1157,1340). 보스 마당 안에는 스폰 없음.
- **보스 마당 블록아웃** `FactoryBlockout.N_BossYard`: 안마당 **220×220** (X −991..−771, Z 1323..1543, 약 4.8만 스터드² ≈ 가스 홀더 부지의 4.6배), 하늘 열림.
  - 둘레: 북 저장 창고동(높이 42), 서 고철 처리동 2동(26), 동 높은 담+배관 랙(22), 남 작업동 2동(24) + 남문 위를 지나는 컨베이어 갤러리(Y 27.5..33.5).
  - 입구 3곳: **남문** X −893..−869 (폭 24, 동서 골목에서) / **서문** Z 1430..1452 (폭 22, 골목 X −1050) / **동문** Z 1414..1436 (폭 22, 큰길 X −700).
  - 안쪽 엄폐 자리: 고철 더미 2, 슬래브 더미 2, 코일 줄, 쓰러진 크레인 다리. 중앙 약 100×100은 비움.
  - `ArenaBounds` (투명·충돌 없음, 220×60×220, 속성 `Purpose=BossArena`) — 보스 스크립트 영역 판정용.
- 확인(플레이 테스트 안 함): 새 땅 6스터드 격자 레이캐스트 구멍 0, 스폰 3곳 아래 땅 Y 0.5, 세 입구 수평 레이 통과, 둘레 건물 막힘, 블록아웃이 다른 콘텐츠와 겹침 없음.
- 운하 동쪽(X −584 너머)은 확장 안 함.

### 보스 마당 `BossYard` — 2026-11-19 완성 (구역 N, Lot_059, Studio 저장 버전 26)
- 결정(사용자): 둘레 건물+마당 전부 / 낮은 고지 몇 곳(지붕·담 위는 못 올라감) / 고철 야적 마당 분위기.
- 위치: `Workspace.FactoryContent.N_BossYard.BossYard_01` (+ `ArenaBounds` 같은 폴더로 옮김), 원본 `ServerStorage.Assets.Factory.BossYard`. 그룹 소유 모델 assetId **129813453500277**. 블록아웃 `FactoryBlockout.N_BossYard` 삭제.
- **좌표계**: `BlenderFrame` = `CFrame.new(-881, 0.5, 1433.5)` (회전 없음). Blender (x,y,z) → 월드 `(-881 - x, 0.5 + z, 1433.5 + y)`. Blender +x = 서쪽, +y = 북쪽. 부지 x ±142, y ±142.5, 안마당 x ±110, y ±110.
- 구성 (Blender 좌표):
  - 바닥: 콘크리트 판 20×20 (이음매 0.3, 7장 깨짐), 기름 얼룩 14, 크레인 레일 x ±96 (y −106..106) + 차막이.
  - 북 고철 창고동 y 110..142.5, 처마 36·용마루 42 (박공, SidingTeal 벽 + RoofZinc 지붕 + 콘크리트 기초벽), 앞면 기둥 20 간격, 창 띠 z 26..31(깨진 유리), 셔터 4 (지면 x ±90, 하역장 x ±30 — x 30 셔터는 반쯤 열림·안은 막힘). **하역장(고지) x −60..60, y 98..110, 높이 6** + 양끝 계단(x ±60..70) + 캐노피 z 16.8.
  - 서 고철 처리 창고 2동 (x 110..142, y −110..−3 / 19..109.2): 앞이 트인 외쪽지붕(앞 22·뒤 26, 지붕판 12% 빠짐). 남동: 콘크리트 칸막이 4 (높이 6) + 칸마다 고철 더미. 북동: 압축기(베일러, 높이 8 + 호퍼 13) + 유압 실린더 + 압축 고철 더미. 서문 y −3..19 (기둥 2 + 쓰러진 철망 문).
  - 동 담: 프리캐스트 콘크리트 판 + H 기둥(높이 20.5, 일부 윗부분 깨짐) + 철조망, 안쪽 배관 랙(x −127/−115, 기둥 18.5, 배관 5줄, 동문 위 트러스), 끊어져 늘어진 배관 1 (y 50..60), 밸브 1. 동문 y −19..3 (기둥 + 열린 미닫이 철문).
  - 남 작업동 2동 (y −142.5..−110, x ±12..142, 높이 24 + 난간벽): 창 2줄, 하역 셔터, 쪽문. **하역장(고지) x ±36..80, y −110..−98, 높이 6** + 양끝 계단 + 캐노피 z 17. 지붕 위 환기 설비·전환탑(x ±64..76, 높이 38) + 그 사이 컨베이어 갤러리(z 27..33, 남문 위 트러스). 남문 x −12..12 (미닫이 문 하나는 밖으로 밀려남, 하나는 쓰러짐).
  - 마당 가운데: 겐트리 크레인(다리 x ±96, y 30, 거더 z 42..47, 운전실, 트롤리 x −60) + 자석이 고철 더미 P2 위에 매달림(z 11.4, 고철 붙어 있음). 고철 더미 P1 (62,−60) 높이 11 / P2 (−58,30) 9 / P3 (66,62) 7. 압축 고철 더미 3, 코일 4개(받침목), 슬래브 더미 2, 스킵 2(하나 넘어져 쏟아짐), 드럼통 묶음 3, 조명탑 4(높이 35), 20ft 컨테이너 2 (기존 `CanalWarehouse.Container_20ft` 복제, (−40,75) 10°, (35,−85)).
- 메쉬 98개(전부 `__NoCollide`), 삼각형 약 25,600. 텍스처는 기존 승인 세트 복제(`BySiding`→WhSiding, `BySteel`→BfSteel, `ByPlate`→BfPlate, `ByConc`→CtConcrete). 새 단색 키: DarkInterior, ScrapDirt(Ground), ScrapBlue, ScrapRed(Metal).
- 충돌 `BossYard_01/Colliders` 162개 (Blender 씬 속성 `BYC_Fl/Nh/Ws/Ew/Sw/Cr/Yd`, 형식 `B 중심 크기 rz ry rx` / `C 끝점1 끝점2 반지름`, Blender 좌표). 메쉬 바운딩 `BY_bbox`, 컨테이너 위치 `BY_containers`.
- 확인(플레이 테스트 안 함): 겹침 검사(줄인 BVH 쌍별) → 고철 더미 속 조각, 바닥 판에 묻힌 받침, 자석-붙은 고철, 배관-배관 연결만 남김. 레이캐스트: 세 문 통과, 마당 가운데에서 360° 수평 레이(높이 3/8/14) → 문 3곳 방향 외에는 모두 막힘, 하역장 계단 3, 바닥 0.2, 고철 더미 P1 꼭대기 10.1, 서쪽 칸막이 6, 북 창고 지붕 42. 마당 안 스폰 0.
- Blender: 컬렉션 `BossYard` (작업 중 다른 컬렉션은 뷰 레이어에서 제외해 둠). .blend 저장 안 됨.
- 남은 것(마감 단계): 실내 없음(창고동·작업동은 닫힌 껍데기), 조명탑 불빛·먼지, 경고 표지. 보스 스크립트가 `ArenaBounds` 쓰도록 연결은 게임 코드 결정 필요.
- **노멀 수정(2026-11-19)**: `prism()`으로 만든 면 일부가 뒤집혀 있었음(북 창고 박공·지붕, 남 컨베이어 갤러리 지붕) → Roblox에서 바깥에서 안 보였을 것. Blender에서 노멀 재계산 후 그 3개 MeshPart만 새 업로드(assetId 117260856713752)에서 교체. **앞으로 `flush()`에서 `bmesh.ops.recalc_face_normals` 필수** (이후 에셋은 적용함). 확인법: 섬별 부호 있는 부피가 음수면 뒤집힘.

### 화물 철도 야드 `RailYard` — 2026-11-19 (Lot_058, Studio 저장 버전 28)
- 결정(사용자): Lot_058 = 화물 철도 야드. 배치 세부는 알아서.
- 위치: `Workspace.FactoryContent.N_RailYard.RailYard_01`, 원본 `ServerStorage.Assets.Factory.RailYard`. assetId **109095229523492**.
- **좌표계**: `BlenderFrame` = `CFrame.new(-1157, 0.5, 1433.5)`. Blender (x,y,z) → 월드 `(-1157 - x, 0.5 + z, 1433.5 + y)`. 부지 x ±80 (+x = 서쪽), y ±142.5.
- 구성 (Blender 좌표): 선로 3줄 x 55 / 32 / −30 (자갈 노반·침목·레일, 양끝 차막이). 가운데 서비스 도로 x −14..18 (스폰 2곳이 이 위: (0,−0.5), (0,−93.5)).
  - T1 (x 55): 호퍼 화차 4량 (y −54/−22/10/42, 높이 10.5 + 광석, 하나는 빈 차). 앞쪽 끝 사다리(TrussPart)로 **광석 위(11.3)까지 올라감 = 고지**.
  - T2 (x 32): 유조차 3량 (y −105/−73/−41) + 탈선해 옆으로 누운 유조차 (42.5, 52) + 바닥에 쏟아진 광석.
  - T3 (x −30): 평판 화차 3량 (y 10 코일 3개 / y 42 20ft 컨테이너(기존 `Container_20ft` 복제) / y 74 슬래브), 유개 화차 (y −80, 플랫폼 쪽 문 열림 → 안으로 들어감).
  - 하역 플랫폼 x −64..−35.5, y −125..−35, 높이 4 (북쪽 경사로 WedgePart, 남쪽 계단 3단) + 캐노피(z 12~13.4) + 화물 창고 x −79..−64 (셔터 3, 닫힘, 지붕 20).
  - 서쪽 띠: 신호소 x 62..76, y 100..116 (벽돌 1층 + 2층 운전실 높이 8, 바깥 계단 8단 → 층계참 → 문, 안에 레버 틀), 레일·침목 더미, 공구 창고, 드럼통. 가로등 4 (x −16), 급수 기중기 (21, 25).
- 메쉬 48개, 삼각형 약 20,000. 충돌 80개 (B/C + T(사다리 TrussPart) + W(경사로 WedgePart, `-1` = 높은 쪽이 Blender −y)). Blender 씬 속성 `RdC_Tk/Pf/Wg/Pr`.
- 새 단색 키: Ballast(Slate), Sleeper(WoodPlanks), RailSteel, Ore(Slate), Brick, Asphalt, Paint.

### 작업자 배랭·사무동 `WorkerCamp` — 2026-11-19 (Lot_060, Studio 저장 버전 30)
- 결정(사용자): Lot_060 = 작업자 배랭·사무동.
- 위치: `Workspace.FactoryContent.N_WorkerCamp.WorkerCamp_01`, 원본 `ServerStorage.Assets.Factory.WorkerCamp`. assetId **139088336377439**.
- **좌표계**: `BlenderFrame` = `CFrame.new(-629, 0.5, 1433.5)`. Blender (x,y,z) → 월드 `(-629 - x, 0.5 + z, 1433.5 + y)`. 부지 x ±32 (+x = 서쪽 = 큰길 쪽), y ±142.5.
  - 2층 숙소동 x 10..26, y −122..−26: 방 20개 (9.6×15, 1층 바닥 0.3 / 2층 10.6), 앞(동쪽) 문·창, 열린 방 8곳 들어감(2층 침대·사물함). 2층은 바깥 복도(x 6..10, 높이 10.6, 난간) + 양끝 계단 10단.
  - 2층 사무동 x 6..26, y 20..60: 1층 출입문 열림, 접수대·책상·서류장, 내부 계단(x 19.4..25.2) → 2층(9.6) 사무실, 깨진 창.
  - 식당 x −4..26, y 72..132: 단층 박공(처마 11, 용마루 16), 남쪽 문 열림, 긴 테이블 6줄(하나 넘어짐), 배식대, 주방.
  - 마당: 농구장 (x −24..2, y −20..16, 스폰 (0,−0.5)이 여기), 버려진 버스, 버스 정류장, 급수탑(높이 ~24), 빨랫줄, 가로등 3, 쓰레기통, 동쪽 철망 울타리(높이 7, 틈 y −8..8 / 64..70).
- 메쉬 51개, 삼각형 약 10,200. 충돌 379개 (벽은 문·창 구멍마다 나눔). Blender 씬 속성 `WkC_Dm/Of/Cn/Yd`.
- 확인(플레이 테스트 안 함): 겹침 검사 → 접합부(난간 기둥, 가로등 팔, 버스 바퀴, 넘어진 테이블)만 남김. 레이캐스트: 복도 10.6, 계단, 2층 방 10.6, 사무동 계단·2층 9.6, 사무동·식당 문 통과. **스폰 21곳 모두 16×12×16 안에 충돌 파트 없음.**

### 가스 홀더 `GasHolder` — 2026-11-19 (구역 F, Lot_043, Studio 저장 버전 31)
- 결정(사용자): 기둥식 프레임(전통형) / 중간 높이 통로(20)까지만 올라감.
- 위치: `Workspace.FactoryContent.F_GasHolder.GasHolder_01`, 원본 `ServerStorage.Assets.Factory.GasHolder`. assetId **116657429672262**. 블록아웃 `F_GasHolder` 삭제, 부지 안 옛 LotDressing 31개는 `ServerStorage.LotDressing_Lot043_Backup`으로 옮김. `Lot_043` Ground → Concrete (128,126,118).
- **좌표계**: `BlenderFrame` = `CFrame.new(-410, 0.5, 1157)`. Blender (x,y,z) → 월드 `(-410 - x, 0.5 + z, 1157 + y)`. 부지 x ±33, y ±80. 홀더 중심 Blender (0, 20) = 월드 (−410, 1177).
- 구성: 아래 콘크리트 수조 r 23 (높이 10, 기둥형 보강 24) + 철판 벨 r 22 (z 10..30, 반쯤 내려간 상태, 리브 24·보강 링 2) + 지붕 원뿔(꼭대기 34.4). 철골 기둥 12개 r 25.5 (높이 62) + 가로 띠장 z 20/40/60 + X 가새(한 칸 빠짐, z 40 띠장 하나 부러져 늘어짐) + 꼭대기 링. 가이드 롤러 12.
  - **둘레 통로** r 26.4..29.4, 높이 20, 노란 난간(높이 3.5). **나선 계단** r 29.4..32.4, 20단(각도 −149°→−86°, 남서쪽에서 시작) → 통로 난간 틈 −97°..−78°로 연결. 그 위(기둥·가새·벨)는 못 올라감(가새는 충돌 없음).
  - 부지: 가압동 x −22..2, y −48..−26 (높이 10, 남쪽 문 열림, 압축기 2·제어반, 깨진 창) → 주 가스관(x −7, r 1.2)이 수조로 들어감. 북쪽 밸브실 x 2..14, y 58..70 (서쪽 문 닫힘) + 배관(x 8) + 통기관(높이 33). 동쪽으로 나가는 배관(y 68, 높이 14, 받침 3개) — 부지 동쪽 끝(x −33 = 월드 X −377)에서 막힘 플랜지 → **배관 다리 키트에서 길 건너로 이어 붙일 것**. 실 포트, 드럼통, 가스병 거치대, 가로등 2.
- 메쉬 28개, 삼각형 약 10,700. 충돌 178개. Blender 씬 속성 `GhC_Hd/St`.
- 확인(플레이 테스트 안 함): 겹침 검사 → 벨 리브·링, 배관-수조/받침, 가로등 팔만 남김(배관이 밸브실 문을 지나던 것 수정). 레이캐스트: 통로 20, 계단 꼭대기 20·중간 10, 계단→통로 수평 통과, 벨 지붕 34.4, 가압동 바닥 0.3. 스폰(Spawn_F1 포함) 주변 충돌 없음.
- 남은 것: 가스 경고 표지(데칼), 통로 조명.

### 원료 야적장 `RawYard` — 2026-11-19 (구역 C, Lot_013, Studio 저장 버전 33)
- 결정(사용자): 긴 더미 2줄 / 스태커-리클레이머 붐이 더미에 처박힘 / 컨베이어는 부지 안 + 코크스로 갤러리 연결까지(용광로로 가는 긴 다리는 컨베이어·배관 키트 단계).
- 위치: `Workspace.FactoryContent.C_RawYard.RawYard_01`, 원본 `ServerStorage.Assets.Factory.RawYard`. assetId **107849528077747**. 블록아웃 `C_RawYard`의 더미·스태커·라벨 삭제(`Conveyor_ToFurnace1/2` 블록아웃은 키트 단계용으로 남김). `Lot_013` 색 (96,92,86).
- **좌표계**: `BlenderFrame` = `CFrame.new(-1157, 0.5, 1130)`. Blender (x,y,z) → 월드 `(-1157 - x, 0.5 + z, 1130 + y)`. 부지 x ±80 (+x = 서쪽), y ±107.
- 구성 (Blender 좌표):
  - 석탄 더미 (서쪽) 능선 x 40, 반폭 24, 높이 14, y −72..78 (+ 원뿔 끝) / 철광석 더미 (동쪽) 능선 x −42, 반폭 22, 높이 13, y −58..84. 경사 약 30° → **걸어 올라가는 고지**(충돌 = WedgePart 2개씩 + 끝 계단식 원통).
  - 스태커 레일 x ±3 (y −90..100, 콘크리트 보 + 차막이). 야드 벨트 컨베이어 x −12..−8 (높이 2.4, y −98..93).
  - 스태커-리클레이머 (y −15): 대차·포털·선회 덱(높이 6.6, 난간, +x 쪽 계단 6단), 마스트(22), 운전실, 평형추 붐, **주 붐이 K(−18,−12,9.5)에서 꺾여 버킷 휠(−30,−10,6.2)이 광석 더미에 반쯤 묻힘**. 붐 위(원통 충돌)로 걸어 올라갈 수 있음 → 덱·마스트까지, 그 이상 없음.
  - 환적탑 x −8.5..8.5, y −107..−92 (기둥 4 + 띠장, 위 z 30..52 함석 헤드하우스). 남쪽 면 구멍(x ±6.2, z 34.2..47.8)에 **코크스로 석탄탑 갤러리 끝(월드 Z 1023.5, X −1163..−1151, Y 34.8..47.5)이 들어옴**. 슈트가 벨트 시작점으로 내려옴.
  - 소품: 불도저(66,−88), 관리 초소(−66,−95), 조명탑 2, 석탄 먼지 바닥, 벨트 옆 떨어진 석탄.
- 메쉬 40개, 삼각형 약 14,000. 충돌 49개. Blender 씬 속성 `RwC_Pl/Cv/Sr/Pr`. 쐐기 형식 `W 중심 크기 방향(+x/−x/+y/−y = 높은 쪽)`.
- **스폰 이동**: `Spawn_C1`이 벨트 위였음(Blender x −7) → (−1164, 1180)으로 옮김(FactorySpawns·RaidSpawns 둘 다). 스폰 21곳 모두 주변 비어 있음.
- 확인(플레이 테스트 안 함): 겹침 검사 → 더미에 묻힌 붐·휠, 붐 접합부, 불도저 블레이드만 남김(슈트-환적탑 가새 겹침은 서쪽 면 가새 제거로 해결). 레이캐스트: 더미 중턱 7.0 / 능선 13.4, 덱 6.6(위에서 쏘면 마스트 14.6), 계단 꼭대기 6.6, 붐 중간 12.6, 환적탑 지붕 52.4.
- **수정 (2026-11-20, Studio 버전 61)**: 사용자가 "RawYard_01이 이상해" → 석탄·광석 더미 메쉬(`RwMisc_PlCoalPile`·`RwMisc_PlOrePile`)의 **면 방향(노멀)이 안쪽으로 뒤집혀** 위·바깥에서 보면 더미가 투명하게 사라져 있었음(낮은 각도에서만 반대편 안쪽 면이 보였음). Workspace·ServerStorage 원본 둘 다 `DoubleSided = true`로 해결(스크립트로 설정됨). .blend가 없어 메쉬 노멀 자체는 그대로. 조명탑·램프 등 나머지 메쉬는 정상. **앞으로 Blender에서 만든 메쉬는 내보내기 전에 노멀 방향(`recalc_face_normals`) 확인할 것.**
- **공장 전체 노멀 검사 (2026-11-20, Studio 버전 64)**: FactoryContent·FactoryLighting·Assets.Factory·SlagWalker의 고유 메쉬 813개를 `AssetService:CreateEditableMeshAsync`로 읽어, 메쉬를 **연결된 덩어리별**로 나눠 "면이 덩어리 중심 바깥을 향하는 넓이 비율"을 계산(0.25 미만 = 뒤집힘). 메쉬 전체 평균으로만 보면 여러 덩어리짜리 메쉬에서 묻혀서 덩어리별로 봐야 함. 평평한 바닥 조각(GroundFinish 패치·웅덩이·기름, BossYard FlOil)은 이 기준이 안 맞아 면 법선이 위(+Y)를 향하는지로 따로 확인 → 정상.
  - 뒤집힌 메쉬 20개 → 같은 MeshId 를 쓰는 MeshPart 40개(Workspace·ServerStorage 원본·SlagWalker/MoltenWalker) 모두 `DoubleSided = true`: 용광로 `BfSteel_Rails / StoveRails / StairRails / CastRails`(덩어리 전부), `BfSteel_Tower / Supports / Supports2 / Skip / Stairs / CastFrame`, `BfMisc_Valves / CastGear / SkipGear`, `BfPlate_SkipCars`, 냉각탑 `CtConcrete_BaseW / BaseE`, `CtMisc_Rebar`, 원료 야적장 더미 2, Slag Walker `RightLowerArm__Slag`(흘러내린 방울 1개).
  - 닫힌 상자가 뒤집히면 반대편 안쪽 면이 보여 모양은 거의 같고 빛 방향만 어긋나서 그동안 눈에 띄지 않았음(바닥이 열린 더미만 사라져 보였음). 용광로 키트의 상자 생성 쪽 감김 방향 문제로 추정 — 원인 코드는 .blend·당시 스크립트가 없어 확인 못 함.
  - 확인 화면(스크린샷)은 Studio 창이 그려지지 않아 시간 초과 → 이번 결과는 계산으로만 판정. 결과 기록 `exports/_preview/normal_check.txt`(이 PC만).
  - Slag Walker 방울(`drip`)이 뒤집힌 건 `scripts/slag_walker_build.py`의 loft 아래 방향 경로에서 단면 축이 뒤집힌 탓 → 다음에 메쉬를 다시 만들 때 고칠 것.

### 배관 다리 키트 `PipeBridges` + H 배관 회랑 `PipeCorridor` — 2026-11-19
- 결정(사용자): 4노선 전부 / 점검 통로 + 사다리 / 부분 파손 / H 회랑도 실제 에셋으로.
- 위치: `Workspace.FactoryContent.K_PipeBridges.PipeBridges_01` (assetId **91418041095353**), `Workspace.FactoryContent.H_PipeCorridor.PipeCorridor_01` (assetId **90595716561148**). 원본 `ServerStorage.Assets.Factory.PipeBridges` / `PipeCorridor`. 그룹 소유.
- **좌표계**: 두 에셋 모두 Blender (x,y,z) → 월드 `(-881 - x, 0.5 + z, 881 + y)` (회전 없음). 배치는 기준 메쉬(`PB1Plt_Pipes…` 바운딩 중심 (-894.625, 14.025, 683.45), `PCPlt_Pipes…` (-990, 10, 627.54))를 맞추는 방식. 모든 지오메트리는 **월드 좌표로 직접** 만들었음(생성 코드에서 world→Blender 변환).
- 노선 (월드 좌표, 데크 = 크로스빔 윗면):
  - **① 용광로→H 회랑** (X −896): 집진기 하강관(-896.3, 752.1) 높이 25.5에서 가스 본관(r1.6)이 남쪽으로 → T1 타워(Z 737..749) → 큰길 위 트러스 84 (Z 737→653, 폭 13, 데크 23.6) → T2 타워(Lot_024, Z 645..653, 서쪽 사다리) → Z 643에서 17.4로 내려가 H 랙 상단 본관(Z 614.8)에 T자로 합류. 증기(r .9, 회색)·물(r .7)은 T1 안에서 땅에서 올라와 T2에서 땅으로 내려감(밸브). **파손**: 증기관이 Z 701~705에서 끊겨 남쪽 토막이 도로 위로 늘어짐(높이 16.5까지, 충돌 없음), 통로 판 Z 683~687 빠짐(구멍, 충돌도 뚫림).
  - **② 헤더 → 코크스로** (Z 743, 폭 12): T1 서쪽에서 Lot_026 남쪽 가장자리를 따라 서쪽으로 타워 H1(X −942)·H2(−990) → 교차로 위 75 경간 → 보도 위 코너 타워 TW(X −1071, 서쪽 사다리). 본관은 TW에서 북쪽으로 꺾여 보도 위 T-받침 2개(Z 760/771) → Z 778에서 서쪽으로 **코크스로 가스관 끝 플랜지(X −1077, 높이 25.5)에 맞물림**. 증기·물은 첫 칸(X −905/−907)에서 올라와 TW에서 땅으로 내려감. 파손: 통로 판 X −1030~−1034 빠짐.
  - **③ 용광로 → Lot_025 분기 → 압연동** (데크 17.8, 폭 10.5): Lot_026 북동쪽 K 타워(-811.2, 936.5, 45° 회전, 뒤쪽 사다리)에서 소형관 3줄(r .75, 땅에서 올라옴, 밸브 1)이 대각선 길을 수직으로 건너(경간 88) Lot_025 분기 타워 J(-877.65, 1003, 12.4×12.4)에서 45° 꺾여 북쪽 → 골목 위 경간 60 → 보도 위 N 받침(Z 1071, 서쪽 사다리) → **압연동 배관 랙 끝(Z 1081.5, X −878.5/−876.5/−874.5, 높이 18.85)에 커플링으로 연결**.
  - **④ 가스 홀더 → 발전소(E)** (Z 1224, 데크 19.2, 폭 7): 가스 홀더 막힘 플랜지(X −377, 높이 14.5)에 맞물린 플랜지 → 보도에서 20.5로 올라감 → 골목 위 경간 40 → E 타워(X −327, 동쪽 사다리) → X −319에서 땅의 밸브 피트로 내려감. 발전소(E) 에셋 만들 때 이 피트에서 이어 붙일 것(변압기 블록아웃 울타리 X −310부터라 그 앞에서 끊음).
- **H 배관 회랑** (Lot_011+Lot_024, X −1230..−750, Z 606..618): 2단 랙 25개 벤트(20 간격), 하단(데크 9.5) 물 r2.4·r1.8, 상단(15.5) 가스 본관 r1.6·회색관 r1.2·케이블 트레이. 양끝 하단관은 땅으로 내려감, 상단관은 막힘 플랜지. X 브레이싱은 bay 3,7,11,15,19,23. 탱크 2기((-1180,642) r12 h24, (-1140,644) r10 h20) + 펌프장(X −1118..−1100, Z 634..652, 문 닫힘·속 막힘)에서 하단 r1.8관으로 지관 3개(밸브). **파손**: bay 11(X −1010..−990)에서 상단 회색관이 끊겨 북쪽 바닥(Z 622~624)에 떨어져 있고 트레이도 없음(케이블만 처짐).
- 메쉬: PipeBridges 42개 32,580 삼각형, PipeCorridor 14개 15,356. 전부 `__NoCollide`. 텍스처는 기존 승인 세트를 **팔레트 키로 찾아 SurfaceAppearance 복제**(FurnaceRust/StoveGrey/SteelOxide/RailYellow/CoolConcrete/RoofZinc). 단색: DiamondPlate(통로), DarkSteel(받침·밸브·트레이), Rubber(케이블), Glass.
- 충돌: `PipeBridges_01/Colliders` 138개 (기둥, 플랫폼, 트러스 바닥·양옆 벽, 배관 원통, 난간 벽, 사다리 TrussPart 5). **트러스 천장 충돌은 위로 4 늘려**(데크+H+4) 플랫폼·배관 위에서 트러스 지붕으로 못 올라가게 함. `PipeCorridor_01/Colliders` 75개 (기둥, 배관, 탱크 원통, 펌프장 통째 상자).
- 확인(플레이 테스트 안 함): Blender 줄인 BVH 쌍별 겹침 → 접합부(트러스-타워 받침, 배관 T자, 칼라·밸브·벽 관통, J 타워에 걸친 대각 트러스 끝)만 남김(T2 남쪽 받침-엘보, 랙 무릎 가새-물관, 받침 블록-밸브 수정). Studio 레이캐스트: 통로 ①② 23.75, ③ 17.95, ④ 19.35, 통로 빠진 곳은 아래로 떨어짐, 다리 밑 도로 높이 ① ② 22.8 / ③ 17.0 / ④ 18.4, H 랙 밑 통과, 스폰 21곳 막힘 없음, TW·④ 받침 옆 보도 한쪽 차선 통과. 텍스처 로드 스크린샷 확인.
- 정리: `K_Common`의 PipeBridge 블록아웃 9개 삭제(굴뚝 A·B는 남김), `H_PipeRack` 블록아웃 → `ServerStorage.H_PipeRack_OldBlockout`. Lot_011·Lot_024 LotDressing 97개(초록 나무·덤불·풀, 랙·탱크 자리) → `ServerStorage.LotDressing_Lot011_024_Backup`. 두 부지 재질 Concrete (128,126,118).
- Blender: 이번 PC의 Blender는 **화면/렌더가 전부 하얗게 나옴**(look·Eevee·Workbench 모두) → 시각 확인은 Studio에서. 안전 모드에서 함수 재사용: `import string; string.pb_xxx = 함수` 로 모듈 속성에 저장하면 다음 호출에서 `string.pb_xxx(...)`로 호출 가능(람다·driver_namespace·이름 대입 호출은 막힘). 키트 함수(pipe/beam/truss/tower/ladder/rail/valve/tbent/finalize/colstr)는 이 세션 Blender에만 있음, .blend 저장 안 함. 충돌 정의 씬 속성 `PBC_1..4`, `PCC`.
- Studio 저장: MCP로 저장 버전을 확인하지 않음 → 다음 작업 전에 Team Create 저장 상태 확인.

### 컨베이어 갤러리 `ConveyorGallery` — 2026-11-19
- 결정(사용자): 덮인 갤러리 / 안 통로 + 중간 계단탑 / Lot_025 서쪽 전환탑 1개 / 부분 파손.
- 위치: `Workspace.FactoryContent.K_Conveyors.ConveyorGallery_01`, 원본 `ServerStorage.Assets.Factory.ConveyorGallery`. assetId **81874299175733**. 좌표계는 배관 다리와 같음(Blender (x,y,z) → 월드 `(-881 - x, 0.5 + z, 881 + y)`, 기준 메쉬 `CV2Stl_Truss…` 바운딩 중심 (-886.1905, 29.3494, 945.3861)). 블록아웃 `C_RawYard.Conveyor_ToFurnace1/2` 삭제.
- 노선 (월드): **S1** 원료 야적장 환적탑 헤드하우스 동쪽 면(X −1148.4, Z ≈1030.5, 바닥 34) → 전환탑 TH 서쪽 면(X −1015, Z 1001, 바닥 32.5), 길이 137, 받침 2개(s 45 코크스로 부지 북동 모서리, s 80 보도). **S2** TH 동쪽 면(X −1001, Z 999) → 방향 (224, −106.4) 252 → 끝 (-773.4, 890.9) 바닥 18, 받침 6개(s 40/80 Lot_025, 120/164 대각선 길 양쪽 보도, 206/238 Lot_026). 끝은 막힌 벽 + 슈트가 장입 피트하우스 지붕(-767.5, 15.4, 888.2)으로 내려감(스킵 경사로를 피하려고 피트 바로 위가 아니라 북서쪽에서 끝남).
- 단면: 폭 9.3(현 중심) / 높이 8 + 박공 1, 프랫 트러스 + 함석 벽(RoofZinc, `Sid_Walls`)·지붕. 걷는 쪽(Z가 작은 쪽) 통로 폭 2.4, 반대쪽 벨트(트러프 아이들러 4 간격, 고무 벨트 + 석탄 짐, 리턴 벨트). 끝이 비스듬히 잘리는 부분(TH 면)은 양쪽 현이 각자 면에서 끝나게 만듦(`gallery2`).
- **전환탑 TH** (X −1015..−1001, Z 993..1007): 철골 탑 + 바닥 32.5, 위에 SidingTeal 집(32.65~42, 지붕 42.3), 서·동쪽 면은 갤러리 입구, 남쪽 벽에 문(X −1015..−1011.5). 안에 호퍼·모터. **계단탑** (Z 985..993, 같은 X): 4구간 꺾음 계단(단 높이 1, 폭 3.4), 층계참 8.5(동)·16.5(서)·24.5(동)·32.5(서, TH 문). 지면 입구는 서쪽 X −1015, Z 985..989.
- 파손: S2 s 52.5~60 구간(Lot_025 위) 벨트가 끊겨 한쪽이 열린 바닥 아래로 늘어져 땅의 석탄 더미(높이 2.8, 낮은 충돌 1.2)에 닿음. 벽판 18장·지붕판 7장 빠짐.
- 메쉬 25개, 삼각형 26,178. 텍스처는 기존 세트 복제(SteelOxide/RoofZinc/SidingTeal/StoveGrey/RailYellow/CoolConcrete), 단색 DiamondPlate·DarkSteel·Rubber·Coke(Slate).
- 충돌 `ConveyorGallery_01/Colliders` 92개: 갤러리 구간마다 바닥(경사 상자)·양옆 벽·두꺼운 천장(못 올라감)·벨트 상자, 받침 다리, TH 기둥·바닥·벽·지붕(+못 올라감), 계단 단 32개·층계참 4·난간 벽·계단탑 바깥 투명 벽.
- 확인(플레이 테스트 안 함): Blender 겹침 검사 → 비스듬한 끝에서 벨트·아이들러가 축에서 틀어지던 문제, 층계참-기둥, 문짝-난간, 모터-기둥 수정. 남은 것은 TH에 갤러리가 물리는 이음, 계단 층계참-기둥 이음, 끊긴 벨트가 롤러에 걸친 곳. Studio 레이캐스트: 통로 높이가 계획값과 0.01 안에서 일치(S1 34.04→32.78, S2 32.07→18.56), TH 바닥 32.65, 층계참 8.5/16.5/32.5, 계단 단 4.5, 계단 입구→층계참→TH 문→S1·S2 통로 수평 통과, 갤러리 밑 높이 골목 32 / 대각선 길 23.5, 스폰 막힘 없음. 텍스처 스크린샷 확인.
- Blender: 함수 `string.pb_gallery2`, `pb_bent2`, `pb_slab3`, `pb_prism` 추가(이 세션 Blender에만 있음). 충돌 정의 씬 속성 `CVC`.

### 굴뚝 `Chimneys` — 2026-11-19
- 결정(사용자): 3기 서로 다르게 / 못 올라감 / B만 꼭대기 부러짐.
- 위치: `Workspace.FactoryContent.K_Chimneys.Chimneys_01`, 원본 `ServerStorage.Assets.Factory.Chimneys`. assetId **139349113532047**. 좌표계는 배관 다리와 같음(기준 메쉬 `CHAPlt_Stack…` 바운딩 중심 (-934.5, 71.5, 793.1)). 블록아웃 `K_Common.Chimney_A/B`, `E_PowerPlant.Chimney_E` 삭제.
- **A 철판 굴뚝** (-934.5, 793.1), 높이 140: 팔각 콘크리트 받침 + 아래가 벌어진 강판 통(r 7 → 5, BfPlate FurnaceRust), 링 보강 10 간격, 플랫폼 70·132(난간), 장식 사다리 9~132(케이지, 충돌 없음 = 못 올라감), 꼭대기 열림(안쪽 4). 열풍로 1번 쪽으로 연도 덕트(r 2.2, 높이 7.5)가 나가 땅으로 꺾여 들어감.
- **B 벽돌 굴뚝** (-1210, 760, 코크스로 부지 남서), 높이 96: 벽돌 받침 13×13 + 콘크리트 캡, 테이퍼 통(r 6 → 3.7, Brick 재질), 쇠띠 8 간격, 벽에 박힌 발판. **꼭대기 북동쪽(+40°)이 최대 10 무너져 들쭉날쭉** + 그쪽 바닥에 벽돌 잔해 더미(높이 3, 낮은 충돌)와 조각 9개. 동쪽에 연도 입구(벽돌 덕트 + 콘크리트 헤드월).
- **E 콘크리트 굴뚝** (-95, 1100, 발전소 부지), 높이 120: 팔각 받침(문) + 테이퍼 통(r 6.6 → 4.4, CtConcrete), 꼭대기 96~120 빨강·흰 띠 4개, 플랫폼 60·112, 항공 장애등(Neon) 112·120, 장식 사다리(테이퍼 따라 5구간으로 나눔).
- 메쉬 21개, 삼각형 26,010. 새 단색 키: PaintRed (150,52,40)·PaintWhite (188,184,174) Concrete, Beacon (200,40,30) Neon, Brick.
- 충돌 10개(굴뚝 원통, 받침 상자, 덕트, 잔해·연도). 사다리 TrussPart는 넣지 않음.
- 확인: 겹침 검사 → B 쇠띠가 속이 찬 원판이라 벽돌 통 안을 가로지르던 것을 고리로 수정, E 사다리가 위로 갈수록 벽에서 떨어지던 것을 구간별 반지름으로 수정, E 문이 받침 면에서 떠 있던 것 수정. 남은 겹침은 덕트-통·받침, 사다리 브래킷-통, 잔해-받침(기대어 쌓임). Studio: 다른 콘텐츠와 충돌 겹침 없음, 스폰 막힘 없음, 텍스처 스크린샷 확인.

### 발전소 `PowerPlant` (터빈홀 + 개폐소) — 2026-11-19 (구역 E, Lot_057)
- 결정(사용자): 남은 블록아웃 순서 E → F2 → G / 터빈홀 안에 들어감 / 대형 변압기 3기 + 개폐소 철탑.
- 위치: `Workspace.FactoryContent.E_PowerPlant.PowerPlant_01`, 원본 `ServerStorage.Assets.Factory.PowerPlant`. assetId **126279640325399**. 좌표계 동일(기준 메쉬 `PPBrk_Walls…` 바운딩 중심 (-78, 14.9, 1209)). 블록아웃 `E_PowerPlant` 그룹 통째 삭제.
- **터빈홀** X −100..−56, Z 1185..1233 (블록아웃의 서·남쪽 면 유지 → 냉각탑 급수관 2줄이 남쪽 벽 (−82, 3.1, 1185)와 서쪽 벽 (−100, 3.1, 1197) 구멍으로 들어가 안의 펌프에 연결). 콘크리트 기둥(8/11 간격) + 벽돌 벽(0.5~10) + 창 띠(10~19, 일부 깨짐) + 벽돌·링보, 처마 24·용마루 29 박공(벽돌 박공, 철골 트러스, 함석 지붕 3장 빠짐). 입구: 서쪽 큰 문 Z 1209.8..1216.2(셔터가 6.2에 걸림), 남쪽 문 X −63..−59, 동쪽 문 Z 1227..1231.
  - 안: 터빈-발전기 2세트(X −87 / −69, 받침 높이 3.5, Z 1193..1215, 케이싱 꼭대기 ~9.9), 천장 크레인(주행보 18, 거더 Z 1202~1205, 훅 12), 냉각수 펌프 2, 배전반 줄, 드럼·상자. 북쪽 메자닌(바닥 8.5, Z 1222.4..1232.2) + 제어실(앞 유리창, 문 X −61..−58, 콘솔 5·패널 8), 동쪽 벽 따라 계단 8단(Z 1209.6..1222.4).
  - 충돌: 벽(문·구멍 제외), 창 띠, 바닥, 기계, 메자닌·제어실, 계단 단, 실내 천장 16.5(크레인·지붕으로 못 올라감), 지붕 위 막음.
- **개폐소** X −290..−190, Z 1204..1235: 자갈 바닥, 철망 울타리(높이 7.6 + 가시철사, 남쪽 문 X −245..−237, 문짝은 밖으로 열림), 변압기 3기(X −270/−240/−210, Z 1215: 몸체·방열판·컨서베이터·HV 부싱 3·LV 부싱 3, **−210은 탄 변압기**(그을음 몸체·부러진 부싱·끊어진 전선이 바닥에 늘어짐)), 격자 철탑 2기(X −284/−196, Z 1229, 높이 17) + 격자 빔, 애자 줄에서 부싱으로 처진 전선, 서쪽 끊어진 송전선. 개폐소 → 터빈홀 서쪽 벽까지 케이블 트렌치 덮개(Z 1218.6..1221.4, 낮음).
- Spawn_E1 (−300,1200)을 피하려고 개폐소를 블록아웃(X −300..−240)보다 동쪽으로 옮김. 배관 다리 ④ 밸브 피트(−319, 1225)는 그대로 울타리 밖.
- 메쉬 27개, 삼각형 21,424. 새 단색 키: Olive(변압기), Insulator (112,70,52), FenceMesh (투명 0.6), Ballast, Soot, Wood. 셔터는 WhSiding ShutterOrange 복제.
- 충돌 205개. 확인(플레이 테스트 안 함): 겹침 검사 → 문짝-변압기 받침(문을 밖으로), 탄 변압기 전선-컨서베이터(끊어진 전선으로), 계단 마지막 단 높이, 크레인 코벨 방향 수정. 남은 것은 받침·이음·전선 연결부. 레이캐스트: 바닥 0.76, 계단 1.7→8.5, 메자닌·제어실 8.5, 세 문·제어실 문·개폐소 문 통과, 셔터 높이에서는 막힘, 스폰 막힘 없음. Lot_057 마른 나무 2개 백업(`LotDressing_Lot057_Backup`). 텍스처 스크린샷 확인.
- Blender 작업 중 실수: 문짝 지우기를 X 범위로 했다가 같은 X를 지나는 철탑 격자 5개도 지워져 다시 넣음 → **섬 삭제는 이름·범위를 좁게**.

### 계량소 `WeighStation` + 덤프트럭 `OreTruck` — 2026-11-19 (구역 F2, Lot_042)
- 결정(사용자): 새 광석 덤프트럭 / 계량 사무소 들어감 / 계량대 2 + 시료 채취 갠트리 + 대기 차선.
- 위치: `Workspace.FactoryContent.F2_Weighbridge` 안에 `WeighStation_01`(assetId **124201129945244**, 기준 메쉬 `WSCon_Concrete…` 중심 (-629, 5.0, 1152.4))과 트럭 5대 `OreTruck_*`(원본 assetId **136661725317875**, 모델 피벗 = 바닥 중앙, 앞 = +Z). 원본 `ServerStorage.Assets.Factory.WeighStation` / `OreTruck`(트럭 원본은 피벗 (-629, 0.5, 1300)에 있음 → 복제 후 `PivotTo(CFrame.new(x, y, z) * CFrame.Angles(0, yaw, 0))`). 블록아웃 `F2_Weighbridge` 삭제, 옛 주차장 꾸밈(승용차 3·주차선·풀) → `ServerStorage.LotDressing_Lot042_Backup`. 부지 재질은 Asphalt 그대로.
- 흐름: 남쪽 길(Z ~1064)에서 들어와 북쪽 골목(Z 1250)으로 나감. 차선 2개(서 X −646 / 동 X −614), 가운데 섬 X −634..−626.
  - 남쪽 출입: 초소(X −632.5..−627.5, Z 1080..1085.5, 바닥 1.5, 문은 남쪽 X −630.6..−629, 서쪽 창 깨짐) + 차단봉 2(동쪽은 내려져 있음, 서쪽은 부러져 바닥에).
  - 계량대 2기 Z 1092..1122(데크 높이 1.35, 양끝 콘크리트 경사로 = WedgePart 충돌). **서쪽 계량대 판 하나 빠짐**(Z 1102..1107, 판은 옆에 기울어져 놓임).
  - 계량 사무소(X −635..−625, Z 1097..1111, 바닥 1.4, 북쪽 문, 양쪽 창으로 계량대가 보임, 서쪽 창 하나 깨짐): 책상 2, 계기 4, 캐비닛, 의자, 서류.
  - 시료 채취 갠트리 Z 1142(서쪽 차선 위, 높이 16, 프로브 7까지 내려옴, 운전 캐빈, 장식 사다리 — 못 올라감).
  - 대기 차선: 가운데 콘크리트 방호벽 줄(Z 1131..1211, 한 개는 사고 트럭에 밀려 틀어짐), 가로등 4, 차선 페인트.
  - 트럭: 서쪽 계량대 위 1(광석), 서쪽 대기 2(석탄·광석), 동쪽 대기 1(석탄), **사고 트럭 1**(동쪽 차선에서 왼쪽으로 틀어져 방호벽에 박힘, (−615.8, 1176.2), yaw −0.5). 석탄 짐은 `OTOre_Load` 색만 Coke(40,38,37)로 바꿈.
- 트럭(OreTruck): 28×~11.4×11, 주황 캡(TruckOrange (168,92,40) Metal) + 녹슨 적재함(BfSteel SteelOxide) + 광석 짐(Ore (78,56,46) Slate), 바퀴 10. 메쉬 8개, 삼각형 2,040. 충돌 상자 1개(`ColBody`).
- 계량소 메쉬 13개, 삼각형 3,292, 충돌 83개(경사로 Wedge 4, 방호벽 13 등). 새 단색 키: Paint, Paper, Hazard.
- 확인(플레이 테스트 안 함): 겹침 검사 → 트럭 앞바퀴-캡(캡 아래를 바퀴 사이로 좁히고 휀더), 뒷바퀴-적재함(적재함을 보조 프레임 위로 0.6 올림), 배기관-캡 보호대, 배터리·연료통-적재함, 갠트리 사다리-캐빈(서쪽 기둥으로 옮김) 수정. 레이캐스트: 경사로 0.55→1.01, 데크 1.35, 빠진 판 자리 1.06, 초소 1.51, 사무소 1.40, 초소·사무소 문과 동쪽 차선 통과, 트럭 5대 서로·방호벽과 안 겹침, 스폰 막힘 없음. 스크린샷 확인.
- **Blender가 작업 중 한 번 꺼짐**(연결 끊김) → 키트 함수를 `.claude/skills/blender-to-roblox/scripts/factory_kit.py`로 저장해 둠. 새 Blender 세션에서는 이 파일 전체를 `execute_blender_code`에 붙여 넣으면 `string.pb_*` 함수가 다시 생김(배관·트러스·타워·사다리·난간·밸브·갤러리·finalize·colstr). 긴 스크립트는 세 덩어리 정도로 나눠 실행하는 게 안전.

### G 남쪽 띠 — 2026-11-19 (Lot_010 / 023 / 037 / 053, Z 377..443)
- 결정(사용자): 4곳 한 번에 / 더미는 올라가는 고지 / 크롤러 크레인 + 자석 / 독성 녹색 물 + 슬러지.
- 위치: `Workspace.FactoryContent.G_SouthStrip` 안에 `SouthSlag_01`(assetId **105574241336192**, 표시 이름이 필터에 걸려 `#########`로 나옴 — 에셋은 정상), `SouthScrap_01`(**86403935962371**), `SouthSiding_01`(**92414000818699**), `SouthClarifiers_01`(**108726217317459**), `HopperCars`(화차 원본 **88961879119500**, 16량). 원본은 `ServerStorage.Assets.Factory`에 같은 이름(화차 원본 `HopperCar`는 피벗 (-490, 0.5, 300), 길이 방향 X, 레일 위에 놓으려면 `PivotTo(CFrame.new(x, 0.5, z))`). 좌표계 동일, 기준 메쉬 바운딩 중심은 각각 (-1154.41, 5.59, 410.53) / (-918.85, 5.08, 406.12) / (-491.5, 0.705, 410) / (-183.2, 2.775, 412.2). 블록아웃 `G_SouthStrip` 삭제, 네 부지 LotDressing → `ServerStorage.LotDressing_SouthStrip_Backup`. 부지 재질: Lot_010 Ground (70,64,58), Lot_023 Ground (80,72,62), Lot_053 Concrete, Lot_037 Asphalt 그대로.
- **슬래그장(Lot_010)**: 슬래그 더미 3개 (−1200,410) r24 h10 / (−1148,398) r16 h7 / (−1095,390) r11 h5 — 걸어 오르는 고지(충돌 = 높이 1씩 쌓은 원통 계단), 슬래그 덩어리 흩뿌림, 받침 위 슬래그 포트(−1135,434, 위에 굳은 슬래그) + 쓰러진 포트(−1176,437)와 쏟아진 슬래그. Spawn_G1 (−1113,424) 주변 비움.
- **고철장(Lot_023)**: 흙 더미 3개 (−980,400) r18 h9 / (−920,418) r14 h7 / (−855,395) r15 h8 (고지) 위에 고철 102개(H빔·철판·드럼·덩어리, 녹·검정·파랑·빨강), 압축 고철 묶음 더미(−1001.6,433), **크롤러 크레인**(−800,410): 무한궤도·상부 선회체·운전실·A프레임 + 격자 붐 60(45°) 끝에서 전자석이 P3 더미 위(높이 ~8)에 매달림(고철 몇 조각 붙음). 붐은 충돌 없음, 차체만 충돌.
- **측선(Lot_037)**: 선로 2줄 Z 395 / 425 (X −656..−327, 자갈 노반·침목·레일·차막이). 호퍼 화차(26×~10.3×9, 녹슨 적재함 + 광석/석탄/빈 차) 15량 + 옆으로 넘어진 1량(−500, 430.5)과 쏟아진 광석(−470,437.5). Z 425 선로의 −582 화차는 6° 틀어져 탈선. Spawn_G3 (−523,410)은 두 선로 사이 그대로.
- **침전조(Lot_053)**: 원형 콘크리트 조 2기 (−240,410)/(−140,410) r27, 벽 높이 3.6, 녹색 독성 물(Glass 투명 0.12) 높이 3.3, 바닥 슬러지 + 가장자리 슬러지 둑, 가운데 기둥. 서쪽 조는 스크레이퍼 다리(높이 6.05, 난간, 걸을 수 있음), **동쪽 조 다리는 무너져 안쪽 끝이 물속에 빠짐**. 펌프장(−92..−68, 413..437, 문 닫힘·속 막힘) → 두 조로 가는 배관 2줄. 조 안 바닥 충돌 1.05(물 속을 걸음 — 피해 판정은 게임 코드 결정).
- 메쉬: 슬래그 4·2,384 / 고철 12·6,698 / 측선 5·3,934 / 침전조 10·2,632 / 화차 4·1,298 삼각형. 새 단색 키: Slag (45,42,40 Basalt), ScrapDirt (74,66,58 Ground), ScrapBlue (58,76,92), ScrapRed (112,50,40), ToxicWater (96,142,46 Glass 0.12), Sludge (58,50,34 Slate).
- 확인(플레이 테스트 안 함): 겹침 검사 → 남은 것은 더미 속 고철끼리, 슬래그 덩어리, 크레인 케이블, 차막이 버팀대(의도). 레이캐스트: 슬래그 더미 꼭대기 10.1, 고철 더미 9.1, 크레인 10.4, 조 안 1.05, 조 테두리 4.1, 다리 6.05, 화차 위 10.85, 조 벽 바깥·안쪽 막힘, 화차끼리 겹침 0, 스폰 막힘 없음. 스크린샷 확인.
- **Blender가 또 한 번 꺼짐**(호퍼 화차 만들던 중) → 이후 부지 하나 끝날 때마다 바로 FBX 내보내기(`string.pb_export`)로 바꿈. 같은 세션에 오브젝트가 별로 없어도 꺼졌으므로 원인 불명(이 PC Blender는 화면도 하얗게 나옴).

### 슬래그장 Exit4 수정 — 2026-11-19
- 첫 슬래그장의 큰 더미 (−1200,410) r24가 레이드 탈출구 `RaidExits.Exit4` (−1220, 3.5, 400)를 덮고 있었음(계획서 규칙: 탈출구·스폰 반경 20 비움). 사용자 결정: 탈출구는 두고 **더미를 옮김**.
- 새 슬래그장 assetId **101180381464830** (`SouthSlag_01` 교체, 원본 `ServerStorage.Assets.Factory.SouthSlag` 갱신, 기준 메쉬 중심 (−1134.85, 5.08, 409.39)). 더미: (−1165,400) r20 h9 / (−1128,393) r12 h6 / (−1093,386) r9 h4.5. 포트·쏟아진 슬래그는 그대로. Exit4 반경 20 안 충돌 0, Spawn_G1 주변 비움.
- 공장 place의 탈출구는 Exit4 하나뿐(Spawn과 달리 RaidExits에 1개).

### 4단계 바닥 마감 — 2026-11-19
- 결정(사용자): Exit4 = 더미 이동 / 공장 부지 전부 텍스처 바닥 + 얼룩 / 도로 승용차 일부를 공장 트럭으로.
- 범위: 공장 부지 17곳(Lot_010·011·012·013·023·024·025·026·027·037·042·043·053·057·058·059·060). 운하 창고 존 부지(038~041, 054~056)는 손대지 않음.
- **부지 색**: 하얗던 Lot_026(용광로) → Concrete (118,114,106), Lot_025 → (128,126,118).
- **노출 바닥 표본**: Studio에서 8스터드 칸마다 5점 레이캐스트(공장 메쉬를 잠깐 CanQuery 켜서) → 땅 위 1 안에 건물·바닥 메쉬·꾸밈이 없고 그 부지 파트 위인 칸만 "열린 칸"(4,367칸). 덮개는 열린 칸에만 깔아서 기존 바닥 메쉬와 z-fighting 없음.
- **바닥 덮개** `Workspace.FactoryGroundDressing.GroundFinish_01` (assetId **91461711314506**, 원본 `ServerStorage.Assets.Factory.GroundFinish`, 기준 메쉬 `GF024Jnt_Joints__Joint__NoCollide` 중심 (−909, 0.515, 629)): 메쉬 110개(부지별×종류), 삼각형 17,676, 전부 위를 보는 평면(높이 0.515~0.557, 종류마다 층을 나눔), 충돌·그림자 없음.
  - 콘크리트 부지: 16스터드 줄눈(일부 끊김), 슬래브 보수 패치, 기름·녹물 얼룩, 웅덩이, 자갈, 균열. 석탄 부지(012·013): 줄눈 어둡게 + 석탄 가루 많이. 슬래그·고철장(010·023): 줄눈 없이 슬래그 가루/흙 패치·웅덩이. 아스팔트(037·042): 보수 패치·기름·균열.
  - 색: Joint (68,66,62) / 석탄 (48,46,44), SlabPatch (106,103,96) / 아스팔트 (62,62,66) Asphalt, Grit 부지별(슬래그 Basalt (38,36,34), 고철 흙 Ground (92,82,66), 석탄 Slate (34,32,31), 그 외 Pebble (98,94,86)), RustStain (98,58,40) 투명 0.4, OilStain (30,28,26) SmoothPlastic 투명 0.18, Puddle (42,44,44) SmoothPlastic(Glass·반사는 하늘이 비쳐 파랗게 떠서 뺌), Crack (30,28,27).
- **잡초·잔해** `FactoryGroundDressing/<Lot>`: 열린 칸에 기존 키트 복제 — GrassClump 174, GrassTuft 50, WeedBush 24(충돌·그림자 끔), TrashPile 21, RubblePile 13. 스폰 반경 12·Exit4 반경 21 안에는 안 놓음.
- **도로 차량**: 공장 구역(운하 존 밖) 도로 승용차 17대 중 8대를 OreTruck으로 교체(`FactoryGroundDressing/RoadTrucks`, 짐은 광석·석탄 번갈아, 방향은 원래 차 방향), 원래 차는 `ServerStorage.RoadCars_Factory_Backup`. 트럭 8대 모두 주변과 겹침 없음.
- 확인(플레이 테스트 안 함): 덮개 평면 법선 전부 위쪽, 스크린샷으로 표시 확인(웅덩이·기름 색 조정 후).
- **겹친 면(z-fighting) 정리 (2026-11-21, Studio 버전 89)**: 맵 전체 검사 — 보이는 파트 7,117개(사람형 모델·RaidSpawns 제외). 방법: ① 블록 면·얇은 메쉬(두께 0.25 미만)를 평면별로 묶어 겹치는 후보 → ② 메쉬는 `AssetService:CreateEditableMeshAsync(Content.fromUri(MeshId))`로 실제 삼각형을 읽어 0.5칸(넓은 면은 더 굵게) 격자로 같은 자리·높이 차이 0.024 미만인 칸을 셈. 같은 색·재질끼리 겹친 것(다리 거더↔운하 벽 등)은 안 보여서 제외. 한 번에 다 돌리면 MCP 연결이 끊김 → `_G`에 후보를 두고 200쌍씩 나눠 실행.
  - 중복(같은 메쉬가 같은 자리에 두 번) 0개.
  - 고친 것(위쪽 층을 올려 간격 0.03): 도로 웅덩이 70곳 물(+진흙 10), 도로 균열·아스팔트 패치가 정지선·횡단보도와 같은 높이, 다리 보도 `BridgeSidewalk` (42,520) 윗면 +0.03·밑면 +0.02, 공장 기름·페인트 선(보스 마당 바닥 기름, 작업자 배랭 코트 선, 압연 공장 마당 페인트·기름), QRail 보, 131개 + 바닥 마감.
  - **바닥 마감 `GroundFinish_01` 층 높이 고정**: 부지마다 제각각이던 높이를 종류별 고정값으로 — Jnt 0.530 / Pat 0.555 / Grt 0.580 / Rst 0.605 / Oil 0.630 / Pud 0.655 / Crk 0.680 (부지 바닥 0.5 위, 층 간격 0.025). `ServerStorage.Assets.Factory.GroundFinish` 원본도 같은 배치로 맞춤. (다른 공장 에셋 원본은 맵 쪽만 고침)
  - 재검사 결과: 다른 색·재질인데 간격 0.024 미만으로 겹친 면 0, 같은 모양 겹침 30(안 보임).
- 재작업 방법: 같은 표본을 다시 뽑으려면 Studio에서 위 레이캐스트 스크립트를 다시 돌려 `_G.GroundCells`를 받고, Blender에서 `GF<lot>…` 메쉬를 다시 만듦(코드는 이 세션 기록 기준; 핵심 = 칸 단위 blob/줄눈/균열, `face.normal_flip()`으로 위 방향 고정).

### 5단계 소품·표지·낙서 — 2026-11-20
- 결정(사용자): 영어 / 산업 표지 + 생존자 낙서·흔적 + 산업 잡동사니 소품 / 이야기 = 갇힌 노동자들 + 보스 경고.
- **데칼 이미지 19장**: `.claude/skills/blender-to-roblox/scripts/make_decals.ps1` (PowerShell System.Drawing, Blender 렌더가 이 PC에서 하얗게 나와서 대신 씀) → `exports/decals/factory/*.png` → Open Cloud assetType **Decal**로 그룹 업로드. 이미지 ID는 `exports/texture_ids.json` → `FactorySigns`. (Decal 에셋 ID ≠ 이미지 ID: 이미지 ID는 `InsertService:LoadAsset(decalId)`의 `Decal.Texture`)
- **`Workspace.FactorySigns`**:
  - 세움 간판(판+기둥 2): BlastFurnace (−860,747) / CokeOvens (−1081,860) / GasHolder (−381,1090) / Weighbridge (−601,1079) / Direction (−747,1244).
  - 벽 데칼(0.05 투명 판, 콜라이더 벽에 레이캐스트 후 0.08 띄움): RollingMill, PowerStation, 고압 위험 2(개폐소·터빈홀), 가스(가스 홀더), 쇳물(출선장), NO ENTRY(보스 마당 입구), 안전모(압연동).
  - 낙서: STILL INSIDE(압연동 벽), DON'T GO NORTH(보스 마당 쪽), DAY 112 집계(배랭 식당 안 북벽), MINA(배랭), WATER(H 펌프장), SOS(펌프장 지붕 15×15).
  - 바닥 스텐실 KEEP CLEAR: 압연동 (−891,1110), 터빈홀 (−106,1213).
- **`Workspace.FactoryProps`** (키트 복제: BunkerPropKit·MapKits·PlazaProps):
  - `Camp_RollingMill` (−852,1129) 11개: 간이침대 3, 드럼 난로(PointLight 주황 + Fire), 보급 상자·SupplyStack·MedCabinet·Boxes·드럼·프로판, 모래주머니 1.
  - `Camp_DiningHall` (−649,1561) 5개: 간이침대, 난로(빛만), Boxes, Toolbox, SupplyStack — DAY 112 낙서 옆.
  - `Clutter/Cluster_xx` 23무더기 66개: `_G.GroundCells` 3×3 열린 칸, 서로 맨해튼 80 이상, 스폰 16·Exit 22 밖. 드럼 2~4(25% 눕힘) + 프로판(50%) + 공구함/카트/군용상자/보급상자/박스/툴박스 1.
  - **주의**: 키트 모델 피벗이 중심이 아님(난로·드럼이 30스터드 어긋났었음) → 배치는 GetBoundingBox 중심 기준으로 해야 함.
- 확인(플레이 테스트 안 함): 모든 소품 콜라이더·표지·서로 겹침 0(겹치는 건 배치 안 함), 실제 파트 최저점 = 바닥(0.5 / 식당 0.8) 오차 0.35 이내. Studio 저장 버전 51.

### 6단계 조명·연기 — 2026-11-20
- 결정(사용자): 공용 패키지에 공장 등록 / 낮밤 유지 + 스모그 덧칠 / 실내 작업등 + 야외 투광등 + 연기·먼지 + 불씨·스파크 전부.
- **공용 코드(패키지) 수정 — ⚠ 사용자가 게시해야 다른 place·실서버에 반영됨**:
  - `ReplicatedStorage.Shared.Config.PlaceConfig`: `FACTORY = 129022811153240` 추가 (이 키를 쓰는 다른 코드는 id 비교만 해서 영향 없음 확인).
  - `ReplicatedStorage.Shared.Config.LightingConfig`: `PlaceScale.FACTORY` — Brightness ×0.75, Atmosphere Density ×1.3·Haze ×1.25, 색은 채널별 곱(Atmosphere Color (0.95,0.85,0.7)·Decay (0.9,0.72,0.55), OutdoorAmbient, ColorShift_Top, ColorCorrection Tint, Clouds), SunRays ×0.5. 모든 낮밤 키프레임에 적용됨.
  - `ServerScriptService.Services.LightingService.scaledValue`: PlaceScale 값이 Color3이면 채널별 곱(3줄 추가).
  - 패키지 게시: Studio에서 `ReplicatedStorage.Shared`, `ServerScriptService.Services` 우클릭 → Publish to Package. (Studio 편집 중 Lighting은 dev 프리셋 그대로라 스모그는 플레이 때만 보임)
- **등기구 에셋** `FactoryLights` assetId **82709794456718** (Blender, 21 메쉬 2,754 tris, StoveGrey/SteelOxide SA, 렌즈는 Neon) → 템플릿 `ServerStorage.Assets.Factory.Lights`: `Lt_Pendant`(피벗=천장 고정점), `Lt_CageWall`(피벗=벽면, LookVector=밖), `Lt_FloodHead`(피벗=받침 아래, LookVector=비추는 방향), `Lt_FloodPole`(피벗=바닥, 팔 위 ±2·높이 21.9에 헤드). Blender 겹침 BVH 검사: 맞닿는 이음새만 남김.
- **`Workspace.FactoryLighting`**:
  - `Interior/<건물>` 펜던트 62개(압연동 29, 배랭 12, 터빈홀 9, 출선장 9, 계량소 2, 코크스로 1): 천장 레이캐스트로 실내 칸(지붕 + 벽 3~4면) 찾고 간격 22/15/16/14/8. 천장 높이 13.5 넘으면 바닥+13.5에 매달고 케이블 Part. SpotLight 아래 120°, 주황 (255,186,120). 켜짐 50 / 깜빡임 4 / 꺼짐 8, 그림자 4개만.
  - `Floodlights` 기둥 8개(계량소·캐스트하우스·개폐소·배랭 켜짐, 철도 야드 깜빡임(헤드 1개 꺼짐), 가스 홀더·원료 야적장·남쪽 측선 꺼짐). 열린 칸에 놓고 대상 쪽으로 돌림, 헤드 28° 숙임, 기둥 콜라이더 0.9×21. 보스 마당 입구는 빈 땅이 없어 기둥 대신 벽등.
  - `WallLamps` 망 벽등 10개(표지 옆 벽에 레이캐스트): NO ENTRY 보스 마당 입구는 **빨간 경고등(깜빡임)**, 고압·WATER 깜빡임, 가스·안전모 꺼짐, 나머지 켜짐.
  - `Effects`: 굴뚝 A(철판, 꼭대기 140) 옅은 연기, 용광로 꼭대기(108) 증기, 압연동·터빈홀 떠다니는 먼지(박스 이미터), 보스 마당 붉은 빛(Range 60, 숨쉬기) + 불씨, 출선장 앞 쏟아진 쇳물 불씨+주황 빛, 개폐소 고압 벽등 스파크(Emit + 소리), 굴뚝 E 항공 경고등 빨간 깜빡임.
- **`StarterPlayer.StarterPlayerScripts.FactoryLightFX`** (LocalScript, 이 place 전용·패키지 밖): CollectionService 태그 `FactoryFlicker`/`FactoryBlink`/`FactoryPulse`/`FactorySparks` 처리, 카메라 260 안에서만 갱신. 컴파일 확인만 함.
- 라이트 총 76개(그림자 12). (7단계 내용은 아래)

### 7단계 태그(상자·등반) — 2026-11-20
- **조사 결과**: 게임 코드에 `LootSpawn`·`ClimbPoint` 태그를 읽는 곳 없음. 실제 루팅 = `ServerScriptService.Services.Crate`: workspace의 모델/파트에 **속성 `Crate` = CrateConfig.TABLES 이름**을 달면 "Search" ProximityPrompt가 붙고, 열면 Loot 서비스로 드롭 후 숨김 → RespawnTime(기본 120초) 뒤 복구. 등반 = Roblox 기본 **TrussPart**. 그래서 상자는 `Crate` 속성 + `LootSpawn` 태그 + `LootSpot`(camp/yard/indoor/high/boss/container) 속성, 등반은 TrussPart + `ClimbPoint` 태그·속성.
- 결정(사용자): 기존 종류 + 공장용 2종 / 공장 25개 안팎 / 올라갈 가치 있는 사다리만 TrussPart / 운하 창고 존도 같이.
- **CrateConfig(공용 패키지 Shared) 추가 — 게시 필요**: `factory_toolchest`("Worker's Tool Chest": 골드 4~10, 고철 6, 못 5, 테이프 2, 톱날 20%, 붕대 30%), `survivor_stash`("Survivor Stash": 골드 8~18, 붕대 2(90%), 해독제 40%, 테이프, 나무). 아이템 id는 기존 것만(다른 Config에 정의 확인).
- **공장 상자 25개**: 캠프 4(압연동 SupplyStack·MedCabinet, 식당 SupplyStack·Toolbox — 기존 소품에 속성), 잡동사니 무더기 6(공구함→factory_toolchest, 군용상자·보급상자→supply_crate, 툴박스→hardware, 카트→garage), 실내 8(`Workspace.FactoryLoot`: 압연동 2·터빈홀 2·계량소 1·배랭 2·출선장 1), 높은 곳 5(배관 다리 사다리 위 4 + 철도 화차 지붕 1), 보스 마당 2(입구 밖·안쪽, survivor_stash).
- **운하 창고 존 상자 11개** (`ZoneContent.Zone_CanalWarehouse.Loot`): 열린 컨테이너 6(뒷벽 앞), 망루·초소 사다리 위 2 + 창고 지붕 1(survivor_stash), 창고 안 1, 야드 생존자 캠프 1.
- **등반**: 모든 TrussPart(공장 11 + 운하 3)와 운하 등반 상자 콜라이더 3에 `ClimbPoint` 태그·속성(17개). G 남쪽 띠 "사다리" 16개는 화차 끝 사다리(폭 27·높이 6)라 제외, 계량소 갠트리 사다리는 꼭대기에 설 발판이 없어 제외. 굴뚝은 못 올라감 유지.
- 확인(플레이 테스트 안 함): 상자 36개 모두 아래에 바닥(오차 0.6 안), 주변 콜라이더·소품·표지·조명과 겹침 0. Studio 저장 버전 55.

### 8단계 테스트·최적화 — 2026-11-20
- 결정(사용자): 플레이 없이 자동 검사 / 소품 고정 + 작은 등기구 그림자 끔 + CanTouch 정리 (스트리밍 반경은 1024 그대로).
- **동선(PathfindingService, 편집 모드, AgentRadius 2·높이 5·점프·등반)**: 스폰 21곳 → Exit4 전부 Success.
- **상자 접근**: 상자 옆(상자 크기 + 2.5) 빈 자리까지 경로 — 36개 중 32개 Success. 나머지 3개(운하 망루·압연동 사다리 위·철도 화차 지붕)는 TrussPart 등반 구간이라 경로 계산이 못 넘음 → 기하 확인: 사다리 꼭대기 = 발판 높이(차 0~0.6), 틈 0.5, 머리 위 비어 있음 → 올라갈 수 있다고 봄(실제 플레이로는 미확인). Crate_WorkerCamp_2는 **문 없는 닫힌 방**(배랭 (−647,1385), 사방 벽·천장) 안이라 갈 수 있는 자리 (−641, 0.8, 1326)로 옮김. 참고: 같은 이유로 그 방 안 펜던트 조명은 장식으로만 남음.
- **최적화**: Anchored 아님 70개(키트 소품, 용접 없음 → 플레이 때 굴러다닐 뻔함) 고정, 작은 등기구 메쉬 그림자 296개 끔(기둥 몸통만 유지), 소품·표지·조명·상자 CanTouch 99개 끔.
- 수치(최적화 전 점검): workspace 파트 10,606, FactoryContent 3,750(메쉬 730·고유 634·SA 367, 충돌 3,019), 조명 76(그림자 12), 이미터 7, StreamingEnabled(Target 1024, PauseOutsideLoadedArea). Studio 저장 버전 56.
- 남은 것(사용자 판단): 공용 패키지(Shared·Services) 게시, 실제 플레이로 스모그 색·사다리 위 상자·Crate 프롬프트 확인, 모바일에서 무거우면 StreamingTargetRadius 512 검토.

### 적 배치(보스·일반 몬스터) — 2026-11-20
- **게임 규칙**(ServerScriptService.Services.Enemy): workspace:FindFirstChild("EnemySpawns", true) 폴더 하나의 파트 = 스폰 지점. 속성 EnemyId(필수, ReplicatedStorage.Shared.Data.Enemies 모듈의 id), Count(기본 3), RespawnTime(기본 20초). 지점은 게임 중 자동으로 숨김, 적은 지점 주변 4스터드에 흩어져 나오고 60 넘게 끌려가면 돌아감. oss = true 적은 보스 체력바. ⚠ EnemySpawns 폴더는 place 안에 **하나만** 있어야 함.
- 결정(사용자): 보스 **Gear Head** / 구역별 몬스터 / 중간 밀도(지점 약 30, 약 70마리, 부활 90초).
- **Workspace.FactoryEnemies.EnemySpawns** 31지점, 67마리 (편집용 Neon 원판, 색 = 종류):
  - Boss_GearHead (−879, 0.7, 1450) 보스 마당 한가운데 — 반경 38 비어 있음, 높이 20 머리 위 비어 있음. Count 1, 부활 900초.
  - 보스 마당 주변 4: Bloated Husk 1마리 ×2(입구 밖 (−905,1310) 근처, 안쪽 북쪽), Failed Subject(lab_subject) 2마리 ×2(마당 서·동). 부활 120초.
  - 실내 Stockroom Brute 2마리 ×4지점: 압연동 2, 터빈홀 1, 용광로/출선장 1 (그 건물 지붕 아래인 곳). 부활 90초.
  - 야외 22지점: Ashen Husk·Toothed Revenant 번갈아, 2~3마리 (공장 부지 + 운하 존 하늘 열린 땅, 서로 70 이상). 부활 90초.
  - 공통 거리 규칙: 플레이어 스폰 45, 생존자 캠프 3곳 30, Exit4 35 밖.
- 합계: ashen_husk 26, toothed_revenant 26, stockroom_brute 8, lab_subject 4, bloated_husk 2, gear_head 1.
- 확인(플레이 테스트 안 함): 31지점 모두 가장 가까운 플레이어 스폰까지 Pathfinding Success, 지점 주변 7×5.5×7 콜라이더 없음.
- 참고: 공장 place는 아직 RaidConfig.MAPS에 없음(지도 창·탈출구 라벨·서버 수명 등 레이드 연결은 별도 작업). Studio 재연결 뒤 _G.GroundCells·_G.LightCells는 사라짐(필요하면 다시 계산). 확인(플레이 테스트 안 함): 등기구·기둥 배치 시 콜라이더·표지·소품과 겹침 0. 스모그 색·밝기는 실제 플레이로 봐야 함. Studio 저장 버전 54.

### 고로 가스 정제 시설 `GasClean` — 2026-11-21 (Lot_025, Studio 저장 버전 90)
- 결정(사용자): 고로 가스 정제 시설 / 들어가는 건물 + 계단으로 오르는 작업대(높이 14). 상자·몬스터 추가는 안 함.
- 위치: `Workspace.FactoryContent.A2_GasClean.GasClean_01`, 원본 `ServerStorage.Assets.Factory.GasClean`. assetId **127159300061579**. 스크립트 `scripts/gas_clean_build.py` (factory_kit 다음 실행, 월드 좌표로 작성). 메쉬 17개, 삼각형 약 13,400. 충돌 `GasClean_01/Colliders` 145개 (높이 0 상자 2개는 뺌).
- 부지: Lot_025 = 웨지 2개로 된 직각삼각형(서쪽 X ≈ −1015, 북쪽 Z ≈ 1017, 빗변 = 대각선 길 보도 x − z ≈ −1858). 비움: Spawn_A2 (−1002, 960) 반경 20, 컨베이어 전환탑(북서 모서리)·갤러리 받침 2쌍·석탄 더미(−948, 975), J 타워.
- 구성 (월드 좌표):
  - **집진기** 중심 (−922, 993): 다리 4개(±4.3) + 링 거더 12 + X 가새(한 칸 빠짐), 녹슨 몸통 r 5.5 (y 12..21) + 아래 원뿔(→ y 6, 먼지 밸브·먼지 통) + 위 원뿔(→ 24.4). 꼭대기 → **반가스 주관** r 1.2 높이 27 → J 타워 안 (−880.5, 27, 1000)으로 들어감(받침 bent2 x −897). 옆 출구(y 18) → 내려와 **높이 9.5 관** r 1.1 이 x −938 을 따라 남쪽 → 대각선 → 세정탑 S2 (T 받침 4개, 밑으로 걸어 지나감).
  - **세정탑 2기** S1 (−975, 912), S2 (−962, 922): 콘크리트 받침 r 4.6, 회색 몸통 r 3.5 (y 1.3..30) + 원뿔(→ 33), 보강 띠 3, 맨홀, 물 분사관. 꼭대기 연결관(높이 35.5) S2 → S1.
  - **작업대** x −983..−955, z 914..921, 높이 14 (세정탑이 판을 뚫고 지나감, 난간). **계단**: 서쪽 끝에서 서쪽으로 1단 10칸(0.7) → 층계참 7 (x −996..−993) → 2단 10칸 → 땅 (x −1006), 폭 z 914.15..916.85, 양쪽 기울어진 난간. 탑 위는 못 올라감.
  - **정제 가스관** r 0.9 높이 9 (z 910, S1 → 서쪽 x −1011 막힘판 + 밸브), T 받침 2. 밑으로 지나감.
  - **펌프동** x −1013..−995, z 882..902, 벽 콘크리트(높이 8.5) + 지붕(RoofZinc), **문 2곳**: 동쪽 z 886.5..891.5, 북쪽 x −1008..−1004 (높이 7.3). 창(깨짐) 남 2·북 1·동 1·서 1. 안: 펌프 3대(모터·볼류트·배관) + 헤더관(4.9) + 제어반 + 공구 상자. 쓰러진 문짝, 지붕 환기통.
  - **급수관** r 0.45 높이 4.9: 펌프동 동쪽 → (−975, 884.4)에서 갈라져 S1·S2 아래로 (받침 5).
  - **슬러지 침전조** (−1005, 867) r 7 높이 3 (Sludge = Mud (58,50,40), 바닥 2.4), 가운데 기둥 + 긁개 다리(난간, 높이 4.35) + 펌프동에서 오는 슬러지 관.
  - 소품: 드럼통(ShutterOrange) 9, 가스병 거치대, 바닥에 굴러다니는 관 토막 3.
- 재질: 팔레트 키별로 기존 공장 메쉬의 SurfaceAppearance·재질·색을 복사(CoolConcrete·SteelOxide·FurnaceRust·StoveGrey·RailYellow·RoofZinc·ShutterOrange, DarkSteel·DiamondPlate·Glass), Sludge 만 새로.
- 정리: 겹치던 잡초 4·드럼 2(Cluster_29) → `ServerStorage.LotDressing_Lot025_Backup`. **몬스터 스폰 이동**: 세정탑 S1 밑에 있던 `Yard_toothed_revenant`(molten_walker) (−974, 908) → (−988, 874).
- 확인(플레이 테스트 안 함): 레이캐스트 — 작업대 14.0, 계단 단 11.9, 층계참 7.0, 펌프동 바닥 0.8 / 지붕 8.95, 침전조 긁개 다리 4.5, 동·북 문 통과, 정제 가스관·집진기 관 밑 (높이 3·4·6.5·7.5) 통과, 계단 꼭대기 → 작업대 통과. 새 충돌이 기존 맵 충돌 파트와 겹침 0, 레이드 스폰 주변 막힘 없음. 스크린샷으로 텍스처 확인.

### 레이드 맵 등록 "Steelworks" (3번째 맵) — 2026-11-21 (Studio 저장 버전 96, 완료 — 게시·플레이 확인은 사용자)
- 결정(사용자): 이름 **Steelworks** ("A dead steel mill. The furnaces are cold, but the workers never left.") / 레벨 8 · 35분 · 12명 (15분 뒤 입장 마감 = entryClosesAt 20*60) / 지도 위치 = 상가 왼쪽 해안 / 탈출구 3개 · 도착 연출 · M키 미니맵 · 로딩 화면 배경.
- PlaceConfig 에는 FACTORY 가 이미 있었음. **RaidConfig.MAPS[PlaceConfig.FACTORY]** 추가 (order 3, boss "The Foreman", entryMap "SteelworksOpenServer", arrivalCinematic 14, exits, zone). **LoadingConfig.PLACES[FACTORY]** 추가 (kicker, accent (214,132,62)). → **공용 패키지 Shared 게시 필요.** 다른 곳에 맵별 하드코딩 없음(grep 확인).
- **탈출구**: `RaidExits` 에 Exit1 (−1230, 3.5, 1561) = A (10분 뒤 닫힘), Exit2 (−42, 3.5, 1230) = B (20분), 기존 Exit4 (−1220, 400) = C (끝까지). 새 두 곳 반경 11 안 충돌 파트 없음, 레이드 스폰과 60 이상.
- **도착 연출**: `Workspace.RaidArrival` VehicleStart (−100, 0, 700) → VehicleEnd (−600, 0, 700) — 동서 큰길을 동→서, 우측 차선 z 692 (주차 차량은 z 680·720), 운하 다리 건너 멈춤. 차선 높이 2.5~13 막힘 없음, 길가 카메라(컷 2, 약 x −487, z 722) 자리 비어 있음. 트럭 모델 `ReplicatedStorage.Assets.Vehicles.RaidVehicle` 이 place 에 있음.
- **월드 지도 구역 그림**: `scripts/steelworks_zone.py`(마스크·합성) + `scripts/steelworks_icons.py`(Blender Workbench 평면 툰 아이콘 11종: 용광로·굴뚝·냉각탑·가스 홀더·창고·톱니 지붕 공장·크레인·석탄 더미·탱크·집·컨테이너) + `scripts/steelworks_zone_rle.txt`(바탕 지도 땅/상가 마스크 RLE, Studio EditableImage 로 읽음). 구역 = 땅 ∧ ¬상가 ∧ 다각형(이미지 x 84..336, y 313..500, 섬 제외). 종이색 (217,193,152) + 결, 길 3개·철길·컨베이어·나무 점, 아이콘 20개. 테두리 흰 5px, 빛 = 바깥 14px 0.78 / 안 26px 0.36 (상가 그림을 픽셀로 읽어 맞춤). 데칼(그룹) → 이미지 ID: zone **98628206512498**, outline **74321785211688**, glow **109612040063235** (1024×746, 위치 확인). points 48개 = 구역 경계 방사선.
- **지도 구역 그림 v2 (2026-11-21, 사용자: "너무 조잡해, 상가·빌딩과 비슷하게")**: 아이콘을 **Cycles CPU + Freestyle 잉크 선**(두께 2.0, 거의 검정, 창문·문 같은 작은 디테일은 ZI_NoInk 컬렉션으로 선 제외) + 평면 색 3단 음영으로 다시 그림, 2배로 렌더해 절반으로 줄임. 연기 구슬 뺌, 창문·문·지붕 마루·굴뚝·옥상 탱크 추가, 지붕색 주황·적갈·청록·회청 섞음. 아이콘 19종 / 배치 25개(길 따라 빽빽하게, 철길·컨베이어 뺌). 새 zone 이미지 **95809363736667** (데칼 96747484253253). 테두리·빛·points 는 그대로. ⚠ 이 PC Blender 는 EEVEE 가 2~3장 렌더 뒤부터 빈 그림을 냄 → Cycles CPU 로.
  - ChatGPT 이미지 생성으로도 시도해 보기로 함 (사용자). 그림이 오면 구역 마스크로 잘라 끼우면 됨(`steelworks_zone.py` 의 region() 마스크 + 같은 outline/glow 재사용).
- **M키 미니맵** `minimap = { image 123326957119863, size {1024, 993}, min {-1252, 323}, max {52, 1588} }`: Studio 위 캡처 7장(높이 1500, **FOV 16**, look_at 을 −Z 로 1 비켜서 위 = −Z, 오른쪽 = +X, 1장 = 1913×670 px = 1204×421.6 스터드)을 `scripts/steelworks_minimap.py` 로 이어 붙임(각 출력 픽셀은 가운데에 가장 가까운 캡처에서 → 기울어짐 최소, 2배 슈퍼샘플). 원본 캡처 `exports/minimap_tiles/`. 캡처 동안 스폰·탈출구·도착 표시·적 스폰 표시와 구름을 숨겼다가 되돌림.
  - ⚠ **높이 5000+·FOV 5 로 찍었다가 Studio 뷰포트가 검게 멈춤** (카메라·조명 되돌려도 안 풀림) → Studio 를 다시 열어서 해결. 위 캡처는 높이 1500·FOV 16 까지만, 캡처는 **한 번에 하나씩**(동시에 부르면 시간 초과 + 카메라 섞임).
- **로딩 화면 배경** (LoadingConfig image): 동서 큰길에서 올려다본 용광로 (카메라 (−690, 16, 650) → (−835, 62, 840), FOV 45) 1913×670 → 1024 + 889 두 장: **140333903077208**, **81638109401459**.
- 확인: RaidConfig·LoadingConfig require OK, 새 이미지 6장 PreloadAsync Success, 미니맵 1024×993.
- **사용자 할 일**: 공용 패키지 **Shared 게시**(RaidConfig·LoadingConfig) — 게시해야 마을 지도 창에 Steelworks 가 뜸. 마을→공장 입장, 도착 연출, 탈출구 A/B/C, M키 지도는 실제 플레이로 확인 필요(플레이 테스트 안 함).

### 공장 습격 + 등급 상자 — 2026-11-21 (Studio 저장 버전 108, 공장 place 전용 — 패키지 게시 필요 없음)
- 사용자 요청: "몬스터는 상가맵 생성 방식과 같은데 개방된 것 / 상자 등급을 테두리 빛으로 / 열면 상가 상자처럼 뿌려지고 자동 흡수". 결정(사용자): **상가 습격 방식(셔터 없이)** / 고정 상자 등급은 **다시 채워질 때마다 무작위** / **공장 place 상자만**(공용 Crate 서비스는 안 건드림).
- 상가 방식 참고: `Services.ShopRaid`(+ Storefront, ShopRaidLogic) + `Shared.Config.ShopRaidConfig` — 웨이브(첫 30초, 300초 간격)마다 상가 셔터가 무작위 등급(Common 45·Uncommon 28·Rare 16·Epic 8·Legendary 3)으로 열림 → 등급 빛, 등급 상자(끈이 Neon 등급 색 + PointLight), 등급별 적 2~10, Legendary 빛기둥·전체 알림, 경고 15초 후 닫힘. 상자 = `Loot.drop(pos, CRATE_DROPS[tier], 6, player)` → 연 사람 전용, 땅에 닿으면 빨려 들어감.
- **`ServerScriptService.FactoryRaid`** (Script, 원본 `scripts/factory_raid.server.lua`): 공용 서비스(Loot·Enemy·Inventory·ShopRaidLogic·MapTools.Kits)를 require 해서 씀, 수치는 ShopRaidConfig 그대로.
  - 습격 지점 `Workspace.FactoryEnemies.FactoryRaidSites` 26곳 = 예전 고정 스폰 Yard_ 22 + Indoor_ 4 (속성 EnemyId 그대로 → 그 자리 몬스터 종류). 웨이브마다 9곳(SITES_PER_WAVE). 지점 위 높이 9 등급 PointLight(범위 30), 반경 11 안 빈 바닥에 등급 상자(Loot_SupplyStack, 광선+겹침 검사), 등급만큼 `Enemy.spawnTemporary`. 닫힐 때 상자·빛 지우고, **플레이어 50 안에 없는 습격 적만 사라짐**(싸우는 적은 남음). 개발용 `_G.FactoryRaid.startWave("Legendary")`.
  - **고정 상자 36개**(공장 25 + 운하 11): 속성 `Crate` → `FactoryCrate`(예전 상자 종류 이름 기록용)로 바꿔 공용 Crate 서비스가 안 잡게 함. 채워질 때마다 등급 무작위, 열면 `CRATE_DROPS[등급]` 연 사람 전용 드랍 + 숨김 → CrateConfig.DEFAULT_RESPAWN_TIME(120초) 뒤 새 등급으로 다시 나옴.
  - 등급 표시: 상자 속성 `CrateTier`·`CrateTierColor`, `CrateOpen`, 태그 `TierCrate`.
- **`StarterPlayerScripts.FactoryCrateOutline`** (LocalScript, 원본 `scripts/factory_crate_outline.client.lua`): 가까운 16개(160 이내) 상자에 등급 색 Highlight(테두리 + 옅은 채움 0.82, Occluded). Highlight 는 한 화면 31개 제한이라 가까운 것만.
- 고정 스폰은 보스 Foreman + 보스 마당 경비 4곳(5지점)만 남김. 예전 31지점 백업: `ServerStorage.EnemySpawns_FixedBackup_20261121`.
- 확인(플레이 테스트 안 함): 두 스크립트 컴파일 OK, 26지점 EnemyId 모두 EnemyDatabase 에 있음, 지점마다 상자 3개 놓을 빈 바닥 있음(Yard (−702, 828)만 빈 곳이 적어 가끔 상자 수가 모자랄 수 있음).
- **상자 경비 + 습격 적 증가 (2026-11-21, Studio 버전 110, 사용자: "야외 상자 먹을 때 주변에 적이 하나도 없음, 상자 등급별로 몬스터 수 늘려줘")**:
  - 습격 지점 적 수 = 공장 전용 `RAID_ENEMIES` Common 4 · Uncommon 6 · Rare 8 · Epic 10 · Legendary 14 (상가는 2·3·5·6·10).
  - **고정 상자 경비** `GUARD_COUNT` Common 2 · Uncommon 3 · Rare 5 · Epic 7 · Legendary 10: 플레이어가 110 안에 처음 오면 상자 둘레 7~16 바닥(높은 곳 상자면 아래 땅)에 `spawnTemporary`. 종류 = 160 안 가장 가까운 습격 지점의 EnemyId(없으면 slag_walker). 한 번 채워질 때 한 번만 나옴(죽이면 다음 채워질 때까지 없음), 170 밖에 30초 있으면 살아 있는 경비 사라짐 → 안 열린 상자면 다시 오면 또 나옴. 보스 Foreman 140 안 상자(보스 마당 2)는 경비 없음.
  - 플레이 확인(Studio, 캐릭터를 압연동 상자 옆으로 옮김): 근처 상자들 경비 hook_hauler 14마리 나와서 플레이어 쪽으로 쫓아옴. 여러 상자가 모인 곳은 한꺼번에 많이 깨어남 → 실제 플레이로 난이도 확인.
- **습격 상자 닫힘 경고 보강 (2026-11-21, Studio 버전 125, 사용자: 추천안대로)**: 전에는 지점 위 PointLight 만 깜빡여서 야외에서는 거의 안 보였음.
  - 서버(FactoryRaid): 경고 시작 때 상자마다 속성 `FadeEnd`(= `workspace:GetServerTimeNow()` + 15). 지점 빛도 마지막 5초(FAST_BLINK)는 0.12/0.08초로 빠르게.
  - 클라이언트(FactoryCrateOutline): FadeEnd 를 보고 Heartbeat 로 등급 끈(`*_Metal`) 색 ↔ 어두운색(45,32,26), 상자 PointLight 1.2 ↔ 0.15, 테두리 Highlight 0 ↔ 0.8 을 같은 박자로 (60% 켜짐). 주기 0.5초 → 마지막 5초 0.2초. 켜질 때마다 상자에서 `rbxasset://sounds/clickfast.wav` 틱 (볼륨 0.55, 롤오프 6~30 → 30 안에서만, 마지막 5초는 속도 1.25). 끈 색은 내 화면에서만 바꿈.
  - 플레이 확인: 느린 구간 1초에 4번, 빠른 구간 1초에 약 10번 바뀜, 테두리·틱 소리 붙음.
- ⚠ 상자 내용물은 상가(레벨 2~4 무기) 수치 그대로 → 레벨 8 맵이라 낮을 수 있음. 웨이브 사이(닫힌 뒤 ~1~3분)에는 야외 적이 거의 없음. **실제 플레이로 확인 필요**: 웨이브 알림, 상자 테두리, 흡수, 적 수.

### 몬스터 위험 능력: 화염 스택 · 죽음 폭발 — 2026-11-21 (Studio 저장 버전 111, 공장 place 전용 — 게시 필요 없음)
- 사용자 요청: 야외 용암 덜 식은 몬스터(Molten Walker) = 주변 반경에 1초마다 화염 스택(최대 10), 스택마다 초당 1 피해(1~10) / 식은 검정 몬스터(Slag Walker) = 죽을 때 암석 폭발, 같은 반경, 피해 30.
- **`ServerScriptService.FactoryHazards`** (원본 `scripts/factory_hazards.server.lua`): 반경 HEAT_RADIUS **14**.
  - molten_walker: 발밑에 옅은 주황 Neon 범위 원 `HeatRing`(투명 0.88, 루트에 용접). 1초마다 범위 안 플레이어 FireStacks +1 (여러 마리여도 +1), 밖이면 −1 (규칙은 임의로 정함 — 바꿀 수 있음). 매초 피해 = 스택 × 1.
  - slag_walker: Died → 0.6초 땅 경고 원(점점 진해짐) → 주황 불덩이 퍼짐·빛·암석 10개·소리 → 반경 14(+1.5) 안 플레이어 30 피해.
  - 피해 방식 = 적 기본 공격과 같음(`TakeDamage(피해 × Shared.Util.DamageTaken(char))`, `LastHitBy` "Burning"/"Slag Walker"). 패링·회피 판정 없음.
  - 습격·경비·Foreman 사이렌 소환으로 나온 같은 종류에도 모두 적용 (EnemyId 로 판단).
- **Slag Walker 균열 예고 + 빠른 범위 표시 (2026-11-21, Studio 버전 112, 사용자: "체력이 낮아지면 몸에 균열, 폭발 예고 / 폭발 때 범위를 빠르게 살짝 보여줬다가 폭발")**:
  - 체력 75% 아래부터 슬래그 껍질 SurfaceAppearance EmissiveStrength 2.5 → 10(10%에서 최대), EmissiveTint 주황 (255,120,40) → 노랑 (255,215,130), SlagGlow 밝기 0.6 → 3.6, Embers·Smoke 양 최대 5배. 30% 아래면 0.24초마다 깜빡임(×1.35 / ×0.7). SlagFX 피격 번쩍임(0.3초)이 기본값으로 되돌리므로 피격 0.35초 뒤 다시 맞춤.
  - 균열 모양 자체(마스크 텍스처)는 그대로, 빛이 세지고 노래지는 것으로 "벌어지는" 느낌. 새 균열 무늬가 필요하면 텍스처를 새로 구워야 함.
  - 폭발 경고: 0.6초 → **0.35초**, 밝은 테두리(반경 14.5, 투명 0.15) + 안쪽(0.55 → 0.25)이 바로 나타났다가 터짐.
  - 플레이 확인: 체력 100/60/40/20% → 세기 2.5/4.2/6.5/7.4, 20%에서 깜빡임(6.2~11.9), 죽을 때 경고 원 2장 → 폭발.
- **스택 규칙 변경 + 야외 반반 생성 (2026-11-21, Studio 버전 113, 사용자 요청)**:
  - 화염 스택: 범위 안 **Molten 마리 수만큼** 1초에 쌓임(최대 10). 범위 밖이면 1초마다 −1, **열기를 5초(CLEAR_AFTER) 동안 안 받으면 전부 0**. ("공격을 안 받으면" = 열기 범위에 안 들어가면으로 해석 — 화상 피해 자체로는 초기화가 안 늦어짐)
  - `FactoryRaid` `enemyKinds()`: EnemyId 가 slag_walker / molten_walker 인 자리(야외 습격 지점 22곳 + 그 근처 상자 경비)는 **Molten ⌈n/2⌉ · Slag ⌊n/2⌋** 으로 나눠 생성. 실내(hook_hauler)는 그대로.
  - 플레이 확인: Molten 3마리 안 → 3·6·9, 밖 → 8·7·6·5 → 5초째 0. 야외 상자 근처 경비 molten 3 · slag 2.
- **폭발 소리·싱크 수정 (2026-11-21, Studio 버전 118, 사용자: "폭발 소리가 과하고 싱크가 안 맞음")**:
  - 원인: ① 엔진 기본 collide.wav 를 볼륨 1.6·속도 0.45 로 틀어 둔하고 큼 ② 터지는 순간 서버에서 소리를 새로 만들어 불러오기·전달 지연 ③ 시체(`workspace.Corpses.SlagWalker_Corpse`)의 SlagFX 가 죽는 순간 3초짜리 균열음(Death+DeathHiss)을 내고 껍질은 1.1초 뒤에야 떨어짐 → 폭발(0.35초)과 소리·깨짐이 따로 놂.
  - 고침: 소리를 **경고 시작 때 미리** `SlagBurst/BurstSound` 에 만들어 두고 터지는 순간 Play (Slag Walker 가 이미 미리 불러온 Impact 9118617342 볼륨 0.9·속도 0.8 + HitSizzle 9119166424 0.35·1.15, 롤오프 10~90). 터지는 순간 시체의 `__Slag` 껍질 9조각을 지우고(대신 암석 14개가 날아감) 시체 Death·DeathHiss 를 멈춤 → 죽을 때 균열음 = 예고, 폭발 = 쿵 한 번.
  - 플레이 확인: 0.1초에 시체 찾음·폭발 소리 IsLoaded true, 0.5초에 껍질 0·폭발 소리 재생 중·시체 균열음 멈춤. 실제 귀로 듣는 크기는 플레이로 확인 필요.
- **범위 원 가까울 때만 + 화면 효과 (2026-11-21, Studio 버전 121, 사용자: "범위가 계속 떠 있어 거슬림, 가까워지면 뜨게 / 화염일 때 화면 효과")**:
  - HeatRing: 클라이언트(FactoryFireHud)가 거리별 `LocalTransparencyModifier` — 28 밖 안 보임, 18 안 완전히 보임. 재질 Neon → **SmoothPlastic**, 투명 0.82 (Neon 은 여러 마리가 겹치면 바닥이 형광 주황으로 덮였음).
  - 화면 효과: `Camera.FactoryHeat` ColorCorrectionEffect (카메라 안 → 내 화면만, LightingService 프리셋에 안 지워짐). 스택 비례 틴트 흰색 → (255,226,205), Contrast 0.05·Saturation 0.05 ×스택/10. 서버가 화염 피해 줄 때마다 캐릭터 속성 `BurnTick` +1 → 클라이언트가 0.35초 붉게 번쩍. 처음 값(255,196,160)은 맵의 주황 안개와 겹쳐 화면 전체가 주황이라 옅게 낮춤.
  - Studio 캡처 2장으로 확인 (첫 장 과함 → 낮춘 뒤 바닥 무늬 비침, 화면 살짝 따뜻함).
- **`StarterPlayerScripts.FactoryFireHud`** (원본 `scripts/factory_fire_hud.client.lua`) — **2026-11-21 다시 만듦 (Studio 버전 119, 사용자: "너무 거슬림, 보이되 시야 방해 없게")**: 화면 가장자리 붉은 효과·큰 동그라미 아이콘 삭제. 체력바(`PlayerGui.StatsHud.StatusHud`) 바로 위 3px 에 붙는 작은 띠(150×18, 반투명 검정): 불 아이콘 16 + 칸 10개(쌓인 만큼 주황, 7 이상 노랑) + 숫자. 스택이 오를 때만 아이콘이 잠깐 밝아짐. StatusHud 의 AbsolutePosition/Size 를 따라 위치·크기(UIScale, 폭/420, 0.75~1.6) 맞춤. Studio 캡처로 겹침 없음 확인.
- 플레이 확인(Studio): 용암 몬스터 옆에서 1초마다 스택 1→6, 멀어지면 1초마다 감소, HUD 표시됨. 검정 몬스터 처치 시 폭발 피해 정확히 30.
- **Hook Hauler 등 약점 (2026-11-21, Studio 버전 122, 사용자 선택 "깔끔한 것 — 등의 갈고리 약점")**: 앞(보는 방향과 내적 ≥ 0.3)에서 맞으면 피해 **×0.5**, 등 뒤(≤ −0.3) **×1.5**, 옆 ×1. 뒤로 맞으면 등 갈고리(`UpperTorso__Paint`)에서 `WeakSparks`(HitSparks 복제) 16개 + `WeakClang`(HitClang 복제, 속도 ×1.35) — 0.15초에 한 번.
  - 방식: 공용 `Combat.DamageDealer` 가 피해마다 `EnemyService.damageTakenMultiplier(humanoid, 때린 사람 위치)` 를 모듈 표로 부르므로, FactoryHazards 가 그 함수를 감싸 hook_hauler 일 때만 배율을 곱함 (공용 패키지 수정 없음). 위치를 안 넘기는 피해(도트 등)는 그대로.
  - 개발용 `ServerStorage.FactoryHazardsTest:Invoke(humanoid, from)` → 현재 배율 (플러그인에서 require 하면 게임과 다른 모듈 사본이라 이걸로 확인).
  - 플레이 확인: 앞 0.50 · 뒤 1.50 · 옆 1.00, WeakSparks·WeakClang 붙음.
- 공용 상태이상(StatusEffects)에 burn 을 넣지 않은 이유: Shared 게시가 필요하고 다른 맵에도 영향 → 공장 전용으로 따로 둠.

### 공장 전용 스크립트 → 패키지로 옮김 (2026-11-21, 사용자: "공장도 패키지 규칙에 맞게 마을로")
- 마을 place(Godstayed)에서 수정, 마을 저장 버전 2410. 수정 전 패키지 최신 확인: Shared v101 · Services v61 · Controllers v87 (Controllers 패키지 ID **80045793841419**).
- Shared `Config.PlaceConfig.SERVICE_PLACE` 에 `FactoryRaid = FACTORY`, `FactoryHazards = FACTORY` 추가.
- Services 에 ModuleScript `FactoryRaid`, `FactoryHazards` (init → task.spawn(run), Main 의 init 순서를 막지 않음). `FactoryRaid.startWave(tier)` 는 모듈 함수로도 노출(_G.FactoryRaid 도 그대로).
- Controllers 에 `FactoryCrateOutlineController`, `FactoryFireHudController`, `FactoryLightFXController` (예전 공장 place LocalScript `FactoryLightFX` 포함, init 에서 `game.PlaceId ~= PlaceConfig.FACTORY` 면 끝).
- 원본: `scripts/packages/Services/*.lua`, `scripts/packages/Controllers/*.lua` (예전 `scripts/factory_*.lua` 는 지움). 내용은 예전 스크립트와 같고 감싸기만 함. 마을에서 6개 모두 컴파일 OK, 저장소 파일과 길이 같음, Source 한 번 다시 써서 패키지 수정 표시.
- **완료 (2026-11-21)**: 사용자 게시 → Shared **v103** · Services **v63** · Controllers **v89**. 공장 place 는 자동으로 새 버전을 받았고, 예전 place 스크립트 5개 삭제(공장 저장 버전 129). 플레이 확인: `[FactoryRaid] 습격 지점 26곳` 한 번, FactoryRaid·FactoryHazards 서비스 시작, 컨트롤러 3개 시작, 상자 36개 CratePrompt 하나씩, FireHud·FactoryHeat·CrateOutlines 하나씩 (두 번 돌지 않음). **사용자 할 일: 공장 place 게시.**
- (예전 남은 순서 메모) ① 사용자가 마을 place 에서 **Shared · Services · Controllers** 게시 → ② 공장 place 에서 세 패키지 "최신 패키지 가져오기" + 예전 place 스크립트 5개 삭제(`ServerScriptService.FactoryRaid`·`FactoryHazards`, `StarterPlayerScripts.FactoryCrateOutline`·`FactoryFireHud`·`FactoryLightFX`) — 안 지우면 습격·경비·화염이 두 번 돎 → ③ 공장 place 게시.

### 화염 피해 틱 화면 흔들림 + 소리 (2026-11-21, 마을 place 에서 Controllers 수정 — 게시 대기)
- 사용자: "불탈 때 소리가 안 남, 화염 피해 받을 때 화면 흔들림과 사운드".
- `Controllers.FactoryFireHudController` 의 BurnTick(서버가 화염 피해 줄 때 +1) 처리에 `burnTick(stacks)` 추가: 게임 공용 `Shared.Util.CameraShake.shake(0.08~0.2, 0.2초)` — 설정에서 흔들림 끈 사람은 `isEnabled()` 로 건너뜀 (무기 타격 0.25, 대지 가르기 0.55 와 비교해 약하게). 소리 = Slag Walker HitSizzle 9119166424 를 SoundService 2D, 볼륨 0.25~0.55(스택 비례), 속도 0.95~1.1 무작위, PreloadAsync.
- 기존 피격 효과(HurtFeedbackController)에는 흔들림이 없어 겹치지 않음(script_grep 확인).
- 마을 컴파일 OK, 저장소 파일과 길이 같음, 수정 표시. **사용자 할 일: 마을에서 Controllers 게시** → 공장은 자동으로 받음(필요하면 "최신 패키지 가져오기") → 공장 place 게시. 실제 흔들림 세기·소리 크기는 플레이로 확인 필요.

### 공장 배경음악 (2026-11-21, 마을 place 에서 Shared 수정 — 게시 대기)
- 사용자 선택: DistroKid 공식 **"Vibration of Decay" 124101361308663** (2분 50초, PreloadAsync Success). Shared `Config.SoundConfig.MUSIC.PLAYLISTS.FACTORY` 추가(한 곡 반복, 볼륨·페이드는 공용 0.35·4초). 음악 규칙 주석에 DistroKid 공식 계정도 허용으로 적음. 마을 저장 버전 2413 무렵. **사용자 할 일: 마을에서 Shared 게시** (Controllers 화염 흔들림 수정과 같이).
- 보스전 음악 후보(로드 확인 Success): APM "Aggressive Intent" 1844326040 (185초), APM "Reap What You Sow E" 9043934139 (148초, 위협적인 메탈 록), APM "Ground Zero A" 1848157566 (173초), DistroKid "Obliterarated Civilization" 128469069192692 (90초). 로드 실패(이 게임에서 못 씀): APM "Pendemonium" 9039352991, "The Evil One" 1846325632.
- 보스전에 곡을 바꾸려면 MusicController 에 기능 추가가 필요 (지금은 장소마다 목록 하나만).
- **추가 (2026-11-21, 마을 저장 2416 무렵)**: FACTORY 재생 목록 3곡 = Vibration of Decay + **Tectonic Drag 79229053489933** (2:56) + **The 50Hz Ritual 71564549639562** (2:44), 섞어서 번갈아.
- **보스전 음악**: Shared `SoundConfig.MUSIC.BOSS.FACTORY = { id 1848157566 (APM "Ground Zero A"), endAt 167.4, range 110, leaveDelay 6, fadeTime 2 }`. 사용자는 "2:58 에서 자르기"라 했지만 실제 길이 2:53.28 — AudioAnalyzer RMS 로 재 보니 **167.5초(2:47.5)부터 무음** → 167.4 에서 처음으로 되감음.
- Controllers `MusicController` 에 보스전 기능 추가: 0.5초마다 `workspace.Enemies` 에서 속성 Boss 인 살아 있는 모델이 내 캐릭터 range 안이면 재생 목록 SoundGroup 볼륨 0 + BossMusic(SoundService, Looped, Heartbeat 에서 endAt 넘으면 TimePosition 0) 페이드 인. 벗어나거나 보스가 쓰러지고 leaveDelay 지나면 되돌림. BOSS 설정이 없는 장소는 아무것도 안 함.
- 두 스크립트 컴파일 OK, 수정 표시. **사용자 할 일: 마을에서 Shared · Controllers 게시** (화염 흔들림 수정 포함) → 공장 place 게시. 보스 근처에서 곡이 바뀌는지는 플레이로 확인 필요.

### 화염·폭발이 옥상까지 닿던 버그 수정 (2026-11-21, 마을 place 에서 Services 수정 — 게시 대기)
- 사용자: "몬스터가 바닥에 있고 내가 옥상에 있어도 화염 데미지". 원인: 3D 거리(14)만 봐서 바로 위 층·지붕도 범위 안.
- `Services.FactoryHazards` 에 `reaches(from, to, radius)`: 수평 거리 ≤ radius + 높이 차이 ≤ **7** + 몬스터→플레이어 광선에 CanCollide 파트가 없음(적·캐릭터 제외, CanQuery 꺼진 연출 파트는 원래 안 잡힘). 화염 스택(heatCount)과 Slag Walker 폭발 피해 둘 다 이 판정.
- 공장 지형 시험: 같은 바닥 8 옆 → 닿음, 압연동 안 지점 바로 위 지붕(y 28) → 안 닿음, 야외 10 옆 → 닿음. 마을 컴파일 OK, 저장소와 길이 같음, 수정 표시.
- **사용자 할 일: 마을에서 Services 게시** (Shared·Controllers 와 같이) → 공장 place 게시.

### 몬스터 소리(상가 방식) + 공격 소리 + 체력바 피격 강조 (2026-11-21, 마을 place 수정 — 게시 대기)
- 확인: 그동안의 수정(옥상 버그·보스전 음악·화염 흔들림)은 이미 게시됨 — Shared v109 · Services v66 · Controllers v91 (마을 사본 = 최신).
- **상가 조사(상점 지구 place, 읽기만)**: 좀비(Toothed Revenant)는 소리 없음. 들리던 소리 = Shutterback 의 `GearSpinController`(클라이언트) — 몸에 반복 톱니음(0.9, 롤오프 10~70, 서버 `Alerted` 속성이면 커짐) + 공격 시작 갈림음(1.2). `Alerted/Attacking` 은 적 정의 `gearSpin = true` 일 때만 서버가 넣음.
- **몸 소리** Controllers `FactoryMonsterSoundController` (원본 `scripts/packages/Controllers/`) + Shared `SoundConfig.FACTORY_MONSTERS`: 몬스터 HRP 에 반복 소리, 가만히 idleVolume → 추격(WalkSpeed > 정의 walkSpeed) alertVolume·alertSpeed, 롤오프 10~70, **가까운 6마리만**(0.5초마다 고름, 부드럽게 줄임), 죽으면 꺼짐. slag 9118030782(타닥, 0.3→0.7, 속도 0.7) · molten 같은 소리(0.4→0.9) · hook_hauler ChainDrag 9113763407(0.25→0.8) · furnace_tender/warden LanceHiss 9119166195(0.3→0.75) · foreman Static 9113073932(0.35→0.9, 거리 110).
- **공격 소리**(Enemies 모델): Slag/Molten Impact 0.8→1.0, HookHauler Swing 0.45→0.7·Impact 0.75→1.0, Tender/Warden Thrust 0.4→0.7·Impact 0.6→0.9, 모두 RollOffMin 8→10 (상가 1.2 보다 낮게). Slag/Molten **예고음** `UpperTorso.Windup`(HookHauler Swing 9119468100, 0.55, 10~60) — SlagFX 가 공격 애니 시작마다 play("Windup").
- **체력바 피격 강조** Controllers `StatsController.HealthBarView` (모든 맵 공통): 깎인 비율 2% 미만은 예전처럼 잔상만, 2~30% 비례 세기 k — 띠 흔들림 1.5~6px·0.12~0.35초, 테두리(frame 이미지) 붉게 번쩍, 잔상 깜빡임(k≥0.3 1번, ≥0.75 2번), 잔상 머무름 0.35~0.6초·줄어듦 0.5~0.8초, 체력 숫자 붉게 + 1~5 커짐. 상수 표 `HIT`. 흰 번쩍은 이미지 밝기를 올릴 수 없어 깜빡임으로 대신.
- 마을 컴파일 OK, 수정 표시, 마을 저장. **사용자 할 일: 마을에서 Shared · Controllers · Enemies 게시** → 공장 place 게시. 실제 소리 크기·체력바 느낌은 플레이 확인 필요.
- **게시 완료**: Shared v110 · Controllers v92 · Enemies v7 · Services v66. ⚠ 게시 전부터 열려 있던 공장 Studio 창은 예전 버전(v107/91/6/64)을 들고 있었고, 패키지 옵션에 업데이트 메뉴가 없었음(버전 비교·세부 정보만) → **공장 place 를 닫고 다시 열자 자동으로 최신**이 됨. 스크립트 InsertService·insert_asset 으로 패키지를 다시 넣는 건 권한 오류로 안 됨. **다른 place 가 예전 버전이면 그 place 를 다시 열 것.**
- 공장 플레이 확인: 보스 마당 근처 적 17마리 모두 `FactoryBodyLoop` 붙음, 소리 나는 건 범위 안 2마리(가까운 6마리 제한 동작), 보스 근처라 BossMusic 재생. **사용자 할 일: 공장 place 게시.**

### 공장 배경음악 크기 70% (2026-11-21, 마을 place 에서 Shared·Controllers 수정 — 게시 대기)
- 사용자: "공장 BGM 만 70%". (처음엔 공용 volume 을 줄였다가 사용자 정정으로 되돌림.) Shared `SoundConfig.MUSIC.volume` 0.35 그대로 + 새 `MUSIC.PLACE_VOLUME = { FACTORY = 0.245 }`. Controllers `MusicController` 가 시작할 때 장소 키로 `VOLUME` 을 골라 재생 목록·보스전 음악 둘 다에 씀 (없으면 공용 volume). 다른 맵은 그대로.
- 마을 컴파일 OK, 수정 표시, 저장. **사용자 할 일: 마을에서 Shared · Controllers 게시** → 공장(예전 버전이면 다시 열기) → 공장 place 게시.

### 패키지 게시 (2026-11-21)
- 공장 place에서 게시 성공: **Shared v88, Services v60, Enemies v5** (Studio 가 "UploadStatusPolling max polling retry reached" 오류를 띄웠지만 실제로는 서버에 올라가 있었음 → 오류가 나도 Open Cloud `GET /assets/v1/assets/<id>` revisionId 로 확인할 것). 패키지 ID: Shared 135710242377375, Services 73196577937994, Enemies 91177418448007.
- ⚠ 사고: 마을 place(신이 머물렀다, 133122559439695)의 **예전 Shared 사본이 v89 로 게시**되면서 공장 내용(RaidConfig·LoadingConfig·PlaceConfig·LightingConfig·CrateConfig·Data.Enemies.Factory)이 빠졌고 공장 place 도 v89 로 자동 업데이트됨. → Open Cloud `POST /assets/v1/assets/135710242377375/versions:rollback` (assetVersion …/versions/88) 로 **v90 = v88 내용** 복구. v89 와 v90 차이는 위 공장 파일들뿐(마을에만 있던 내용 없음, 전체 소스 해시 비교). 마을 place `ServerStorage.Shared_v89_backup` 에 v89 사본 보관(확인 후 지워도 됨).
- **2차 게시 (2026-11-21 06:54 UTC, 사용자) — 확인 완료**: Enemies **v6** (Foreman 메쉬 크기 + 공장 적 6종 AutomaticScalingEnabled=false), Shared **v91** (지도 구역 그림 v2 95809363736667), Services v60 그대로. 공장 place 06:55 · 마을 place 06:57 게시. 두 place 모두 Shared v91·Enemies v6, RaidConfig 에 새 그림·Steelworks·Data.Enemies.Factory 있음. (마을 ServerStorage 의 Foreman 은 팔 CFrame 이 옛 값이라 겉보기 폭이 11 이지만, 꺼내면 3.95×5.97×3.19 로 정상.)
- **백업 정리 (2026-11-21, 사용자 요청)**: 공장 place ServerStorage 에서 LotDressing_Lot057/043/011_024/042/SouthStrip/Lot025_Backup, RoadCars_Factory_Backup, Foreman_v1_backup 삭제 (Studio 버전 115). 마을 place `Shared_v89_backup` 삭제 (마을 버전 2385). 남김: `EnemySpawns_FixedBackup_20261121`(습격 방식 되돌릴 때), 원래 있던 Backup·BuildingKit_Backup·Backup_FloorPortals·WeatherSwapBackup(다른 작업 것). 되살리려면 place 버전 기록에서.
- **규칙 (2026-11-21 바뀜, `CLAUDE.md` "Roblox 패키지 스크립트 수정 규칙")**: 패키지 코드는 **마을 place(Godstayed)에서만** 수정(multi_edit → execute_luau 로 Source 한 번 다시 써서 수정 표시), 게시는 사용자가 직접. 다른 place 에서는 "최신 패키지 가져오기"만. 공장 전용 스크립트(FactoryRaid·FactoryHazards·FactoryCrateOutline·FactoryFireHud)는 패키지 밖이라 공장 place 에서 고치고 place 게시.

## 2. 다음 할 일

1. 사용자 확인 → 수정. 보스 마당·철도 야드·배랭 완료(✔).
2. 랜드마크 4종 완료(용광로 ✔ → 냉각탑 ✔ → 압연 공장동 ✔ → 코크스로 ✔). 계획서 6장 3단계 중간 에셋: 가스 홀더(F) ✔, 스태커-리클레이머(C) ✔, 배관 다리 키트 ✔ + H 회랑 ✔, 컨베이어 갤러리 ✔ (코크스로 석탄탑 갤러리는 원료 야적장 환적탑에 이미 연결됨), 굴뚝 ✔ → **3단계(중간 에셋) 끝**. 남은 블록아웃 에셋화 끝(E ✔ → F2 ✔ → G ✔). `FactoryBlockout`에는 빈 그룹(C_RawYard, K_Common)만 남음. 4단계 바닥 마감 ✔. 5단계 소품·표지·낙서 ✔. 6단계 조명·연기 ✔. 7단계 상자·등반 태그 ✔(공장 + 운하 존). ⚠ 공용 패키지(Shared: PlaceConfig·LightingConfig·CrateConfig, Services: LightingService) 게시는 사용자. 8단계 자동 검사·최적화 ✔. **계획서 1~8단계 모두 끝.** 남은 것: 패키지 게시, 실제 플레이 확인(사용자). 이전 메모: 6단계(조명: 출선장·압연동·터빈홀 실내등, 먼지·연기).
   - Lot_025: 서쪽 모서리에 컨베이어 전환탑·계단탑(X −1015..−1001, Z 985..1007)과 S2 갤러리가 대각선으로 지나감, 동쪽 모서리에 배관 다리 J 타워 → 가스 시설은 그 사이 빈 땅에.
3. ✔ (2026-11-21) 대각선 길 북서쪽 삼각 부지 Lot_025 → **고로 가스 정제 시설** `GasClean` 완성 (아래 "### 고로 가스 정제 시설" 참고).
4. (완료) 굴뚝 3기 배치 — 블록아웃 자리 그대로 사용.
5. 옛 LotDressing(공원 나무·주차 차량) 정리 → 산업 부지 바닥 마감 (사용자가 알아서 정리해도 된다고 함).

## 3. 창(Polearm) 무기 스킬 (2026-11-23 시작, 마을 place 패키지 코드)
- 설계(사용자): 창 = 긴 사거리로 거리를 지배하는 창병. 스킬 5종 — 도약 찌르기 / 창 휘두르기 / 관통 돌격 / 사슬 갈고리 / 신의 창.
- 결정(사용자): 관통 돌격 = 기존 `piercing_lunge` **강화**(새로 만들지 않음) / **하나씩 만들고 확인** / 모션은 **기존 모션 재활용**(든 무기 첫 타 콤보를 당긴 자세로 멈췄다 빠르게, PiercingLunge 방식).
- 구조: 스킬 정의 `Shared.Data.Skills`(kind별 판정), 성유물 `Shared.Data.Relics.PolearmRelics`(skill = id, 무기 소켓에 끼움), 서버 판정 `Services.Skill`(plan()에서 kind별 분기), 연출 `Controllers.SkillController.Vfx.<vfx>`. 기존 끌어당기기 = `Skill.pullTarget` → `Enemy.pull`(보스는 안 끌림).
- ✔ **사슬 갈고리** `chain_hook` (kind **"hook"** 새로 추가, 성유물 `relic_chain_hook`):
  - 판정: castDelay 0.22 → 창이 직선 150스터드/초, 최대 45, 폭 2.5(벽·첫 적에서 멈춤, Humanoid 모델은 벽으로 안 봄) → 도착 순간 그 적이 6스터드 안에 있으면 피해 ×1.6 + 내 앞 4.5까지 0.35초에 끌어옴 → 끌려온 뒤 경직 0.6. 쿨 9초. 분신(echo)은 따라 하지 않음.
  - 연출 `Vfx.ChainHook`: 든 창(HeldWeapon) 복제본을 실제로 던짐(원래 창은 이 화면에서만 숨김), 손→창 꼬리 쇠사슬 고리 70개(BulkMoveTo) + 금빛 Beam, 벽이면 불꽃·먼지, 걸리면 섬광·불꽃·타격음·화면 흔들림, 창끝이 끌려오는 적 몸에 붙어 따라옴 → 손으로 회수 + 짤랑. 빗나가면 빈 사슬을 거둠. 소리는 Hook Hauler 사슬 소리 재사용.
  - 확인: Studio 플레이에서 서버 모듈 로드 OK, 클라이언트 연출(빗나감·걸림) 오류 없음, 창 숨김/복귀·사슬·창이 대상에 붙음 확인.
  - **실제 시전 확인 (2026-11-23, 사용자 데이터로)**: Bloated Husk(스킬 훈련용, `Enemy.spawnTemporary` 를 플레이 중 임시 Script 로 호출)에 43스터드에서 시전 → +0.54초 phase "hit", 0.3초 만에 47→6스터드로 끌려옴, 피해 들어감, 오류 없음.
    - 고친 버그 2: ① 큰 적(몸 중심이 5스터드 높음)을 옆 거리 3D로 재서 빗나감 → 옆은 수평으로만, 높이는 따로(HOOK_HEIGHT 8). ② 몸에 붙은 적(창 출발점보다 뒤)은 안 걸림 → 몸 중심부터(along > −CAST_FORWARD−1). ②는 로드만 확인.
    - 참고: 플러그인(MCP execute_luau)에서 require 한 모듈은 게임과 다른 복사본 → 실제 서비스 함수는 플레이 중 Script 를 만들어 부르면 됨. NPC(RelicKeeper)는 Humanoid 가 없어 벽으로 막힘(정상).
    - 사용자 저장 데이터 변경: stone_spear 1개 지급(/get), 창 성유물(/relics polearm), 돌창 소켓 1칸 해금(비용만큼 /money 1000·/get bloodstone 1 먼저 지급), relic_chain_hook 끼움, **장착 무기를 Junkyard Ripper → Stone Spear 로 바꿈**.
  - 임시: 성유물·스킬 아이콘 = Piercing Lunge 아이콘(전용 아이콘 필요). `Skills` 의 `TEST_COOLDOWN = 1`은 예전부터 켜져 있음(게시 전 nil 로).
  - **게시할 패키지: Shared(Skills·PolearmRelics), Services(Skill), Controllers(Vfx.ChainHook 새 모듈).** 수정 표시 후 패키지 버전이 Shared v127 · Services v75 · Controllers v106 으로 올라가 있었음(이전 v126/74/104).
- ✔ **사슬 갈고리 위·아래 조준 (2026-11-23, 사용자: "카메라 + 보정, 보정은 조금만 낮게" / "포물선으로 끌어옴")**:
  - 클라이언트 `SkillController.cast`: 카메라 화면 가운데 레이가 닿는 점(캐릭터 앞부터, 250)을 내 가슴에서 본 방향 = `aim` → `SkillCast:FireServer(소켓, facing, nil, aim)` (모든 스킬에 보내지만 hook만 씀). hook은 조준 쪽으로 몸을 돌리고 던짐.
  - 서버 `hookAim`: 몸 방향(facing)에 aim 의 **높낮이만** 가져옴(±maxPitch 55°, aim 수평 방향이 facing 에서 30° 넘게 벗어나면 수평). 그다음 **보정 aimAssist 6°**: 그 안의 가려지지 않은 적 몸 중심으로.
  - `hookPath` 교체: 가슴에서 3D. 벽 = **가는 레이**(굵은 구로 재면 턱 위 적을 노릴 때 턱 모서리에 걸림 — 테스트에서 실제로 걸렸음), 적 = 굵기 pathRadius 구를 대상 모델만 Include 로(큰 적은 몸 어디든), 몸에 붙은 적은 따로. HOOK_SLACK 8(3D).
  - `hookPull`(새): 적 폴더 안·보스 아닌 적을 서버가 매 프레임 위치를 옮겨 **포물선**(높이 arcHeight 3 + 올라올 때 높이 차 × 0.5)으로 내 앞 4.5 **바닥(레이로 찾음)**에 내려놓음, 끌리는 동안+끝나고 flinch 경직. 플레이어(PvP)는 forceMove 직선. 보스·더미는 피해만. pullTime 0.35 → 0.4.
  - 테스트(임시 발판 12스터드 높이, Bloated Husk): ① 발판 위 적(24 앞, 13.7 위)을 3° 낮게 조준 → 보정으로 맞음, 포물선으로 내 앞 바닥(4.5)에 내려옴. ② 내가 발판 위, 적은 9.8 아래 → 포물선(최고 +6.8)으로 발판 위 내 앞 4.5에 올라옴(착지 후 살짝 튐). 오류 없음.
  - ⚠ 테스트 팁: 서버에서 캐릭터를 PivotTo 하면 클라이언트 위치와 어긋남 → 캐릭터 이동은 Client 쪽에서.
  - 한계: 서버에 몸 회전이 늦게 도착하면 facing 이 예전 방향(±90° 안)일 수 있음 → 그때는 수평으로 던짐.
  - 게시할 패키지에 **Controllers(SkillController)** 추가.
- **사슬 갈고리 개선 3가지 (2026-11-24 시작, 하나씩 사용자 확인)**: ① 1.5초 기절 ② 그랩 보정 ③ 바닥에 맞으면 끊기지 않고 직선으로 이어 나감.
  - ✔ ① **기절 1.5초** (결정: 맞은 순간부터 / 기절 중 이동 스킬로 못 풂 / 적+PvP 플레이어, 보스 제외 / 끝난 뒤 경직 0.6 은 기절로 대체 / 이미 진행 중인 대시·돌격·도약은 **그대로 둠** / 강철 의지(Unstoppable)면 기절도 무시).
    - `Skills.chain_hook`: `flinch = 0.6` 삭제 → `stun = 1.5`. `Services.Skill` `hookHits`: 피해가 들어가면 `StatusEffect.apply(target, "stun", 1.5초)` (Boss·Unstoppable 제외) 후 끌기. `hookPull` 의 flinch 기본값 0.6 → 0 (적은 끌리는 동안만 hitReact).
    - 기존 기절(Stunned 속성)이 이미 대시(클라 MovementController)·모든 스킬(클라+서버)·점프·걷기(Movement WalkSpeed 0)·공격·적 AI 를 막음 → 따로 막을 코드 없음.
    - 플레이 확인: 훈련용 적(bloated_husk)에 22 거리 시전 5번 → 서버 Stunned 지속 1.50~1.52초, 끌려와 4.6 앞, 오류 없음. PvP 는 혼자라 확인 못 함.
    - 게시할 패키지: Shared(Skills), Services(Skill).
  - ✔ ② **그랩 보정** (사용자: "너무 맞추기 힘듦, 추천해 줘" / PvP 도 적용): `Skills.chain_hook` `aimAssist 6 → 12`, `pathRadius 2.5 → 3.5`, 새 필드 `hookSlack = 12`(날아가는 동안 움직여도 걸리는 거리, 서버 `HOOK_SLACK` 8 대신 `skill.hookSlack or HOOK_SLACK`). 조준 보정은 원래부터 `humanoidsInRadius(..., true)` 로 플레이어도 찾음(보호 대상 제외) → PvP 추가 코드 없음.
    - 확인: 플레이 시작 시 Skill 서비스 로드 오류 없음. **각도별 명중 테스트는 실패**(테스트 중 캐릭터·적 위치가 계속 밀려 결과를 못 믿음) → 실제 플레이로 손맛 확인 필요. 더 쉽게/어렵게는 위 세 수치로 조절.
    - 게시할 패키지: Shared(Skills), Services(Skill).
  - ✔ ③ **바닥에 맞으면 수평 직선** (결정: 꺾지 않고 **처음부터 가슴 높이 수평**으로 / 길이는 최대 사거리 45 그대로): `Services.Skill` `hookPath` 를 안쪽 함수 `trace(dir)` 로 나눔 → 아래로 조준해 적보다 먼저 닿은 면이 바닥(법선 Y ≥ `HOOK_FLOOR_NORMAL` 0.7)이면 같은 수평 방향으로 다시 잼. 위로 조준·벽은 그대로. 연출(Vfx.ChainHook)은 origin·impact 를 따라가므로 수정 없음.
    - 플레이 확인(SkillFx payload): 조준 0°/−20°/−45° → 모두 수평(높이 차 0) 41.5 앞, +20° → 위로 14.2·수평 39 (높낮이 조준 유지). 오류 없음.
    - 게시할 패키지: Services(Skill).
  - ✔ **회수 뒤 남는 빛** (사용자: "돌아왔을 때 몸 앞에 빛 하나가 남음 → 창 날 끝에"): 원인 = 창끝 빛(`HookTip` 의 HolyFlare glint)이 회수 지점(손)에 멈춘 채 연출 끝까지 남음. `Vfx.ChainHook`: `heldTip()`(든 창 Handle 의 TrailTip) 추가, 회수가 끝나면 매 프레임 glint 를 든 창 날 끝에 붙이고 마지막 0.3초에 사라짐. 플레이 확인: 회수 뒤 날 끝과 거리 0.00~0.01, 끝에 투명도 0→1, 오류 없음.
  - **사슬 갈고리 3가지 + 빛 끝. 전체 게시: Shared(Skills), Services(Skill), Controllers(Vfx.ChainHook).**
- ✔ **도약 찌르기** `leap_strike` (kind **"leap"** 새로 추가, 성유물 `relic_leap_strike`, 2026-11-23). 결정(사용자): 착지 = **카메라 조준 지점** / 천장이 낮으면 **낮게 뛰어 찌르기**.
  - 서버 `leapPlan`: 조준(사슬 갈고리와 같은 `hookAim`, 높낮이 ±55°) 레이가 닿는 곳(최대 28)의 바닥 = 착지. 보정 6°: 조준선 안의 보이는 적이면 그 적 바로 앞 발밑. 바닥이 없으면(허공) 제자리 도약.
  - **천장 처리**: 경로 a→b 위 포물선 높이 4h·k(1−k)를 몸 크기 구(root+1.1, 반지름 1.4)로 12구간 미리 훑고, 막히면 최고 높이 apex(10)를 ×0.7/0.45/0.25/0.1/0 으로 낮춤 → 직선도 막히면 막히기 직전 바닥에 착지. 캐릭터는 물리 점프가 아니라 연출 모듈이 같은 식으로 매 프레임 CFrame 을 옮김(속도 0) → 머리를 박지 않음.
  - 판정 `leapHits`: 자세부터 착지까지 무적(ForceField)·적 통과, 착지(castDelay 0.2 + airTime 0.32~0.62) 순간 반경 9 피해 ×2.4 + 바깥으로 밀침 9(가까울수록 멀리) + 경직 0.5. 쿨 8.
  - 연출 `Vfx.LeapStrike`: 첫 타 모션을 당긴 자세로 멈췄다 착지 직전 빠르게 찌르기, 착지 자리에 도는 빛의 고리(예고, 다른 사람에게도), 창끝 빛 모임 → 뛰어오를 때 발밑 먼지·바람 소리·시야각 킥·빛 꼬리 → 착지 섬광·빛의 창 기둥·충격파 고리·균열·돌 파편·먼지·불꽃·화면 흔들림.
  - **같이 고친 버그(hook·leap 공통)**: 클라이언트가 조준 쪽으로 몸을 돌려도 그 회전이 시전 신호보다 늦게 서버에 도착 → 서버의 몸 방향 검사(±90°)에 걸려 **예전 방향으로 나감**(테스트에서 거의 반대로 뜀). hook·leap 은 보낸 수평 방향을 그대로 씀(어느 쪽이든 돌아서면 되는 것이라 이득 없음).
  - 테스트(사용자 데이터, 테스트 동안 내 캐릭터에 보이지 않는 ForceField — 적에게 맞아 죽고 리스폰하면 위치가 튀어 결과가 엉킴): ① 몸 방향과 40° 다른 쪽 20 앞 적 → 적 바로 앞 착지, 피해 들어감, apex 10, 0.62초. ② 허리 위 +6 천장(임시 판) 아래 → apex 10→2.5 로 자동, 머리 꼭대기가 천장에서 0.55 아래까지만, 18.5 앞 착지. 오류 없음.
  - 사용자 데이터 변경 추가: 돌창 소켓 2칸째 해금(비용만큼 /money 3000·/get bloodstone 2 먼저 지급), /relics polearm 한 번 더, 소켓 2 = relic_leap_strike.
  - 게시할 패키지: Shared(Skills·PolearmRelics), Services(Skill), Controllers(SkillController·Vfx.LeapStrike 새 모듈).
- ✔ **도약 찌르기 수정 + 이펙트 새로 (2026-11-24, 사용자: 달리면서 쓰면 제자리 점프 / 지그재그 균열 AI티 / 이펙트 밋밋 → Blender 프레임 시트로)**
  - 결정(사용자): **무기별 이펙트 색 — 창 = 흰 + 초록** (헤비 주황, 대거 보라, 라이트 파랑, 원핸드 자홍) / 제작 = Blender 시뮬·렌더 / 균열 = 그림 + 들린 돌판 둘 다 / PC 우선 고품질 / 요소 = 착지 폭발·균열+돌판·도약 구간(착지 예고 표시는 뺌) / 간판 = 땅에 박힌 초록 빛 결정 창 / 다른 창 스킬 초록은 나중에.
  - **달리며 쓰면 제자리**: 원인 ① 서버가 보는 내 자리가 달리는 동안 뒤처져 착지가 짧아짐 ② 기본 카메라 각도면 조준이 ~16 앞이라 달리는 거리를 빼면 거의 안 뜀. 수정: 클라이언트가 시전 순간 자기 자리를 같이 보냄(`SkillCast` 5번째 인자, 서버 자리 10 안이면 씀), `minDistance 14`, **달리던 힘**(조준 쪽 속도 × (castDelay + 0.5)) 만큼 더 멀리(최대 28). W+F 실제 키 입력 테스트: 14 → 21 앞.
  - **Blender 이펙트 파이프라인** (`scripts/vfx_sheet_kit.py`: vfx_scene / pack_sheet / render_sheet): 이 PC Blender 는 **GPU 렌더 없음(CPU)**, 볼륨은 프레임당 ~20초 고정 비용 → `.blend` 저장 후 **명령줄 Blender 4개 병렬** `D:lender.exe -b <blend> -S <장면> -o //_frames/<이름>/f#### -F PNG -t 4 -s a -e b -a`, 그다음 pack_sheet 로 8x8(칸 128) 합침. 업로드 = Open Cloud Decal(그룹) → childOperations 의 이미지 ID.
    - `vfx_leap_dust.py` 흙먼지 덩이(볼륨 구 + 4D 노이즈, 콜리플라워 모양) → `Dust` 138956275728767
    - `vfx_leap_shock.py` 바닥 충격파(발광, 날카로운 앞 날 + 뒤 초록 꼬리 + 둘레 밝기 + 방사 줄기) → `Shock` 139231006156621
    - `vfx_leap_crack.py` 균열: 선을 실제 리본 메시로 그림(주 균열 8개 랜덤워크 + 가끔 꺾임 + 갈래 + 동심 이음 + 중심 잔금), 1024x512 = 왼쪽 선 / 오른쪽 빛(굵게+흐림) → `Crack` 110852548933346
    - `vfx_leap_meshes.py` 결정 창날 7조각(+옆 결정 가시, 코등이) + Core + BaseShards + 돌판 8 + 돌 4 → Model 114243306439321 → **`ReplicatedStorage.Assets.Vfx.LeapStrike`** (CrystalSpear·Slabs 피벗 = 땅 높이 중심, 결정 = Glass 초록, 심 = Neon)
    - ID 기록: `exports/texture_ids.json` → `VFX.LeapStrike`
  - 연출 `Vfx.LeapStrike` 새로 씀: 웅크림 초록 기운 → 뛸 때 발밑 작은 충격파 + 먼지 + 초록 꼬리 → 착지: 결정 창(1.6배, 땅에 2.2 박힘, 크게 나타났다 제 크기, 0.7초 뒤 조각이 튀며 부서짐), 바닥 충격파 시트, 먼지(파티클 Flipbook Grid8x8 OneShot, ZOffset 2.5 — 큰 덩이가 바닥에 잘려 보이는 문제), 균열 선(2.4초)+빛, 돌판 고리 솟음→1.3초→가라앉음, 돌 파편 12(물리), 섬광·짧은 초록 빛, 화면 흔들림.
    - ⚠ 같은 속성 트윈을 지연으로 미리 만들면 앞 트윈이 취소됨(돌판이 안 솟던 원인) → 뒤 트윈은 `ctx:at` 으로 나중에 만듦. 시트 재생 시작 시각은 `ctx:clock()` 기준.
  - 확인: `/fx` 대신 Client 에서 모듈을 직접 불러 0.2배속 재생 + 확인용 캡처(보고용 아님). 남은 아쉬움: 결정 조각 튀는 순간·먼지 색은 실제 플레이로 봐 줘야 함.
  - **게시할 패키지 추가: Assets (Vfx.LeapStrike 메시)**. 전체: Shared(Skills·PolearmRelics), Services(Skill), Controllers(SkillController·Vfx.ChainHook·Vfx.LeapStrike), Assets.
- **✖ 접음 (2026-11-24, 사용자: "접어") — 꽂히는 창을 든 창 복제본으로 바꿔서 더 안 함. 아래는 기록용.** 도약 찌르기 '빛의 창' 다시 만들기 (2026-11-24) — 사용자: 결정 창이 "초록 덩어리 같다, 렌더링 안 된 느낌" → 참고 이미지(기계식 검은 창 + 빛나는 결정 날)와 **모양은 똑같이, 색은 초록**. **단계마다 사용자 검사받기.**
  - 같이 바꿈(마을 place, 게시 전): 도약을 빠르게 — `castDelay 0.2→0.1`, `apex 10→8`, 체공 `0.24~0.42`, `LEAP_RUN_AIR 0.35`.
  - 중간 시도(폐기): v1 `vfx_leap_lance(_mat).py`(잎 모양 날, SurfaceAppearance 색·발광·금속·거칠기 구워 업로드 → `Assets.Vfx.LeapStrike.LightLance` 에 들어가 있음, 이미지 ID 색 126950760243716 / 발광 100757329927763 / 금속 93798015252632 / 거칠기 125238419555069, 모델 109484363035524) — **Vfx.LeapStrike 코드는 아직 옛 CrystalSpear 사용**(lightLance 교체 편집은 사용자가 중단). v2 `vfx_leap_lance2(_mat).py` 도 참고 이미지와 달라 폐기.
  - **v3 = reference-modeling 스킬 절차** (새로 설치: reference-modeling·game-asset-modeling·blender-modeling·roblox-vfx·roblox-animation-vfx):
    - 0단계 ✔: 참고 `references/lance_ref.jpg` → 세로로 세움 `lance_ref_straight.png`(머리 끝 아래 z=0, 꼬리 위 z=30, **1스터드 = 49.15px, 아래 여백 20px, 폭 260 / 높이 1514**), 실루엣 마스크 `lance_mask.png`(어두운 모양/밝은 배경), 확대 `zoom_head/neck/butt.png`. 사용자 확인함.
    - 부위(세운 이미지 기준, x 가로 / z 높이): **오른쪽 큰 결정** z0→9.7(끝 x0.45 → 뿌리 x1.75, 폭~0.85) / 왼쪽 작은 결정 z2→7 / 왼쪽 위로 솟은 검은 지느러미 2 z6.5→10.3 / 가운데 검은 창끝 z0.4→6 / 머리 하우징(링 구멍) z5.5→8 / 톱니 척추 z8→11 / 늘어진 빛 띠(왼쪽 사선) z10.7→11.6 / 오른쪽 케이블 z11→12.5 / 빛 구슬 허브 z12.3→12.9 / 열린 틀(오른쪽 연 모양) z12.9→14.8 / 자루 z14.8→23.4 / 캡슐 틀(빛 관) z23.4→25 / 꼬리: 세로 창끝 + 오른쪽 삼각 지느러미(바깥 날에 빛 줄) z25→30.
    - 1단계 블록아웃 ✔(사용자 검사 대기였음): `scripts/lance3_blockout.py`(상자 17 + 꼬리 삼각), 측정 `scripts/lance3_iou.py`(정면 렌더 vs 마스크 IoU, 구간별 넘침/모자람, 차이 그림 `references/lance_iou_diff.png`). IoU 0.594 (머리 0.61/목 0.39/자루 0.80/꼬리 0.62). 비교 그림 `references/lance3_blockout_check.png`. 저장 `exports/vfx/lance3.blend`.
    - **다음 2단계 계획**: 마스크를 행 단위(≈0.1스터드)로 읽어 부품별 윤곽을 그대로 따라 메시 생성 → IoU ≥ 0.9. 색으로 나눔(파랑 채도 큰 곳 = 결정, 작은 조각 = 금속 위 빛 줄 → 꼭짓점 Glow, 어두운 곳 = 금속). 단면: 결정 = 가운데 능선 마름모(폭 따라 두께), 금속 = 폭에 비례한 두께. **참고 그림 픽셀을 텍스처로 쓰지 않음**(모양만 측정, 재질은 직접). 그다음 3단계 두께·단면 → 굽기(색/발광/금속/거칠기) → 업로드 → `Vfx.LeapStrike` 에서 CrystalSpear 대신 사용(내리꽂힘 + 빛 조각으로 흩어짐).
    - ⚠ Blender MCP 가 응답 없음(Blender 는 멀쩡, CPU 0) → **명령줄 Blender 로 작업**: `D:lender.exe -b --factory-startup --python-expr "exec(open(r'D:\god\scripts\lance3_blockout.py', encoding='utf-8').read()); exec(open(r'D:\god\scripts\lance3_iou.py', encoding='utf-8').read())"` (한 번 10초). 스크립트는 창이 없으면 기본 장면을 비워 씀. 시스템 Python 엔 numpy 없음 → 이미지 처리는 Blender 안에서.
    - 저작권: 참고 이미지가 남의 작품인지 사용자에게 물었고 아직 답 없음.
- ✔ **도약 찌르기: 꽂히는 창 = 내 창, 먼지 회백색 (2026-11-24, 사용자 지시)** — 결정: 손의 창은 그대로(땅에는 복제본) / 초록 빛 유지 / 크기 1.6배 / 먼지 = 밝은 회백색.
  - `Vfx.LeapStrike`: `cloneHeld()`(HeldWeapon 복제, 손 연결·스크립트 떼고 Trail 끔, 손잡이만 고정, `Model:ScaleTo` ×`HELD_SCALE 1.6`, 창 축 = Handle 의 TrailBase→TrailTip) + `heldLance()`(창끝이 땅 속 2, 진행 방향으로 10° 기울어 위에서 내리꽂힘 → 초록 불빛·후광·알갱이 → 0.7초 뒤 투명해지며 초록 빛 조각으로 흩어짐). 든 창이 없으면 예전 `lightLance`(빛의 창 v1) 그대로. 빛의 창 v3 작업은 **접음**(사용자 결정).
  - 먼지: `dustEmitter` 색 (200,188,170) → `DUST_COLOR` (232,230,226) — 착지 먼지·뛸 때 발밑 먼지 모두.
  - 플레이 확인: 돌창 복제본 scale 5.51→8.82(1.6배), 창끝이 바닥 2.0 아래, 자루가 위(축 Y 0.98), 먼지 색 적용, 손의 창 보임, 오류 없음. 화면으로 모양은 안 봄.
  - 게시할 패키지: Controllers(Vfx.LeapStrike).
- ✔ **도약 찌르기 추가 수정 (2026-11-24, 사용자)**: ① 먼지 더 하얗게 → `DUST_COLOR` (255,255,255) + `DUST_LIGHT_INFLUENCE 0.35`(0.9면 어두운 곳에서 회색) ② 시전 중 몸 앞에 떠 있던 창끝 빛(모임 알갱이·반짝임·불빛)을 새 holder `LeapSpearTip` 으로 옮겨 **든 창 TrailTip** 을 매 프레임 따라가게(든 창 없으면 예전 몸 앞). 빛 꼬리(Trail)는 몸 기준 `LeapTip` 그대로 ③ 적중 범위 1.3배: `Skills.leap_strike.radius 9 → 11.7` (서버 `leapHits`·착지 연출 크기 모두 이 값).
  - 플레이 확인: 빛과 창끝 거리 대부분 0.0~0.15(측정 타이밍 차로 한두 프레임 튐), 먼지 색 (1,1,1)·LI 0.35, 오류 없음. 넓어진 범위로 실제 적이 맞는지는 확인 안 함(서버가 같은 값 사용).
  - 게시할 패키지: Shared(Skills), Controllers(Vfx.LeapStrike).
- ✔ **창 휘두르기** `spear_sweep` (kind **"spin"** 새로 추가, 성유물 `relic_spear_sweep`, 2026-11-24). 결정(사용자): **제자리 한 바퀴 회전** / 반경 **20** / 맞으면 그 자리에서 **바깥으로 15 + 살짝 위로(높이 4)** 날아감 / 보스는 피해만, PvP 플레이어는 날아감 / 이펙트 = **Blender 프레임 시트** / 모션 = **새 모션 만들기**.
  - ✔ 1단계 판정: `Skills.spear_sweep` (cd 9, 피해 ×2.2, castDelay 0.2, spinTime 0.35, radius 20, flingDistance 15, flingHeight 4, flingTime 0.45, flinch 0.4, vfx "SpearSweep"), `PolearmRelics.relic_spear_sweep` (아이콘 임시 = Piercing Lunge). 서버 `spinHits`: 반경 20·높이 차 10 안, 가슴에서 보이는(벽 너머 아님) 대상을 **창이 그 각도를 지나는 시각**(castDelay + spinTime × 각도/360, 바라보는 방향에서 시작해 왼쪽=반시계)에 때림 → `spinFling`: 적(적 폴더·보스 아님)은 서버가 포물선으로 15(벽이면 벽 앞) 옮기고 바닥에 내려놓음 + 경직, 플레이어는 수평 forceMove + 위로 띄움, 보스·더미는 피해만. 분신(echo) 제외.
    - 플레이 확인: 주변 4마리(각도 38/260/295/345°) 모두 맞음, 각각 정확히 15 밀려나 최고 +3.7~4.0, 맞는 시각 차이가 각도 계산과 일치(0.217/0.265/0.312초). 오류 없음.
    - 사용자 데이터 변경: 돌창 **소켓 3칸째 해금**(테스트라 비용은 안 냄 — 원래 bloodstone 3·금화 8000), 소켓 3 = relic_spear_sweep.
  - ✔ 2단계 모션 — **사용자가 도중에 "기존 모션 재활용"으로 바꿈**: 새 `Vfx.SpearSweep` 이 다른 창 스킬처럼 든 무기 콤보 첫 타를 당긴 자세(HOLD_FRACTION 0.25)에서 멈췄다가 castDelay 에 남은 휘두르기를 spinTime 에 맞춰 빠르게 + **내 몸(HRP)을 왼쪽으로 한 바퀴** 돌림(AutoRotate 잠금, 끝나면 처음 방향으로 맞춤). 내 캐릭터만(다른 사람은 회전이 복제돼 보임), /fx(timeScale)면 안 함.
    - 플레이 확인: 시전 신호 +0.05 에 연출 도착, 0.27~0.61 동안 몸이 0→360°, 끝나고 0°, 오류 없음. 창끝은 몸보다 ~10° 뒤에서 바닥 높이(0~0.7)로 따라감(콤보 동작 자세 그대로).
    - 폐기(쓰지 않음): 전용 모션 `scripts/spear_sweep_anim.py` → 업로드 v1 112805095494076, v2 99353418131605 (그룹 소유, Skills 에서 뺌). 기록용으로 스크립트는 남김.
    - 참고: 이 세션 중 Studio 에 다른 작업(`skyfall` kind·`relic_god_spear` — 신의 창?)이 들어와 있음. 이 작업에서 만든 것 아님.
  - ✔ 3단계 이펙트 (결정: 원호 간판 + 바닥 바람 고리·흰 먼지 + 맞은 적 섬광·꼬리 + 창날 Trail / 원호는 허리 높이):
    - ① 회전 궤적 원호 = 새 Blender 시트 `scripts/vfx_sweep_arc.py`(발광만, 명령줄 Blender 17초): 바깥 띠(0.5~0.98)에 하얀 앞 날 + 결로 끊기는 초록 꼬리(~150°)가 반시계로 한 바퀴(앞 37칸 = 0.35초) → 사그라듦. **이미지 70714911497187** (Decal 71426770544323). 허리 높이(바닥 +2.5) 눕힌 판, 빛 테두리(시트 반지름 0.88)가 반경 20에 오게 크기 = radius×2/0.88, Brightness 3, LightInfluence 0.
      - ⚠ **눕힌 판(SurfaceGui Top)은 그림 오른쪽이 판 앞(-Z)** (90° 돌아감, 뒤집힘 없음) — 고정 칸을 위에서 찍어 확인. 그래서 판을 `lookAt(정면) * Angles(0, -90°, 0)` 로 돌림. (위아래 뒤집어 다시 구운 v2 130739621951445 는 잘못된 보정이라 폐기.) 도약 찌르기 시트는 둥글어서 상관없었음.
      - 미리보기: 시트는 색이 알파 없이 저장돼 그냥 보면 꽉 찬 부채꼴처럼 보임 → 어두운 바탕에 합성해서 판단 (`exports/vfx/preview_SweepArc.png`).
    - ② 바닥 바람 고리 = 도약 찌르기 Shock 시트 재사용(크기 radius×1.6, castDelay+0.05부터 0.6초), 흰 먼지 = 도약 찌르기 Dust 시트 파티클 10개(흰색, LightInfluence 0.35).
    - ③ 서버 `spinHits` 가 맞을 때마다 phase **"hit"**(target, flingTime) 를 보냄 → 초록 섬광·불티·타격음 + 날아가는 동안 대상 몸에 흰·초록 Trail.
    - ④ 든 창 TrailBase→TrailTip 에 흰→초록 Trail (castDelay ~ 회전 끝).
    - 소리: 당기기 쇠 긁는 소리, 회전 Doppler Whoosh(×1.35), 맞음 타격음.
    - 플레이 확인: SweepArc·SweepShock·SweepDust·창 Trail·맞음 연출 모두 생성, 3마리 맞음 이벤트, 오류 없음. 실제 손맛·밝기는 사용자 확인 필요.
    - **원호가 몸을 따라감** (사용자: "이펙트가 제자리에서 나옴" → 결정: 원호만 따라가기, 바람 고리·먼지는 제자리): 시전자 HRP 위치를 매 프레임 따라감(방향은 시전 때 정면 고정, 높이 = root 기준 허리). 서버 판정도 맞는 순간 내 자리 기준이라 일치. 테스트: 회전 중 옆으로 12 옮겨도 원호-몸 거리 0.3 이하.
      - 사용자 확인: **따라가기 괜찮음** (2026-11-24). (대안이었던 '더 빠르게 + 회전 중 제자리'는 안 함)
  - ✔ **AI티 고침 v3 (2026-11-24, 사용자: "다 고쳐줘" + 참고 이미지 = 언리얼 회전 베기, 불꽃색 → 흰+초록으로)**. 지적했던 7가지:
    1. **몸 회전**: 일정 속도 턴테이블 → 움찔(오른쪽 22° 감기) → **ease-out**(처음 빠르고 끝에 느림) 한 바퀴 → 20° 더 넘어갔다 되돌아옴. 서버 `spinHits` 맞는 시각도 같은 식: `castDelay + spinTime × (1 − sqrt(1 − 각도/2π))`. 발이 같이 도는 건 HRP 회전 방식이라 그대로.
    2. **원호 시트 v3** `scripts/vfx_sweep_arc.py` → **이미지 79647901942562** (Decal 85299104343894): 앞머리 굵고 하얀 심 → 꼬리로 가늘어지며 원을 따라 늘어난 붓질 결(길이·굵기 제각각) → 큰 덩어리 노이즈로 갈라져(침식) 사라짐, 바깥 옅은 테(타 들어간 가장자리)·안쪽 바람 테 겹. 회전도 ease-out. (v2 의 같은 간격 동심 줄무늬 = 레코드판 → 폐기)
    3. **날려보냄** `spinFling`: 거리 ×0.85~1.15, 높이 ×0.75~1.3, 시간 ×0.9~1.12 제각각 + 날아가며 뒤로 35~70° 기울었다 착지 전 서고 ±70° 돌며, 착지 뒤 한 번 튐(0.2초, 높이 0.9, 1.6 더 미끄러짐, 벽이면 안 미끄러짐). 테스트: 16.2/16.3/13.5/7.1(벽), 높이 4.1~4.7, 기울기 40~75°, 모두 다시 서 있음.
    4. **원호 2겹**: 본체(허리) + 0.7 위·1.05배·0.035초 늦게·옅은(투명 0.45, 밝기 1.4) 겹 → 판 한 장 스티커 느낌 덜기. 원호 앞머리(서버와 같은 ease-out 각도, 반경 ×0.97) 자리에서 초록 불티가 튀어 오름(초당 140).
    5. **바닥**: 도약 찌르기 충격파 재사용 → 새 **바닥 물결 시트** `scripts/vfx_sweep_ground.py` → **이미지 124073006315493** (Decal 74240308583751): 고리 3개가 시차를 두고 번짐(끊김은 낮은 주파수 노이즈로 긴 호 몇 개 — 첫 렌더는 고른 점선이라 AI티라 고침) + 안쪽 연무. 먼지는 가운데서 퍼지던 것 → 둘레 7곳에서 **회전 방향(접선)으로 쓸려 나감**.
    6. **맞음**: 범용 십자 섬광 → 창이 지나간 방향(접선)으로 긴 빛 자국(네온 막대 2겹이 0.06초에 늘어났다 가늘어지며 사라짐, ±18° 기울기) + 날아가는 쪽으로 튀는 불티 + 짧은 초록 빛.
    7. **소리**: 회전 = 낮은 바람(0.9) + 공기 가르는 쉭(1.3) + 쇠 울림(1.7) 3겹, 맞음 = 타격음 + 묵직한 충격(Rock Impact 1.45).
    - 확인: 편집 모드에서 회전 중간 칸(22)을 고정해 비스듬히 위에서 캡처 → 하얀 앞머리·결·초록 꼬리·바닥 고리 확인(확인용, 보고용 아님). 플레이: 몸 회전 −20° → 35° → 219° → 324° → 359° → +19° → 0°, 원호 2겹·불티·바닥·먼지·빛 자국 모두 생성, 오류 없음.
    - 남은 한계: 시트 칸이 128px 라 반경 20 크기로 늘리면 조금 흐림(1024 한 장 제한). 더 선명하게 하려면 → 1장짜리 큰 초승달 이미지를 ImageLabel.Rotation 으로 돌리는 방식(칸 수 대신 해상도).
    - Studio 가 도중에 다시 열림(새 studio_id) — 넣은 코드는 모두 남아 있었음.
  - ✔ **입체감 + 즉시 피해 + 1.5배 빠르게 (2026-11-24, 사용자)**:
    - "바닥에만 깔려 옆에서 보면 입체감 없음, 몸 주변에도 / 뚝뚝 끊기면 안 됨" → **몸을 감는 바람 띠 3줄** (반경 4.6/6.4/5.3, 높이 1.4/2.8/4.3, 폭 1.3/2.0/1.0, 조금씩 기울어짐, 0/0.02/0.04초 늦게 따라옴). 띠마다 **휘어진(베지어) Beam 6개**, 앞머리 = 몸·원호와 같은 ease-out 각도, 꼬리 210° (뒤로 갈수록 옅고 가늘고 초록), 매 프레임 위치 갱신(플립북 아님), 0.06초에 나타나고 회전 끝나면 0.35초 동안 위로 떠오르며 퍼져 사라짐. 결 텍스처 = 새 `scripts/vfx_sweep_wind.py` → **이미지 117960767975250** (Decal 121045523827133, 1024x256, 가로로 이음매 없음 → Stretch 로 마디 경계가 이어짐).
      - 1차(짧은 직선 마디 24개 × Wrap)는 마디마다 결이 다시 시작해 **타일처럼** 보여서 폐기 → 휘어진 6개 + Stretch. 앞머리 끝이 판자처럼 잘려 보여 첫 15% 옅게.
      - Beam 방향 규칙(Studio 확인): FaceCamera 끈 빔의 **폭 = 붙임점 Y축**, **곡선 제어점 = 붙임점 X축 방향**(CurveSize0·1 둘 다 + 로 원을 따라감, 길이 = 반지름 × 4/3 × tan(각/4)).
    - 먼지: 크고 누런 구름 같다 → 크기 0.9~3.8, 투명 0.55~, 한 곳 1개, LightInfluence 0.2·LightEmission 0.15.
    - "시전하면 즉시 주변에 데미지" → 서버 `spinHits` 가 각도별 시각 대신 **시전 순간 반경 안 모두** (테스트: 신호 3ms 뒤 3마리 동시). castDelay **0.2 → 0.08**.
    - "창 1.5배 빠르게" → spinTime **0.35 → 0.233**. 원호 시트 재생 시간 = spinTime ÷ (37/64) (= 0.4초), 띠·불티·몸 회전도 spinTime 따라감.
  - ✔ **몸 주변 = 퍼지는 고리로 교체 (2026-11-24, 사용자: "바닥 물결처럼 몸 주변에서 뻗어 나가는 그림을 생각했는데 몸과 같이 돌게 만들었음 → 바닥 느낌을 활용")**: 도는 띠(windRibbons) 삭제 → `windRings`: **몸 높이에 세운 바람 고리 3개**(바닥 위 1.3 / 2.7 / 4.1, 시차 0 / 0.05 / 0.1초)가 회전 시작과 함께 몸에서 바깥으로 번짐(반지름 1.6→11 / 1.8→13 / 1.5→9.5, ease-out ^2.4, 0.48~0.55초), 퍼지며 0.9 떠오르고 반시계로 0.6rad 살짝 돎, 폭 45% 까지 얇아짐, 세기 1−k². 고리 = 휘어진 Beam 8개(45°), 마디 경계 점마다 무작위 진하기 + 1~2곳 거의 끊김(바닥 물결의 불규칙한 끊김처럼), 조금씩 기울어짐, 결 = 바람 텍스처 Stretch(TextureSpeed 0.6), 밝기 2.6.
    - 확인: 편집 모드에서 실제 모듈을 0.05배속으로 재생해 옆에서 캡처 → 몸 높이 고리가 바닥 물결과 같이 바깥으로 번짐(1차는 퍼진 뒤 너무 옅어 세기·폭 조정). 플레이: Beam 24개, 최대 반지름 13, 오류 없음.
  - ✔ **원뿔 띠 + 창날 꼬리 시작 + 피해 버그 (2026-11-24, 사용자)**:
    - "띠는 위에서 보면 선" → 대안 비교(카메라를 보는 빔은 눈높이에서 납작한 타원·마디 꺾임·결 미끄러짐·네온 관 느낌) 후 사용자 선택 **원뿔 띠**: 띠 폭 방향을 위에서 바깥으로 눕힘(아래 고리 55° / 가운데 42° / 위 30°, 퍼질수록 +12°). 고리마다 둘레 4곳에서 옅은 바람 연무 파티클(smoke_main, 초당 30, 퍼지는 앞 60%)이 바깥으로 → 띠가 얇아 보이는 각도를 메움. 위·옆 캡처로 둘 다 면이 보이는 것 확인.
    - "창 휘두르는 이펙트 시작이 끊겨 보임" → 창날 Trail 을 회전 0.04초 전에 켜고 0.09초 동안 투명→진하게(그전: 회전 순간 켜서 첫 조각이 진한 채 툭 나타남). 화면으로는 확인 안 함.
    - **발밑도 따라가게 (사용자: "발에 있는 것도 나를 따라가게")**: 바닥 물결 시트 판이 재생되는 동안 매 프레임 몸 발밑으로, 흰 먼지는 터지는 순간 발밑에서 (그전: 시전 자리에 남음). 이제 원호·몸 고리·바닥 물결이 모두 몸을 따라감. 테스트: 회전 중 12 옮겨도 바닥 물결 중심-몸 1.1~1.6(테스트 중 프레임 낮아 한 프레임 늦음), 오류 없음.
    - **점프 중 시전 시 이펙트 안 보임 버그 (사용자: "점프하고 내려오면서 쓰면 안 들어감" → 확인해 보니 피해는 들어가고 이펙트만 안 보임)**: 몸을 따라가게 하면서 높이를 '시전 순간 (바닥 − 몸) 차이'로 고정해 더했더니, 공중에서 쓰고 착지하면 원호·몸 고리·바닥 물결이 그만큼 바닥 밑으로 들어감 → 매 프레임 몸 바로 아래 바닥을 레이(80, 캐릭터·적·연출 제외)로 재서 그 높이 기준으로. 테스트: 7.1 위에서 시전 → 떨어지는 동안·착지 뒤 모두 원호 바닥+2.5, 바닥 물결 +0.06, 고리 바닥에서 시작. (서버 판정은 공중에서도 정상이었음 — 디버그 출력으로 확인 후 지움)
    - **"데미지도 안 들어가" 버그**: `spinHits` 벽 검사가 terrainParams(적 폴더·플레이어만 뺌)로 가슴→대상 레이를 쏴서, **적 폴더 밖 훈련용 더미(Lobby.TrainingDummies)는 자기 몸을 벽으로 봐서 안 맞았음** → 대상 모델을 빼고 Humanoid 모델은 벽이 아닌 것으로 건너뜀(최대 4번). 플레이 확인: 더미 8.9 거리에서 phase hit + 피해 숫자 26.4.
  - 게시할 패키지: Shared(Skills·PolearmRelics), Services(Skill), Controllers(Vfx.SpearSweep 새 모듈).
- **진행 중: 신의 창** `god_spear` (kind **"skyfall"** 새로 추가, 성유물 `relic_god_spear`, 2026-11-24). 결정(사용자): 떨어질 자리 = **카메라 조준 지점**(최대 40, 보정 6°) / **반경 18, 예고 0.9초** / 맞은 효과 = **속박 2초**(보스·강철 의지는 피해만) / 창 모습 = **Blender 로 새 빛의 창**(흰+초록).
  - 판정 수치: cd 14, 피해 ×3.5, castDelay 0.3(창을 하늘로 치켜듦, 이때 예고 원) + warnTime 0.9 → 꽂힘. 벽 너머 안 맞음, 높이 차 radius×0.6. 지붕은 무시(하늘에서 떨어짐). 맞은 대상 목록은 phase "pin" 연출(targets = { model, pinned }).
  - **속박 상태 새로 추가**: `StatusEffects.rooted` (kind "root", 아이콘 임시 = Slow) → `Services.StatusEffect.publish` 가 MoveSpeedMult 0 + 모델 속성 **Rooted**. 막는 곳: MovementController 대시·점프, SkillController(클라)·Skill(서버 `ROOT_BLOCKED`) 의 lunge·charge·leap. 공격·다른 스킬은 됨. 적은 MoveSpeedMult 0 으로 못 걸음.
  - ✔ 1단계 판정 Studio 적용(마을 place): Shared(Skills·PolearmRelics·StatusEffects), Services(StatusEffect·**Skill** — `skyfallPlan`·`skyfallHits`·`ROOT_BLOCKED`, 원본 기록 `scripts/patches/god_spear_skill_service.lua`), Controllers(MovementController·SkillController). 수정 표시(Source 다시 쓰기) 함 — 패키지 버전 Shared v129 · Services v76 · Controllers v107 기준.
  - 플레이 확인 (2026-11-24): 돌창 소켓 3 을 **메모리에서만** 잠깐 relic_god_spear 로 바꿔 시전(끝나고 relic_spear_sweep 로 되돌림, 사용자 인벤토리에 god_spear 성유물은 없음). 훈련용 적 4마리에 조준 → 보정으로 적 발밑, **+1.28초 phase "pin" targets=4**, 4마리 모두 피해(42) + Rooted **2.02초**, 오류 없음. 새로 만든 ashen_husk: MoveSpeedMult 0 → WalkSpeed 20→0, 1.5초 이동 0.1 → 풀린 뒤 다시 걸음. 내 캐릭터에 rooted: WalkSpeed 0·점프 꺼짐 → 2초 뒤 13·점프 켜짐.
    - ⚠ 테스트 팁: 오래 있던 훈련용 적(bloated_husk)은 AI가 멈춰 있어 MoveSpeedMult 에 반응 안 함(속박과 무관) → 이동 확인은 새로 만든 적으로. 서버 Script 에 넣는 코드 문자열에 `]]` 가 있으면(`t[a[b]]`) 잘림 → `[==[ ]==]` 사용.
    - 확인 안 함: 대시·이동 스킬이 속박 중 막히는지 실제 키 입력, PvP, 보스(피해만), 벽 너머 제외.
  - ✔ **빛의 창 메시** (2026-11-24, 단계마다 사용자 확인): 결정 = 순수한 빛 결정 / 길고 가느다란 잎사귀형 날 / 길이 40 / 장식 없이(밋밋하면 나중에 추가) / v1 가늘어서 굵게 → v2 날이 통통해서 날 폭 3.2 / 목 = 6각 쌍뿔 결정 마디(지름 2.5) / 디테일 = 날 결정 면 나눔(띠 9개, 단면 꺾임 번갈아 → 삼각 결정면) + 양날 빛 테두리 띠 / 재질 = 날·자루 Glass + 심·테두리 Neon.
    - `scripts/vfx_god_spear.py` (Blender MCP 로 exec, `export()` → `exports/vfx/GodSpear.fbx`), 부품 6(Blade 214면·Edge·Core·Collar·Shaft·Butt), 삼각형 750. 미리보기 `exports/_preview/godspear_*.png`(이 PC만).
    - Open Cloud 그룹 업로드 Model **128999563181818** → **`ReplicatedStorage.Assets.Vfx.GodSpear`** (피벗 = 창끝, +Y = 꼬리, Anchored·충돌/쿼리/터치/그림자 끔). Glass (205,255,220) 투명 0.3, Core Neon (120,255,150), Edge Neon (225,255,232). ID → `exports/texture_ids.json` `VFX.GodSpear`.
    - ⚠ FBX 로 넣은 MeshPart 는 **PivotOffset 에 회전(−90° X)** 이 들어 있음 → 모델에 PrimaryPart 를 두고 PivotTo 하면 창이 눕혀짐. PivotOffset 을 비우고 PrimaryPart 없이 WorldPivot 으로.
    - 확인용 사본 `Workspace.GodSpear_Preview`(로비 도착 데크 앞, 8° 기울임) — 사용자 확인 뒤 지울 것. Assets 패키지에 들어갔는지(Assets 가 패키지면 게시 필요) 확인 필요.
  - ✔ **연출 `Vfx.GodSpear`** (2026-11-24, 원본 `scripts/packages/Controllers/Vfx_GodSpear.lua`). 결정(사용자): 예고 = 바닥 빛의 원 + 하늘 빛 기둥 + 하늘 높이 창이 나타남 / 꽂힘 = 크고 화려하게(도약 찌르기 시트 재사용) / 창은 속박 끝날 때까지 박혀 있다 빛 조각으로 / 속박 = 발밑 빛의 사슬.
    - 순서: 0 → 마법진 3겹(반경 18, 돎) + 바깥 1.7배에서 조여드는 고리(꽂히는 순간 반경에 맞음) + 높이 160에서 내려오며 굵어지는 빛 기둥(Beam PillarCore) / castDelay 0.3 → 높이 70에 창이 빛 알갱이에서 맞춰지며 나타나 살짝 떠 있음 / 1.06 → 0.14초 동안 가속 낙하 / 1.2 꽂힘: 창끝 5 박힘(4° 기울기), 섬광·충격파 시트 2겹·퍼지는 빛 고리·균열(선+빛)·흰 먼지 18+4·초록 불뛰·돌 16·돌판 고리(×2 크기)·소리(충격·타격·하강 바람), 내 캐릭터가 70 안이면 화면 흔들림(가까울수록 세게) / 박힌 채 2초 빛남 → 아래부터 투명해지며 알갱이 120 + 결정 조각 14.
    - phase "pin": 대상마다 창 아래(바닥+2) → 발밑까지 Neon 사슬 고리(1.1 간격, 90° 교차, 살짝 처짐, 0.12초에 뻗음) + 감싸는 Beam + 발밑 HaloRing(돎), root 초 뒤 알갱이로 부서짐. 보스(pinned false)는 반짝임만.
    - ⚠ **HolyCircle·HaloRing·PillarCore·HolyFlare 텍스처는 금색** → ImageColor3 를 WHITE/연초록으로 두면 금빛·노란빛. **GREEN(70,255,110)** 으로 물들일 것. 초록 PointLight 가 세면 흰 먼지가 초록으로 물듦 → 먼지 LightInfluence 0.1, 섬광 불빛 3·0.35초, 창 불빛 2.
    - 플레이 확인: 실제 시전(ashen_husk 3, 돌창 소켓 3 메모리에서만 바꿨다 되돌림) → +1.27초 phase "pin" targets=3, 사슬·고리 생성, 오류 없음. 느린 재생(timeScale 0.05~0.12) 확인용 캡처로 기둥·낙하·충격·사슬 확인. **실제 속도 손맛·소리 크기는 사용자 확인 필요**. 로비처럼 천장이 70보다 낮은 실내에서는 하늘의 창이 천장에 가려짐(공장 실내 확인 필요).
    - 시전 모션은 아직 없음(창을 치켜드는 자세 등) — 필요하면 다음에.
  - ✔ **연기 고리** (2026-11-24, 사용자: 뭉게 덩이 먼지가 "방귀 같다" + 참고 그림 = 바닥에 낮게 깔려 바깥으로 퍼지는 연기 고리): `scripts/vfx_smoke_ring.py` (Blender 볼륨 2장 — SmokeRing 위에서 본 고리(덩이가 고리를 따라 뭉게뭉게, 사용자 v5 확인) / SmokeWisp 옆에서 본 낮은 가닥) → `VfxKit.smokeRing(ctx, ground, radius, opts)` 새 공용 함수(원본 기록 `scripts/packages/Controllers/VfxKit_smokeRing.lua`). **도약 찌르기도 착지·도약 먼지를 이것으로 교체**(사용자 결정). ID → texture_ids.json `VFX.SmokeRing`.
    - 렌더 팁: 명령줄 Blender 는 `-S <장면>` 을 줘야 그 장면 애니메이션이 돎(안 주면 활성 장면이 아닌 장면은 정지 화면). 해상도는 `--python-expr` 로 128 로 맞춘 뒤 `-a`. `vfx_sheet_kit.vfx_scene` 은 창 없는 명령줄에서도 되게 고침. 미리보기 `scripts/vfx_preview_frames.py`.
  - ✔ **v2 다시 만듦** (2026-11-24, 사용자: "밋밋, 몰아치듯 빠르게, 3번에 나눠서, 단색이 아닌 오로라치는 영롱하고 깔끔한 창" + 참고 그림 2장 — 번개 내리꽂힘·빛 균열 / 빛나는 결정 검). 결정(사용자): **3연타 낙뢰**(0.15/0.35/0.55초) / **작은 창 2(길이 26, 조준점 둘레 6, 반경 9, ×1.0) → 가운데 큰 창(40, 반경 18, ×1.8 + 속박)** / 예고 = 꽂힐 자리 순간 번쩍(큰 마법진·하늘 기둥 뺌) / 창 모양 유지, 재질·빛만 / 오로라 색 = 흰·초록 + 청록·엷은 보라 / 표현 = 날 속 흐르는 빛 + 감는 오로라 커튼 + 번개 빛 줄기 + 바닥 빛 균열.
    - `Skills.god_spear`: damage 1, castDelay 0.15, `strikes` 3개(time·radius·damage·offset·size·root). 서버 `skyfallPlan` 이 strikes 자리(작은 창은 가운데 둘레 무작위 방향 130° 차이, 벽 너머면 가운데) → payload.strikes, `skyfallHits` 가 창마다 그 시각·자리에서 판정, root 인 창만 속박 + phase "pin". 높이 차 제한 `max(radius×0.6, 8)`.
    - 오로라 그림 `scripts/vfx_aurora.py` (명령줄, 셰이더 평면 렌더): AuroraCurtain 1024x256 / AuroraFlow 1024x128, 가로 이음매 없음 → texture_ids.json `VFX.GodSpearAurora`.
    - 연출 `Vfx.GodSpear` v2 (원본 `scripts/packages/Controllers/Vfx_GodSpear.lua`, v1 은 git 기록): 창마다 꽂힐 자리 빛 고리 번쩍 → 0.12초 가속 낙하 + 하늘(140)에서 창 꼬리까지 번개 빛 줄기(Neon 막대 꺾은선 + 가지 2, 0.05초마다 다시 그림, 꽂힌 뒤 0.22초) → 섬광·충격파 시트·빛 균열(청록)·연기 고리·불뛰·돌(큰 창은 돌판·센 흔들림). 창 = 더 맑은 유리(투명 0.45) + 날·자루 속 AuroraFlow Beam(흐름) + AuroraCurtain 나선 띠 2줄기(점 5개 Beam 4개, 회전) + 창끝 빛·반짝임 + 청록 불빛·오로라 알갱이. 작은 창은 마지막 창 0.7초 뒤, 큰 창은 속박 끝에 빛 알갱이로 흩어짐. 속박 사슬도 청록·Flow 빛.
    - ⚠ 오로라 커튼 Beam 은 **FaceCamera = false** (true 면 카메라 쪽으로 펴져 톱니 조각처럼 보였음). 점의 X축 = 나선 접선(CurveSize 0.36 × 현).
    - 플레이 확인: 실제 시전(훈련용 적 4, 소켓 3 메모리에서만 바꿨다 되돌림) → strikes 3개(작은 창 가운데서 6), +0.60초 큰 창이 4마리 피해 + 속박 + pin, 창 3개 차례로 생김. 느린 재생 캡처로 낙하·번개·커튼 모양 확인(확인용). **실제 속도 느낌은 사용자 확인 필요**. 사용자 소켓 4 에 relic_god_spear 가 이미 끼워져 있음(V 키).
  - ✔ **사용자 피드백 1 (2026-11-24)**: "번개 퀄리티가 떨어지고 너무 가늘다" / "연기가 바닥에서 뚝 끊겨 어색"
    - 번개: `scripts/vfx_lightning.py` — 주 줄기(가운데 밀어내기 7단계, 비율로 줄여 화면 안에 — 잘라내면 평평한 구간이 생겼음) + 잔가지 4~6을 흰 심·연초록 커브로 렌더 → numpy FFT 흐림 3겹(청록 좁게·초록청록·엷은 보라 넓게)으로 빛무리, 밝기를 알파로. 4장 1024x256 → `VFX.GodSpearLightning`. 연출은 하늘→창 꼬리 Beam 두 겹(FaceCamera, Stretch, 큰 창 폭 8·작은 창 5), 0.05초마다 그림 교체·밝기 깜빡임. (Neon 막대 번개는 뺌)
    - 연기 가닥 아래를 부드럽게: `vfx_smoke_ring.py` 바닥 마스크 -1..-0.82 → -1..-0.4 로 다시 렌더 → Wisp v2 89179403504248, 파티클 중심 높이 0.42 → 0.36.
  - ✔ **AI티 줄이기 (2026-11-24, 사용자 요청으로 찾은 목록 중 1~4·9번)**:
    - ① 효과 쌓기: 작은 창은 섬광 작게·충격파 작게·불뛰 12·돌 4·연기 가닥 7, **균열은 큰 창에만**. 큰 창은 요소마다 시간차(균열 +0.03, 돌 +0.02, 돌판 +0.04, 연기 +0.06).
    - ② 반짝이: 창끝 반짝이 분수 뺌, 박힌 뒤 알갱이 큰 창 10·작은 창 0, 흩어질 때 110/50 → 45/18.
    - ③ 규칙성: 서버 작은 창 각도 130±25°, 거리 ×0.8~1.25, 시각 ±0.03초. 연출 낙하 시간 ±15%, 높이 ±15%, 기울기 5°±60%. 연기 고리 가닥 개수 ±2, 각도·크기(0.7~1.3)·출발 거리·나오는 시각(0~0.08초) 무작위.
    - ⑨ 소리: 매번 높낮이 ±6~10% (`vary`).
    - 플레이 확인: 바닥 위 훈련용 적 6마리 → 작은 창 0.18·0.32초(가운데서 6.6·7.3), 큰 창 0.55초 → 6마리 모두 맞고 속박 + pin, 오류 없음. 새 이미지는 올린 직후 "content representation is being generated" 로 아직 안 불러와짐 → 잠시 뒤·Studio 다시 열면 보임.
    - 남은 목록(사용자 확인 후): ⑤ 오로라 커튼이 기계적인 나선 ⑥ 창 모양이 너무 반듯함 ⑦ 금색 마법진 텍스처를 물들인 예고 고리 ⑧ 속박 사슬이 너무 반듯함.
  - ✔ **사용자 피드백 2 + AI티 ⑤~⑧ (2026-11-24)**: "뭉게 연기는 빼고, 번개는 그냥 바람 같고 뚝 끊기는 것도 부자연스러움, 나머지 AI 수정도"
    - 연기: 신의 창에서 `Kit.smokeRing` 호출 뺌 (도약 찌르기는 그대로 씀).
    - 번개: 그림 한 장을 140 길이로 늘려 줄기처럼 보였음 → `bolt()` 를 꺾인 길 5마디(각 ~30, 마디마다 번개 그림 무작위, 0.05초마다 길·그림 교체)로. 아래 끝 = 떨어지는 동안 창끝, 꽂힌 뒤 땅(창이 번개를 타고 내려옴). 위 마디는 하늘 쪽이 투명, 0.04초에 나타나고 끝에 `BOLT_FADE` 0.18초 동안 옅어지며 가늘어짐. 폭 큰 창 6·작은 창 4.
    - ⑤ 오로라 커튼: 줄기마다 감는 수(0.95~1.35)·도는 속도(×0.6~1.4, 가끔 반대)·폭·밝기·흐름 속도 다르게, 반지름 ±18% 출렁임, 위로 갈수록 가늘고(-45%) 옅어짐.
    - ⑥ 창 메시 v2: `vfx_god_spear.py` 에 시드 고정 무작위 — 결정 띠 위치 ±0.025, 꺾임 위치·높이 띠마다 무작위(번갈아 반복 대신), 좌우 날 폭 ±4% + 이 빠짐 2곳, 능선 살짝 옆으로, 자루 11단·꼭짓점 ±6%·비틀림, 마디 꼭짓점 ±8%. 삼각형 814. 업로드 Model **108868223933171** → `Assets.Vfx.GodSpear` 교체(이름·피벗 같음). 미리보기 `exports/_preview/godspear_v4_*.png`.
    - ⑦ 금색 마법진 텍스처 예고 고리·속박 발밑 고리 → `groundArcs()` 땅을 긁는 번개(바닥에 눕힌 번개 Beam, 0.06초마다 각도·그림 바꿈, 가끔 한 줄씩 꺼짐). 예고 = 큰 창 6줄·작은 창 4줄, 발밑 = 4줄 작게(속박 시간 동안).
    - ⑧ 속박 사슬: 고리마다 크기 0.85~1.15·색(연초록~청록)·투명도·비틀림 ±0.25 rad, 꽂힌 순간 팽팽 → 0.4초에 걸쳐 늘어지며 살짝 출렁임.
    - 플레이 확인: 소켓 4 실제 시전 → 4마리 피해 46·속박·pin, 번개 마디 5개씩 켜졌다 꺼짐, 발밑 번개 4. 오류 없음. ⚠ 적을 만든 직후(2~3초 안) 시전하면 피해가 안 들어감(스폰 직후 보호로 보임) — 테스트는 조금 기다렸다가.
  - ✔ **사용자 피드백 3 (2026-11-24)**: "작은 창도 큰 창과 같은 범위, 셋 다 같은 곳" / 번개 마디 이음매가 끊겨 보임 → "투명 메쉬 이미지로"
    - `Skills.god_spear.strikes`: 작은 창도 radius 18·offset 0 (세 창 모두 조준한 같은 자리, 반경 18. 큰 창만 속박). 연출에서 작은 창은 같은 자리에 15°±25% 기울어 꽂힘(큰 창과 겹치지 않게), 작은 창의 바닥 효과는 반경 ×0.6.
    - 번개 v2: `vfx_lightning.py` 1024x128 (8:1), 잔 꺾임 더(DECAY 0.82, 6단계), 심 가늘게 → 띠 **한 장**(마디 없음)에 씌움. **길이 고정**(큰 창 140·폭 16 / 작은 창 96·11 = 그림 비율) — 아래 끝(창끝→땅)에서 위로, 하늘 쪽 끝 30% 투명. 두 겹 0.05초마다 그림 교체. ID → `VFX.GodSpearLightning`.
    - 플레이 확인: 바닥에 고정한 훈련용 적 4(가운데·8·10·12 거리) → 0.25/0.40/0.61초 세 번 모두 4마리 피해 + 속박. 오류 없음.
    - ⚠ 테스트 함정: 풀어 둔 훈련용 적이 내 캐릭터 위·옆으로 몰려오면 조준이 위로 꺾여(±55°) 엉뚱한 곳에 꽂힘 → 적을 Anchored 로 바닥에 고정하고 바닥 점을 조준할 것.
  - ✔ **박힐 때 연출 추가 (2026-11-24, 사용자 참고 그림: 번개가 꽂힌 자리 꽃잎 날개·옆 번개·빛 돔)**. 결정(사용자): 꽃잎 날개(어두운 색 말고 **밝은 빛**, v1 둥근 꽃잎 → "더 길고 날카롭게") / 옆으로 튀는 번개 날 / 바닥 빛 돔 / 타격감(떨림·줌·번쩍) / **돌은 범위 전체로 넓게 + 바깥에서 솟구치는 돌 하나 더**.
    - 메시 `scripts/vfx_god_spear_impact.py` → Model **115679458568936** → `Assets.Vfx.GodSpearImpact` (Petal 길이 8.5 칼날형·Ring 토러스·Dome 반구·Shard1~4 뾰족 돌, Neon, 피벗 = 뿌리). ⚠ 이 FBX 는 Blender (x, y, z) → Roblox 로컬 (−x, z, y) 로 들어옴 → 꽃잎은 로컬 **+Z** 쪽으로 휨. ⚠ MeshPart 는 Size 를 바꿔도 PivotOffset 이 그대로 → `scalePart()` 로 같이 늘림.
    - 옆 번개 날 그림: `vfx_lightning.py` `blade()` (ONLY_BLADES=True), 512x256, 구간 길이·꺾임 높이 무작위 + 끝 갈고리 (v1 은 같은 간격 "W" 라 규칙적). ID → `VFX.GodSpearImpact.Blades`.
    - 연출 `Vfx.GodSpear`: `impactBloom()` — 빛 돔(0.08초 부풀어 0.35초에 커지며 사라짐, 연초록→청록) + 엷은 보라 고리(퍼짐) + 꽃잎 날개 큰 창 12·작은 창 7(뿌리 둘레, 0.12초에 솟으며 5~13° → 28~44° 바깥으로 펼쳐지고 사라짐) + 옆 번개 날 큰 창 6·작은 창 3(0.07초에 뻗고 0.25초에 사라짐). `rocks()` = 판정 반경 원판 전체에 큰 창 22·작은 창 8, 먼 돌일수록 0.08초까지 늦게. `outerShards()` = 큰 창에만 테두리(반경 ×0.82~1)에서 뾰족 돌 9개가 바깥으로 기울어 솟았다(0.09초) 버티고 가라앉음 + 작은 돌·불뛰. `hitFeel()` = 70 안이면 줌(FOV −7/−3) + ColorCorrection 짧은 밝아짐. 창은 박히는 순간 0.18초 부르르 떨림.
    - 확인: 플레이 느린 재생 캡처(확인용)로 돔·고리·꽃잎·옆 번개·돌판·번개가 같이 나옴, 스크립트 오류 없음. 새 그림은 올린 직후라 "being generated" — 잠시 뒤 보임. **실제 속도 느낌은 사용자 확인 필요**.
  - 다음: 사용자 피드백 → 시전 모션(선택)(예고 원·하늘에서 내리꽂힘·충격·속박 사슬/빛 조각, phase "pin" 의 targets 에 붙임) → 시전 모션. 지금은 연출 모듈이 없어 눈에 보이는 게 없음.
  - 게시할 패키지(지금까지): Shared(Skills·PolearmRelics·StatusEffects), Services(StatusEffect·Skill), Controllers(MovementController·SkillController·VfxKit·Vfx.LeapStrike·**Vfx.GodSpear 새 모듈**), **Assets(Vfx.GodSpear·Vfx.GodSpearImpact 메시, 패키지 v15)**.
- ✔ **훈련용 더미 움직이게 (2026-11-24, 사용자: "고정시켜 놓지 말고 기절도 당하고 갈고리에도 끌리게")** — 마을 place `Workspace.Lobby.TrainingDummies.TrainingDummy` (패키지 아님 → **place 저장 필요**):
  - 부품 고정(Anchored) 전부 해제, 모델 속성 **`TrainingDummy = true`**. `DummyRegen` 스크립트에 추가: 서버가 물리 담당(SetNetworkOwner(nil)), 원래 자리에서 벗어난 채 4초 동안 맞지도 움직이지도 기절하지도 않으면 0.6초에 걸쳐 원래 자리·방향으로 돌아감. (피해 기록·2초 뒤 회복·죽으면 3초 뒤 다시 생김은 그대로)
  - `Services.Skill`: 갈고리 끌기(`hookPull`)·창 휘두르기 날림(`spinFling`)이 적 폴더 안 적뿐 아니라 `TrainingDummy` 속성 모델도 옮김. 기절은 원래 StatusEffect 가 아무 Humanoid 에나 걸어서 그대로.
  - 플레이 확인: 갈고리 18 → 4.5 끌려옴 + Stunned·기절 아이콘(1.5초), 창 휘두르기 17.4 날아감, 약 6.8초 뒤 원래 자리 0.0·똑바로 섬, 오류 없음.
  - ⚠ Studio MCP: `multi_edit` 의 `replace_all` 편집이 "적용됨"이라고 나왔는데 Source 에 안 들어간 일이 있었음 → 같은 줄이 여러 개면 앞뒤 문맥을 넣어 따로 편집하고, 편집 뒤 Source 에서 바뀐 것을 확인할 것.
  - 게시할 패키지: Services(Skill). + **마을 place 저장**(더미).
- ✔ **관통 돌격(창 대시) 색 → 흰+초록 (2026-11-24, 사용자: "창 대시 스킬 초록색으로")** — `Controllers.SkillController.Vfx.PiercingLunge`(piercing_lunge 만 씀): 금빛(255,220,170)·주황 불꽃 → 도약 찌르기·창 휘두르기와 같은 GREEN(70,255,110)/GREEN_SOFT(170,255,185)/GREEN_DEEP(20,150,55). 잔상·멈춤 원판·빛(LIGHT, STREAK_COLOR = GREEN_SOFT), 모임 반짝이 흰→초록, 꼬리 Trail 흰→초록, 관통 섬광 HolyFlare 연두→초록, 관통 불꽃 연두→짙은 초록, 바닥 충격 고리·창끝 반짝 연두. 플레이: 잔상·원판·빛·이미지·꼬리 모두 초록 계열, 오류 없음. 게시: Controllers(Vfx.PiercingLunge).
- ✔ **창 스킬·성유물 아이콘 + 관통 돌격 사거리 (2026-11-24, 사용자)**:
  - 관통 돌격 `piercing_lunge`: 사용자 "원핸드 라이트 돌진과 같은 범위·사거리" → 한손 무기엔 돌진이 없고 라이트 무기 돌진 = 양손 라이트 `flash_slash`(44 / 11) → **distance 29 → 44, width 6 → 11** (dashTime 0.3 그대로).
  - 스킬 아이콘(기존 스킬 아이콘처럼 흰 실루엣 기호) `scripts/spear_skill_icons.py`: 사슬 갈고리(창 + 늘어진 사슬) **123513643390143**, 도약 찌르기(점선 포물선 + 내리꽂는 창 + 땅) **108793794450569**, 창 휘두르기(창 + 회전 원호) **121844632731315**, 신의 창(빛살 속 내리꽂는 창 + 표적 고리) **73977985421128**. 관통 돌격은 기존 88017100002295 그대로. → `Skills` 의 icon 에 연결 (이 네 스킬은 icon 이 없었음).
    - 주의: 원호를 오목 다각형 하나로 만들면 삼각분할이 안쪽을 채움 → 사각형 띠로 만듦.
  - 성유물 아이콘(기존 성유물처럼 룬 새긴 돌판 + 가장자리 빛 + 반짝이, 창 = 초록 룬) `scripts/spear_relic_icons.py`: 관통 돌격(오벨리스크·위로 꿰뚫는 화살) **132639492526129**, 사슬 갈고리(둥근 판·갈고리·고리) **136135172445211**, 도약 찌르기(깨진 조각·포물선·땅) **101552959946591**, 창 휘두르기(원반·나선·창) **104596984114484**, 신의 창(마름모·빛살·고리) **95627576562842** → `PolearmRelics` 의 icon 교체(전부 임시 130318329623590 이었음). Cycles 64, 돌 = 노이즈 색 + 범프 + 구름 변위, 룬 = 밝은 심 + 초록 빛 3겹, 테두리 빛 4겹(세게 하면 흰색으로 날아가서 약하게).
  - ID: `exports/texture_ids.json` → `SpearIcons`. 확인: 플레이 스킬 바 R F G V X 에 새 아이콘 표시. 성유물 아이콘은 인벤토리에서 직접 확인 필요.
  - 게시: Shared(Skills·PolearmRelics).
- ✔ **신의 창도 더미에 피해 안 들어가던 버그 (2026-11-24, 사용자)**: 창 휘두르기와 같은 원인 — `skyfallHits` 의 벽 검사가 terrainParams(적 폴더·플레이어만 뺌)라 적 폴더 밖 훈련용 더미가 자기 몸에 막힘. `Services.Skill` 에 공용 **`wallBetween(from, to, target)`**(대상 모델 빼고, 맞은 게 Humanoid 모델이면 건너뛰며 최대 4번) 추가 → 창 휘두르기(`spinHits`)·신의 창(`skyfallHits`) 둘 다 이걸 씀. 플레이: 신의 창 더미에 12·12·22 + pin, 창 휘두르기 26, 오류 없음. 게시: Services(Skill).
  - ✔ **전체 점검 (사용자: "점검해 줘")**: `Services` 의 모든 레이캐스트를 훑음.
    - 피해 판정 함수 중 시야(벽) 검사가 있던 건 창 휘두르기·신의 창뿐(→ wallBetween 으로 고침). 진동·삼연격·난무·광륜·처형·폭발·파도 판정은 벽 검사가 없어 더미에 원래 들어감. 투사체(castPath)·파도(wavePath)·사슬 갈고리 경로·도약 보정은 이미 Humanoid 몸을 벽으로 안 봄.
    - **문제였던 것: 돌진 경로**(`lungePath` = 관통 돌격·섬광 베기, `chargeHits` = 어깨 돌진)가 terrainParams 로 앞을 훑어 **더미 몸 앞에서 멈춤**, 신의 창 보정(skyfallPlan)도 더미에 안 붙음 → `terrainParams()` 가 적 폴더처럼 **태그 `TrainingDummy`** 모델도 뺌(CollectionService). 더미 `DummyRegen` 이 시작할 때 태그를 달고 부품 CollisionGroup 을 **"Enemies"**(적과 같은 그룹 → 돌진 중 passThroughEnemies 로 통과)로.
    - 플레이 확인(더미): 관통 돌격 26(47 지나감) / 사슬 갈고리 19 / 도약 찌르기 29 / 창 휘두르기 26 / 신의 창 12·12·22, 오류 없음. 다른 무기 스킬은 무기를 바꿔야 해서 실제로는 안 쏴 봄(코드로만 확인).
    - 게시: Services(Skill) + 마을 place 저장(더미 스크립트).
- 다음: 창 휘두르기 → 신의 창 → 관통 돌격 강화 (하나씩).

## 4. 단검(Dagger) 스킬 — 그림자 발걸음 Shadow Step (2026-11-25, 마을 place 패키지 코드)
- 요청(사용자): 적 뒤로 순간이동 후 찌르는 단검 스킬의 VFX (검은 연기·보라 잔상·날카로운 칼날 궤적, 절제된 스타일). **스킬 자체가 없어서** 사용자 결정 "스킬까지 새로 만들기"로 판정까지 새로 만듦.
- 정의 `Shared.Data.Skills.shadow_step` (kind **"blink"**, 수치 임시: 쿨 8 / 피해 ×2.4 / castDelay 0.15 = 사라짐→도착 / stabDelay 0.27 = 도착 뒤 찌르기(단검 기본 공격 windup 과 같게) / maxDistance 30 / aimAssist 180 = 사방 가장 가까운 적 (사용자 2026-11-25 "주변 가장 가까운 적에게", 처음엔 앞쪽 50°) / behindDistance 3.5 / flinch 0.5). 성유물 `DaggerRelics.relic_shadow_step` (아이콘 임시 = Parry 아이콘, 전용 아이콘 필요). `TEST_COOLDOWN = 1` 이라 지금은 쿨 1초.
- 서버 `Services.Skill`: `blinkTarget`(aimAssist 각도(180 = 사방)·사거리 안, 벽에 안 가린 가장 가까운 적) / `blinkDest`(적이 보는 반대쪽 → 대각 뒤 → 옆 → 내 쪽 순으로 벽·바닥 검사, 적을 보는 CFrame) / `blinkHits`(시전~도착+0.15 무적 ForceField, 적 통과 충돌 그룹, castDelay+stabDelay 에 대상 하나 피해 + 경직 + phase "hit"). 대상이 없으면 "No target in reach." 안내, 쿨다운 없음. ECHO_EXCLUDED·ROOT_BLOCKED 에 blink 추가(클라 SkillController 속박 검사도). 이동은 leap 처럼 **클라 연출 모듈이 내 캐릭터를 dest 로 PivotTo**.
- 연출 `Controllers.SkillController.Vfx.ShadowStep` (원본 `scripts/packages/Controllers/Vfx_ShadowStep.lua`):
  - 사라짐(0): 어두운 보라 잔상(뒤로 밀리며 0.35초) + 발밑 검은 연기 고리(VfxKit.smokeRing 어둡게, 바깥으로) + FsSmokeDark 덩이 5 + 보라 알갱이 9. 시전자 몸·무기 빛을 모든 화면에서 숨김(LocalTransparencyModifier).
  - 도착(castDelay): 연기·알갱이가 **안쪽으로 빨려 듦**(Sphere Inward) + 세로 보라 틈 번쩍 + 작은 연기 고리 → 출발과 반대 움직임으로 구분. 몸 0.08초에 다시 보임. 내 캐릭터면 단검 콤보 첫 타 모션.
  - 찌르기(+stabDelay): **임시 칼날 = Beam 4개 마름모**(보라 바깥 + 흰 심, 길이 6.5, 0.06초 뻗고 0.14초 사라짐). 모듈 아래 MeshPart **`BladeMesh`** 가 있으면 그걸 씀(없으면 임시). 맞음(phase "hit"): EbSpark 흰 7 + 보라 10, 작은 섬광 구, 빛, 타격음, 약한 흔들림.
  - 정리: 연출 폴더 1.62초 뒤 삭제, 몸 숨김·회전 잠금은 무슨 일이 있어도 0.92초 뒤 복구(task.delay).
- 플레이 확인(더미, 창 무기 소켓 1에 임시 Script 로 끼워 SkillCast 직접 발사): 15.5 이동 → 더미 정확히 뒤 3.5(뒤 방향 내적 −1.00), +0.44초 hit 연출, 몸 숨김 1 → 복구 0, 남은 폴더·ForceField 없음, AutoRotate 복구, 오류 없음. 대상 없는 쪽으로 쓰면 연출·이동 없음. **실제 단검 + 키 입력·남의 화면·PvP 는 안 해 봄.**
- Blender 칼날 메시(선택, 아직 안 만듦): 길이 6.5 × 폭 0.8 × 두께 0.05 스터드 납작한 마름모(가장 넓은 곳 꼬리에서 72%), 앞 = Roblox −Z, 피벗 = 꼬리 가운데, Neon·보라(110,0,230)·투명 0.2, CanCollide/CanQuery/CanTouch 끔, CastShadow 끔. Studio 에서 `Vfx.ShadowStep` 아래 `BladeMesh` 로 두고 PivotOffset 을 꼬리로.
- 게시 필요: **Shared**(Skills, DaggerRelics) / **Services**(Skill) / **Controllers**(SkillController, Vfx.ShadowStep).
- ✔ **대상 = 주변 가장 가까운 적 (2026-11-25, 사용자)**: `Skills.shadow_step.aimAssist` 50 → 180, 서버 `blinkTarget` 은 180 이면 방향 검사를 건너뜀(정확히 뒤 적이 부동소수 오차로 빠지지 않게). 설명문도 "in front of you" 뺌. 플레이: 더미를 정확히 등진 채(−1.00) 시전 → 더미 뒤 3.5 로 이동 + hit, 오류 없음. 게시: Shared(Skills) + Services(Skill).
- ✔ **Blender 칼날 메시 (2026-11-25, 사용자 "만들어줘")**: `scripts/shadow_step_blade.py` — 마름모 단면(가운데 능선 두께 0.12, 날 0) 칼날, 길이 6.5·최대 폭 0.78(꼬리에서 72%), 꼬리는 가늘게 끌리고 끝은 오목하게 날카로움 + 안쪽 흰 심 Core(폭 35%), 삼각형 284. 모델 에셋 **127313928571413**(그룹), BladeMesh MeshId 119094222831278 (`exports/texture_ids.json` → ShadowStepBlade).
  - Studio: `Vfx.ShadowStep.BladeMesh`(Neon 보라 110,0,230 투명 0.3) + 자식 `Core`(Neon 흰 투명 0.05). PivotOffset = 꼬리, 앞(LookVector) = 칼날 끝(메시 로컬 −X, 보정표대로), 위 = 두께 축. 충돌·그림자 끔.
  - 모듈: 메시가 있으면 자식 MeshPart 도 상대 위치 그대로 같이 밀려나가며 사라짐. 시각 맞춤 `atAbs`(연출 시작 기준) — 잔상 복제 등 앞 작업 시간만큼 도착·찌르기가 밀리던 것 고침.
  - 플레이: 칼날 끝이 더미 쪽(내적 1.00), Core 같이 나옴, 0.25초 뒤 투명 1, 남은 폴더 없음. Studio 에서 칼날 = 받은 뒤 0.53~0.57초, 서버 타격 연출 0.56~0.61초로 거의 같이 나옴(Studio 자체 지연 0.15~0.22 포함). 실제 화면 모양은 눈으로 안 봄.
  - 게시: Controllers (Vfx.ShadowStep + BladeMesh).

### 칼날 회오리 Blade Whirl (2026-11-25, 단검 스킬 2번째, 마을 place 패키지 코드)
- 요청(사용자): 제자리 회전 연속 베기 VFX(Blender 칼날 메시 + 파티클, 어두운 보라 중심, 절제). 스킬이 없어서 사용자 결정 "스킬까지 새로" + "지금 Blender로 메시 제작".
- 정의 `Skills.blade_whirl` (kind **"whirl"**, 임시: 쿨 9 / castDelay 0.1 / spinTime 0.9 / turns 3 / radius 10 / flinch 0.3 / hits 0.4·0.7·1.0 = 바퀴 끝마다, 피해 0.8·0.8·1.2, 마지막 knockback 8). 성유물 `DaggerRelics.relic_blade_whirl` (아이콘 임시 = Parry).
- 서버 `Services.Skill.whirlHits`: 타 시각마다 그 순간 내 자리 반경 안(높이 차 radius/2, 벽 너머 제외) 대상 피해 + 경직 + 바깥 넉백, 맞은 대상마다 phase "hit"(index). ECHO_EXCLUDED 에 whirl. 속박 중에도 사용 가능(제자리).
- 메시 `scripts/blade_whirl_arc.py`: 수평 초승달 칼날 2장 180° 마주 봄(바운딩 중심 = 회전 중심), 바깥 날 반지름 4.6, 호 110°, 최대 폭 0.55(끝 쪽 82%), 두께 0.07, 꼬리 가늘게 끌림 + 흰 심 Core(폭 40%). 삼각형 824. 모델 **138502072838714**, WhirlBlade MeshId 102624018300327 / Core 76586362218692 (`texture_ids.json` → BladeWhirl). Studio `Vfx.BladeWhirl.WhirlBlade`(Neon 보라 투명 0.35) + `Core`(Neon 흰 0.1), CFrame·PivotOffset identity. EditableMesh 로 확인: 넓은 부분이 115~128°/295~308° → 칼날 끝이 회전(왼쪽) 방향 앞.
- 연출 `Vfx.BladeWhirl` (원본 `scripts/packages/Controllers/Vfx_BladeWhirl.lua`): 발동 = 발밑 검은 연기 고리(2.6) + 원기둥 둘레 보라 알갱이 안쪽으로 16 + 보라 빛 / 회전 = 내 몸 왼쪽 3바퀴(HRP CFrame, 회전 잠금, 단검 첫 타 55% 자세 멈춤) + 칼날 메시가 몸과 같은 각도로 허리 높이에서 돎(5° 기울임, 0.1초에 0.6→1 크기·투명→보임) + 칼날 끝 보라 불티(Rate 45) / 맞음 = 접선 방향 흰 EbSpark 5 + 보라 6 + 작은 섬광 + 타격음 / 끝 = 칼날 1.12배로 커지며 0.18초에 사라지고 회전 감속, 원 둘레 잔광 알갱이 22 + 빛 0.4초. 메시가 없으면 Beam 곡선 초승달 2장(보라+흰 심).
- 플레이 확인(더미, 창 무기 소켓 2에 임시 Script): 타격 연출 3번(index 1·2·3, 받은 뒤 0.45/0.76/1.11초), 칼날과 몸 각도 매 순간 같음, 끝나고 처음 방향(내적 1.00)·AutoRotate 복구, 남은 폴더 없음, 오류 없음. 메시를 뗀 임시 Beam 버전도 빔 4개로 정상·정리됨. **눈으로 모양은 안 봄, 실제 단검·남의 화면 안 해 봄.**
- 게시: Shared(Skills, DaggerRelics) / Services(Skill) / Controllers(Vfx.BladeWhirl + WhirlBlade).
- ✔ **칼날 회오리 연출 v2 — 교차하는 초승달 베기 (2026-11-25, 사용자 요청 "원형 Trail 말고 Blender 초승달 베기 메시를 여러 방향으로 교차")**: 판정·피해·타격 시각·몸 회전·자세는 그대로, `Vfx.BladeWhirl` 만 교체 (v1 원형 궤도 칼날·검은 연기·끝 잔광 제거, 흰 + 선명한 보라).
  - 메시 `scripts/blade_whirl_slashes.py` (원점 = 호 중심 = 휘두르는 축, 쐐기 단면 + 길이 방향 활·들림): **A** 반지름 3.6·호 150°·폭 0.78 대칭 / **B** 4.4·175°·폭 1.30·앞이 두툼·나선 들림 0.6 / **C** 7.0·72°(현 약 8.2, 거의 곧은 긴 대각)·폭 0.95·끝 아주 날카로움. 각각 흰 심 Core. 삼각형 312 씩. 모델 **107005971350233**(폭 넓힌 v2, 처음 것 100915407961479 안 씀), MeshId 는 `texture_ids.json` → BladeWhirlSlashes.
  - Studio: `Vfx.BladeWhirl.SlashA/B/C` (Neon 보라 140,40,255 투명 0.2) + 자식 `Core`(Neon 흰 0.05). **PivotOffset = 호 중심** (Blender bbox 중심 (x,y,z) → 피벗 (x, −z, −y)), EditableMesh 로 확인: 칼날 가운데 = 로컬 −X, 끝 = +X 쪽.
  - 배치표 `SLASHES`(모듈 맨 위): A 8개(0.10~0.84초, 그 순간 몸 각도 + yaw, 평면 기울기 −55~75°, 높이 −0.9~1.0, 크기 0.8~1.15, 방향 ±), B 2개(0.36·0.67, 서버 1·2타 직전), 각 0.2~0.28초 동안 호 중심 둘레로 110~150° 휘둘러지며 나타남→사라짐. 마무리 C 2개(0.92·0.97) 몸 앞 3.6·위 0.3 수직 평면에서 X 교차(크기 1.15) → 1.0 흰 섬광 + 허리에서 바깥으로 튀는 불꽃 24(보조 충격파). 발동 = 가슴 앞 흰 섬광 + 반짝이 8.
  - `isMine` 이 LocalPlayer 없을 때(편집 화면 미리보기) 오류 안 나게.
  - 확인: 편집 화면 느린 미리보기 캡처(v2 폭 넓히기 전)로 여러 평면 교차·강조 베기·X 교차를 눈으로 봄 → 칼날이 가늘고 X 가 몸에 가려 폭 1.8배·X 앞으로 옮김. 폭 넓힌 뒤에는 편집 화면이 그려지지 않아 **눈으로 다시 못 봄**. 플레이(더미): A 8·B 2·C 2 모두 생성, 칼날 평면 법선 제각각, 타격 연출 3번, 방향 복구, 남은 폴더 없음, 오류 없음.
  - Blender MCP 가 응답 없음(look 뒤 시작 화면에 막힌 듯) → `D:\blender.exe -b --factory-startup --python-expr "exec(open(r'D:\god\scripts\blade_whirl_slashes.py', encoding='utf-8').read())"` 로 명령줄 실행해서 만듦.
  - 게시: Controllers (Vfx.BladeWhirl + SlashA/B/C).
- ✔ **칼날 회오리 연출 v3 — 참고 그림(흰 앞날 → 보라 → 어두운 꼬리, 번짐·빛줄기·불티) 방식 (2026-11-25, 사용자: "전부에, 그 퀄리티 안 나오면 만들지 마" → 시험 후 "바로 적용해서 직접 보기" 선택, 못 미치면 v2 로 되돌림)**
  - 텍스처 `scripts/vfx_whirl_slash_tex.py` (명령줄 Blender, 1024x256): 색+투명도 맵(앞날 흰 → 라일락 → 보라 → 어두운 보라 꼬리, 길이 방향 붓질 결) **이미지 99342720630432** / 발광 마스크 **이미지 117824323402160** (Decal 88923218582093 / 102808745498924, 그룹, 승인 확인 후 붙임).
  - 메시 v3 = `blade_whirl_slashes.py` 에 UV 추가 (u = 길이 0 꼬리 → 1 끝, v = 바깥 날 0 → 안쪽 1), 모델 107046513668773. Studio `Vfx.BladeWhirl.SlashA/B/C` = SmoothPlastic 흰 + DoubleSided + **SurfaceAppearance**(ColorMap, AlphaMode Transparency, EmissiveMask, EmissiveStrength 4, EmissiveTint 255,225,255), Core 없음. 원본 `ServerStorage.WhirlProto`.
  - 모듈: 베기마다 앞머리(호 끝 85%)에 보라 PointLight(A 2.2 / B·C 3.5, 사라지며 꺼짐) + 흰·보라 불티(Rate 40/70). 강조 B 는 휘두름 18% 시점 앞머리에서 접선 빛줄기(FsSlashLine Beam, 길이 11, 0.16초), 마무리 C 는 그어지는 대각 방향 빛줄기(13). 
  - 플레이(더미): A 8·B 2·C 2, 앞머리 12, 빛줄기 4, 타격 3번, 방향 복구, 남은 폴더 없음, 텍스처·스크립트 오류 없음. 맵 Bloom 0.68/30/1.6. **화면으로는 못 봄**(Studio 편집 화면 캡처가 빈 화면, 플레이는 타이틀 화면이 덮음) → 사용자가 `/fx blade_whirl 0.3` 으로 판단. 못 미치면 git 의 v2 모듈 + `SlashA/B/C` 를 v2 메시(Neon 보라 + Core)로 되돌리기.
  - Blender MCP 창이 응답 없음 상태(이 세션) — 다음에 Blender 창 확인.
  - 게시: Controllers (Vfx.BladeWhirl + SlashA/B/C).
- ✔ **칼날 회오리 v4 (2026-11-25, 사용자 피드백 3가지 + 참고 그림)**: ① "플레이어에 이펙트가 없다"(참고: 발밑 빛 원 + 솟는 불티 + 빛기둥) ② "광역 스킬, 범위 넓게" ③ "베기가 너무 얇다, 두껍게(넓은 띠)"
  - ② `Skills.blade_whirl.radius` 10 → **16** (서버 판정 반경). 더미 14스터드에서 3타 모두 맞음 확인.
  - ③ 메시 v4 `blade_whirl_slashes.py` SPECS: A 반지름 7·호 150°·폭 2.2·두께 0.16 / B 9·170°·폭 3.4·두께 0.22·나선 들림 1.2 / C 11·72°·폭 2.0. 모델 **107706310707069** (MeshId 는 texture_ids.json). SurfaceAppearance 같은 이미지. 모듈 HEADS·C_RADIUS 11·FINISH_FORWARD 5·UP 0.5·FINISH_SCALE 1, 앞머리 빛 범위 14/20·불티 60/100, 빛줄기 16/18.
  - ① `playerAura` (castDelay 전부터 spinEnd + 0.35초 사라짐, 몸을 따라감): 캐릭터 Highlight(보라, 채움 0.72·테두리 0.25) + 발밑 빛 원(새 이미지 **88252622732116**, Decal 103431041913167, 지름 3→8로 커지며 천천히 돎) + 원기둥 안에서 솟는 흰·보라 불티(Rate 80) + PillarCore 빛기둥(발~+8, 보라) + 보라 PointLight 16.
  - 플레이: 오라 4종·베기 12·앞머리 12·빛줄기 4·섬광 2·충격 불꽃 1, 타격 3번, 방향 복구, 남은 폴더 없음, 오류 없음. **화면으로는 못 봄** (사용자 확인 대기).
  - 게시: Shared(Skills) + Controllers(Vfx.BladeWhirl + SlashA/B/C).
- ✔ **칼날 회오리 v5 — 무료 Creator Store "Slash VFX System" 기반 (2026-11-25, 사용자 "그걸로 다시")**
  - 발견: v3·v4 SurfaceAppearance 메시 칼날은 실제 화면에서 거의 안 보였음(어둡고 투명). 플레이 화면 캡처로 확인 → 이제 확인 방법: 플레이 시작 후 `user_keyboard_input` Space(타이틀 넘김) → screen_capture.
  - 무료 에셋 격리 검사 `ServerStorage.VfxQuarantine` (4개, 위험 스크립트 없음). 채택: "Slash VFX System" (MorphoTheNoob, 85889779196357, "Free to use") → 재료를 `Vfx.BladeWhirl.WhirlKit` Part 로: CrescentA/CrescentB(휘어진 텍스처 빔 5겹 반원, 반지름 7, 법선 로컬 X) / Slash(평면 플립북 combo1) / Burst(불꽃·별·선·번개). 텍스처는 다른 소유자지만 게임에서 로드 확인(Success).
  - 모듈 v5: 베기 10개 = 빔 초승달을 배치표 평면에 두고 법선 둘레로 휘두르며 나타났다 사라짐(강조 B 는 1.3배·굵기 1.6 + 터짐), 마무리 = 몸 앞 수직 평면 큰 초승달 2개 X + 1.0초 섬광·터짐. 오라·타격·범위 16 그대로. 메시 SlashA/B/C 는 모듈에서 뺌(ServerStorage.WhirlProto 에 남음).
  - 확인: 실제 F 키 시전 화면 캡처에서 굵은 보라 초승달들이 몸을 감싸며 교차하는 것 확인. 마무리 X·정리 여부는 아직 화면으로 확인 안 함.
  - 게시: Shared(Skills 범위 16) + Controllers(Vfx.BladeWhirl + WhirlKit).
- ✔ **칼날 회오리 색 더 진하게 (2026-11-26, 사용자 "괜찮은데 색을 조금 더 진하게")**: `Vfx.BladeWhirl.WhirlKit` 안 빔·파티클 16개의 밝은 라일락 (193,94,255) → 짙은 보라 **(140,35,255)** (검은 결 이미터는 그대로). 코드 변경 없음(키트 인스턴스 색만). 플레이 F 키 시전 캡처로 확인, 끝난 뒤 남은 폴더 없음. 게시: Controllers.
- ✔ **칼날 회오리 색을 다른 스킬 규칙에 맞춤 (2026-11-26, 사용자 "혼자 다른 게임 같다" → "색을 바꿔 달라는 것")**: 모양(v5 키트)·코드·판정·오라는 그대로, `Vfx.BladeWhirl.WhirlKit` 인스턴스 색·밝기만 바꿈. 원인 = 빔·파티클 16개가 전부 한 색 (140,35,255) + Brightness 10~20 이라 네온 자홍으로 타 보였음.
  - 규칙(VfxConfig.WEAPON_COLORS): 흰 = 날·별·불꽃, 본색 = 단검 (110,0,230), 사이 = 라일락 (190,130,255, 그림자 발걸음 PURPLE_SOFT), 어두운 꼬리 (60,0,140). Brightness 최대 4 (빔 Beam2 2.5, Slash 2·Alpha 2).
  - CrescentB: Beam2(앞 겹) 본색→라일락→흰(머리) / Beam3 어두운→라일락 / Beam·Beam4·Beam5 어두운→본색. Slash: 1 흰→라일락, 2·Alpha 본색, Specs1 라일락. Burst: Sparks·Lines1 흰→라일락, star 흰, 25R 라일락→본색, Lightning 본색. 검은 결 이미터 그대로.
  - 플레이 캡처(같은 자리 /fx 0.05배속)로 회전 중·마무리 X 확인: 자홍 → 짙은 보라 몸통 + 라일락/흰 날. 끝난 뒤 남는 폴더 없음.
  - 중간에 v6(반월 베기 검기 텍스처로 새로 씀)을 만들었으나 사용자 의도(색만)와 달라 버리고 v5 로 되돌림 (저장소에 남기지 않음).
  - 게시: Controllers (Vfx.BladeWhirl.WhirlKit).
- **칼날 회오리 텍스처 자체 제작 시험 (2026-11-26, 사용자 "Blender 말고 Python 으로 해 봐")** — 적용 안 함, 비교만
  - `scripts/vfx_whirl_brush.py` (numpy·Pillow): v5 키트 텍스처 6장(빔 3 + 4x4 플립북 3)을 대신할 붓질 그림. 원본을 화면에 띄워 보니 빔은 흐릿한 흰 덩어리(연기 줄·가운데 마름모·끊긴 가닥), 플립북은 가는 흰 초승달 → 같은 역할로 그림.
  - 3번 고침: 1차 결이 자로 그은 줄·플립북이 넓은 면 → 2차 플립북 바깥 날만 밝게·몸통 번짐 줄임 → 3차 심(빔 5겹 중 3겹이 씀)을 띠 가운데 구간만 차지하는 또렷한 칼날로. ID 는 `texture_ids.json` → `VFX.BladeWhirlBrush` (그룹, 승인).
  - 같은 자리 /fx 0.05배속 비교: 마무리 X 는 v5 와 비슷하게 나오지만, 회전 중 베기는 v5 보다 얇고 납작한 반투명 띠로 보여 대비·밀도가 떨어짐. 플레이 클라이언트 복사본에서만 바꿔 끼워 봄, 패키지·Studio 원본은 v5(색 조정본) 그대로.
  - ✔ **적용 (2026-11-26, 사용자 "잘 만들었어" → "방금 만든 걸로 바꿔줘")**: Studio `Vfx.BladeWhirl.WhirlKit` 빔 5·이미터 5개 텍스처를 위 3차 그림으로 교체 (터짐 Burst 는 키트 그대로). 원래 무료 키트 텍스처는 각 인스턴스 속성 `OrigTexture` 에 남김 → 되돌릴 때 그 값으로. 모듈 코드는 머리 주석 2줄만 추가.
  - 확인: 바꾼 키트로 /fx 0.05배속 회전 중·마무리 X 화면 캡처(위 비교), 실제 F 키 시전은 오류 없음·끝난 뒤 남는 폴더 없음·AutoRotate 복구 (이때 Studio 창이 가려져 3D 캡처는 검게 나옴 → 실제 시전 화면은 눈으로 못 봄).
  - 게시: **Controllers** (Vfx.BladeWhirl + WhirlKit).

### 단검 5번 스킬 "그림자 연쇄"(가칭) — 구상·연쇄 규칙 시험 (2026-11-26 시작, 사용자: "가장 중요한 스킬")
- 기획(사용자 글): 첫 적 공격 → 주변 다른 적에게 순간이동해 공격(같은 적 다시 안 벰) → 대상 없을 때까지 → 첫 대상에게 돌아가 잃은 체력 비례 추가 피해.
- 결정(사용자): 다음 대상 = **방금 벤 적 주변** 반경 R / **최대 6명**(첫 대상 포함) / 첫 대상이 연쇄 중 죽으면 **처형 생략** / 무기 **5번 소켓** / **스킬 내내 캐릭터는 완전히 안 보이고 이펙트만** (벨 때도).
- 구상: kind "chain" 새로, `blinkTarget`·`blinkDest` 재사용, 매 순간 다음 대상을 다시 고름(죽거나 움직여도 안 꼬임), 무적·적 통과, 처형 = 기본 + 잃은 체력 × 계수(보스 상한). 연출 = 그림자 발걸음 결(흰 + 보라 + 검은 연기), 적 사이 잉크 궤적, 벤 적에 표식 → 처형 때 같이 터짐. 텍스처·잉크 연기는 Python(numpy) 붓질·2D 유체 시뮬로.
- 시험 `scripts/sim_shadow_chain.py` (상황 4종 × 반경 8~20 × 4000회, 예시 그림 exports/vfx/shadow_chain/sim_examples.png):
  - R 12: 밀집 무리 평균 5.6명(전원 89%), 넓은 무리 3.0, 복도 일렬 5.7(귀환 거리 평균 40), 무리 두 개 4.1(옆 무리로 넘어감 10%). 시간 약 1.1~1.55초.
  - R 8 은 복도에서 거의 안 이어짐(1.5명), R 16~20 은 떨어진 다른 무리까지 넘어가는 일이 늘어남.
  - 처형 예시 2.0 + 잃은 체력 × 3.0 (반피 ×3.5, 10% ×4.7), 보스는 잃은 체력 몫 +1.0 상한.
- 다음: 사용자에게 R·한 타 배율·처형 계수·쿨다운 확정 받기 → 서버 판정 + 임시 연출.
- ✔ **2단계: 서버 판정 + 임시 연출 (2026-11-26, 사용자 "추천대로": 반경 12 / 한 타 ×1.0 / 처형 2.0 + 잃은 체력 × 3.0, 보스 +1.0 상한 / 쿨 16)**
  - `Shared.Data.Skills.shadow_chain` (kind **"chain"**, 필드 hopTime 0.18·chainRadius 12·maxTargets 6·returnTime 0.25·executeDelay 0.3·executeBase/Scale/BossCap, 타입 SkillDef 에도 추가) + `DaggerRelics.relic_shadow_chain` (아이콘 임시 = Parry).
  - `Services.Skill`: `chainNext`(방금 벤 적 자리 기준 수평 반경·높이 차 8·안 벤·벽 검사, 가장 가까운 적) / `chainDest`(blinkDest 를 지금 내 자리 기준으로) / `chainHits`(무적 ForceField + 적 통과, 벨 때마다 phase "strike"(index, from, target, point), 기다리는 동안 다시 고름, 끝나면 "return" → "execute"(missing, mult), 첫 대상이 죽었으면 "finish"). ECHO_EXCLUDED·ROOT_BLOCKED(서버+클라 SkillController)에 chain, 대상 없으면 "No target in reach." 쿨다운 없음.
  - 임시 연출 `Vfx.ShadowChain` (원본 `scripts/packages/Controllers/Vfx_ShadowChain.lua`): 시전~끝까지 몸·무기 빛을 모든 화면에서 숨김(사용자 결정), 내 캐릭터는 서버가 보낸 자리로 옮겨 고정. 출발 잔상·검은 연기 고리 / 적 사이 그림자 궤적(Beam) / 적에 X 칼자국(Beam)·불꽃 / 벤 적 보라 표식 → 처형 때 터짐 / 처형 큰 X·섬광·흔들림(잃은 체력만큼 크게) → 몸 다시 보임. 텍스처는 기존 것(FsSmokeDark·EbSpark·HolySparkle), 다음 단계에서 Python 그림으로.
  - 플레이 시험 (로비, office_husk 8마리 제자리 고정, 시험 동안만 단검 5번 소켓에 성유물·무적, 끝나고 되돌림: 5번 소켓 원래 비어 있음): ① 무리 7 + 먼 1 → strike 1~6 → return → execute, 6명 제한으로 1명·먼 적은 안 벰, 피해 들어감, 끝나고 머리 보임·AutoRotate 복구·연출 폴더·표식 남지 않음. ② 첫 대상 체력 3 → 첫 타에 죽고 연쇄 5명 뒤 "finish"(처형 생략). 오류 없음. 첫 시도는 로비 훈련용 더미가 첫 대상이 되어 1명에서 끝남(더미 주변 12 안에 적 없음, 정상 동작).
  - 화면: 몸은 안 보이고 칼자국·궤적만 보임 확인. 임시 연출이라 얇고 작음 → 3단계에서 키움.
  - 게시: Services(Skill), Shared(Skills·DaggerRelics), Controllers(SkillController·Vfx.ShadowChain). `TEST_COOLDOWN = 1` 이 켜져 있어 지금은 쿨 1초.
- ✔ **3단계: 자체 텍스처 연출 (2026-11-26)** — `scripts/vfx_shadow_chain_tex.py` (Python numpy·Pillow, Blender 안 씀), ID 는 `texture_ids.json` → `VFX.ShadowChain`
  - 잉크 연기 `ink_puff` 8x8(칸 128): 2D 흐름 계산(두 흐름 함수를 시간에 따라 섞은 회전 흐름 + 처음 바깥으로 터짐, 반-라그랑주 이류) → 말려 퍼지며 옅어짐. 2차에서 터짐 1.6→3.2(칸을 더 채움)·늦게 옅어지게.
  - 궤적 `streak_body`(잉크 몸통, 출발 쪽 갈라짐) + `streak_edge`(1D 로 끊기는 가는 테두리 두 줄 + 심 — 1차 2D 노이즈 덩어리는 지저분해서 바꿈), 칼자국 `slash` 4x4(그어짐 → 머묾 → 결로 갈라짐), 표식 `mark`(끊긴 고리 + 네 갈래 가시 + 가운데 마름모 — 1차 가로 가시가 끝까지 새던 것 고침).
  - `Vfx.ShadowChain` 2차: 잉크 연기(검게 + 옅은 보라 기운), 궤적 Beam 두 겹, X = 칼자국 플립북 두 장 ±38°(보라 번짐 + 흰 심), 표식 = 적 몸 BillboardGui(돌다가 처형 때 커지며 터짐), 처형 = 큰 X + 표식 문양 충격 + 잉크 + 연기 고리, 처형 직전 내 화면 ColorCorrection 눌림 → 처형 순간 밝게.
  - 화면 확인: 실제 시전 X 칼자국 또렷·캐릭터 안 보임, 미리보기 0.08배속으로 궤적·잉크 확인 → 궤적 테두리가 흰 판처럼 넓고 밝아 좁고 어둡게(2.2, 보라→라일락, 밝기 1.6), 몸통은 조금 빛나게(0.45). 실제 무리 시전: 5명 + 처형, 마지막 적에서 15.6 떨어진 1마리는 규칙대로 안 벰, 끝나고 폴더·표식·화면 효과 남지 않음, 오류 없음.
  - 사용자 데이터: 시험 중 단검 5번 소켓을 다시 원래대로 → 원래 값이 이미 relic_shadow_chain (사용자가 직접 끼운 것으로 보임) 이라 그대로 둠.
  - 게시: Services(Skill), Shared(Skills·DaggerRelics), Controllers(SkillController·Vfx.ShadowChain). 남은 것: 전용 아이콘, `TEST_COOLDOWN` 끄기.
- ✔ **4단계: 처형 대상 터짐 = 플라즈마 구슬 → 핵 폭발 (2026-11-26)**
  - 1차(폐기): 리본 소용돌이 `scripts/vfx_shadow_chain_burst.py` (빛 구슬을 그림자 리본이 감쌌다 찢어짐, 이미지 body 114166786881687 / rim 120873567690290). 사용자가 새 참고 그림(검은 바탕 남보라 소용돌이 구름 구슬 + 흰·라일락 번개 + 밝은 핵)을 주며 "이걸로 바꿈, 캐릭터보다 작았다가 조금 크게 터짐, 밖에서 안으로 빨리 압축된 뒤 터짐" → 코드에서 뺌(빛 구슬 `burstGlow` 96253058174530 만 계속 씀).
  - 텍스처 `scripts/vfx_shadow_chain_plasma.py` (Python numpy·Pillow, 색 들어간 RGBA, 4x4 칸 256): `plasma_orb` **이미지 93620747404382** (Decal 104092823311094) = 넓게 퍼진 줄기 구름이 빠르게 감기며 안으로 압축 → 번개가 핵으로 빨려 듦·핵이 작고 밝아짐 / `plasma_pop` **이미지 120435824829957** (Decal 111147598409051) = 핵 섬광(가시 빛살) → 끊긴 충격파 고리 → 껍질이 부풀며 2D 노이즈 구멍으로 찢어짐 + 바깥 연기 가닥 → 어두운 보라로 식음. 소용돌이는 노이즈로 감김을 흐트러뜨림(1차는 바람개비처럼 규칙적), 찢김은 2D 노이즈(각도만 쓰면 부채꼴 직선 자국).
  - `Vfx.ShadowChain`: burstStart = 구슬 ParticleEmitter 하나(LightEmission 1, Brightness 1.2, Lifetime = executeDelay + 0.08, RotSpeed -40), **크기 Size 키 `ORB_SIZE_KEYS` 9.5 → (0.3) 3.9 → 4.5 → 4.2** (텍스처의 압축과 같은 값 — 크기를 파티클로 줄여 해상도 유지). burstPop = 구슬 Clear → 폭발 emitter(크기 `POP_SIZE` 9 × min(grow, 1.2), 0.55초, Brightness 1.4) + 기존 반짝이·빛. 가운데 빛(BillboardGui core·halo)은 덜 하얗게(halo 투명 0.6·core 0.2, 처형 때 0.45·0.1).
  - 화면 확인: 첫 적용 Brightness 2.2·2.5 + 흰 빛 구슬이 겹쳐 하얗게 타서 결이 안 보임 → 따로 띄워 1로 맞춰 보니 소용돌이·번개 또렷 → 위 값으로 낮춤. 실제 미리보기(0.12배속, 파티클 TimeScale 0 으로 멈춰 캡처): 압축된 구슬 = 참고 그림 느낌 OK. 처형 순간엔 기존 큰 X 칼자국(EXEC_SIZE 17)이 가장 밝아 폭발이 그 뒤에 보임.
  - 게시 필요: **Controllers** (Vfx.ShadowChain).
  - X 줄임 (사용자 "X 줄이기"): 처형 X 칼자국 `EXEC_SIZE` 17 → 11, 밝기 4+2×missing → 2.2+1×missing, 표식 충격 15 → 11 (× grow).
  - 처형 X 색 (사용자 "마지막 X는 다른 X랑 달랐으면, 흰색 줄이기"): `slashX(..., final=true)` 일 때 흰 심 → 라일락 심(밝기 ×0.45, 투명 0.35), 보라 번짐 주로(×1.1, 크기 1.22). 화면 확인: 처형 X 가 보라로 일반 X(흰 심)와 구분됨, 폭발 구슬이 X 앞에 또렷. 폭발 초반엔 가운데가 하얗게 탐(섬광 + 빛 구슬).

### 단검 스킬 "은신"(Vanish) — 1차 완성 (2026-11-26)
- 기획(사용자): 남에게는 이펙트가 안 보이고 가만히 선 나와 똑같은 분신만 남음, 시전하면 내 화면이 살짝 어두워지고 이동 속도 +25%, 지속 4초, 다른 스킬·기본 공격이면 끊김.
- 결정(사용자 체크리스트): 몬스터 = **분신 미끼형**(나를 쫓던 적이 분신으로, 은신 중엔 나를 새로 못 찾음) / 분신 = **맞으면 연기로 사라짐**·**은신 끝나면 같이 사라짐**·기본 서 있는 자세 / 내 모습 = **반투명 보라 실루엣** / 파티원 = **아주 흐린 윤곽** / **맞아도 끊김** (상호작용은 유지) / **끊은 첫 공격 1.5배** / 쿨다운 **1초(테스트)** / 소리 = **나한테만 작게**.
- 구현 (마을 place, Studio):
  - Shared: `Skills.vanish` (kind "stealth": castDelay 0.1, duration 4, speedBoost 0.25, ambushMult 1.5, ambushWindow 1.2초, cooldown 1 — 정식 값 미정, 추천 14) + `DaggerRelics.relic_vanish`(임시 Parry 아이콘).
  - Services: 새 `Skill.StealthState` (저장소 `scripts/packages/Services/Skill_StealthState.lua`) — 분신 = 캐릭터 복제(스크립트·소리 뺌, 루트만 고정, 관절은 쉬는 자세, 바닥에 맞춤, `workspace.StealthDecoys`), 체력이 줄면 연기로 사라짐. 캐릭터 속성 `Stealthed`·`StealthSpeedMult`. 끊김: 기본 공격 시작(Combat "start") / 다른 스킬 시전(Skill.onCast) / 피격(HealthChanged) / 사망 / 4초.
    - `Skill`: plan 에 stealth, 다른 스킬이면 `StealthState.finish(player, "skill")`, 연출 핸들러(phase "decoy"·"end"), 분신 따라 하기 제외.
    - `Combat.DamageDealer.deal`: `amount *= StealthState.ambushMult(player)` (끊은 순간부터 1.2초).
    - `Movement.applySpeed`: × `StealthSpeedMult`. `Enemy.EnemyAI`: `aliveRoot` 가 은신 중이면 분신 몸통(없으면 nil)을 돌려줌 → 추격·탐색이 분신으로, 분신을 때리면 `popDecoy`, 예비 동작 중에 대상이 은신하면 빗나감.
  - Controllers: 새 `SkillController.Vfx.Vanish` (저장소 `scripts/packages/Controllers/Vfx_Vanish.lua`) — 화면마다 LocalTransparencyModifier(남 1, 파티원 0.9 + 흐린 테두리, 나 0.55 + 검은 보라 Highlight), 남에게는 캐릭터 안 이름표 끔. 나만: 발밑 잉크 연기 + ColorCorrection 어둡게 + 작은 소리. 분신 사라질 때 연기(모두). `CombatController.AttackSlow` 도 `StealthSpeedMult` 곱함.
- 시험 (로비, office_husk 임시 소환 — 시험 Script 는 플레이 끝나며 사라짐): 은신 4.0초 유지, 걷기 13 → 16.25, 분신 생김/끝나면 사라짐, 화면 어둡게·내 실루엣 확인(캡처). 적 3마리가 나를 쫓다가 시전 → 분신 쪽으로 가서 분신을 때림 → 분신 사라짐, 나는 피해 0, 적은 나를 놓치고 돌아감, 은신 끝나자 다시 나를 쫓음. 첫 공격 배율: 서버에서 직접 확인 10 → 15(끊은 직후·0.8초 뒤) → 10(1.4초 뒤), 시간 끝으로 끝나면 보너스 없음.
  - 첫 시도에서 고친 것: 적 공격 예비 동작 중에 은신해도 그 공격이 나에게 들어가 바로 끊김 → 예비 동작 뒤 대상이 은신 중이면 빗나가게.
  - **확인 못 한 것**: 다른 플레이어 화면(완전히 안 보임)·파티원 화면(흐린 윤곽) — 클라이언트 하나로만 시험함.
- 사용자 데이터: 시험하려고 `/get relic_vanish` 로 성유물을 받아 들고 있던 karambit **3번 소켓(G 키)** 에 끼움 (원래 비어 있었음, 그대로 둠). 시험 중 캐릭터가 두 번 죽음(로비).
- **살짝 대시 (2026-11-26 사용자 "누르면 살짝 대시하면서 분신을 남기고 가는 느낌, 적당한 거리")**: `Skills.vanish.dashSpeed 45 × dashTime 0.18` — 연출 모듈이 내 캐릭터를 이동 방향(서 있으면 바라보는 쪽)으로 밀고(기본 대시와 같은 LinearVelocity, 벽에서 멈춤), 미끄러짐까지 실제 약 13스터드(기본 대시 16보다 짧게. 처음 60 은 15.5 라 줄임). 분신은 **누른 자리**: 클라이언트가 보낸 자리(서버 자리에서 10 안, 도약과 같은 검사)로 `StealthState.begin(..., at)` → 서 있을 때·걸을 때 모두 누른 자리와 0.0 차이 (처음엔 서버 자리라 걸을 때 6 어긋남). 화면: 누른 자리에 분신, 대시한 끝에 보라 실루엣 확인.
- **남 화면에 아무 티도 안 나게 (2026-11-26 사용자 "남들은 이펙트가 아예 안 보이게, 스킬을 쓴지도 모르게")**: castDelay 0.1 → **0** (0.1 이면 남 화면에 대시 시작이 보였음). 서버 `onCast` 가 은신일 때만 분신을 **먼저** 만들고 연출을 보냄 → 연출이 도착할 때 분신·Stealthed 가 이미 있음(확인), 남 화면은 같은 프레임에 내 몸만 숨기고 분신이 그 자리에. 분신 사라질 때 연기는 **나만**(남에게는 그냥 사라짐). 남 화면에서는 내 캐릭터의 입자·광선·Trail·빛·하이라이트·이름표도 끄고(다른 코드가 다시 켜도 매 프레임 끔) 끝나면 되돌림. `FootstepController`: 은신 중인 남의 발소리는 안 냄. 시험: 주인 없는 캐릭터 복제(=남 취급)에 입자·빛·이름표를 달아 돌려 봄 → 전부 숨김(LTM 1)·꺼짐·분신 연기 없음·화면 어둡게 없음, 끝나면 모두 되돌아옴. 실제 두 번째 클라이언트로는 아직 안 봄.
  - 남는 것(없앨 수 없음): 분신이 맞아 사라지거나 은신이 끝나 내가 다른 자리에서 나타나는 순간은 남에게도 보임 (연출 없이).
- 게시 필요: **Shared** (Skills·DaggerRelics), **Services** (Skill·StealthState·Combat·DamageDealer·Movement·Enemy.EnemyAI), **Controllers** (Vfx.Vanish·AttackSlow·FootstepController). 남은 것: 정식 쿨다운, 전용 아이콘, 다른 화면 확인.

### 칼날 회오리 마무리 = 꽃잎 터짐 (2026-11-26)
- 사용자: "마지막 X 베기를 빼고 꽃잎이 날리면서 터지는 느낌, 파이썬이든 뭐든 다 활용, 퀄리티 좋게". 결정: **보라 + 흰 끝** / **소용돌이쳐 퍼진 뒤 흩날림** / **많고 작게** / 제작은 "둘 다 써서 좋은 쪽으로".
- 꽃잎 그림: Python 판(`scripts/vfx_whirl_petals.py`, numpy 로 곡면 꽃잎 점 구름을 돌려 z 버퍼 투영·빛) 과 Blender 판(`scripts/vfx_whirl_petals_blender.py`, 실제 메시 + 반투명 재질 + 키·역광, Cycles 256px 16칸) 을 나란히 비교(`_petal_compare.png`) → Blender 는 돌 때 빛을 받아 반짝이는 게 좋고 Python 은 빛 번짐·색이 좋아서 **Blender 렌더 + Python 빛 번짐**으로 합침(`python scripts/vfx_whirl_petals.py final`). Blender 첫 렌더의 잎맥이 기계로 그은 줄 같아서 밑동 쪽만 옅게. 꽃잎 2종(끝 둥근 잎 a, 가늘고 뾰족한 잎 b). 이미지 **a 79525251161536 / b 78183119470395** (`texture_ids.json` → `VFX.BladeWhirlPetals`).
  - 참고: Blender MCP 로 렌더하다 연결이 끊기고 Blender 가 7칸째에서 멈춤 → 명령줄 `D:lender.exe -b --factory-startup --python scripts/vfx_whirl_petals_blender.py` 로 렌더(40초). 열려 있던 Blender 는 건드리지 않음.
- `Vfx.BladeWhirl`: 마무리 X(초승달 2개·0.92 쉭 소리·X 점 키트 터짐·허리 불꽃 고리) 제거 → 1.0(서버 3타) 에 `petalBurst`: 몸 둘레 18곳에서 회전 방향 접선 0.8 + 바깥 0.6 으로 꽃잎(Loop 플립북, 시작 칸 무작위, 회전) 12개씩 속도 30~50·Drag 2.4·아래 가속 3.2 → 반경 16까지 퍼지고 흩날림, 느린 꽃잎 5개씩(9~18, 2.4~3.4초), 몸 가까이 큰 꽃잎 10장, 은은한 섬광. 연출 폴더 수명 + 3.6초. 판정은 그대로.
- 화면 확인 (`/fx blade_whirl 0.1` 로 느리게): 터진 직후 몸 둘레에 몰렸다가 1초 뒤 반경 전체에 흩어져 돌며 떨어짐. 처음 밝기 1.7·LightEmission 0.35 는 로비 조명과 겹쳐 분홍빛 흰색 → 1.15·0.2 로 낮추니 보라 + 흰 끝으로 보임.
- 2차 (사용자 "꽃잎이 뚝 사라짐, 공격 범위보다 너무 넓게 퍼짐"):
  - 사라짐: 투명도가 70% 까지 거의 불투명하다가 크기까지 0 으로 줄며 0.4초 만에 사라졌음 → `PETAL_FADE` (40% 부터 서서히, 75% 에 0.4, 끝 1) + 크기는 끝까지 유지(조금만 작아짐), 수명 조금 늘림(빠른 2.2~3.2 / 느린 2.8~3.8 / 큰 2.0~2.8), `PETAL_LIFE` 4.2.
  - 범위: Roblox 파티클 Drag 는 "속도가 반으로 주는 빈도"라 멈추는 거리 = 속도 / (Drag × ln2) ≈ 1.44 × 속도 / Drag. 처음 값(50 / 2.4)은 약 30 스터드까지 날아갔음 → 빠른 꽃잎 17~29 × (반경/16), Drag 3.2 → 7.7~13, 느린 꽃잎 6~12 / 1.6 → 5.4~10.8.
  - 화면 확인 (`/fx blade_whirl 0.1`, 반경 16 초록 원판을 깔고 위에서): 꽃잎이 원판 안 약 3/4 까지만 퍼짐, 2.4초 뒤에는 반투명으로 서서히 옅어진 상태.
- 3차 (사용자 "꽃잎이 너무 오래 남음, 확 뿌려지고 샥 사라지게"): 수명 빠른 0.9~1.35 / 느린 1.1~1.6 / 큰 0.8~1.2, `PETAL_FADE` = 절반까지 불투명 → 80% 에 0.45 → 끝 1, `PETAL_LIFE` 2.0. 퍼지는 거리는 그대로(Drag 로 정해짐). 화면 확인(0.1배속): 터지고 0.5초엔 빽빽이 퍼짐, 1.4초엔 몇 장만 옅게 남음.
- 게시 필요: **Controllers** (Vfx.BladeWhirl).

### 한국어 언어 전환 (2026-11-26, 마을 place 패키지 코드)
- 사용자 요청: 기존 기능·UI 는 그대로 두고 설정에서 English / 한국어를 고르게. 고유 이름(무기·몬스터·스킬·아이템)은 **뜻을 살려 번역**(사용자 선택).
- 방식: UI 코드 수백 곳을 고치지 않고, 새 컨트롤러가 화면 글자를 지켜보다가 영어 원문을 번역해 바꿔 넣는다 (English 로 돌리면 원문 그대로 복원).
  - **새 파일**: `Controllers.LanguageController` (저장소 `scripts/packages/Controllers/LanguageController.lua`) — PlayerGui·workspace 의 TextLabel/TextButton.Text, TextBox.PlaceholderText, ProximityPrompt 글자. 찾는 순서: 같은 글자 → 대문자 → 형식 문구(%d %s {value}, %s 안 이름도 다시 번역) → 줄마다 → 문장 묶음(특성 설명+추가 문장). RichText 태그는 그대로. 바꾼 글자에는 속성 `LangSource`(영어 원문). 번역 안 할 UI 는 속성 `NoTranslate=true`. API: `get(키)`, `translate(영어)`, `setLanguage`, `changed`.
  - **새 파일**: `Shared.Data.LanguageData` (저장소 `scripts/packages/Shared/LanguageData.lua`, 자동 생성) — 원본은 **`scripts/lang/ko.tsv`** (`키 | 영어 | 한국어`, 1059항목, 용어집은 파일 끝). 고친 뒤 `python scripts/lang/build_language_data.py` → Studio 모듈 Source 를 같은 내용으로 (로컬 HTTP 는 Assistant 허용 목록 밖이라 막힘 → 조각으로 붙여 넣고 체크섬 비교, `--chunks 22000`).
  - **수정**: `Services.Settings` (settings 칸에 `language` 추가, 예전 데이터는 "en", 리모트 `setLanguage`) · `Controllers.SettingsController` (DISPLAY 셋째 줄 Language 버튼, 저장 실패 시 되돌림) · `Controllers.TutorialController` 4곳·`LoadingScreenController.LoadingView` 1곳 (화면 글자를 영어와 비교하던 곳 → `GetAttribute("LangSource") or Text`).
- 번역 범위: HUD·메뉴·인벤토리·대장장이(제작/강화/각성/흡수/이식/분해)·성유물·상인·보관함·업그레이드·의뢰·도감·파티·레이드(지도/출발/도착/출구/결과/부활)·튜토리얼·로딩 팁·인트로·로비 간판, 스킬 22·성유물 설명·아이템·무기·방어구·설계도·적 이름·특성 20·상태 이상, 서버 안내 메시지(배너) 약 200. 개발자 명령(DevCommands)·로그는 제외.
- 플레이 확인(Studio): 설정에서 한국어 → 설정 창·메뉴·인벤토리·아이템 이름·로비 간판 즉시 바뀜(175개), 다시 English → 원문 그대로, 한국어 상태에서 화면 흔들림 버튼 정상, 새로 만든 라벨·나중에 바뀐 글자도 번역, 서버 `get` 이 `language=ko` 돌려줌. **재접속 후 유지는 확인 못 함**(사용자가 중단, 첫 시도는 Return 키가 언어 버튼을 눌러 되돌려 무효). 레이드·대장장이 등 다른 창은 화면으로 못 봄.
- 남은 것: 덜 된 문구 — 분해 결과 "얻은 것: 30 Scrap Metal"(수량+이름 묶음), Roblox 기본 머리 위 이름·기본 ProximityPrompt 모양 글자, 맵 표지(B-07·LIFT A 등 장식은 일부러 둠). 한글 글꼴은 Roblox 기본 대체 글꼴로 나옴(픽셀 글꼴 아님). 영어 문구를 새로 넣으면 `ko.tsv` 에도 추가해야 번역됨(없으면 영어로 나옴, 오류 없음).
- 게시 필요: **Shared**(LanguageData) · **Services**(Settings) · **Controllers**(LanguageController·SettingsController·TutorialController·LoadingView).

### 튜토리얼 지도 단계 (2026-11-26, 마을 place 패키지 코드)
- 사용자 요청: "상가 이동해서 M으로 미니맵 여는 것까지". 순서 = … 레이드 출발(depart, 상가 거리) → **지도 열기(map, 새 8/9)** → 탈출(extract 9/9).
- `Shared.Config.TutorialConfig`: `map` 단계 (`key = "M"`, town 변형 = 출발 문구·RaidDeployZone 목적지 — 지도를 안 열고 마을로 돌아오면 다시 출격 안내).
- `Services.Tutorial`: 레이드 입장 시 `map` 으로 (RaidConfig.MAPS[place].minimap 이 없는 레이드(The Godwound)면 바로 `extract`). 요청 `"map"` = 클라이언트가 지도를 열었음 → 레이드에서 map 단계면 다음으로. map 단계에서 탈출해도 보상 인정, 실패면 다음 레이드에서 다시 map.
- `Controllers.TutorialController`: 패널 안 키 안내 줄(KeyRow: 금색 M 키 그림이 숨 쉬듯 빛나고 1.4초마다 눌림 + "PRESS M"), `PlayerGui.RaidMap` 이 열리면 서버에 "map" 한 번. `RaidMap` 을 WINDOW_GUIS 에 넣어 깨기 연출은 지도를 닫은 뒤에.
- 번역: `ko.tsv` 에 Tutorial.Map.Title/Text, "Press M" 추가 → LanguageData 재생성, Studio 와 길이 일치(90033).
- 확인(마을 place 플레이): 마을에서 map 단계 = "튜토리얼 8/9 레이드에 출발하세요"(한국어), 레이드 데이터 흉내 → "지도를 여세요" + M 키 안내 표시, 가짜 RaidMap 연 채 다음 단계 알림 → 지도 닫을 때까지 8/9 유지, 닫으니 9/9 "레이드에서 탈출하세요". 테스트 뒤 내 튜토리얼은 done 으로 되돌림. **실제 상가 place 에서 M 눌러 넘어가는 것은 게시 후 확인 필요.**
- **모바일 지도 버튼** (`Controllers.RaidMapController`, 터치 기기 ScreenFit.TOUCH 만, 지도 있는 레이드만): ScreenGui `RaidMapButton` → `MapButton` = 가방 버튼(오른쪽 위)과 같은 원·붉은 테두리·크기 56, 가방 바로 왼쪽(간격 12, ScreenFit.hud). 아이콘 = 접힌 지도 띠 3장 + 금색 위치 점, 아래 테두리 MAP(→지도). 지도가 열리면 화면 아무 곳이나 눌러 닫음(`Closer` 버튼), 닫기 안내는 지도 안 오른쪽 아래 "Tap to close".
  - 처음엔 메뉴(…) 버튼 아래에 뒀다가 모바일 스킬 5번 칸과 겹쳐서 옮김.
  - 튜토리얼(터치): 패널 설명 = `touchText`("지도 버튼을 누르면…"), M 키 그림 대신 지도 버튼에 금색 테두리 + 말풍선 "TAP THE MAP"(→지도를 누르세요, 버튼 아래 왼쪽, 꼬리 위쪽). 말풍선 글자는 바뀔 때만 넣음(매 프레임 넣으면 번역이 덮여 영어로 보였음).
  - 확인(iPhone 17 Pro 시뮬레이터, 마을 place 에서 RaidMapController 를 잠깐 상가 지도로 띄워 테스트 후 되돌림): 버튼 배치·겹침 없음(지도 653–692, 가방 700–739), 말풍선 한국어, 지도 열림·아무 곳이나 눌러 닫힘. 닫기 안내 새 위치는 화면으로 못 봄.
- 게시 필요: **Shared**(TutorialConfig·LanguageData) · **Services**(Tutorial) · **Controllers**(TutorialController·RaidMapController).

### 모바일 버튼 배치 설정 (2026-11-26, 마을 place 패키지 코드)
- 사용자 요청: "버튼 위치가 고정이라 불편하고 작다 → 유저가 크기·배치를 조정". 결정(사용자): **전투 버튼 + 가방·메뉴·지도 모두** / **전체 크기 + 버튼마다 크기** / **화면에서 끌어서 편집**. 터치 기기(ScreenFit.TOUCH)만, PC 배치는 그대로.
- 여는 곳: 설정 창 DISPLAY 넷째 줄 **Button Layout [EDIT]**(터치 기기만) → 설정 창을 닫고 편집 화면, 끝나면 설정 창으로 돌아옴.
- 편집 화면 `Controllers.ButtonLayoutController` (ScreenGui ButtonLayoutEditor, DisplayOrder 60): 버튼마다 금색 둥근 손잡이(고르면 진하게 깜빡 + 이름), 끌면 옮김(6px 넘게 움직여야 끌기, 화면 밖으로 안 나감), 화면 전체 투명 판(Active)이 입력을 막아 공격·이동·카메라가 안 움직임 + 화면 가장자리 금색 테두리. 가운데 위 패널(▼로 아래로 옮김): 모든 버튼 −/+ (70~150%), 고른 버튼 −/+ (60~200%, 10%씩), 기본값으로·취소·저장. 패널은 손가락 크기 기준 배율(화면 높이/420, 0.75~1.3).
  - Studio 전용 테스트: `LocalPlayer.ButtonLayoutDebug` (BindableFunction: open/select/move/scale/buttonScale/reset/cancel/save/state). 기기 시뮬레이터에서는 user_mouse_input 좌표가 어긋나서 이것으로 테스트함.
- 적용 `Shared.UI.ButtonLayout`: `container(frame)`(모바일 전투 버튼 틀, 전체 배율) · `register(id, handle, object?)`. 자리·배율은 화면에 그려진 값을 읽지 않고 설정값으로 계산(Roblox 신호 지연 때문에 접속 직후·배율 바꾼 직후 읽은 값이 틀려서 버튼이 화면 밖으로 나가던 버그 고침).
  - `Shared.UI.ScreenFit.hud`: 속성 `LayoutScale`(배율 곱)·`LayoutPos`(ScreenGui 비율 자리) 반영, 제자리를 속성 `FitPosition` 으로 남김.
  - 등록: MobileControlsController(attack·jump·dash·skill1~5, 누를 때 줄어드는 반응은 배치 배율 기준) · InventoryView(bag) · RaidMapController(map) · HudMenu(menu = Bar 를 옮기고 MenuButton 이 손잡이). **메뉴를 화면 왼쪽 절반에 두면 오른쪽으로 펼쳐짐**.
  - HudSlideController HUD 목록에 RaidMapButton 추가 (창 열면 지도 버튼도 밀려남).
- 저장 `Services.Settings`: settings 섹션 `layout = { scale, buttons = { [id] = { x, y(버튼 가운데, 화면 비율), s } } }`, 리모트 `setLayout`, 검사 `Shared.Config.ButtonLayoutConfig.sanitize`(모르는 id·범위 밖 값 버림). 불러오기 = SettingsController "get" → `ButtonLayout.load`.
- 번역(ko.tsv): Button Layout·Edit·안내 문구·All Buttons·Tap a button·Save·Menu·Skill %d 등 10개.
- 확인(iPhone 17 Pro 시뮬레이터): 편집 화면 표시, 옮기기(오차 1px)·버튼 130%, 전체 90%/130% 에서도 옮긴 버튼 자리 유지, 저장 → 다시 접속하면 같은 배치(오차 2px), 취소하면 이전 배치, 메뉴 왼쪽 → 오른쪽으로 펼침, 설정 창 "버튼 배치 [편집]" 줄, PC 플레이 오류 없음. 테스트 계정 배치는 기본값으로 저장해 둠. **실제 손가락 끌기는 시뮬레이터 마우스 좌표 문제로 못 해 봄 → 실기기 확인 필요.**
- 알려진 점: 창(설정 등)을 열 때 HudSlide 가 전투 버튼 틀을 밀어내는데, 틀에서 멀리 옮긴 버튼(예: 왼쪽 아래로 옮긴 공격)은 덜 밀려 창 뒤에 흐리게 보임. 스킬 칸은 지금 이름 글자 — 사용자가 나중에 아이콘을 넣을 예정(배치 기능과 무관).
- 게시 필요: **Shared**(ScreenFit·HudMenu·ButtonLayout·ButtonLayoutConfig·LanguageData) · **Services**(Settings) · **Controllers**(ButtonLayoutController·SettingsController·MobileControlsController·InventoryController.InventoryView·RaidMapController·HudSlideController).

### 핑 + 튜토리얼 핑 단계 (2026-11-26, 마을 place 패키지 코드)
- 결정(사용자): **파티원만**(혼자면 나만) · **자동 + 휠** · 표시 = **월드 표시 + 거리, M 지도** (소리·글 알림은 고르지 않음 → 없음) · **레이드에서만**. 이어서 "핑도 튜토리얼에 넣어줘".
- 입력: PC = **마우스 휠 클릭**(마우스 자리, 시프트 락이면 화면 가운데), 0.25초 넘게 누르면 휠 → 마우스를 그 방향으로 움직이고 떼기(가운데면 취소). 모바일 = **핑 버튼**(지도 버튼 왼쪽, 과녁 아이콘 + 핑, 버튼 배치 설정 id `ping`), 누르면 조준점 표시 — 조준점은 화면 가로 가운데·세로 38%(정가운데는 3인칭에서 내 발밑이라).
- 휠: 위 적(빨강 X) · 오른쪽 전리품(금색 상자) · 아래 도와줘(주황 !) · 왼쪽 여기로(하늘색 ◆▼). 자동 = 적(workspace.Enemies 안 → 그 적을 따라다님) / 전리품(속성 Crate 또는 E 키 안내가 붙은 것) / 그 외 여기로. 투명 판정 상자는 뚫고 조준.
- 표시(PingController): 머리 위 표시(아이콘 + 찍은 사람 이름 + 거리, 나타날 때 터지는 고리·아이콘 튕김), 바닥 빛기둥 + 퍼지는 원판(적 핑은 머리 위만), 화면 밖이면 가장자리 화살표 + 작은 아이콘. 12초(끝 2초 흐려짐), 한 사람 3개까지. 따라가던 적이 죽으면 그 자리에서 흐려짐. **M 지도**에 종류 색 마름모(RaidMapController).
- 서버 `Services.Ping`: 리모트 PingSend/PingShow, 검사 = 종류·위치(내 캐릭터에서 500 안)·대상(Enemies 모델만)·연타(0.35초, 3초에 4번). 받는 사람 = 나 + 같은 PartyId. `Ping.onSent(fn)`. 설정 `Shared.Config.PingConfig`.
- **튜토리얼**: 지도(8) → **핑(9) "핑을 찍어 보세요"** → 탈출(10). PC 는 키 그림 "휠" + "마우스 휠을 누르세요"(키 그림 폭은 글자 수에 맞춤), 모바일은 핑 버튼에 금색 테두리 + "핑을 누르세요" 말풍선(지도 단계와 같은 함수 `updateButtonGuide`, 버튼을 옮겨도 말풍선이 화면 안쪽으로). 레이드 입장 시 지도 없는 레이드면 핑 단계부터. 핑 단계에서 탈출해도 보상 인정.
- Studio 테스트: Workspace 속성 `PingTest = true` 면 마을에서도 핑이 켜짐(Studio 만), `LocalPlayer.PingDebug`(auto/send/wheel/close/count). **Studio 화면 캡처에는 BillboardGui(머리 위 표시)가 안 찍힘** → 표시 모양은 화면 UI 에 복사해 확인했음.
- 확인: PC — 자동 핑(앞쪽 바닥, 빛기둥·원판), 아이콘 3종 모양, 휠(한국어, 고른 칸 강조), 튜토리얼 9/10 패널, 핑 찍으면 서버가 extract 로 넘김, M 지도에 핑 점. 모바일(iPhone 17 Pro) — 핑 버튼 자리(지도 왼쪽, 겹침 없음), 튜토리얼 말풍선, 조준점. 오류 없음. 테스트 뒤 튜토리얼 done, PingTest 속성·지도 테스트 줄 제거, 시뮬레이터 끔.
- **못 해 본 것**: 실제 레이드에서 2인 파티로 상대 화면에 보이는지, 진짜 마우스 휠 클릭·손가락 길게 누르기(테스트 도구가 휠 버튼·터치를 못 보냄), 실제 적·상자에 자동 분류.
- 게시 필요: **Shared**(PingConfig·ButtonLayoutConfig·TutorialConfig·LanguageData) · **Services**(Ping·Tutorial) · **Controllers**(PingController·RaidMapController·HudSlideController·TutorialController).

### 핑을 M 지도에서만 찍게 변경 + 튜토리얼 "탈출구에 핑" (2026-11-26, 완료)
- 사용자: "M을 눌러서 핑을 찍으려 했다" → 결정: **지도 핑만**(마우스 휠 클릭·모바일 핑 버튼·조준점 없앰), 튜토리얼 핑 단계 = **지도에서 탈출구를 눌러 핑**. (위 "핑" 절의 입력 설명은 이것으로 대체)
- 지도(RaidMapController): 지도 판 위 투명 버튼 PingArea(**Modal** → 시프트 락에서도 마우스 풀림)를 누르면 → 탈출구 표시 22px 안이면 **탈출구 핑**(초록 원 + 문, 위치 = Gate), 아니면 지도 좌표 → 월드 X·Z + 위(3000)에서 아래로 광선(플레이어·투명 판정 제외)으로 높이 → **여기로 핑**. 길게(0.25초) 누르면 휠(적·전리품·도와줘·여기로). 지도 아래 왼쪽 "클릭해서 핑 · 길게 누르면 더 보기"(터치는 "눌러서…"). 지도 닫히면 누르던 것 취소. 터치: 닫기 버튼 Closer 를 지도 판 아래(ZIndex 0)로 → **지도 밖을 눌러 닫기**.
- 튜토리얼 핑 단계(9/10) "탈출구에 핑을 찍으세요": 키 그림 M + "지도를 여세요", 모바일은 지도 버튼을 가리킴. 지도를 열면 위에 "탈출구를 클릭해(눌러) 핑을 찍으세요" + 탈출구 표시가 두근거림(플레이어 속성 TutorialStep == "ping"). 서버는 **kind "exit" 핑일 때만** 다음 단계.
- 서버 Ping: kind "exit" 은 열린 탈출구 Gate 30스터드(평면) 안이면 문 자리로, 아니면 move. MAX_DISTANCE 5000 (지도 핑은 멀리 찍힘).
- 지운 것: PingController 의 휠 클릭·핑 버튼·조준점, ButtonLayoutConfig "ping", HudSlide PingButton, 번역 Tap ping/Click the mouse wheel/Wheel.
- 확인(PC, 실제 마우스 클릭): 가짜 탈출구(ModelStreamingMode Persistent 필요 — 아니면 먼 Gate 가 스트리밍 안 됨)를 클릭 → 탈출구 핑 + 튜토리얼 ping → extract. 지도 안내 한국어. 모바일(iPhone 17 Pro): 튜토리얼이 지도 버튼을 가리킴, 지도 안내·"지도 밖을 눌러 닫기". 오류 없음. 테스트 뒤 튜토리얼 done, PingTest·지도 테스트 줄·가짜 탈출구 제거, 시뮬레이터 끔.
- 못 해 본 것: 실제 레이드 2인 파티로 상대에게 보이는지, 손가락 길게 누르기(시뮬레이터 좌표 문제).
- 게시 필요: **Shared**(PingConfig·ButtonLayoutConfig·TutorialConfig·LanguageData) · **Services**(Ping·Tutorial) · **Controllers**(PingController·RaidMapController·HudSlideController·TutorialController) — 앞 절들(버튼 배치·핑) 게시 목록과 합쳐서 세 패키지 모두.

### 공장 복귀 포탈 · 도착 자리 · 물 속 감속 (2026-11-26)
- 사용자: "공장에 복귀하는 텔포가 없어 상가맵이랑 똑같은 구조로 / 공장 이동 시 랜덤이지만 주변에 몬스터 없게, 보스룸 안으로 가는 것 지양 / 물에서 이동속도 15% 느리게".
- **복귀 포탈 원인**: 탈출구·도착 마을행 포탈은 `ServerStorage/TownPortalTemplate` 을 복제해서 만드는데 **공장 place 에 템플릿이 없었음** → 탈출구 3개·도착 포탈이 하나도 안 생겼음. 상가 place 의 템플릿(파트 5: Base·PillarL·PillarR·Lintel(Basalt 38,28,28)·Gate(Neon 90,170,230, 투명 0.15) + PointLight + "Return to City" 빌보드 + ReturnPrompt E 5초 14스터드)을 속성 그대로 읽어 **공장 ServerStorage 에 똑같이 다시 만듦**. 확인(공장 플레이): RaidExit A(-1230,1561)·B(-42,1230)·C(-1220,400) + 도착 포탈 생김.
- **도착 자리** (`Services.Raid` blockedSpot/randomSpawn, `RaidConfig.SPAWN`): RaidSpawns 후보 중 ① Workspace/**RaidNoSpawn** 파트(상자) 안 ② 살아 있는 몬스터(workspace.Enemies) **MONSTER_CLEAR 80** 안 ③ 보스(속성 Boss) **BOSS_CLEAR 320** 안 을 빼고 고름. 모두 걸리면 경고 + 예전처럼. RaidNoSpawn 은 게임에서 숨김(hideMarkers).
  - 공장 조사: 도착 자리 21곳·SpawnLocation 21곳 중 보스 마당(BossYard_01, 가운데 -881,1433, 286×287) **안에 있는 것은 없음**. 보스(foreman -879,1450) 가까운 곳: Spawn_D2 211(마당 남쪽 인도), N2 250, N1 278, N3 298 → BOSS_CLEAR 320 으로 빠짐. 공장 Workspace/RaidNoSpawn/BossYard 상자(마당 +60 여유, 높이 200, 빨간 ForceField 0.85 — 편집 중에만 보임) 추가.
  - ⚠ 몬스터 80 은 실제 공장 배치(31지점 67마리)에서 몇 곳이 남는지 **확인 못 함** (패키지 게시 전이라 공장에서 새 코드가 안 돎). 너무 많이 걸리면 MONSTER_CLEAR 를 낮출 것.
- **물 속 −15%** (`Services.Movement`, `MovementConfig.WATER_SPEED_MULT 0.85 / WATER_CHECK 0.2`): 0.2초마다 발이 지형 물 복셀(4스터드)·Water 재질 파트에 잠기거나 수영 중이면 캐릭터 속성 **WaterSpeedMult** = 0.85 → applySpeed 에 곱함, 클라이언트 AttackSlow 도 같은 계산. 모든 레이드 맵 공통. 공장 운하는 지형 물(높이 -12~0). 확인(마을, 물 재질 파트): 걷기 13 → 11.05 → 벗어나면 13.
- 게시 필요: **공장 place**(ServerStorage.TownPortalTemplate, Workspace.RaidNoSpawn — 사용자가 공장 place 를 게시) + **Shared**(RaidConfig·MovementConfig) · **Services**(Raid·Movement) · **Controllers**(CombatController.AttackSlow).
- (추가, 2026-11-26) 사용자 "포탈 이동시간 10초, 범위 1.5배" → `RaidConfig.EXIT.STAND` 15 → **10**초, `EXIT.RADIUS` 10 → **15** (바닥 원판·판정·탈출 타이머 표시 모두 이 값을 읽음, 모든 레이드 맵 공통). 도착 마을행 포탈의 E키 5초는 그대로. 게시: **Shared**(RaidConfig).
