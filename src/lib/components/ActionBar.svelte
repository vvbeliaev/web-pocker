<!-- src/lib/components/ActionBar.svelte -->
<script lang="ts">
  import type { ActionRequired } from '$lib/types';

  let {
    actionRequired,
    isMyTurn,
    onAction,
  }: {
    actionRequired: ActionRequired | null;
    isMyTurn: boolean;
    onAction: (type: string, amount?: number) => void;
  } = $props();

  let raiseAmount = $state(0);

  $effect(() => {
    if (actionRequired) raiseAmount = actionRequired.min_raise;
  });

  const canRaise = $derived(actionRequired?.options.includes('raise') ?? false);
  const callAmount = $derived(actionRequired?.call_amount ?? 0);
</script>

{#if isMyTurn && actionRequired}
  <div class="action-bar">
    <button class="btn fold" onclick={() => onAction('fold')}>Fold</button>

    <button class="btn call" onclick={() => onAction('call')}>
      {callAmount === 0 ? 'Check' : `Call ${callAmount}`}
    </button>

    {#if canRaise}
      <div class="raise-group">
        <button class="btn raise" onclick={() => onAction('raise', raiseAmount)}>
          Raise
        </button>
        <input
          type="number"
          bind:value={raiseAmount}
          min={actionRequired.min_raise}
          max={actionRequired.max_raise}
          step={actionRequired.min_raise}
          class="raise-input"
        />
      </div>
    {/if}

    <button class="btn allin" onclick={() => onAction('all_in')}>All In</button>
  </div>
{:else}
  <div class="action-bar waiting">
    <span>Waiting for other players…</span>
  </div>
{/if}

<style>
  .action-bar {
    display: flex;
    gap: 8px;
    align-items: center;
    justify-content: center;
    padding: 10px 16px;
    background: #0d0d1a;
    border: 1px solid #ffffff10;
    border-radius: 10px;
  }

  .action-bar.waiting {
    color: #444;
    font-size: 0.85rem;
    letter-spacing: 0.05em;
  }

  .btn {
    padding: 8px 18px;
    border-radius: 7px;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    border: 1px solid transparent;
    transition: all 0.15s;
  }

  .fold {
    background: transparent;
    border-color: rgba(248, 113, 113, 0.3);
    color: #f87171;
  }
  .fold:hover { border-color: rgba(248, 113, 113, 0.7); }

  .call {
    background: transparent;
    border-color: rgba(255, 255, 255, 0.15);
    color: #aaa;
  }
  .call:hover { border-color: rgba(255, 255, 255, 0.3); color: #fff; }

  .raise-group {
    display: flex;
    gap: 4px;
    align-items: center;
  }

  .raise {
    background: #1a3a1a;
    border-color: rgba(74, 222, 128, 0.3);
    color: #4ade80;
  }
  .raise:hover { border-color: rgba(74, 222, 128, 0.6); }

  .raise-input {
    width: 68px;
    background: #0d0d1a;
    border: 1px solid #ffffff15;
    border-radius: 6px;
    padding: 7px 6px;
    color: #e8c96a;
    font-size: 12px;
    text-align: center;
  }

  .allin {
    background: transparent;
    border-color: rgba(251, 146, 60, 0.3);
    color: #fb923c;
  }
  .allin:hover { border-color: rgba(251, 146, 60, 0.7); }
</style>
