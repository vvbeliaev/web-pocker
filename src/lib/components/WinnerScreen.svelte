<!-- src/lib/components/WinnerScreen.svelte -->
<script lang="ts">
  let {
    winnerName,
    onNewGame,
  }: {
    winnerName: string;
    onNewGame: () => void;
  } = $props();
</script>

<div class="winner-screen">
  <div class="trophy">🏆</div>
  <h2>Tournament Over</h2>
  <p class="winner-name">{winnerName}</p>
  <p class="subtitle">wins the tournament</p>
  <button onclick={onNewGame} class="new-game-btn">New Game</button>
</div>

<style>
  .winner-screen {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 70vh;
    gap: 1rem;
    text-align: center;
  }

  .trophy { font-size: 4rem; }

  h2 {
    font-size: 1rem;
    font-weight: 400;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #555;
  }

  .winner-name {
    font-size: 2.5rem;
    font-weight: 700;
    color: #e8c96a;
    letter-spacing: 0.05em;
  }

  .subtitle {
    color: #555;
    font-size: 0.85rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
  }

  .new-game-btn {
    margin-top: 1.5rem;
    padding: 0.75rem 2rem;
    background: #1a1a2e;
    border: 1px solid #ffffff20;
    border-radius: 8px;
    color: #aaa;
    font-size: 0.95rem;
    cursor: pointer;
    transition: all 0.2s;
  }

  .new-game-btn:hover {
    border-color: #ffffff40;
    color: #fff;
  }
</style>
