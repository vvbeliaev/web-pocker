<!-- src/lib/components/LobbyWaiting.svelte -->
<script lang="ts">
  import type { PlayerData } from '$lib/types';

  let {
    players,
    mySid,
    roomId,
    onReady,
  }: {
    players: PlayerData[];
    mySid: string | null;
    roomId: string;
    onReady: (ready: boolean) => void;
  } = $props();

  const me = $derived(players.find(p => p.sid === mySid));
  const shareUrl = $derived(typeof window !== 'undefined'
    ? window.location.href : '');

  async function copyLink() {
    await navigator.clipboard.writeText(shareUrl);
  }
</script>

<div class="lobby">
  <h2>Waiting for players</h2>
  <p class="room-code">Room · <span>{roomId.toUpperCase()}</span></p>

  <div class="share-row">
    <input readonly value={shareUrl} class="share-input" />
    <button onclick={copyLink} class="copy-btn">Copy link</button>
  </div>

  <ul class="player-list">
    {#each players as player (player.sid)}
      <li class:ready={player.ready} class:me={player.sid === mySid}>
        <span class="seat">Seat {player.seat + 1}</span>
        <span class="name">{player.name}{player.sid === mySid ? ' (you)' : ''}</span>
        <span class="status">{player.ready ? '✓ Ready' : 'Waiting…'}</span>
      </li>
    {/each}
  </ul>

  {#if players.length < 2}
    <p class="notice">Need at least 2 players to start</p>
  {/if}

  {#if me}
    <button
      onclick={() => onReady(!me.ready)}
      class="ready-btn"
      class:active={me.ready}
    >
      {me.ready ? 'Cancel Ready' : 'Ready'}
    </button>
  {/if}
</div>

<style>
  .lobby {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1.25rem;
    padding: 2rem;
    max-width: 480px;
    margin: 0 auto;
  }

  h2 {
    font-size: 1.25rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #aaa;
  }

  .room-code {
    color: #555;
    font-size: 0.8rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
  }

  .room-code span { color: #e8c96a; }

  .share-row {
    display: flex;
    gap: 0.5rem;
    width: 100%;
  }

  .share-input {
    flex: 1;
    background: #0d0d1a;
    border: 1px solid #ffffff15;
    border-radius: 6px;
    padding: 0.5rem 0.75rem;
    color: #888;
    font-size: 0.8rem;
  }

  .copy-btn {
    padding: 0.5rem 1rem;
    background: #1a1a2e;
    border: 1px solid #ffffff20;
    border-radius: 6px;
    color: #aaa;
    cursor: pointer;
    font-size: 0.8rem;
  }

  .copy-btn:hover { border-color: #ffffff40; color: #fff; }

  .player-list {
    list-style: none;
    padding: 0;
    margin: 0;
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  li {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.6rem 1rem;
    background: #0d0d1a;
    border: 1px solid #ffffff10;
    border-radius: 8px;
    transition: border-color 0.2s;
  }

  li.ready { border-color: rgba(74, 222, 128, 0.3); }
  li.me { border-color: rgba(232, 201, 106, 0.2); }

  .seat { color: #555; font-size: 0.75rem; min-width: 3rem; }
  .name { flex: 1; color: #ddd; font-size: 0.9rem; }
  .status { font-size: 0.75rem; color: #555; }
  li.ready .status { color: #4ade80; }

  .notice { color: #555; font-size: 0.8rem; }

  .ready-btn {
    padding: 0.75rem 2rem;
    background: #1a1a2e;
    border: 1px solid #ffffff20;
    border-radius: 8px;
    color: #888;
    font-size: 0.95rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
  }

  .ready-btn.active {
    background: #1a3a1a;
    border-color: rgba(74, 222, 128, 0.4);
    color: #4ade80;
  }

  .ready-btn:hover { border-color: #ffffff30; }
</style>
