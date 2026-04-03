<script lang="ts">
  import { goto } from '$app/navigation';

  let loading = $state(false);
  let error = $state('');

  async function createTable() {
    loading = true;
    error = '';
    try {
      const res = await fetch('/api/rooms', { method: 'POST' });
      if (!res.ok) throw new Error('Server error');
      const { room_id } = await res.json();
      await goto(`/room/${room_id}`);
    } catch (e) {
      error = 'Could not create table. Is the server running?';
      loading = false;
    }
  }
</script>

<main>
  <div class="hero">
    <h1>Web Poker</h1>
    <p class="subtitle">Texas Hold'em · Tournament · No registration</p>

    <button onclick={createTable} disabled={loading} class="create-btn">
      {loading ? 'Creating...' : 'Create Table'}
    </button>

    {#if error}
      <p class="error">{error}</p>
    {/if}

    <p class="hint">Create a table → share the link → start playing</p>
  </div>
</main>

<style>
  main {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #080810;
  }

  .hero {
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
  }

  h1 {
    font-size: 3rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    color: #fff;
    text-transform: uppercase;
  }

  .subtitle {
    color: #555;
    font-size: 0.85rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
  }

  .create-btn {
    margin-top: 1rem;
    padding: 0.85rem 2.5rem;
    background: #1a3a1a;
    border: 1px solid rgba(74, 222, 128, 0.3);
    border-radius: 8px;
    color: #4ade80;
    font-size: 1rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    cursor: pointer;
    transition: background 0.15s, border-color 0.15s;
  }

  .create-btn:hover:not(:disabled) {
    background: #1f4a1f;
    border-color: rgba(74, 222, 128, 0.6);
  }

  .create-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .hint {
    color: #333;
    font-size: 0.8rem;
  }

  .error {
    color: #f87171;
    font-size: 0.85rem;
  }
</style>
