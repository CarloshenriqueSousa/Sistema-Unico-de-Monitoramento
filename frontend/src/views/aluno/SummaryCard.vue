<template>
  <div class="summary-root card-style">
    <div class="row">
      <div>
        <h3 class="title">{{ title }}</h3>
        <p class="value">{{ value }}</p>
      </div>
      <div class="icon-wrap">
        <i :class="icon" class="icon"></i>
      </div>
    </div>
    <div class="bar"><span :style="{ width: progress + '%', background: 'var(--cor-azul-prim)' }"></span></div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'SummaryCard',
  props: {
    title: { type: String, required: true },
    value: { type: [String, Number], required: true },
    icon: { type: String, required: true },
    color: { type: String, default: '#0f1e3f' },
    progress: { type: Number, default: 0 }
  }
});
</script>

<style scoped>
.summary-root { background:rgba(23,24,30,0.94); box-shadow:0 3.5px 19px rgba(52,152,219,0.13); border-radius:18px; border:1.7px solid var(--cor-azul-prim); color:var(--cor-primaria); padding:1.25rem 1rem; }
.row { display:flex; align-items:center; justify-content:space-between; }
.title { font-size:1.15rem; color:var(--cor-azul-light); margin-bottom:0.36rem; font-weight:700; }
.value { font-size:2.07rem; font-weight:900; color:var(--cor-primaria); letter-spacing:-0.01em; }
.icon-wrap { background:rgba(52,152,219,0.19); border:1px solid var(--cor-azul-prim); border-radius:12px; padding:0.7rem; display:flex; align-items:center; justify-content:center; }
.icon { font-size:1.55rem; color:var(--cor-azul-sec); }
.bar { margin-top:0.93rem; height:7px; background:rgba(52,152,219,0.15); border-radius:16px; overflow:hidden; }
.bar span { display:block; height:100%; border-radius:16px; }
@media(max-width:700px){.summary-root{padding:0.95rem 6px;}}
</style>