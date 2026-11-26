--!strict
-- 언어 데이터 (자동 생성 — 직접 고치지 말 것). 원본: 저장소 scripts/lang/ko.tsv → build_language_data.py
-- 아래 SOURCE 는 TSV 원문 (키 | 영어 | 한국어). 키가 '-' 이면 "## 구역" + 영어 단어로 키를 만든다.
-- 돌려줌: { names = { en, ko }, entries = { [키] = { en = 영어, ko = 한국어 } } }. 영어·한국어가 같은 키를 쓴다.
-- 쓰는 곳: Controllers.LanguageController. 형식 문구 규칙은 그쪽 머리말 참고.

local SOURCE = [==[
## Common
- | %s: %s | %s: %s
- | %s · %s | %s · %s
- | %s  ·  %s | %s  ·  %s
- | %s / %s | %s / %s
- | %s x%d | %s x%d
- | %s +%d | %s +%d
- | +%d %s | +%d %s
- | Close | 닫기
- | Cancel | 취소
- | Max | 최대
- | Back | 뒤로
- | Confirm | 확인
- | ON | 켜짐
- | OFF | 꺼짐
- | None | 없음
- | Nothing. | 없음.
- | Working... | 작업 중...
- | Not enough gold. | 골드가 부족합니다.
- | Something went wrong. | 문제가 생겼습니다.
- | Something went wrong. Please try again. | 문제가 생겼습니다. 다시 시도해 주세요.
- | Could not reach the server. | 서버에 연결할 수 없습니다.
- | Invalid request. | 잘못된 요청입니다.
- | Slow down. | 조금 천천히 해 주세요.
- | Already full. | 이미 가득 찼습니다.
- | Already claimed. | 이미 받았습니다.
- | Already completed. | 이미 완료했습니다.
## Terms
- | Inventory | 인벤토리
- | Equipment | 장비
- | Equip | 장착
- | Unequip | 장착 해제
- | Equipped | 장착 중
- | Drop | 버리기
- | Use | 사용
- | Weapon | 무기
- | Weapons | 무기
- | Armor | 방어구
- | Relic | 성유물
- | Relics | 성유물
- | Material | 재료
- | Materials | 재료
- | Consumable | 소모품
- | Supplies | 보급품
- | Other | 기타
- | Item | 아이템
- | Items | 아이템
- | Bag | 가방
- | Backpack | 가방
- | Character | 캐릭터
- | Item Info | 아이템 정보
- | Level | 레벨
- | Item Level | 아이템 레벨
- | Health | 체력
- | Max Health | 최대 체력
- | Stamina | 기력
- | Sanity | 정신력
- | Sanity Cost | 정신력 소모
- | Defense | 방어력
- | Damage | 피해
- | Element | 속성
- | Grade | 등급
- | Trait | 특성
- | Traits | 특성
- | Unique | 고유
- | Unique Trait | 고유 특성
- | Ability | 능력
- | Original Ability | 원본 능력
- | Socket | 소켓
- | Sockets | 소켓
- | Skill | 스킬
- | Recipe | 제작법
- | Blueprint | 설계도
- | Learn | 배우기
- | Learned | 배움
- | Owned | 보유
- | Status | 상태
- | Original | 원본
- | Extracted | 추출됨
- | Destroyed | 파괴됨
- | Lost | 사라짐
- | Kept | 유지
- | Keep | 유지
- | New | 새로
- | Replaced | 교체됨
- | Target | 대상
- | Compare | 비교
- | Description | 설명
- | Chance | 확률
- | Success | 성공
- | Fail | 실패
- | Limit | 한도
- | Cost | 비용
- | Total | 합계
- | Amount | 수량
- | Reward | 보상
- | Rewards | 보상
- | Guide | 안내
- | Summary | 요약
- | Add | 추가
- | Add All | 모두 추가
- | Remove | 빼기
- | Clear | 비우기
- | Sort | 정렬
- | Pick | 선택
- | Check | 확인
- | Open | 열림
- | Next | 다음
- | Locked | 잠김
- | Available | 입장 가능
- | Map | 지도
- | Boss | 보스
- | Players | 인원
- | Monsters | 몬스터
- | Experience | 경험치
- | Result | 결과
- | Continue | 계속
- | Party | 파티
- | Me | 나
- | Settings | 설정
- | Language | 언어
- | Upgrade | 업그레이드
- | Upgrades | 업그레이드
- | Contract | 의뢰
- | Contracts | 의뢰
- | Archive | 도감
- | Collection | 수집
- | Enemies | 적
- | Merchant | 상인
- | Blacksmith | 대장장이
- | Storage | 보관함
- | Buy | 구매
- | Sell | 판매
- | Craft | 제작
- | Enhance | 강화
- | Enhanced | 강화됨
- | Awaken | 각성
- | Absorb | 흡수
- | Transplant | 이식
- | Dismantle | 분해
- | Expand | 확장
- | Exchange | 교환
- | Shards | 파편
- | Stone | 각성석
- | Gear | 장비
- | Dash | 대시
- | Sprint | 달리기
- | Attack | 공격
- | ATK | 공격
- | Jump | 점프
- | Pick up | 줍기
- | Search | 뒤지기
- | Common | 일반
- | Uncommon | 고급
- | Rare | 희귀
- | Epic | 영웅
- | Legendary | 전설
- | Deicide | 신살
- | Divine | 신성
- | Steel | 강철
- | Holy | 성스러움
- | Earth | 대지
- | Dagger | 단검
- | Polearm | 창
- | OneHanded | 한손 무기
- | TwoHandedLight | 양손 경량 무기
- | TwoHandedHeavy | 양손 중량 무기
- | Gold | 골드
- | Crystal | 크리스탈
- | Gold x%d | 골드 x%d
- | %d Gold | 골드 %d
- | %d XP | 경험치 %d
- | %d Crystal | 크리스탈 %d
- | +%d Crystal | 크리스탈 +%d
- | %s XP | 경험치 %s
- | XP +%d%% | 경험치 +%d%%
- | Space Distortion | 공간 왜곡
## Status
- | Bleed | 출혈
- | Infection | 감염
- | Slow | 둔화
- | Freeze | 빙결
- | Stun | 기절
- | Rooted | 속박
- | Frozen | 얼어붙음
- | Stunned | 기절
## UI.Inventory
- | This socket is locked. | 이 소켓은 잠겨 있습니다.
- | Select an item to inspect. | 살펴볼 아이템을 선택하세요.
- | Relic Sockets | 성유물 소켓
- | Select a destination (same slot cancels) | 옮길 곳을 선택하세요 (같은 칸을 누르면 취소)
- | SAFE POUCH %d/%d  ·  KEPT ON DEATH | 안전 주머니 %d/%d  ·  사망 시 유지
- | UNSECURED %d  ·  LOST ON DEATH | 미확보 %d  ·  사망 시 잃음
- | Socket %d | 소켓 %d
- | SOCKET %d | 소켓 %d
- | Escape to secure | 탈출해야 확보됩니다
- | Empty | 비어 있음
- | EMPTY  %d | 빈 칸  %d
- | Drop Item | 아이템 버리기
- | %s (You have %d) | %s (보유 %d)
- | LV x%.2f | 레벨 x%.2f
- | ENH x%.2f | 강화 x%.2f
- | GRADE x%.2f | 등급 x%.2f
- | TRAITS  %d / %d | 특성  %d / %d
- | ABILITIES  %d / %d | 능력  %d / %d
- | ABILITIES  %d / 2 | 능력  %d / 2
- | Empty slot | 빈 칸
- | LEVEL UP!  LV %d | 레벨 업!  LV %d
- | HEALTH  %s / %s | 체력  %s / %s
- | STAMINA  %d / %d | 기력  %d / %d
- | SANITY  %d / %d | 정신력  %d / %d
- | LV %d  ·  XP %s / %s | LV %d  ·  경험치 %s / %s
- | LV %d  ·  MAX | LV %d  ·  최대
- | Locked socket | 잠긴 소켓
- | Unsecured ×%d | 미확보 ×%d
- | Closing... | 닫히는 중...
- | %s  -  STAGGERED | %s  -  무력화
## UI.Contracts
- | The contract board is not available. | 지금은 의뢰 게시판을 쓸 수 없습니다.
- | The contract board is only in town. | 의뢰 게시판은 마을에만 있습니다.
- | Contracts refresh every day. Hunts and extractions count in raids; bring deliveries here. | 의뢰는 매일 바뀝니다. 사냥·탈출 의뢰는 레이드에서 진행되고, 납품 의뢰는 여기로 가져오세요.
- | Daily | 일일
- | NEW CONTRACTS IN %dH %dM | 새 의뢰까지 %d시간 %d분
- | NEW CONTRACTS IN %dM | 새 의뢰까지 %d분
- | Completed | 완료
- | Ready | 보상 가능
- | Delivered | 납품 완료
- | IN BAG  %s | 가방에  %s
- | In Bag | 가방 보유
- | Kills | 처치
- | Extractions | 탈출
- | Turn In | 납품
- | Not Enough | 부족
- | Claim Reward | 보상 받기
- | In Progress | 진행 중
- | Hunt | 사냥
- | Delivery | 납품
- | Extract | 탈출
- | Shop | 상가
- | Dungeon | 던전
## UI.Blacksmith
- | You do not have this blueprint. | 이 설계도를 가지고 있지 않습니다.
- | Blueprint learned. You can craft it now. | 설계도를 배웠습니다. 이제 제작할 수 있습니다.
- | Could not learn this blueprint. | 이 설계도를 배울 수 없습니다.
- | COST  ·  %s | 비용  ·  %s
- | Drop on DONOR or RECEIVER. | 제공 칸이나 수령 칸에 놓으세요.
- | Choose two weapons or two armor pieces. | 무기 두 개 또는 방어구 두 개를 고르세요.
- | Equipped items cannot be given. | 장착한 아이템은 줄 수 없습니다.
- | This weapon has no traits to give. | 이 무기에는 줄 특성이 없습니다.
- | DONOR  ·  DESTROYED | 제공  ·  파괴됨
- | Donor | 제공
- | Equipment to give | 줄 장비
- | Receiver | 수령
- | Your equipment | 내 장비
- | %s  ·  EQUIPPED | %s  ·  장착 중
- | Pick a slot | 칸 선택
- | → SLOT %d | → %d번 칸
- | Click to replace | 눌러서 교체
- | Click to place | 눌러서 배치
- | Not allowed | 불가
- | SLOT %d  ·  %s | %d번 칸  ·  %s
- | EXTRACTED  ·  CANNOT MOVE | 추출됨  ·  이동 불가
- | ORIGINAL  ·  LOCKED | 원본  ·  잠김
- | %s will be destroyed. Unmoved abilities are lost. | %s은(는) 파괴됩니다. 옮기지 않은 능력은 사라집니다.
- | %s will be destroyed. Unmoved traits are lost. | %s은(는) 파괴됩니다. 옮기지 않은 특성은 사라집니다.
- | will be destroyed. Unmoved abilities are lost. | 은(는) 파괴됩니다. 옮기지 않은 능력은 사라집니다.
- | will be destroyed. Unmoved traits are lost. | 은(는) 파괴됩니다. 옮기지 않은 특성은 사라집니다.
- | %d MOVING%s | {1}개 이동{2}
- | ·  %d LOST | ·  {1}개 사라짐
- | Drag equipment into DONOR and RECEIVER. | 장비를 제공 칸과 수령 칸에 끌어다 놓으세요.
- | Click the hammer again to transplant. | 망치를 한 번 더 누르면 이식합니다.
- | Drag another armor piece into DONOR. | 다른 방어구를 제공 칸에 끌어다 놓으세요.
- | Drag a weapon with traits into DONOR. | 특성이 있는 무기를 제공 칸에 끌어다 놓으세요.
- | Drag your armor into RECEIVER. | 방어구를 수령 칸에 끌어다 놓으세요.
- | Drag your weapon into RECEIVER. | 무기를 수령 칸에 끌어다 놓으세요.
- | Pick a slot on the right. | 오른쪽에서 칸을 고르세요.
- | Pick the original ability, then slot 2. Click it again to undo. | 원본 능력을 고른 뒤 2번 칸을 고르세요. 다시 누르면 취소됩니다.
- | Pick a trait, then a slot. Click a filled slot to undo. | 특성을 고른 뒤 칸을 고르세요. 채워진 칸을 누르면 취소됩니다.
- | Godscar Pearl | 신흔 진주
- | Learning... | 배우는 중...
- | %s  ·  LV %d  ·  DEFENSE %d  ·  HEALTH +%d | %s  ·  LV %d  ·  방어력 %d  ·  체력 +%d
- | %s  ·  LV %d  ·  DAMAGE %d | %s  ·  LV %d  ·  피해 %d
- | %s  ·  LV %d | %s  ·  LV %d
- | WEAPONS\nONLY | 무기\n전용
- | Click LEARN twice to learn this recipe (uses 1 blueprint). | 배우기를 두 번 누르면 이 제작법을 배웁니다 (설계도 1개 사용).
- | Click LEARN again to learn. | 배우기를 한 번 더 누르세요.
- | Select an armor | 방어구 선택
- | Select a weapon | 무기 선택
- | Select an item | 아이템 선택
- | Select two items | 아이템 두 개 선택
- | Select a relic | 성유물 선택
- | Missing materials | 재료 부족
- | %s PEARL | %s 진주
- | No pearl | 진주 없음
- | Pearl | 진주
- | Click the pearl slot to add a random trait (optional). | 진주 칸을 누르면 무작위 특성을 더할 수 있습니다 (선택).
- | Click the hammer twice to craft. | 망치를 두 번 누르면 제작합니다.
- | Click the hammer again to craft. | 망치를 한 번 더 누르면 제작합니다.
- | No recipes yet. Find blueprints in raids and use them to learn. | 아직 아는 제작법이 없습니다. 레이드에서 설계도를 찾아 사용하면 배울 수 있습니다.
- | Pick an armor on the left. | 왼쪽에서 방어구를 고르세요.
- | Pick a weapon on the left. | 왼쪽에서 무기를 고르세요.
- | Not enough materials. | 재료가 부족합니다.
- | Click the hammer again to enhance. | 망치를 한 번 더 누르면 강화합니다.
- | Click the hammer twice to enhance. | 망치를 두 번 누르면 강화합니다.
- | CHANCE  ·  +%d → +%d | 확률  ·  +%d → +%d
- | LEVEL  +%d / +%d | 강화 단계  +%d / +%d
- | AWAKEN TO UNLOCK +%d | 각성하면 +%d 해금
- | +%d%%  PER LEVEL | 단계당  +%d%%
- | Max Level | 최대 단계
- | %s limit +%d. Awaken to raise it. | %s 한도 +%d. 각성하면 한도가 오릅니다.
- | Max level reached. | 최대 단계에 도달했습니다.
- | Fails from this level can drop a level. | 이 단계부터는 실패하면 단계가 내려갈 수 있습니다.
- | Click the hammer again to awaken. | 망치를 한 번 더 누르면 각성합니다.
- | Click the hammer twice to awaken. | 망치를 두 번 누르면 각성합니다.
- | Drag a weapon or armor into the slot. | 무기나 방어구를 칸에 끌어다 놓으세요.
- | %s  ·  MAX GRADE | %s  ·  최고 등급
- | Max Grade | 최고 등급
- | +%d kept | +%d 유지
- | UPGRADE | 상승
- | No change | 변화 없음
- | Highest grade reached. | 최고 등급에 도달했습니다.
- | Not enough %s. | %s이(가) 부족합니다.
- | Drop outside the slot to remove it. | 칸 밖에 놓으면 빠집니다.
- | Drop on the slot to %s it. | 칸에 놓으면 %s합니다.
- | This weapon cannot go here. | 이 무기는 여기에 놓을 수 없습니다.
- | Drag a weapon into the slot. | 무기를 칸에 끌어다 놓으세요.
- | No weapon | 무기 없음
- | BEFORE  →  AFTER | 이전  →  이후
- | Drop on FEED or TARGET. | 재료 칸이나 대상 칸에 놓으세요.
- | Drag your weapon or armor into TARGET. | 무기나 방어구를 대상 칸에 끌어다 놓으세요.
- | Click the hammer again to absorb. | 망치를 한 번 더 누르면 흡수합니다.
- | Click the hammer twice to absorb. | 망치를 두 번 누르면 흡수합니다.
- | Armor can only absorb armor. | 방어구는 방어구만 흡수할 수 있습니다.
- | Weapons can only absorb weapons. | 무기는 무기만 흡수할 수 있습니다.
- | Equipped items cannot be absorbed. | 장착한 아이템은 흡수할 수 없습니다.
- | Remove the relics first. | 먼저 성유물을 빼세요.
- | Needs an item level above %d. | 아이템 레벨이 %d보다 높아야 합니다.
- | You must be level %d to absorb this item. | 이 아이템을 흡수하려면 레벨 %d이 필요합니다.
- | FEED  ·  DESTROYED | 재료  ·  파괴됨
- | Feed | 재료
- | Item to absorb | 흡수할 아이템
- | Your item | 내 아이템
- | ITEM LEVEL  %d → %s / %d | 아이템 레벨  %d → %s / %d
- | ITEM LEVEL  %d / %d | 아이템 레벨  %d / %d
- | YOUR LEVEL %d  ·  FEED LIMIT | 내 레벨 %d  ·  재료 한도
- | Req. Level | 필요 레벨
- | Lost with feed | 재료와 함께 사라짐
- | Nothing else is lost. | 그 밖에 잃는 것은 없습니다.
- | Target keeps its grade and abilities. | 대상은 등급과 능력을 유지합니다.
- | Target keeps its grade, enhance and traits. | 대상은 등급, 강화, 특성을 유지합니다.
- | LV %d → %d | LV %d → %d
- | Drag a higher-level armor into FEED. | 레벨이 더 높은 방어구를 재료 칸에 끌어다 놓으세요.
- | Drag a higher-level weapon into FEED. | 레벨이 더 높은 무기를 재료 칸에 끌어다 놓으세요.
- | Click the hammer again to dismantle. | 망치를 한 번 더 누르면 분해합니다.
- | Click the hammer twice to dismantle. | 망치를 두 번 누르면 분해합니다.
- | Equipped items cannot be dismantled. | 장착한 아이템은 분해할 수 없습니다.
- | %s items cannot be dismantled. | %s 아이템은 분해할 수 없습니다.
- | Drop outside the queue to remove it. | 목록 밖에 놓으면 빠집니다.
- | Drop on the queue. | 분해 목록에 놓으세요.
- | QUEUE  %d | 분해 목록  %d
- | Queue | 분해 목록
- | Queued | 대기 중
- | ADD ALL  ·  +%d, NO TRAITS | 모두 추가  ·  +%d, 특성 없음
- | You get | 얻는 것
- | Check before | 확인하세요
- | %d DESTROYED | {1}개 파괴
- | %d item%s (up to +%d) | {1}개 (최대 +{3})
- | With traits | 특성 있음
- | %d item%s | {1}개
- | No enhanced or traited items. | 강화했거나 특성이 있는 아이템은 없습니다.
- | Move traits or abilities with Transplant first. | 특성이나 능력은 먼저 이식으로 옮기세요.
- | DISMANTLE  ·  %d ITEM%s | 분해  ·  {1}개
- | →  %d %s%s | →  {2} x{1}
- | Drag weapons or armor into the queue. | 무기나 방어구를 분해 목록에 끌어다 놓으세요.
## UI.Relic
- | %s  ·  %d/%d SOCKETS | %s  ·  소켓 %d/%d
- | No open sockets. Expand them in the EXPAND tab. | 열린 소켓이 없습니다. 확장 탭에서 소켓을 여세요.
- | Click a relic to socket it. Click a socketed relic to remove it. | 성유물을 누르면 소켓에 끼웁니다. 끼운 성유물을 누르면 뺍니다.
- | Hover a relic. | 성유물에 마우스를 올려 보세요.
- | SANITY -%d | 정신력 -%d
- | Choose a weapon first. | 먼저 무기를 고르세요.
- | No empty socket. Expand sockets in the EXPAND tab. | 빈 소켓이 없습니다. 확장 탭에서 소켓을 늘리세요.
- | Click the hammer again to open a socket. | 망치를 한 번 더 누르면 소켓을 엽니다.
- | Click the hammer twice to open a socket. | 망치를 두 번 누르면 소켓을 엽니다.
- | %s  ·  %d/%d MAX | %s  ·  %d/%d 최대
- | Max Sockets | 최대 소켓
- | All sockets are open. | 모든 소켓이 열렸습니다.
- | FITS: %s | 장착 가능: %s
- | FITS: ANY WEAPON | 장착 가능: 모든 무기
- | No relic | 성유물 없음
- | Pick a relic on the left to forge it from Relic Shards. | 왼쪽에서 성유물을 고르면 성유물 파편으로 만들 수 있습니다.
- | %d RELIC SHARDS  →  %s | 성유물 파편 %d개  →  %s
- | 1 RELIC | 성유물 1개
- | Pick a relic to forge. | 만들 성유물을 고르세요.
- | Not enough Relic Shards. | 성유물 파편이 부족합니다.
- | Click the hammer again to forge the relic. | 망치를 한 번 더 누르면 성유물을 만듭니다.
- | Click the hammer twice to forge the relic. | 망치를 두 번 누르면 성유물을 만듭니다.
## UI.Settings
- | Control | 조작
- | Click a key, then press the new key. Esc cancels. | 키 칸을 누른 뒤 새 키를 누르세요. Esc를 누르면 취소됩니다.
- | Press Key | 키 입력
- | Could not save. Try again. | 저장하지 못했습니다. 다시 시도하세요.
- | Relic Skills | 성유물 스킬
- | Display | 화면
- | My Overhead Bar | 내 머리 위 체력바
- | Screen Shake | 화면 흔들림
- | Reset Default | 기본값으로
- | Button Layout | 버튼 배치
- | Edit | 편집
- | Drag a button to move it. Tap one to change its size. | 버튼을 끌어서 옮기세요. 버튼을 누르면 크기를 바꿀 수 있습니다.
- | All Buttons | 모든 버튼
- | Tap a button | 버튼을 누르세요
- | Reset to default. Press Save to keep it. | 기본 배치로 되돌렸습니다. 저장을 눌러야 유지됩니다.
- | Button layout saved. | 버튼 배치를 저장했습니다.
- | Save | 저장
- | Menu | 메뉴
- | Skill %d | 스킬 %d
- | Ping | 핑
- | Go here | 여기로
- | Enemy | 적
- | Loot | 전리품
- | Need help | 도와줘
- | Exit | 탈출구
- | %s can't be used. Use A-Z (not WASD, Q, E, C, B, P, J, I, O) or 5-0. | %s 키는 쓸 수 없습니다. A-Z(WASD, Q, E, C, B, P, J, I, O 제외)나 5-0을 쓰세요.
## UI.Party
- | In Combat | 전투 중
- | MEMBERS  %d / %d | 파티원  %d / %d
- | No party yet. Invite a player from the list. Two members earn XP +10%. | 아직 파티가 없습니다. 목록에서 플레이어를 초대하세요. 2명이면 경험치 +10%.
- | Make Leader | 파티장 넘기기
- | Alive | 생존
- | In Party | 파티 중
- | Invite | 초대
- | No friends on this server. | 이 서버에 친구가 없습니다.
- | No other players found. | 다른 플레이어가 없습니다.
- | Waiting for %s...  %ds | %s 님의 응답을 기다리는 중...  %d초
- | %s (@%s) invited you to a party.  %ds | %s (@%s) 님이 파티에 초대했습니다.  %d초
- | Message your party... | 파티에 메시지 보내기...
- | Join a party to chat. | 파티에 들어가면 대화할 수 있습니다.
- | Leave | 나가기
- | Disband | 해산
- | Party Chat | 파티 채팅
- | Send | 보내기
- | Invite Players | 플레이어 초대
- | All | 전체
- | Friends | 친구
- | Search name or display name | 이름 또는 표시 이름 검색
- | Accept | 수락
- | Decline | 거절
## UI.Raid
- | Requirements | 조건
- | Raid Time | 레이드 시간
- | PvP | PvP
- | Enter | 입장
- | Coming Soon | 준비 중
- | %d+   (YOU %d) | %d+   (나 %d)
- | %d MIN | %d분
- | UP TO %d | 최대 %d명
- | This zone is not open yet. | 아직 열리지 않은 구역입니다.
- | Die and you lose everything in your bag. | 죽으면 가방에 든 것을 모두 잃습니다.
- | Reach level %d to enter. | 레벨 %d부터 입장할 수 있습니다.
- | Escaped | 탈출 성공
- | Secured Loot | 확보한 전리품
- | Secured loot is now in your bag. | 확보한 전리품이 가방에 들어왔습니다.
- | Nothing new this time. | 이번에는 새로 얻은 것이 없습니다.
- | Killed in Action | 전사
- | Lost Loot | 잃은 전리품
- | Your equipped gear was kept. | 장착한 장비는 지켰습니다.
- | Nothing was lost. | 잃은 것이 없습니다.
- | Missing in Action | 실종
- | KEPT  ·  SAFE POUCH | 유지  ·  안전 주머니
- | You made it out alive. | 살아서 빠져나왔습니다.
- | Killed by %s. | %s에게 당했습니다.
- | Killed by %s | %s에게 사망
- | You were killed. | 사망했습니다.
- | Time ran out before you reached an exit. | 출구에 닿기 전에 시간이 다 됐습니다.
- | You left the raid before escaping. | 탈출하기 전에 레이드를 떠났습니다.
- | Raid Report | 레이드 결과
- | %s    SURVIVED %s | %s    생존 시간 %s
- | %d min | %d분
- | Up to %d players | 최대 %d명
- | Tip | 팁
- | Loading | 불러오는 중
- | No Revives Left | 남은 부활 없음
- | Too Late to Revive | 부활하기엔 늦었습니다
- | REVIVE  %d R$ | 부활  %d R$
- | Return to Lobby | 로비로 돌아가기
- | Returning to lobby... | 로비로 돌아가는 중...
- | Reviving... | 부활하는 중...
- | Revives left: %d   ·   Returning to lobby in %d | 남은 부활: %d   ·   %d초 후 로비로 돌아갑니다
- | DEPARTING  —  %s | 출발  —  %s
- | ARRIVING  —  %s | 도착  —  %s
- | Surface | 지상
- | BUNKER 07  //  SURFACE ACCESS  //  CONVOY 1 | 벙커 07  //  지상 출입구  //  호송대 1
- | CONVOY 1  //  QUARANTINE CHECKPOINT  //  DROP-OFF | 호송대 1  //  검역 검문소  //  하차 지점
- | EXIT %s | 출구 %s
- | Closes in %s | %s 후 닫힘
- | Open until the end · %s | 끝까지 열림 · %s
- | Open until the end | 끝까지 열림
- | EXTRACTING · EXIT %s · %.1fs | 탈출 중 · 출구 %s · %.1f초
- | [M] Close | [M] 닫기
- | Tap to close | 눌러서 닫기
## UI.Merchant
- | The merchant is not here. | 상인이 여기 없습니다.
- | Scrap | 고철
- | Sell List | 판매 목록
- | You can sell up to %d stacks at once. | 한 번에 최대 %d묶음까지 팔 수 있습니다.
- | Drop outside the list to remove it. | 목록 밖에 놓으면 빠집니다.
- | Drop on the sell list. | 판매 목록에 놓으세요.
- | %s EACH | 개당 %s
- | Not for sale. | 팔 수 없습니다.
- | SELL LIST  %d | 판매 목록  %d
- | Nothing selected | 선택한 것 없음
- | Pick an item in the sell list\nto change how many to sell. | 판매 목록에서 아이템을 골라\n팔 개수를 바꾸세요.
- | Subtotal | 합계
- | %d ENHANCED | 강화됨 %d개
- | %d WITH TRAITS | 특성 있음 %d개
- | %d RARE OR HIGHER | 희귀 이상 %d개
- | Nothing valuable in the list. | 목록에 귀한 아이템은 없습니다.
- | Sold items can't be bought back | 판 아이템은 다시 살 수 없습니다
- | SELL  ·  %d ITEM%s | 판매  ·  {1}개
- | Counting coins... | 동전 세는 중...
- | Click the coin again to sell. | 동전을 한 번 더 누르면 팝니다.
- | Click the coin twice to sell. | 동전을 두 번 누르면 팝니다.
- | For Sale | 판매 중
- | RESTOCK IN %d:%02d:%02d | 재입고까지 %d:%02d:%02d
- | RESTOCK IN %02d:%02d | 재입고까지 %02d:%02d
- | Sold Out | 품절
- | %d LEFT | %d개 남음
- | Common · +0 | 일반 · +0
## UI.Storage
- | The storage is not available. | 지금은 보관함을 쓸 수 없습니다.
- | Drop on the storage to store it. | 보관함에 놓으면 보관합니다.
- | Drop on the bag to take it. | 가방에 놓으면 꺼냅니다.
- | Click an item to move the whole stack. Drag it to the other side to move it too. | 아이템을 누르면 한 묶음을 통째로 옮깁니다. 반대쪽으로 끌어서 옮길 수도 있습니다.
- | click to store | 눌러서 보관
- | click to take | 눌러서 꺼내기
- | Capacity | 용량
- | Store Materials | 재료 모두 보관
- | Upgrades are not available. | 지금은 업그레이드를 쓸 수 없습니다.
- | Upgrades are permanent. Materials come from your bag. | 업그레이드는 영구적입니다. 재료는 가방에서 씁니다.
- | Slots | 칸
- | Stacks Kept | 유지되는 묶음
- | Maxed | 최대
- | Fully Upgraded | 업그레이드 완료
## UI.Archive
- | The archive is not available. | 지금은 도감을 쓸 수 없습니다.
- | Craft at the blacksmith (blueprint needed). | 대장장이에게서 제작 (설계도 필요).
- | Craft at the blacksmith. | 대장장이에게서 제작.
- | Not Discovered | 미발견
- | Defeat this enemy to record it. | 이 적을 처치하면 기록됩니다.
- | Obtain this item to record it. | 이 아이템을 얻으면 기록됩니다.
- | FOUND IN  ·  %s | 발견 장소  ·  %s
- | DAMAGE %d  ·  x%s  ·  MAX ENHANCE +%d | 피해 %d  ·  x%s  ·  최대 강화 +%d
- | Obtained | 획득
- | Not Yet Obtained | 미획득
- | Damage at item level 1, +0. | 아이템 레벨 1, +0 기준 피해.
- | No unique ability. | 고유 능력 없음.
- | %s  ·  BODY ARMOR | %s  ·  몸 방어구
- | DEFENSE %d  ·  HEALTH +%d | 방어력 %d  ·  체력 +%d
- | At item level 1. Absorb and awaken to raise them. | 아이템 레벨 1 기준. 흡수와 각성으로 올릴 수 있습니다.
- | LV %d  ·  HEALTH %d%s | LV %d  ·  체력 %d%s
- | ·  BOSS | ·  보스
- | DEFEATED  x%d | 처치  x%d
- | Drops | 드롭
- | New archive entry | 새 도감 기록
- | New archive entry: %s | 새 도감 기록: %s
- | Invalid reward. | 잘못된 보상입니다.
- | Not discovered yet. | 아직 발견하지 않았습니다.
- | The archive is still loading. | 도감을 아직 불러오는 중입니다.
## UI.Intro
- | T A P   T O   S T A R T | 화 면 을   눌 러   시 작
- | P R E S S   A N Y   K E Y   T O   S T A R T | 아 무   키 나   눌 러   시 작
## UI.Tutorial
- | The shelter is safe. The city is not. | 대피소는 안전합니다. 도시는 아닙니다.
- | TUTORIAL  %d/%d | 튜토리얼  %d/%d
- | First Steps | 첫걸음
- | Objective | 목표
- | Press Equip | 장착을 누르세요
- | Click your sword | 검을 누르세요
- | Close to continue | 닫고 계속하기
- | Press Buy | 구매를 누르세요
- | Select the bandage | 붕대를 고르세요
- | Click an item to store it | 아이템을 눌러 보관하세요
- | 3 new contracts every day | 매일 새 의뢰 3개
- | Claim rewards here when done | 완료하면 여기서 보상을 받으세요
- | Press Enter | 입장을 누르세요
- | SELECT %s | %s 선택
- | Complete | 완료
- | Escaped! Return to town to claim your tutorial reward. | 탈출 성공! 마을로 돌아가 튜토리얼 보상을 받으세요.
- | Raid failed. Head out again and reach an exit alive. | 레이드 실패. 다시 출발해 살아서 출구에 도착하세요.
- | +%d Bandage | 붕대 +%d
- | Tutorial complete! | 튜토리얼 완료!
- | Hold Space to skip | 스페이스를 길게 눌러 건너뛰기
- | Skip >> | 건너뛰기 >>
- | Press M | M을 누르세요
- | Tap the map | 지도를 누르세요
- | Tap outside to close | 지도 밖을 눌러 닫기
- | Tap to ping · Hold for more | 눌러서 핑 · 길게 누르면 더 보기
- | Click to ping · Hold for more | 클릭해서 핑 · 길게 누르면 더 보기
- | Tap an exit to ping it | 탈출구를 눌러 핑을 찍으세요
- | Click an exit to ping it | 탈출구를 클릭해 핑을 찍으세요
Tutorial.Equip.Title | Equip your weapon | 무기를 장착하세요
Tutorial.Move.Title | Go to the training dummy | 훈련용 허수아비로 가세요
Tutorial.Move.Text | Hold Shift to sprint. Press Q to dash at least once on the way. | Shift를 누르고 있으면 달립니다. 가는 길에 Q로 대시를 한 번 이상 해 보세요.
Tutorial.Attack.Title | Strike the training dummy | 훈련용 허수아비를 공격하세요
Tutorial.Attack.Text | Click to attack. Keep clicking to chain a combo. | 클릭하면 공격합니다. 계속 클릭하면 연속 공격이 이어집니다.
Tutorial.Buy.Title | Buy a bandage | 붕대를 사세요
Tutorial.Buy.Text | The merchant sells supplies. Buy a Bandage to heal during raids. | 상인은 보급품을 팝니다. 레이드 중 회복할 붕대를 사세요.
Tutorial.Storage.Title | Put an item in storage | 보관함에 아이템을 넣으세요
Tutorial.Storage.Text | Loot found in a raid is lost if you die before escaping. Storage keeps things safe. | 레이드에서 얻은 전리품은 탈출 전에 죽으면 잃습니다. 보관함에 두면 안전합니다.
Tutorial.Board.Title | Check the contract board | 의뢰 게시판을 확인하세요
Tutorial.Board.Text | Contracts change every day and pay extra rewards. Progress counts on its own. | 의뢰는 매일 바뀌고 추가 보상을 줍니다. 진행도는 저절로 올라갑니다.
Tutorial.Depart.Title | Head out on a raid | 레이드에 출발하세요
Tutorial.Depart.Text | Walk to the raid gate and choose Shop District. | 레이드 관문으로 걸어가 상가 거리를 고르세요.
Tutorial.Extract.Title | Escape the raid | 레이드에서 탈출하세요
Tutorial.Extract.Text | Grab loot, then stand in an exit before time runs out. If you die, you lose what you found here. | 전리품을 챙긴 뒤 시간이 끝나기 전에 출구에 서 있으세요. 죽으면 여기서 얻은 것을 잃습니다.
Tutorial.Map.Title | Open the map | 지도를 여세요
Tutorial.Map.Text | Press M to see where you are and where the exits are. | M을 누르면 내 위치와 출구 위치를 볼 수 있습니다.
Tutorial.Map.TouchText | Tap the map button to see where you are and where the exits are. | 지도 버튼을 누르면 내 위치와 출구 위치를 볼 수 있습니다.
Tutorial.Ping.Title | Ping an exit | 탈출구에 핑을 찍으세요
Tutorial.Ping.Text | Open the map and click an exit to ping it. Hold to choose other pings. Your party sees your pings. | 지도를 열고 탈출구를 누르면 핑이 찍힙니다. 누르고 있으면 다른 핑을 고를 수 있습니다. 핑은 파티원에게 보입니다.
Tutorial.Ping.TouchText | Open the map and tap an exit to ping it. Hold to choose other pings. Your party sees your pings. | 지도를 열고 탈출구를 누르면 핑이 찍힙니다. 누르고 있으면 다른 핑을 고를 수 있습니다. 핑은 파티원에게 보입니다.
Tutorial.Retry.Title | Escape a raid | 레이드에서 탈출하기
Tutorial.Retry.Text | Head out again. Reach an exit alive to finish the tutorial. | 다시 출발하세요. 살아서 출구에 도착하면 튜토리얼이 끝납니다.
## UI.Loading
- | Your bag is only secured once you extract. | 가방 속 물건은 탈출해야만 확보됩니다.
- | Die in a raid and your bag drops where you fall. | 레이드에서 죽으면 쓰러진 자리에 가방을 떨어뜨립니다.
- | When the timer runs out, you fail to extract. | 시간이 다 되면 탈출에 실패합니다.
- | Gear is locked during a raid. Choose it in Godstayed. | 레이드 중에는 장비를 바꿀 수 없습니다. 신이 머물렀다에서 고르세요.
- | Deicide Stone is the blood of a god, crystallized into red ore. | 신살석은 붉은 광석으로 굳은 신의 피입니다.
- | Relics hold a god's memory. Your Sanity pays for every use. | 성유물에는 신의 기억이 깃들어 있습니다. 쓸 때마다 정신력을 치릅니다.
- | You can't escape for a few seconds after attacking. | 공격한 뒤 몇 초 동안은 탈출할 수 없습니다.
- | The Ash Scavengers keep their safe zones alive with recovered relics. | 잿빛 약탈자들은 되찾은 성유물로 안전 구역을 지킵니다.
- | Entering raid | 레이드 입장
- | Returning to | 귀환
- | Godstayed | 신이 머물렀다
- | Lobby | 로비
- | Craft and upgrade | 제작과 업그레이드
- | Traveling | 이동 중
## World
- | Squad Up | 파티 모집
- | Forge | 대장간
- | Reliquary | 성유물 보관소
- | BUY  ·  SALVAGE  ·  TRADE | 구매  ·  판매  ·  거래
- | PERSONAL VAULT  ·  NO. 07 | 개인 금고  ·  07번
- | Hell Dungeon | 지옥 던전
- | ⚠ GODWOUND BREACH ⚠ | ⚠ 신의 상처 균열 ⚠
- | BUNKER 07  —  LAST SHELTER | 벙커 07  —  마지막 대피소
- | Raid Gate | 레이드 관문
- | SECTOR 7  ·  SURFACE ACCESS  ·  NO RETURN WITHOUT CLEARANCE | 7구역  ·  지상 출입구  ·  허가 없이 귀환 불가
- | Deploy | 출격
## Places
Places.OfficeBuilding.Name | Office Building | 사무 빌딩
Places.OfficeBuilding.Description | A district of glass towers. Loot gets better the higher you climb. | 유리 빌딩이 늘어선 구역. 높이 올라갈수록 전리품이 좋아집니다.
Places.Godwound.Name | The Godwound | 신의 상처
Places.Godwound.Description | A burning wound in the earth. Relic bosses roam here. | 땅에 난 불타는 상처. 성유물 보스들이 돌아다닙니다.
Places.ShopDistrict.Name | Shop District | 상가 거리
Places.ShopDistrict.Description | A ruined shopping street. Shutters open at random. | 폐허가 된 상가 거리. 셔터가 무작위로 열립니다.
Places.Steelworks.Name | Steelworks | 제철소
Places.Steelworks.Description | A dead steel mill. The furnaces are cold, but the workers never left. | 멈춰 버린 제철소. 용광로는 식었지만 작업자들은 떠나지 않았습니다.
Places.TownTower.Name | Town Tower | 마을 탑
## Currency
Currency.Gold.Description | Currency used in the ruins. Spend it in shops and trades. | 폐허에서 쓰는 화폐. 상점과 거래에 씁니다.
Currency.Crystal.Description | A special currency purchased with Robux. | Robux로 사는 특별한 화폐.
## Crates
Crates.SupplyCrate | Supply Crate | 보급 상자
Crates.StoreSupplies | Store Supplies | 상점 물품
Crates.MedicineCabinet | Medicine Cabinet | 약품 수납장
Crates.Toolbox | Toolbox | 공구함
Crates.MechanicsToolbox | Mechanic's Toolbox | 정비공의 공구함
Crates.WorkersToolChest | Worker's Tool Chest | 작업자 공구 상자
Crates.SurvivorStash | Survivor Stash | 생존자 은닉처
## Contracts
Contracts.ClearTheStreet.Title | Clear the Street | 거리 청소
Contracts.ClearTheStreet.Text | Kill 15 monsters in the Shop District. | 상가 거리에서 몬스터 15마리를 처치하세요.
Contracts.ThinTheHorde.Title | Thin the Horde | 무리 솎아 내기
Contracts.ThinTheHorde.Text | Kill 25 monsters in any raid. | 아무 레이드에서 몬스터 25마리를 처치하세요.
Contracts.IntoTheWound.Title | Into the Wound | 상처 속으로
Contracts.IntoTheWound.Text | Kill 10 monsters in The Godwound. | 신의 상처에서 몬스터 10마리를 처치하세요.
Contracts.BigGame.Title | Big Game | 대물 사냥
Contracts.BigGame.Text | Defeat a boss in any raid. | 아무 레이드에서 보스를 처치하세요.
Contracts.ScrapDrive.Title | Scrap Drive | 고철 모으기
Contracts.ScrapDrive.Text | Bring 10 Scrap Metal to the board. | 고철 10개를 게시판으로 가져오세요.
Contracts.Firewood.Title | Firewood | 땔감
Contracts.Firewood.Text | Bring 10 Scrap Wood to the board. | 폐목재 10개를 게시판으로 가져오세요.
Contracts.PatchJob.Title | Patch Job | 땜질
Contracts.PatchJob.Text | Bring 5 Duct Tape to the board. | 덕트 테이프 5개를 게시판으로 가져오세요.
Contracts.NailsForTheWall.Title | Nails for the Wall | 벽에 박을 못
Contracts.NailsForTheWall.Text | Bring 15 Rusted Nails to the board. | 녹슨 못 15개를 게시판으로 가져오세요.
Contracts.SharpSupply.Title | Sharp Supply | 날카로운 보급
Contracts.SharpSupply.Text | Bring 3 Saw Blades to the board. | 톱날 3개를 게시판으로 가져오세요.
Contracts.MakeItHome.Title | Make It Home | 무사 귀환
Contracts.MakeItHome.Text | Extract alive from any raid twice. | 아무 레이드에서 살아서 두 번 탈출하세요.
Contracts.ShoppingTrip.Title | Shopping Trip | 장보기
Contracts.ShoppingTrip.Text | Extract alive from the Shop District. | 상가 거리에서 살아서 탈출하세요.
Contracts.BackFromTheWound.Title | Back From the Wound | 상처에서 돌아오다
Contracts.BackFromTheWound.Text | Extract alive from The Godwound. | 신의 상처에서 살아서 탈출하세요.
## Upgrades
Upgrades.StorageSpace.Name | Storage Space | 보관 공간
Upgrades.StorageSpace.Description | More shelves in your vault. Raises how many stacks your storage can hold. | 금고에 선반을 더 놓습니다. 보관함에 둘 수 있는 묶음 수가 늘어납니다.
Upgrades.BiggerBag.Name | Bigger Bag | 더 큰 가방
Upgrades.BiggerBag.Description | A tougher, roomier pack. More bag slots, so you can carry more loot out of a raid. | 더 튼튼하고 넉넉한 배낭. 가방 칸이 늘어 레이드에서 전리품을 더 많이 가지고 나올 수 있습니다.
Upgrades.SecurePouch.Name | Secure Pouch | 안전 주머니
Upgrades.SecurePouch.Description | A hidden pouch for your best finds. If you die in a raid, your most valuable loot stacks stay with you. | 가장 좋은 전리품을 숨겨 두는 주머니. 레이드에서 죽어도 가장 값진 전리품 묶음은 남습니다.
## Skills
Skills.BladeWhirl.Name | Blade Whirl | 칼날 회오리
Skills.BladeWhirl.Description | Spin on the spot in a storm of shadowed steel, cutting everything around you three times. The last turn throws them back. | 그림자 진 칼날의 폭풍 속에서 제자리를 돌며 주위의 모든 것을 세 번 벱니다. 마지막 회전은 적을 뒤로 날려 버립니다.
Skills.ShadowStep.Name | Shadow Step | 그림자 걸음
Skills.ShadowStep.Description | Melt into shadow and reappear behind the nearest foe, driving your blade into its back. Nothing can touch you while you are unseen. | 그림자에 녹아들어 가장 가까운 적의 등 뒤에 나타나 칼날을 꽂습니다. 모습을 감춘 동안에는 아무것도 당신을 건드리지 못합니다.
Skills.ShadowChain.Name | Shadow Chain | 그림자 연쇄
Skills.ShadowChain.Description | Vanish into shadow and cut through every foe around your mark, one after another, never striking the same one twice. Then return to the first and finish it - the more it has bled, the harder it falls. | 그림자 속으로 사라져 표식 주위의 적을 하나씩 베어 나갑니다. 같은 적은 두 번 베지 않습니다. 그리고 첫 번째 적에게 돌아가 끝을 냅니다. 피를 많이 흘렸을수록 더 크게 쓰러집니다.
Skills.Vanish.Name | Vanish | 은신
Skills.Vanish.Description | Slip out of sight and leave a still copy of yourself behind. Foes chase the copy while you move faster, unseen. Striking or using another skill reveals you, and that first blow lands harder. | 모습을 감추고 그 자리에 움직이지 않는 분신을 남깁니다. 적이 분신을 쫓는 동안 당신은 보이지 않은 채 더 빠르게 움직입니다. 공격하거나 다른 스킬을 쓰면 모습이 드러나고, 그 첫 일격은 더 강하게 들어갑니다.
Skills.LeapStrike.Name | Leap Strike | 도약 강타
Skills.LeapStrike.Description | Vault high and drive your spear down where you aim. The ground breaks around the point, hurling everything nearby away. Nothing can touch you in the air. | 높이 뛰어올라 겨눈 곳에 창을 내리꽂습니다. 창끝 주위의 땅이 갈라지며 근처의 모든 것을 날려 버립니다. 공중에 있는 동안에는 아무것도 당신을 건드리지 못합니다.
Skills.SpearSweep.Name | Spear Sweep | 창 휩쓸기
Skills.SpearSweep.Description | Swing your spear in one full circle at arm's length. Everything it reaches is hurled away. | 팔을 쭉 뻗어 창을 한 바퀴 크게 휘두릅니다. 창이 닿는 모든 것이 날아갑니다.
Skills.SpearOfGod.Name | Spear of God | 신의 창
Skills.SpearOfGod.Description | Point your spear at the ground and call down a colossal lance of light from the sky. It pierces everything around where it lands and pins them in place. | 창끝으로 땅을 가리키면 하늘에서 거대한 빛의 창이 떨어집니다. 떨어진 곳 주위의 모든 것을 꿰뚫어 그 자리에 묶어 둡니다.
Skills.ChainHook.Name | Chain Hook | 사슬 갈고리
Skills.ChainHook.Description | Hurl your spear on a length of chain. Whatever it bites is dragged to your feet. | 사슬에 매단 창을 던집니다. 창에 걸린 것은 발밑까지 끌려옵니다.
Skills.SunfireOrb.Name | Sunfire Orb | 태양불 구슬
Skills.SunfireOrb.Description | Opens a sacred circle and hurls an orb of holy fire that bursts on impact. | 신성한 원을 펼치고, 부딪히면 터지는 성스러운 불의 구슬을 던집니다.
Skills.GroundSlam.Name | Ground Slam | 대지 강타
Skills.GroundSlam.Description | Slams the ground and drives a wave of sacred earth spikes forward, launching every enemy in its path. | 땅을 내리쳐 신성한 바위 가시의 물결을 앞으로 밀어 보내고, 그 길에 있는 모든 적을 띄워 올립니다.
Skills.JudgmentHalo.Name | Judgment Halo | 심판의 광륜
Skills.JudgmentHalo.Description | A halo of judgment descends around you, drags every nearby enemy to its heart, and bursts in a pillar of holy light. | 심판의 광륜이 주위에 내려와 근처의 모든 적을 한가운데로 끌어당긴 뒤 성스러운 빛기둥으로 터집니다.
Skills.Parry.Name | Parry | 패링
Skills.Parry.Description | Raise your weapon to catch an incoming blow. A caught strike is turned back on the attacker, leaving it stunned. | 무기를 들어 날아오는 공격을 받아 냅니다. 받아 낸 공격은 상대에게 되돌아가고, 상대는 기절합니다.
Skills.PiercingLunge.Name | Piercing Lunge | 관통 돌진
Skills.PiercingLunge.Description | Lower the spearhead and charge, skewering every enemy in your path. Nothing can touch you mid-charge. | 창끝을 낮추고 돌진해 길에 있는 모든 적을 꿰뚫습니다. 돌진하는 동안에는 아무것도 당신을 건드리지 못합니다.
Skills.FlashSlash.Name | Flash Slash | 섬광 베기
Skills.FlashSlash.Description | Vanish forward in a single stroke of light. A heartbeat later, everything you passed through falls apart. Nothing can touch you mid-dash. | 한 줄기 빛이 되어 앞으로 사라집니다. 한순간 뒤, 지나간 자리의 모든 것이 갈라집니다. 돌진하는 동안에는 아무것도 당신을 건드리지 못합니다.
Skills.CrescentSlash.Name | Crescent Slash | 초승달 베기
Skills.CrescentSlash.Description | Draw back and cleave a great crescent of light before you, hurling everything in its arc away. | 무기를 끌어당겼다가 앞으로 거대한 초승달 모양의 빛을 베어 내, 그 호 안의 모든 것을 날려 버립니다.
Skills.TripleSlash.Name | Triple Slash | 삼연참
Skills.TripleSlash.Description | Three cuts faster than the eye can follow, each a step deeper. The last one throws everything in front of you back. | 눈으로 좇을 수 없을 만큼 빠른 세 번의 베기. 한 번 벨 때마다 한 걸음씩 파고듭니다. 마지막 베기는 앞의 모든 것을 뒤로 날려 버립니다.
Skills.BladeTempest.Name | Blade Tempest | 칼날 폭풍
Skills.BladeTempest.Description | Two crescents of steel, then a crossing storm. Every cut tears through all that stands in line. | 강철 초승달 두 번, 이어서 교차하는 폭풍. 한 번 벨 때마다 줄지어 선 모든 것을 찢어 놓습니다.
Skills.PhantomEdge.Name | Phantom Edge | 환영 칼날
Skills.PhantomEdge.Description | Leave a blue afterimage where you stand. For a few seconds it repeats your strikes a heartbeat later, then shatters in a burst of steel. Press again to step into it and break it at once. | 선 자리에 푸른 잔상을 남깁니다. 몇 초 동안 잔상이 한순간 늦게 당신의 공격을 따라 하다가 강철 파편으로 부서집니다. 다시 누르면 잔상 속으로 들어가 바로 부숩니다.
Skills.Earthbreaker.Name | Earthbreaker | 대지 분쇄
Skills.Earthbreaker.Description | Bring your weapon down with all your weight. The ground splits around you and hurls every nearby enemy away. | 온 체중을 실어 무기를 내리칩니다. 주위의 땅이 갈라지며 근처의 모든 적을 날려 버립니다.
Skills.ShoulderCharge.Name | Shoulder Charge | 어깨 돌진
Skills.ShoulderCharge.Description | Drop your shoulder and charge. Anything in your way is carried along and thrown aside at the end. Nothing can touch you mid-charge. | 어깨를 낮추고 돌진합니다. 길을 막는 것은 함께 밀려가다가 끝에서 옆으로 내던져집니다. 돌진하는 동안에는 아무것도 당신을 건드리지 못합니다.
Skills.ExecutionersFall.Name | Executioner's Fall | 처형인의 일격
Skills.ExecutionersFall.Description | Hold to raise your weapon and gather its weight, then release to bring it down. The longer you hold, the harder and wider it lands, and the wounded suffer most. | 누르고 있으면 무기를 들어 올려 무게를 모으고, 떼면 내리칩니다. 오래 누를수록 더 세고 넓게 떨어지며, 다친 적일수록 더 큰 피해를 입습니다.
Skills.IronWill.Name | Iron Will | 강철 의지
Skills.IronWill.Description | A great shield of light crashes down before you. For a few seconds nothing can move you, you take less damage, and every nearby enemy turns to face you. | 거대한 빛의 방패가 앞에 내리꽂힙니다. 몇 초 동안 밀려나지 않고, 받는 피해가 줄며, 근처의 모든 적이 당신을 향해 돌아섭니다.
## Relics
Relics.Parry.Description | A shard of the Transcendent's shield, cracked when the god fell. Bolted to scrap steel, it still knows how to turn a killing blow aside. | 신이 쓰러질 때 금이 간 초월자의 방패 조각. 고철에 볼트로 박혀 있지만, 아직도 치명적인 일격을 흘려 낼 줄 압니다.
Relics.ShadowStep.Description | A sliver of the god's shadow, still cold. Hold it and the dark lets you through, one step behind whatever you mean to kill. | 아직 차가운 신의 그림자 조각. 손에 쥐면 어둠이 길을 내주어, 죽이려는 상대의 한 걸음 뒤로 데려다줍니다.
Relics.BladeWhirl.Description | A ring of black iron that never stops turning. Slip it on and your blade wants to follow. | 멈추지 않고 도는 검은 쇠고리. 끼우면 칼날도 따라 돌고 싶어 합니다.
Relics.ShadowChain.Description | Six links of a chain that casts no shadow. Wear it and the dark carries you from throat to throat, and always back to the first. | 그림자가 지지 않는 사슬 여섯 고리. 지니면 어둠이 당신을 이 목에서 저 목으로 옮겨 주고, 언제나 첫 번째로 되돌려 놓습니다.
Relics.Vanish.Description | A scrap of the veil the god wore when it walked among us. Pull it close and the world forgets where you stand, but not where you stood. | 신이 우리 사이를 걷던 때 쓰던 베일의 조각. 몸에 두르면 세상은 당신이 선 자리를 잊지만, 서 있던 자리는 잊지 않습니다.
Relics.SunfireOrb.Description | A shard of the god's sun, torn loose when the Transcendent fell. It still burns with holy fire. | 초월자가 쓰러질 때 떨어져 나온 신의 태양 조각. 아직도 성스러운 불로 타오릅니다.
Relics.JudgmentHalo.Description | The broken crown of the Transcendent. Those it judges are dragged before it, whether they will or not. | 초월자의 부서진 왕관. 심판받는 자는 원하든 원치 않든 그 앞으로 끌려옵니다.
Relics.FlashSlash.Description | A sliver of the blade that cut the Transcendent's last ray of light in two. Whoever holds it moves faster than their own shadow. | 초월자의 마지막 빛줄기를 둘로 가른 칼날의 조각. 쥔 자는 제 그림자보다 빠르게 움직입니다.
Relics.CrescentSlash.Description | A curved shard from the edge of the Transcendent's halo, worn thin as a dying moon. Swung wide, it still cuts everything it passes over. | 초월자의 광륜 가장자리에서 떨어진 휜 조각. 저무는 달처럼 얇게 닳았지만, 크게 휘두르면 지나가는 모든 것을 벱니다.
Relics.TripleSlash.Description | Three slivers of the same blade, each from a different wound on the Transcendent. Held together, they cut three times before the first one lands. | 초월자의 서로 다른 상처에서 나온 같은 칼날의 조각 셋. 함께 쥐면 첫 베기가 닿기도 전에 세 번 벱니다.
Relics.BladeTempest.Description | The edge that parted the sky on the day the Transcendent fell. Swing it and the wind remembers how to cut. | 초월자가 쓰러지던 날 하늘을 가른 칼날. 휘두르면 바람이 베는 법을 기억해 냅니다.
Relics.PhantomEdge.Description | A splinter of the mirror the Transcendent watched itself fall in. It remembers every cut you make, and makes it again. | 초월자가 자신의 추락을 지켜본 거울의 조각. 당신의 모든 베기를 기억했다가 다시 벱니다.
Relics.GroundSlam.Description | A fist of hallowed stone from the god's fallen throne. Strike the ground and the earth rises to obey. | 무너진 신의 옥좌에서 떨어진 주먹만 한 성석. 땅을 내리치면 대지가 일어나 따릅니다.
Relics.Earthbreaker.Description | A shard of the bedrock the god once stood upon. It remembers the weight of that step. | 신이 딛고 섰던 기반암의 조각. 그 걸음의 무게를 기억합니다.
Relics.ShoulderCharge.Description | A splinter of the wall that once held the god's gate. It refuses to stand still. | 신의 문을 떠받치던 벽의 조각. 가만히 있기를 거부합니다.
Relics.ExecutionersFall.Description | The block where the god's judgments were carried out. It grows heavier the longer it is held. | 신의 심판이 집행되던 처형대. 오래 들수록 무거워집니다.
Relics.IronWill.Description | A shard of the shield that stood between the god and the end of the world. It still will not yield. | 신과 세상의 끝 사이를 막아섰던 방패의 조각. 아직도 굴하지 않습니다.
Relics.PiercingLunge.Description | The lance that pinned the Transcendent to the earth. Lashed to a length of scrap pipe, it still drags its bearer forward, through anything that stands in the way. | 초월자를 땅에 꿰어 박은 창. 고철 파이프에 묶여 있지만, 아직도 쥔 자를 앞으로 끌고 나가 길을 막는 모든 것을 꿰뚫습니다.
Relics.ChainHook.Description | A spearhead welded to a length of anchor chain. Thrown, it never misses twice: what it bites, it brings home. | 닻 사슬에 용접한 창끝. 던지면 두 번 빗나가지 않습니다. 문 것은 반드시 끌고 돌아옵니다.
Relics.LeapStrike.Description | A broken spearhead that fell point-first from the sky and split a road in half. Hold it and the ground starts to feel far below. | 하늘에서 창끝부터 떨어져 도로를 반으로 가른 부러진 창날. 쥐면 땅이 아득히 멀게 느껴집니다.
Relics.SpearSweep.Description | A lance-butt worn smooth by a thousand turns. It remembers the circle it cut through the crowd, and wants to cut it again. | 수천 번 돌아 매끈하게 닳은 창자루 끝. 무리를 가르며 그린 원을 기억하고, 다시 그리고 싶어 합니다.
Relics.SpearOfGod.Description | A splinter of the lance that fell when the god fell. Raise it to the sky and the sky remembers, and throws the rest of it down. | 신이 쓰러질 때 함께 떨어진 창의 조각. 하늘로 치켜들면 하늘이 기억해 내고 나머지를 내던집니다.
## Items
Items.Bandage.Name | Bandage | 붕대
Items.Bandage.Description | A simple bandage for emergency first aid. | 응급 처치용 간단한 붕대.
Items.PurificationSerum.Name | Purification Serum | 정화 혈청
Items.PurificationSerum.Description | Washes away divine contamination and restores sanity. | 신성 오염을 씻어 내고 정신력을 회복합니다.
Items.DeicideStone.Name | Deicide Stone | 신살석
Items.DeicideStone.Description | A fully awakened Deicide Stone pulsing with the absolute malice of a dead god. Binding this relic to a weapon severs the boundaries of mortal physics, turning the blade into a divine-slaying instrument. | 죽은 신의 절대적인 악의로 맥동하는, 완전히 깨어난 신살석. 이 성유물을 무기에 묶으면 필멸의 물리 법칙이 끊어지고, 칼날은 신을 베는 도구가 됩니다.
Items.ScrapMetal.Name | Scrap Metal | 고철
Items.ScrapMetal.Description | Rusty scraps salvaged from the ruins. Used to craft and enhance weapons at the blacksmith. | 폐허에서 건진 녹슨 쇳조각. 대장장이에게서 무기를 제작하고 강화하는 데 씁니다.
Items.GrindingStone.Name | Grinding Stone | 숫돌
Items.GrindingStone.Description | A high-density sharpening stone salvaged from a building maintenance workshop. | 건물 관리 작업장에서 건진 고밀도 숫돌.
Items.SurgicalBlade.Name | Surgical Blade | 수술용 칼날
Items.SurgicalBlade.Description | Found inside sealed medical supply cases in a deserted hospital. | 버려진 병원의 봉인된 의료 용품 상자 안에서 찾았습니다.
Items.CrystallizedBlade.Name | Crystallized Blade | 결정화된 칼날
Items.CrystallizedBlade.Description | Unstable chemical crystals recovered from a ruined school science lab. | 무너진 학교 과학실에서 건진 불안정한 화학 결정.
Items.DeicideStoneShard.Name | Deicide Stone Shard | 신살석 파편
Items.DeicideStoneShard.Description | A razor-sharp shard chipped from a Deicide Stone. Cold to the touch, it pulses with a faint crimson light. | 신살석에서 떨어져 나온 면도날처럼 날카로운 파편. 만지면 차갑고, 희미한 진홍빛으로 맥동합니다.
Items.ScrapWood.Name | Scrap Wood | 폐목재
Items.ScrapWood.Description | Splintered planks from collapsed homes. Good enough for a handle. | 무너진 집에서 나온 쪼개진 널빤지. 손잡이로 쓰기엔 충분합니다.
Items.RustedNails.Name | Rusted Nails | 녹슨 못
Items.RustedNails.Description | A fistful of bent, rusted nails. Still sharp where it counts. | 구부러지고 녹슨 못 한 줌. 필요한 곳은 아직 날카롭습니다.
Items.DuctTape.Name | Duct Tape | 덕트 테이프
Items.DuctTape.Description | Holds the world together, one weapon at a time. | 무기 하나씩, 세상을 붙들어 놓습니다.
Items.SawBlade.Name | Saw Blade | 톱날
Items.SawBlade.Description | A chipped circular saw blade pulled from a dead workshop. | 멈춘 작업장에서 뽑아 온 이 빠진 원형 톱날.
Items.UncommonAwakeningStone.Name | Uncommon Awakening Stone | 고급 각성석
Items.UncommonAwakeningStone.Description | A crystal that awakens a weapon to Uncommon grade at the blacksmith. | 대장장이에게서 무기를 고급 등급으로 각성시키는 결정.
Items.RareAwakeningStone.Name | Rare Awakening Stone | 희귀 각성석
Items.RareAwakeningStone.Description | A crystal that awakens a weapon to Rare grade at the blacksmith. | 대장장이에게서 무기를 희귀 등급으로 각성시키는 결정.
Items.EpicAwakeningStone.Name | Epic Awakening Stone | 영웅 각성석
Items.EpicAwakeningStone.Description | A crystal that awakens a weapon to Epic grade at the blacksmith. | 대장장이에게서 무기를 영웅 등급으로 각성시키는 결정.
Items.LegendaryAwakeningStone.Name | Legendary Awakening Stone | 전설 각성석
Items.LegendaryAwakeningStone.Description | A crystal that awakens a weapon to Legendary grade at the blacksmith. | 대장장이에게서 무기를 전설 등급으로 각성시키는 결정.
Items.RelicShard.Name | Relic Shard | 성유물 파편
Items.RelicShard.Description | A splinter of divine power torn from a guardian of the Godwound. Gather enough and the relic keeper can forge them into a whole relic. | 신의 상처의 수호자에게서 뜯겨 나온 신성한 힘의 조각. 충분히 모으면 성유물 관리인이 온전한 성유물로 만들어 줍니다.
Items.RelicShards | Relic Shards | 성유물 파편
Items.CommonGodscarPearl.Name | Common Godscar Pearl | 일반 신흔 진주
Items.GodscarPearl.Description | A pearl formed in the wound of a fallen god. Add it when crafting to grant a random trait. Its grade affects the trait value. | 쓰러진 신의 상처에서 생긴 진주. 제작할 때 넣으면 무작위 특성이 붙습니다. 진주 등급이 특성 수치에 영향을 줍니다.
Items.UncommonGodscarPearl.Name | Uncommon Godscar Pearl | 고급 신흔 진주
Items.RareGodscarPearl.Name | Rare Godscar Pearl | 희귀 신흔 진주
Items.EpicGodscarPearl.Name | Epic Godscar Pearl | 영웅 신흔 진주
Items.LegendaryGodscarPearl.Name | Legendary Godscar Pearl | 전설 신흔 진주
Items.Blueprint.Name | %s Blueprint | %s 설계도
Items.ScrapPlateVestBlueprint.Description | A creased, oil-stained sheet showing how to rivet scrap plates onto a work vest. Use it to learn the recipe at the blacksmith. | 작업 조끼에 고철판을 리벳으로 박는 법이 그려진, 구겨지고 기름 묻은 종이. 사용하면 대장장이에게서 제작법을 배웁니다.
Items.RiotVestBlueprint.Description | A police supply sheet for a padded riot vest, first-aid pouch marked in pencil. Use it to learn the recipe at the blacksmith. | 패드를 댄 진압 조끼의 경찰 보급 문서. 구급 주머니가 연필로 표시돼 있습니다. 사용하면 대장장이에게서 제작법을 배웁니다.
Items.ButchersApronBlueprint.Description | A slaughterhouse supply sheet for a heavy leather apron, the margins smudged with grease. Use it to learn the recipe at the blacksmith. | 두꺼운 가죽 앞치마의 도축장 보급 문서. 여백이 기름으로 얼룩져 있습니다. 사용하면 대장장이에게서 제작법을 배웁니다.
Items.RimeheartMailBlueprint.Description | A frost-rimed sheet that never quite thaws: plate armor grown over with ice around a glowing shard. Use it to learn the recipe at the blacksmith. | 끝내 녹지 않는 서리 낀 종이. 빛나는 파편 둘레로 얼음이 자라난 판금 갑옷이 그려져 있습니다. 사용하면 대장장이에게서 제작법을 배웁니다.
Items.NightveilLeathersBlueprint.Description | A pattern sheet inked in silver, folded small enough to hide in a boot: layered leathers, crescent clasps, a stone at the collar. Use it to learn the recipe at the blacksmith. | 장화 속에 숨길 만큼 작게 접은, 은색 잉크로 그린 본. 겹친 가죽, 초승달 걸쇠, 깃의 보석이 그려져 있습니다. 사용하면 대장장이에게서 제작법을 배웁니다.
Items.EmberforgePlateBlueprint.Description | A smith's plan scorched at the edges: heavy plate with a furnace grate set in the chest. Use it to learn the recipe at the blacksmith. | 가장자리가 그을린 대장장이의 설계. 가슴에 화로 창살을 박은 무거운 판금 갑옷입니다. 사용하면 대장장이에게서 제작법을 배웁니다.
Items.RiftveilMantleBlueprint.Description | A sheet torn from the Shutterback's shell. The lines on it keep shifting a little to the left. Use it to learn the recipe at the blacksmith. | 셔터 갑각의 껍데기에서 뜯어낸 종이. 그려진 선이 자꾸 조금씩 왼쪽으로 밀립니다. 사용하면 대장장이에게서 제작법을 배웁니다.
Items.NovicesSwordBlueprint.Description | A smudged sketch of a plain cleaver-blade sword with a bolted guard. Use it to learn the recipe at the blacksmith. | 볼트로 고정한 날밑에 식칼 같은 날을 단 평범한 검의 번진 스케치. 사용하면 대장장이에게서 제작법을 배웁니다.
Items.NailBatBlueprint.Description | A page torn from a notebook: a baseball bat, nails, and a lot of tape. Use it to learn the recipe at the blacksmith. | 공책에서 찢어 낸 한 장. 야구 배트, 못, 그리고 테이프가 잔뜩. 사용하면 대장장이에게서 제작법을 배웁니다.
Items.JunkyardRipperBlueprint.Description | Grease-stained plans for mounting a saw blade on a pipe handle. Use it to learn the recipe at the blacksmith. | 파이프 손잡이에 톱날을 다는 법이 적힌 기름 얼룩진 설계도. 사용하면 대장장이에게서 제작법을 배웁니다.
Items.RustyGreatswordBlueprint.Description | A forger's outline of a long, notched greatsword with a hooked guard. Use it to learn the recipe at the blacksmith. | 갈고리 날밑이 달린, 이 빠진 긴 대검을 그린 대장장이의 밑그림. 사용하면 대장장이에게서 제작법을 배웁니다.
Items.StoneSpearBlueprint.Description | A long pole, a knapped stone head, and wire wound in a cage to hold it. Use it to learn the recipe at the blacksmith. | 긴 장대, 깨뜨려 다듬은 돌 창끝, 그리고 그것을 감싸 고정하는 철사. 사용하면 대장장이에게서 제작법을 배웁니다.
Items.KarambitBlueprint.Description | A hooked blade traced on the back of a receipt, with a grip ring made of hex nuts. Use it to learn the recipe at the blacksmith. | 영수증 뒷면에 따라 그린 갈고리 칼날. 손잡이 고리는 육각 너트로 만들었습니다. 사용하면 대장장이에게서 제작법을 배웁니다.
## Weapons
Weapons.NovicesSword.Name | Novice's Sword | 초보자의 검
Weapons.NovicesSword.Description | A plain sword that survivors first take in hand. | 생존자들이 처음 손에 쥐는 평범한 검.
Weapons.RustyGreatsword.Name | Rusty Greatsword | 녹슨 대검
Weapons.RustyGreatsword.Description | A long blade gone red with rust. Quick enough to swing, and its last strike shakes the ground. | 녹으로 붉게 변한 긴 칼날. 휘두르기에 충분히 빠르고, 마지막 일격은 땅을 뒤흔듭니다.
Weapons.NailBat.Name | Nail Bat | 못 박힌 배트
Weapons.JunkyardRipper.Name | Junkyard Ripper | 고철장 톱날검
Weapons.JunkyardRipper.Description | Scrap pipe with a rusted saw blade bolted to the end. Crude, heavy, and brutal. | 끝에 녹슨 톱날을 볼트로 박은 고철 파이프. 조잡하고, 무겁고, 잔인합니다.
Weapons.StoneSpear.Name | Stone Spear | 돌창
Weapons.StoneSpear.Description | A long spear with a stone head. | 돌 창끝을 단 긴 창.
Weapons.Karambit.Name | Karambit | 카람빗
Weapons.Karambit.Description | A hook blade ground out of scrap, with a finger ring of welded hex nuts. | 고철을 갈아 만든 갈고리 칼날. 손가락 고리는 육각 너트를 용접해 만들었습니다.
Weapons.MasterSword.Name | Master Sword | 마스터 소드
Weapons.MasterSword.Description | Temporary test weapon. | 임시 시험용 무기.
## Armor
Armor.ScrapPlateVest.Name | Scrap Plate Vest | 고철판 조끼
Armor.ScrapPlateVest.Description | Rusted sheet metal riveted over a work vest. It rattles with every step. | 작업 조끼 위에 리벳으로 박은 녹슨 철판. 걸을 때마다 덜컹거립니다.
Armor.RiotVest.Name | Riot Vest | 진압 조끼
Armor.RiotVest.Description | A police riot vest, padded and scuffed. Someone stitched a first-aid pouch to the front. | 패드를 댄, 긁힌 경찰 진압 조끼. 누군가 앞에 구급 주머니를 꿰매 달았습니다.
Armor.ButchersApron.Name | Butcher's Apron | 도축업자의 앞치마
Armor.ButchersApron.Description | A heavy slaughterhouse apron, black with old grease. Meat hooks still hang from the belt. | 묵은 기름때로 검게 변한 무거운 도축장 앞치마. 허리띠에는 아직 고기 갈고리가 매달려 있습니다.
Armor.RimeheartMail.Name | Rimeheart Mail | 서리심장 갑옷
Armor.RimeheartMail.Description | Steel overgrown with ice that never melts. A shard of the fallen god's frost still glows at its heart. | 녹지 않는 얼음으로 뒤덮인 강철. 한가운데에는 쓰러진 신의 서리 조각이 아직 빛납니다.
Armor.NightveilLeathers.Name | Nightveil Leathers | 밤장막 가죽 갑옷
Armor.NightveilLeathers.Description | Layered dark leathers clasped with silver crescents. The moonstone at the collar glows brighter the faster you strike. | 은빛 초승달 걸쇠로 여민 겹겹의 검은 가죽. 빠르게 공격할수록 깃의 월장석이 더 밝게 빛납니다.
Armor.EmberforgePlate.Name | Emberforge Plate | 잉걸불 판금 갑옷
Armor.EmberforgePlate.Description | Blackened plate forged around a living ember. Every blow it takes stokes the fire in its seams. | 살아 있는 불씨를 품고 벼린 검게 그을린 판금. 공격을 받을 때마다 이음매의 불길이 거세집니다.
Armor.RiftveilMantle.Name | Riftveil Mantle | 균열장막 망토
Armor.RiftveilMantle.Description | Torn cloth that never quite lines up with itself. A cracked red halo drifts behind the shoulders, still turning. | 끝내 제 모양이 맞지 않는 찢어진 천. 어깨 뒤로 금 간 붉은 광륜이 떠다니며 아직도 돕니다.
Armor.BodyArmor | Body Armor | 몸 방어구
## Enemies
Enemies.ToothedRevenant | Toothed Revenant | 이빨 망령
Enemies.Shutterback | The Shutterback | 셔터 갑각
Enemies.ShutterbackShort | Shutterback | 셔터 갑각
Enemies.FailedSubject | Failed Subject | 실패한 실험체
Enemies.OvertimeHusk | Overtime Husk | 야근 망자
Enemies.WardPatient | Ward Patient | 병동 환자
Enemies.StockroomBrute | Stockroom Brute | 창고 거한
Enemies.ScaldedBarista | Scalded Barista | 화상 입은 바리스타
Enemies.CinderHusk | Cinder Husk | 잿불 망자
Enemies.ScorchedStalker | Scorched Stalker | 그을린 추적자
Enemies.MoltenBrute | Molten Brute | 용암 거한
Enemies.AbyssAbomination | Abyss Abomination | 심연의 흉물
Enemies.WardenOfTheRuinedKeep | Warden of the Ruined Keep | 무너진 성채의 파수꾼
Enemies.CanyonDevourer | Canyon Devourer | 협곡 포식자
Enemies.HeartOfTheCaldera | Heart of the Caldera | 칼데라의 심장
Enemies.LordOfTheBurningLake | Lord of the Burning Lake | 불타는 호수의 군주
Enemies.ScionOfTheWound | Scion of the Wound | 상처의 후예
Enemies.SlagWalker | Slag Walker | 슬래그 배회자
Enemies.MoltenWalker | Molten Walker | 용융 배회자
Enemies.HookHauler | Hook Hauler | 갈고리 운반자
Enemies.FurnaceTender | Furnace Tender | 용광로 화부
Enemies.FurnaceWarden | Furnace Warden | 용광로 수문장
Enemies.TheForeman | The Foreman | 작업반장
Enemies.Foreman | Foreman | 작업반장
Enemies.AshenHusk | Ashen Husk | 잿빛 망자
## Traits
Traits.SurvivorsRhythm.Name | Survivor's Rhythm | 생존자의 리듬
Traits.SurvivorsRhythm.Description | Each enemy hit grants +{speedPerStack}% attack speed, up to {maxStacks} stacks. Loses 1 stack every {decayInterval}s without a hit, and all stacks when you take damage. | 적을 맞힐 때마다 공격 속도 +{speedPerStack}% (최대 {maxStacks}중첩). 맞히지 못하면 {decayInterval}초마다 1중첩씩 잃고, 피해를 받으면 모두 잃습니다.
Traits.SurvivorsRhythm.Extra | Reaching max stacks makes your next hit a guaranteed critical. | 최대 중첩에 도달하면 다음 공격이 반드시 치명타로 들어갑니다.
Traits.Tetanus.Name | Tetanus | 파상풍
Traits.Tetanus.Description | Hits infect the target for {duration}s. Each stack makes it take +{perStack}% damage, up to {maxStacks} stacks. | 공격하면 대상을 {duration}초 동안 감염시킵니다. 중첩마다 받는 피해 +{perStack}% (최대 {maxStacks}중첩).
Traits.Tetanus.Extra | Enemies that die at max stacks spread the infection to nearby enemies. | 최대 중첩에서 죽은 적은 근처 적에게 감염을 퍼뜨립니다.
Traits.SerratedEdge.Name | Serrated Edge | 톱니 칼날
Traits.SerratedEdge.Description | Hits apply {stacksPerHit} Bleed stacks for {duration}s. Each stack deals {perStack}% weapon damage per second, up to {maxStacks} stacks. | 공격하면 출혈 {stacksPerHit}중첩을 {duration}초 동안 겁니다. 중첩마다 매초 무기 피해의 {perStack}%를 줍니다 (최대 {maxStacks}중첩).
Traits.SerratedEdge.Extra | Critical hits on bleeding enemies detonate all remaining Bleed at once. | 출혈 중인 적에게 치명타를 넣으면 남은 출혈이 한 번에 터집니다.
Traits.RustQuake.Name | Rust Quake | 녹슨 진동
Traits.RustQuake.Description | The last hit of a combo sends out a shockwave dealing {damagePercent}% weapon damage within {radius} studs. | 연속 공격의 마지막 타격이 충격파를 일으켜 {radius}스터드 안에 무기 피해의 {damagePercent}%를 줍니다.
Traits.RustQuake.Extra1 | It stuns enemies for {stunDuration}s. | 적을 {stunDuration}초 동안 기절시킵니다.
Traits.RustQuake.Extra2 | It also infects them: +{infectPerStack}% damage taken per stack. | 감염도 겁니다: 중첩마다 받는 피해 +{infectPerStack}%.
Traits.ScrapPlating.Name | Scrap Plating | 고철 도금
Traits.ScrapPlating.Description | Each time you take damage, you take {perStack}% less damage, up to {maxStacks} stacks. Stacks reset {duration}s after the last hit. | 피해를 받을 때마다 받는 피해 {perStack}% 감소 (최대 {maxStacks}중첩). 마지막으로 맞고 {duration}초가 지나면 중첩이 초기화됩니다.
Traits.SecondWind.Name | Second Wind | 기사회생
Traits.SecondWind.Description | When a hit leaves you below {threshold}% health, instantly restore {healPercent}% of your max health. Cooldown {cooldown}s. | 공격을 받아 체력이 {threshold}% 아래로 떨어지면 즉시 최대 체력의 {healPercent}%를 회복합니다. 재사용 대기시간 {cooldown}초.
Traits.BloodPrice.Name | Blood Price | 피의 대가
Traits.BloodPrice.Description | Hits on Bleeding enemies deal +{bonus}% damage and heal you for {healPercent}% of the damage dealt. | 출혈 중인 적에게 주는 피해 +{bonus}%, 준 피해의 {healPercent}%만큼 체력을 회복합니다.
Traits.Shatter.Name | Shatter | 산산조각
Traits.Shatter.Description | Hits on Slowed, Freezing, Frozen, Stunned or Rooted enemies deal +{bonus}% damage. | 둔화·빙결·얼어붙음·기절·속박 상태의 적에게 주는 피해 +{bonus}%.
Traits.Shatter.Extra | Hitting a Frozen enemy shatters the ice, dealing {shatterPercent}% weapon damage to enemies within {shatterRadius} studs (once per freeze). | 얼어붙은 적을 치면 얼음이 깨지며 {shatterRadius}스터드 안의 적에게 무기 피해의 {shatterPercent}%를 줍니다 (빙결마다 한 번).
Traits.MoonlitFrenzy.Name | Moonlit Frenzy | 달빛 광란
Traits.MoonlitFrenzy.Description | +{critChance}% critical hit chance. Critical hits grant +{speedPerStack}% attack speed, up to {maxStacks} stacks. Stacks fade {duration}s after the last critical hit. | 치명타 확률 +{critChance}%. 치명타마다 공격 속도 +{speedPerStack}% (최대 {maxStacks}중첩). 마지막 치명타 뒤 {duration}초가 지나면 중첩이 사라집니다.
Traits.MoonlitFrenzy.Extra | Critical hits at max stacks heal you for {healPercent}% of your max health. | 최대 중첩에서 치명타를 넣으면 최대 체력의 {healPercent}%를 회복합니다.
Traits.Backdraft.Name | Backdraft | 역화
Traits.Backdraft.Description | Taking damage builds 1 Heat, up to {maxStacks}. Heat fades {duration}s after the last hit. The last hit of your combo vents all Heat, dealing {perStack}% weapon damage per Heat to enemies within {radius} studs. | 피해를 받으면 열기가 1 쌓입니다 (최대 {maxStacks}). 마지막으로 맞고 {duration}초가 지나면 열기가 사라집니다. 연속 공격의 마지막 타격이 열기를 모두 뿜어, {radius}스터드 안의 적에게 열기 1당 무기 피해의 {perStack}%를 줍니다.
Traits.Backdraft.Extra | Venting also makes you take {guardPercent}% less damage for {guardDuration}s. | 열기를 뿜으면 {guardDuration}초 동안 받는 피해도 {guardPercent}% 줄어듭니다.
Traits.DimensionalEcho.Name | Dimensional Echo | 차원 메아리
Traits.DimensionalEcho.Description | Every {every} attacks that land, a rift afterimage repeats the last one {delay}s later, dealing {echoPercent}% of its damage again to the same enemies. | 공격이 {every}번 맞을 때마다 균열 잔상이 {delay}초 뒤 마지막 공격을 되풀이해, 같은 적에게 그 피해의 {echoPercent}%를 다시 줍니다.
Traits.BleedingEdge.Name | Bleeding Edge | 출혈 칼날
Traits.BleedingEdge.Description | {value}% chance on hit to apply 1 Bleed stack ({perStack}% weapon damage per second for {duration}s, up to {maxStacks} stacks). | 공격 시 {value}% 확률로 출혈 1중첩 (매초 무기 피해의 {perStack}%, {duration}초, 최대 {maxStacks}중첩).
Traits.Contagion.Name | Contagion | 전염
Traits.Contagion.Description | {value}% chance on hit to apply 1 Infection stack (+{perStack}% damage taken for {duration}s, up to {maxStacks} stacks). | 공격 시 {value}% 확률로 감염 1중첩 ({duration}초 동안 받는 피해 +{perStack}%, 최대 {maxStacks}중첩).
Traits.Frostbite.Name | Frostbite | 동상
Traits.Frostbite.Description | {value}% chance on hit to apply 1 Freeze stack (-{perStack}% move and attack speed for {duration}s, up to {maxStacks} stacks). | 공격 시 {value}% 확률로 빙결 1중첩 ({duration}초 동안 이동·공격 속도 -{perStack}%, 최대 {maxStacks}중첩).
Traits.Hamstring.Name | Hamstring | 힘줄 끊기
Traits.Hamstring.Description | {value}% chance on hit to Slow the target by {amount}% for {duration}s. | 공격 시 {value}% 확률로 대상을 {duration}초 동안 {amount}% 둔화시킵니다.
Traits.Concussive.Name | Concussive | 뇌진탕
Traits.Concussive.Description | {value}% chance on hit to Stun the target for {duration}s. | 공격 시 {value}% 확률로 대상을 {duration}초 동안 기절시킵니다.
Traits.Keen.Name | Keen | 예리함
Traits.Keen.Description | +{value}% critical hit chance. | 치명타 확률 +{value}%.
Traits.Swift.Name | Swift | 신속
Traits.Swift.Description | +{value}% attack speed. | 공격 속도 +{value}%.
Traits.Leech.Name | Leech | 흡혈
Traits.Leech.Description | Heal {value}% of max health for each enemy hit. | 적을 맞힐 때마다 최대 체력의 {value}%를 회복합니다.
Traits.AttackUp.Name | Attack Up | 공격력 증가
Traits.AttackUp.Description | +{value}% damage. | 피해 +{value}%.
## Messages
- | Your data is being saved on another server. Please rejoin in a moment. | 다른 서버에서 데이터를 저장하는 중입니다. 잠시 뒤 다시 접속해 주세요.
- | The game has been updated. Please rejoin. | 게임이 업데이트됐습니다. 다시 접속해 주세요.
- | Failed to load your data. Please rejoin in a moment. | 데이터를 불러오지 못했습니다. 잠시 뒤 다시 접속해 주세요.
- | Cannot access the data store. | 데이터 저장소에 접근할 수 없습니다.
- | Your account's data was opened on another server. Please rejoin. | 다른 서버에서 계정 데이터가 열렸습니다. 다시 접속해 주세요.
- | You can't change equipment during a raid. | 레이드 중에는 장비를 바꿀 수 없습니다.
- | You can't drop items from your bag during a raid. | 레이드 중에는 가방에서 아이템을 버릴 수 없습니다.
- | Blueprint learned: %s. Craft it at the blacksmith. | 설계도를 배웠습니다: %s. 대장장이에게서 제작하세요.
- | You cannot drop items right now. | 지금은 아이템을 버릴 수 없습니다.
- | The secure pouch is only used in raids. | 안전 주머니는 레이드에서만 씁니다.
- | Invalid slot. | 잘못된 칸입니다.
- | That slot is empty. | 그 칸은 비어 있습니다.
- | Upgrade your Secure Pouch at the vault first. | 먼저 금고에서 안전 주머니를 업그레이드하세요.
- | Your secure pouch is full. | 안전 주머니가 가득 찼습니다.
- | Your secure pouch kept %d stack%s. | 안전 주머니가 {1}묶음을 지켰습니다.
- | Your loot is secured. | 전리품을 확보했습니다.
- | Invalid amount. | 잘못된 수량입니다.
- | A weapon with relics socketed cannot be discarded. Remove the relics first. | 성유물을 끼운 무기는 버릴 수 없습니다. 먼저 성유물을 빼세요.
- | That is the same slot. | 같은 칸입니다.
- | That item cannot be equipped there. | 그 아이템은 거기에 장착할 수 없습니다.
- | That item cannot be equipped. | 그 아이템은 장착할 수 없습니다.
- | Requires level %d. | 레벨 %d이 필요합니다.
- | Invalid equipment slot. | 잘못된 장비 칸입니다.
- | Nothing is equipped there. | 거기에 장착한 것이 없습니다.
- | Your bag is full. | 가방이 가득 찼습니다.
- | Invalid weapon. | 잘못된 무기입니다.
- | That weapon does not exist. | 그 무기는 없습니다.
- | That socket does not exist. | 그 소켓은 없습니다.
- | A relic is already socketed there. | 거기에는 이미 성유물이 끼워져 있습니다.
- | That item is not a relic. | 그 아이템은 성유물이 아닙니다.
- | %s only fits %s weapons. | %s은(는) %s 무기에만 끼울 수 있습니다.
- | That socket is empty. | 그 소켓은 비어 있습니다.
- | Invalid quickslot. | 잘못된 빠른 칸입니다.
- | Only consumables can be assigned to a quickslot. | 빠른 칸에는 소모품만 넣을 수 있습니다.
- | That is the same quickslot. | 같은 빠른 칸입니다.
- | That item cannot be used. | 그 아이템은 쓸 수 없습니다.
- | You cannot use that right now. | 지금은 쓸 수 없습니다.
- | That quickslot is empty. | 그 빠른 칸은 비어 있습니다.
- | This blueprint is not ready yet. | 이 설계도는 아직 쓸 수 없습니다.
- | You already know this blueprint. | 이미 아는 설계도입니다.
- | You do not have enough materials. | 재료가 부족합니다.
- | This weapon's sockets cannot be expanded any further. | 이 무기의 소켓은 더 늘릴 수 없습니다.
- | Currency data is still loading. | 화폐 정보를 아직 불러오는 중입니다.
- | Invalid price. | 잘못된 가격입니다.
- | Contract complete: %s. Claim it at the board. | 의뢰 완료: %s. 게시판에서 보상을 받으세요.
- | Invalid contract. | 잘못된 의뢰입니다.
- | Your bag is still loading. | 가방을 아직 불러오는 중입니다.
- | You need %d %s. | {2} {1}개가 필요합니다.
- | Not finished yet. | 아직 끝나지 않았습니다.
- | Contract complete! +%s | 의뢰 완료! +%s
- | Contracts are still loading. | 의뢰를 아직 불러오는 중입니다.
- | Step up to the contract board. | 의뢰 게시판 앞으로 가세요.
- | Inventory data is still loading. | 인벤토리를 아직 불러오는 중입니다.
- | You are too far from the blacksmith. | 대장장이에게서 너무 멉니다.
- | You cannot afford that. | 비용이 부족합니다.
- | Enhancement succeeded! %s | 강화 성공! %s
- | Enhancement failed. The weapon was not damaged. | 강화 실패. 무기는 손상되지 않았습니다.
- | Enhancement failed. The weapon dropped to +%d. | 강화 실패. 무기가 +%d(으)로 떨어졌습니다.
- | %s awakened to %s! | %s이(가) %s 등급으로 각성했습니다!
- | Choose items to dismantle. | 분해할 아이템을 고르세요.
- | Nothing could be dismantled. | 분해할 수 있는 것이 없습니다.
- | Dismantled %d item%s. Got %s.%s | {1}개를 분해했습니다. 얻은 것: {3}.{4}
- | %d skipped. | {1}개는 건너뛰었습니다.
- | Level data is still loading. | 레벨 정보를 아직 불러오는 중입니다.
- | %s is now item level %d! | %s의 아이템 레벨이 %d이 되었습니다!
- | Crafted %s! | %s을(를) 제작했습니다!
- | Crafted %s with %s (%s%%)! | %s을(를) 제작했습니다! 특성: %s (%s%%)
- | Moved %d trait%s to %s! | {3}에 특성 {1}개를 옮겼습니다!
- | Extracted %s into %s! | %s을(를) %s에 추출했습니다!
- | This weapon is already at the maximum enhancement level. | 이 무기는 이미 최대 강화 단계입니다.
- | %s weapons cannot go above +%d. Awaken it to raise the limit. | %s 무기는 +%d을 넘을 수 없습니다. 각성하면 한도가 오릅니다.
- | That item does not exist. | 그 아이템은 없습니다.
- | This item is already at the highest grade. | 이 아이템은 이미 최고 등급입니다.
- | You do not have enough materials to awaken to %s. | %s 등급으로 각성할 재료가 부족합니다.
- | Choose two different items. | 서로 다른 아이템 두 개를 고르세요.
- | Unequip the item to absorb first. | 흡수할 아이템의 장착을 먼저 해제하세요.
- | Remove the relics from the weapon to absorb first. | 흡수할 무기에서 먼저 성유물을 빼세요.
- | Absorb an item with a higher item level. | 아이템 레벨이 더 높은 아이템을 흡수하세요.
- | That recipe does not exist. | 그 제작법은 없습니다.
- | You have not learned this blueprint yet. | 아직 이 설계도를 배우지 않았습니다.
- | Pearls can only be used on weapons. | 진주는 무기에만 쓸 수 있습니다.
- | That pearl cannot be used. | 그 진주는 쓸 수 없습니다.
- | You do not have that pearl. | 그 진주가 없습니다.
- | Choose two different pieces of equipment. | 서로 다른 장비 두 개를 고르세요.
- | Remove the relics from the donor weapon first. | 제공할 무기에서 먼저 성유물을 빼세요.
- | Choose an ability to move. | 옮길 능력을 고르세요.
- | Invalid transplant. | 잘못된 이식입니다.
- | Armor cannot have the same ability twice. | 방어구에 같은 능력을 두 번 넣을 수 없습니다.
- | The original ability cannot be replaced. | 원본 능력은 바꿀 수 없습니다.
- | Choose a trait to move. | 옮길 특성을 고르세요.
- | That trait can only replace the same trait. | 그 특성은 같은 특성만 대신할 수 있습니다.
- | A weapon cannot have the same trait twice. | 무기에 같은 특성을 두 번 넣을 수 없습니다.
- | Unknown item. | 알 수 없는 아이템입니다.
- | Unknown weapon. | 알 수 없는 무기입니다.
- | The merchant won't buy %s. | 상인은 %s을(를) 사지 않습니다.
- | Unequip it first. | 먼저 장착을 해제하세요.
- | The merchant won't touch divine relics. | 상인은 신성한 성유물에 손대지 않습니다.
- | A %s store has opened in the market district! | 상가 거리에 %s 상점이 열렸습니다!
- | The shutter is closing in %d seconds! | %d초 뒤 셔터가 닫힙니다!
- | You were pushed out as the shutter closed. | 셔터가 닫히면서 밖으로 밀려났습니다.
- | Shutters are rising in the market district. | 상가 거리의 셔터가 올라가고 있습니다.
- | Golden Key | 황금 열쇠
- | The Golden Key is found! The door opens, and the way back seals behind you. | 황금 열쇠를 찾았습니다! 문이 열리고, 돌아가는 길은 등 뒤에서 막힙니다.
- | The elevator is open! | 엘리베이터가 열렸습니다!
- | All monsters down. Find the Golden Key to open the elevator. | 몬스터를 모두 쓰러뜨렸습니다. 황금 열쇠를 찾아 엘리베이터를 여세요.
- | Find the Golden Key on this floor to open the door! | 이 층에서 황금 열쇠를 찾아 문을 여세요!
- | Monsters awaken! Defeat them all (%d) | 몬스터가 깨어납니다! 모두 처치하세요 (%d)
- | Monsters left: %d | 남은 몬스터: %d
- | The tower falls silent again. You are back outside. | 탑이 다시 조용해집니다. 밖으로 돌아왔습니다.
- | The tower resets in %d seconds! | %d초 뒤 탑이 초기화됩니다!
- | The broken elevator groans and carries you to the next floor... | 고장 난 엘리베이터가 삐걱거리며 다음 층으로 데려갑니다...
- | The elevator shudders to a stop. You reach the rooftop. | 엘리베이터가 덜컹이며 멈춥니다. 옥상에 도착했습니다.
- | You escaped the building! | 건물에서 탈출했습니다!
- | You leave the tower behind. | 탑을 뒤로하고 떠납니다.
- | The entrance is sealed. Wait for the tower to reset. | 입구가 막혔습니다. 탑이 초기화될 때까지 기다리세요.
- | You step into the ruined building... | 무너진 건물 안으로 들어섭니다...
- | %s now has %d socket%s! | {1}의 소켓이 {2}개가 되었습니다!
- | That relic does not exist. | 그 성유물은 없습니다.
- | You forged %s! | %s을(를) 만들었습니다!
- | You are too far from the relic keeper. | 성유물 관리인에게서 너무 멉니다.
- | Relic socketed. | 성유물을 끼웠습니다.
- | Relic removed. | 성유물을 뺐습니다.
- | You can't invite yourself. | 자기 자신은 초대할 수 없습니다.
- | That player is not on this server. | 그 플레이어는 이 서버에 없습니다.
- | That player is not on your friends list. | 그 플레이어는 친구 목록에 없습니다.
- | Could not check your friends list. Try again. | 친구 목록을 확인하지 못했습니다. 다시 시도하세요.
- | That player is already in a party. | 그 플레이어는 이미 파티에 있습니다.
- | You are already in a party. | 이미 파티에 있습니다.
- | The party is full. | 파티가 가득 찼습니다.
- | Only the party leader can do that. | 파티장만 할 수 있습니다.
- | You are not in a party. | 파티에 속해 있지 않습니다.
- | That player is not in your party. | 그 플레이어는 내 파티에 없습니다.
- | You already have an invite waiting. | 이미 대기 중인 초대가 있습니다.
- | That player already has an invite waiting. | 그 플레이어에게는 이미 대기 중인 초대가 있습니다.
- | Answer your invite first. | 받은 초대에 먼저 답하세요.
- | That invite is no longer available. | 더 이상 유효하지 않은 초대입니다.
- | That invite has expired. | 초대가 만료됐습니다.
- | Wait a moment before sending another invite. | 잠시 뒤에 다시 초대하세요.
- | You are sending messages too quickly. | 메시지를 너무 빨리 보내고 있습니다.
- | You can't leave the party during combat. | 전투 중에는 파티를 나갈 수 없습니다.
- | Invite sent to %s. | %s 님에게 초대를 보냈습니다.
- | Party formed! XP +10% | 파티 결성! 경험치 +10%
- | %s declined your invite. | %s 님이 초대를 거절했습니다.
- | %s cancelled the party invite. | %s 님이 파티 초대를 취소했습니다.
- | You left the party. | 파티를 나갔습니다.
- | %s left the party. You are now the leader. | %s 님이 파티를 나갔습니다. 이제 당신이 파티장입니다.
- | The party was disbanded. | 파티가 해산됐습니다.
- | You are now the party leader. | 이제 당신이 파티장입니다.
- | %s is now the party leader. | 이제 %s 님이 파티장입니다.
- | %s left the server. You are now the leader. | %s 님이 서버를 떠났습니다. 이제 당신이 파티장입니다.
- | Your invite to %s expired. | %s 님에게 보낸 초대가 만료됐습니다.
- | Your party is back together. | 파티가 다시 모였습니다.
- | %s must be level %d to enter. | %s 님은 레벨 %d이 돼야 입장할 수 있습니다.
- | Exit %s has closed. | 출구 %s이(가) 닫혔습니다.
- | Exit %s closes in %d sec. | 출구 %s이(가) %d초 뒤 닫힙니다.
- | %s closes in %d min. Get to an exit! | %s이(가) %d분 뒤 닫힙니다. 출구로 가세요!
- | %s closes in %d sec. | %s이(가) %d초 뒤 닫힙니다.
- | Time's up. You failed to escape. | 시간이 다 됐습니다. 탈출에 실패했습니다.
- | No revives left. | 남은 부활이 없습니다.
- | Too late to revive. | 부활하기엔 늦었습니다.
- | Revive is unavailable. | 지금은 부활할 수 없습니다.
- | Nothing to sell. | 팔 것이 없습니다.
- | Step into the merchant's zone to sell. | 팔려면 상인 구역으로 들어가세요.
- | Your bag changed. Check the list again. | 가방이 바뀌었습니다. 목록을 다시 확인하세요.
- | That item can't be sold. | 그 아이템은 팔 수 없습니다.
- | Sold %d item%s for %s$. | {1}개를 {3}$에 팔았습니다.
- | The shop is still loading. | 상점을 아직 불러오는 중입니다.
- | The merchant just restocked. Take another look. | 상인이 방금 물건을 채웠습니다. 다시 살펴보세요.
- | That item is not for sale. | 그 아이템은 팔지 않습니다.
- | Sold out. Wait for the next restock. | 품절입니다. 다음 재입고를 기다리세요.
- | Step into the merchant's zone to buy. | 사려면 상인 구역으로 들어가세요.
- | Bought %s. Your bag is full. | %s을(를) 샀습니다. 가방이 가득 찼습니다.
- | Bought %s. | %s을(를) 샀습니다.
- | That item is missing. | 그 아이템이 없습니다.
- | Your storage is full. | 보관함이 가득 찼습니다.
- | Nothing to store. | 보관할 것이 없습니다.
- | Stored what fit. Your storage is full. | 들어가는 만큼 보관했습니다. 보관함이 가득 찼습니다.
- | Your storage is still loading. | 보관함을 아직 불러오는 중입니다.
- | Step into the vault to use your storage. | 보관함을 쓰려면 금고 안으로 들어가세요.
- | Invalid upgrade. | 잘못된 업그레이드입니다.
- | Your upgrades are still loading. | 업그레이드 정보를 아직 불러오는 중입니다.
- | Already at the highest level. | 이미 최고 단계입니다.
- | %s upgraded to level %d! | %s이(가) %d단계로 올랐습니다!
- | Step into the upgrade area. | 업그레이드 구역으로 들어가세요.
- | A %s cache is glowing in the steelworks! | 제철소에서 %s 보급 상자가 빛나고 있습니다!
- | The %s cache fades in %d seconds! | %s 보급 상자가 %d초 뒤 사라집니다!
- | Caches are glowing across the steelworks. | 제철소 곳곳에서 보급 상자가 빛나고 있습니다.
]==]

