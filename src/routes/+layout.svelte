<script lang="ts">
  import './layout.css';
  import favicon from '$lib/assets/favicon.svg';
</script>

<svelte:head>
  <link rel="icon" href={favicon} />
  <title>BBQ Chicken Pocket - Questionnaire</title>
  <meta name="description" content="Quick tasting questionnaire for BBQ Chicken Pocket product feedback" />
</svelte:head>

<slot />
