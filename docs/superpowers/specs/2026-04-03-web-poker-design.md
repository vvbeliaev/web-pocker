# Web Poker — Design Spec

**Date:** 2026-04-03  
**Status:** Approved

---

## Overview

Веб-версия Texas Hold'em для игры с друзьями. Создаёшь стол, получаешь ссылку, друзья заходят — и сразу играешь. Без регистрации, один деплой, быстрые турниры с прогрессией блайндов.

---

## Stack

| Layer     | Technology                                                          |
| --------- | ------------------------------------------------------------------- |
| Backend   | Python 3.12+, FastAPI, python-socketio (AsyncServer)                |
| State     | In-memory (Python dict/dataclasses), без БД                         |
| Frontend  | SvelteKit, Tailwind CSS v4 (без компонентных библиотек), Motion One |
| Transport | Socket.IO over WebSocket                                            |
| Deploy    | Single container: uvicorn отдаёт и API и статику SvelteKit          |

---

## Game Rules

- **Вариант:** Texas Hold'em
- **Формат:** Турнир, один стол, 2–9 игроков
- **Стек:** Фиксированный при входе (10 000 фишек), rebuy нет
- **Старт:** Автоматически когда все подключённые игроки (≥2) нажали «Готов»
- **Блайнды:** Быстрая прогрессия по таймеру (см. ниже)
- **Конец:** Остался один игрок с фишками — он победитель

### Blind Schedule (default)

| Level | SB                | BB   | Duration |
| ----- | ----------------- | ---- | -------- |
| 1     | 25                | 50   | 3 мин    |
| 2     | 50                | 100  | 3 мин    |
| 3     | 100               | 200  | 2 мин    |
| 4     | 200               | 400  | 2 мин    |
| 5     | 300               | 600  | 2 мин    |
| 6     | 500               | 1000 | 2 мин    |
| 7+    | ×2 каждый уровень |      | 2 мин    |

---

## Entities

### Room

```
id: str                  # короткий код, напр. "a3f9"
state: waiting | playing | finished
players: list[Player]
blind_level: int         # индекс в blind_schedule
blind_timer_start: float # timestamp начала текущего уровня
community_cards: list[Card]  # 0–5 карт
pot: int
hand_phase: preflop | flop | turn | river | showdown | between_hands
dealer_pos: int          # индекс в players
action_pos: int          # чья очередь
current_bet: int         # максимальная ставка в раунде
```

### Player

```
sid: str                 # socket.io session id
name: str
seat: int                # 0–8, позиция за столом
chips: int
hole_cards: list[Card]   # 2 карты, видны только владельцу
ready: bool
status: active | folded | all_in | eliminated
current_bet: int         # ставка в текущем раунде
```

### Card

```
rank: 2–14 (14 = Ace)
suit: hearts | diamonds | clubs | spades
```

---

## State Machine

```
Lobby (waiting)
  ├─ player joins via link → enters name → socket join_room
  ├─ player clicks Ready → set_ready event
  └─ all players ready AND count ≥ 2 → transition to Playing

Playing
  ├─ deal hole cards → preflop betting
  ├─ deal flop (3 cards) → betting
  ├─ deal turn (1 card) → betting
  ├─ deal river (1 card) → betting
  ├─ showdown → determine winner → award pot
  ├─ eliminate players with 0 chips
  ├─ blind timer fires → increment blind_level
  ├─ only 1 player remains → transition to Finished
  └─ repeat next hand

Finished
  └─ show winner screen, offer "New Game" (creates new room)
```

### Betting Round Rules

- Действие по кругу начиная с позиции после big blind (preflop) или после dealer (остальные раунды)
- Игрок может: fold, call (сравнять текущую ставку), raise (поднять минимум на BB), all-in
- Раунд завершается когда все active игроки сравняли ставку или сделали all-in
- Если все кроме одного сфолдили — этот игрок забирает банк без вскрытия

### Side Pots

При all-in с разными суммами создаются side pots. Алгоритм:

- All-in игрок участвует только в main pot (до своего вклада × число участников)
- Остаток идёт в side pot, разыгрываемый между остальными active игроками
- Реализуется функцией `calculate_pots(players)` → `list[Pot(amount, eligible_sids)]`

### Disconnect Handling

- Если игрок дисконнектится во время своего хода — автоматически fold через 30 секунд
- Если дисконнектился вне своего хода — его место сохраняется 60 секунд, потом fold on next turn
- Дисконнект в лобби (state=waiting) — игрок просто удаляется из списка

---

## File Structure

### Backend

