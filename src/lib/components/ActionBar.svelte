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
  let timeLeft = $state(0);
  let timerInterval: ReturnType<typeof setInterval> | null = null;

  $effect(() => {
    if (actionRequired) {
      raiseAmount = actionRequired.min_raise;
      timeLeft = actionRequired.timeout_seconds;
      if (timerInterval) clearInterval(timerInterval);
      timerInterval = setInterval(() => {
        timeLeft = Math.max(0, timeLeft - 1);
      }, 1000);
    } else {
      if (timerInterval) {
        clearInterval(timerInterval);
        timerInterval = null;
      }
    }
    return () => {
      if (timerInterval) clearInterval(timerInterval);
    };
  });

  const canRaise = $derived(actionRequired?.options.includes('raise') ?? false);
  const callAmount = $derived(actionRequired?.call_amount ?? 0);
  const timerPct = $derived(
    actionRequired ? (timeLeft / actionRequired.timeout_seconds) * 100 : 0
  );
  const urgent = $derived(timeLeft <= 10);
</script>

{#if isMyTurn && actionRequired}
  <div class="action-bar">
    <div class="timer-track">
      <div
        class="timer-bar"
        class:urgent
        style="width: {timerPct}%"
      ></div>
      <span class="timer-label" class:urgent>{timeLeft}s</span>
    </div>

    <div class="buttons">
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
  </div>
{:else}
  <div class="action-bar waiting">
    <span>Waiting for other players…</span>
  </div>
{/if}

<style>
  .action-bar {
    display: flex;
    flex-direction: column;
    gap: 8px;
    padding: 10px 16px;
    background: #0d0d1a;
    border: 1px solid #ffffff10;
    border-radius: 10px;
  }

  .action-bar.waiting {
    align-items: center;
    justify-content: center;
    color: #444;
    font-size: 0.85rem;
    letter-spacing: 0.05em;
  }

  .timer-track {
    position: relative;
    height: 3px;
    background: #1a1a2e;
    border-radius: 2px;
    overflow: visible;
  }

  .timer-bar {
    height: 100%;
    background: #4ade80;
    border-radius: 2px;
    transition: width 1s linear, background 0.3s;
  }

  .timer-bar.urgent { background: #f87171; }

  .timer-label {
    position: absolute;
    right: 0;
    top: -16px;
    font-size: 10px;
    color: #4ade80;
    font-weight: 600;
    letter-spacing: 0.05em;
    transition: color 0.3s;
  }

  .timer-label.urgent { color: #f87171; }

  .buttons {
    display: flex;
    gap: 8px;
    align-items: center;
    justify-content: center;
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