local entries = {}
local used = {}
local section = ""

local function autoKey(sec: string, en: string): string
	local words = {}
	for word in string.gmatch(en, "[%w]+") do
		if #words >= 6 then
			break
		end
		table.insert(words, string.upper(string.sub(word, 1, 1)) .. string.lower(string.sub(word, 2)))
	end
	local base = if #words > 0 then table.concat(words) else "Text"
	local key = if sec ~= "" then sec .. "." .. base else base
	local k, n = key, 2
	while used[k] do
		k = key .. "_" .. n
		n += 1
	end
	return k
end

for line in string.gmatch(SOURCE, "[^\n]+") do
	if string.sub(line, 1, 3) == "## " then
		section = string.match(string.sub(line, 4), "^%s*(.-)%s*$")
	elseif string.sub(line, 1, 2) ~= "# " then
		local key, en, ko = string.match(line, "^(.-) | (.-) | (.*)$")
		if key and en and en ~= "" then
			en = string.gsub(en, "\\n", "\n")
			ko = string.gsub(ko, "\\n", "\n")
			if key == "" or key == "-" then
				key = autoKey(section, en)
			end
			if not used[key] then
				used[key] = true
				entries[key] = { en = en, ko = ko }
			end
		end
	end
end

return {
	names = { en = "English", ko = "한국어" },
	entries = entries,
}