```
main.py                      # uvicorn entry, монтирует static
poker/
  __init__.py
  server.py                  # FastAPI app + socketio AsyncServer
  events.py                  # socket.io event handlers
  game/
    deck.py                  # Card, Deck, shuffle
    evaluator.py             # hand ranking (7-card best hand)
    engine.py                # Hand: одна раздача от начала до конца
    tournament.py            # Room, Player, BlindSchedule, стейт-машина
```

### Frontend

```
src/
  routes/
    +page.svelte             # главная: "Создать стол"
    room/[id]/
      +page.svelte           # лобби + игра (один маршрут)
  lib/
    socket.ts                # socket.io-client singleton
    store.ts                 # gameState store (Svelte runes)
    components/
      Card.svelte            # карта, flip-анимация через Motion One
      Chip.svelte            # стопка фишек с анимацией slide
      Table.svelte           # эллипс-стол, позиционирование мест
      PlayerSeat.svelte      # аватар + имя + фишки + статус
      ActionBar.svelte       # fold / call / raise + input для суммы
      BlindTimer.svelte      # прогресс-бар + время до следующего уровня
      CommunityCards.svelte  # борд: 3+1+1 с анимацией появления
      LobbyWaiting.svelte    # список игроков + кнопка "Готов"
      WinnerScreen.svelte    # победитель + "Новая игра"
```

---

## Socket.IO Events

### Client → Server

| Event       | Payload                                           | Description       |
| ----------- | ------------------------------------------------- | ----------------- |
| `join_room` | `{room_id, name}`                                 | Войти в комнату   |
| `set_ready` | `{ready: bool}`                                   | Toggle готовности |
| `action`    | `{type: fold\|call\|raise\|all_in, amount?: int}` | Действие в раунде |

### Server → Client

| Event             | Payload                                                                                       | Description                               |
| ----------------- | --------------------------------------------------------------------------------------------- | ----------------------------------------- |
| `room_state`      | полный стейт комнаты                                                                          | При подключении и после каждого изменения |
| `deal`            | `{hole_cards: Card[]}`                                                                        | Карты только этому игроку                 |
| `community`       | `{cards: Card[], phase}`                                                                      | Борд обновился                            |
| `action_required` | `{player_name, options: ["fold","call","raise","all_in"], call_amount, min_raise, max_raise}` | Чья очередь                               |
| `hand_result`     | `{winner, hand_name, pot}`                                                                    | Итог раздачи                              |
| `blind_up`        | `{level, sb, bb}`                                                                             | Блайнды выросли                           |
| `eliminated`      | `{player_name}`                                                                               | Игрок выбыл                               |
| `winner`          | `{player_name}`                                                                               | Турнир завершён                           |
| `error`           | `{message}`                                                                                   | Ошибка (напр. комната не найдена)         |

---

## Pages & Routing

### `GET /`

Главная страница. Кнопка «Создать стол» → `POST /api/rooms` → redirect на `/room/{id}`.

### `GET /room/[id]`

Единственный игровой маршрут. Рендерит разные компоненты в зависимости от `room.state`:

- `waiting` → `LobbyWaiting` (ввод имени, список игроков, кнопка «Готов»)
- `playing` → `Table` + `ActionBar` + `BlindTimer`
- `finished` → `WinnerScreen`

Если зашёл по ссылке во время активной игры — видит сообщение «Игра идёт, ждите следующей раздачи».

### `POST /api/rooms`

Создаёт новую Room, возвращает `{room_id}`.

---

## UI Design

- **Стиль:** Тёмный минимализм. Чёрный/тёмно-синий фон, зелёное сукно для стола, золотые акценты для фишек/банка
- **Типографика:** System font, uppercase letter-spacing для лейблов
- **Компонентные библиотеки:** не используются — всё пишем сами
- **Анимации (Motion One):**
  - Карты: flip при получении, slide при раздаче на борд
  - Фишки: slide в банк при ставке
  - Игрок: подсветка border при его очереди действовать
  - Блайнд-таймер: плавный прогресс-бар

---

## Deployment

```dockerfile
# Build frontend
FROM node:22 AS frontend
WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN npm i -g pnpm && pnpm install
COPY . .
RUN pnpm build

# Python backend serves everything
FROM python:3.12-slim
WORKDIR /app
COPY --from=frontend /app/build ./static
COPY pyproject.toml main.py poker/ ./
RUN pip install uv && uv sync
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Деплой: Fly.io или Railway. Один сервис, один порт.

---

## Out of Scope (v1)

- Регистрация / авторизация
- История игр / статистика
- Чат
- Мобильная адаптация (делаем для десктопа, мобайл — потом)
- Multi-table турниры
- Rebuy / add-on
- Звуки
