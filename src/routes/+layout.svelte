<script lang="ts">
    import './layout.css';
    import favicon from '$lib/assets/favicon.svg';

    export const data = undefined;
</script>

<svelte:head>
    <link rel="icon" href={favicon} />
</svelte:head>

<!-- render child pages via the default slot -->
<slot />
