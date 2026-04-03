<!-- src/lib/components/Card.svelte -->
<script lang="ts">
  import { animateMini } from 'motion';
  import { onMount } from 'svelte';
  import type { CardData } from '$lib/types';

  let {
    card,
    faceDown = false,
    small = false,
  }: {
    card: CardData | null;
    faceDown?: boolean;
    small?: boolean;
  } = $props();

  let el: HTMLDivElement;

  const isRed = $derived(card && (card.suit === 'h' || card.suit === 'd'));

  onMount(() => {
    // Flip-in animation when card appears
    animateMini(el, { rotateY: [90, 0], opacity: [0, 1] }, { duration: 0.35, ease: 'easeOut' });
  });
</script>

<div
  bind:this={el}
  class="card"
  class:small
  class:face-down={faceDown || !card}
  class:red={isRed}
>
  {#if !faceDown && card}
    <span class="rank">{card.rank_symbol}</span>
    <span class="suit">{card.suit_symbol}</span>
  {/if}
</div>

<style>
  .card {
    width: 42px;
    height: 60px;
    background: #fff;
    border-radius: 5px;
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.7), 0 1px 3px rgba(0, 0, 0, 0.5);
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
    padding: 4px 5px;
    will-change: transform;
    flex-shrink: 0;
  }

  .card.small {
    width: 30px;
    height: 42px;
    padding: 2px 3px;
  }

  .card.face-down {
    background: linear-gradient(135deg, #1a1a3e, #0d0d2e);
    border: 1px solid #ffffff15;
  }

  .rank {
    font-size: 13px;
    font-weight: 700;
    line-height: 1;
    color: #222;
  }

  .suit {
    font-size: 13px;
    line-height: 1;
    color: #222;
  }

  .red .rank,
  .red .suit {
    color: #c00;
  }

  .small .rank,
  .small .suit {
    font-size: 10px;
  }
</style>
