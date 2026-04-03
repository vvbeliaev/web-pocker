<!-- src/lib/components/BlindTimer.svelte -->
<script lang="ts">
  let {
    blindLevel,
    sb,
    bb,
    secondsUntilNext,
    totalDuration,
  }: {
    blindLevel: number;
    sb: number;
    bb: number;
    secondsUntilNext: number;
    totalDuration: number;
  } = $props();

  const progress = $derived(
    totalDuration > 0 ? (1 - secondsUntilNext / totalDuration) * 100 : 100
  );

  const mins = $derived(Math.floor(secondsUntilNext / 60));
  const secs = $derived(Math.floor(secondsUntilNext % 60).toString().padStart(2, '0'));
</script>

<div class="blind-timer">
  <div class="info">
    <span class="label">BLINDS</span>
    <span class="values">{sb} / {bb}</span>
  </div>
  <div class="progress-track">
    <div class="progress-bar" style="width: {progress}%"></div>
  </div>
  <div class="next">
    next level in <span class="countdown">{mins}:{secs}</span>
  </div>
</div>

<style>
  .blind-timer {
    display: flex;
    flex-direction: column;
    gap: 4px;
    padding: 6px 12px;
    background: #0d0d1a;
    border: 1px solid #ffffff10;
    border-radius: 8px;
    min-width: 140px;
  }

  .info {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
  }

  .label {
    font-size: 9px;
    letter-spacing: 0.2em;
    color: #555;
    text-transform: uppercase;
  }

  .values {
    font-size: 13px;
    font-weight: 600;
    color: #e8c96a;
  }

  .progress-track {
    height: 2px;
    background: #1a1a2e;
    border-radius: 1px;
    overflow: hidden;
  }

  .progress-bar {
    height: 100%;
    background: #e87c4a;
    border-radius: 1px;
    transition: width 1s linear;
  }

  .next {
    font-size: 9px;
    color: #444;
  }

  .countdown {
    color: #e87c4a;
    font-weight: 600;
  }
</style>
