<script lang="ts">
  import { goto } from '$app/navigation';
  import { questions } from '$lib/questions';
  import type { FormAnswers } from '$lib/types';
  import type { Question } from '$lib/types';

  let answers: FormAnswers = {};
  let hasChildren: 'Yes' | 'No' | null = null;
  let childrenAges: number[] = [];
  let isSubmitting = false;

  function initAnswers() {
    questions.forEach((q) => {
      if (q.id in answers) return;
      answers[q.id] = q.type === 'checkbox' ? [] : null;
    });
  }
  initAnswers();

  $: if (hasChildren === 'No') childrenAges = [];
  $: if (hasChildren !== null) answers['hasChildren'] = hasChildren;
  $: if (hasChildren === 'Yes') {
    answers['childrenAges'] = childrenAges.map(String);
  } else {
    delete answers['childrenAges'];
  }

  function setCheckbox(questionId: string, option: string, checked: boolean) {
    const arr = (answers[questionId] as string[]) ?? [];
    answers[questionId] = checked ? [...arr, option] : arr.filter((v) => v !== option);
  }

  function isChecked(questionId: string, option: string): boolean {
    const a = answers[questionId];
    return Array.isArray(a) && a.includes(option);
  }

  function isEmpty(q: Question): boolean {
    const a = answers[q.id];
    if (a === null || a === undefined) return true;
    if (typeof a === 'string') return a.trim() === '';
    if (Array.isArray(a)) return a.length === 0;
    return false;
  }

  async function handleSubmit(e: Event) {
    e.preventDefault();
    isSubmitting = true;
    try {
      const missing = questions.filter((q) => q.required && isEmpty(q));
      if (missing.length > 0) {
        alert(`Please complete: ${missing.map((q) => q.label).join(', ')}`);
        return;
      }
      const res = await fetch('/api/save-response', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...answers, timestamp: new Date().toISOString() })
      });
      if (!res.ok) throw new Error('Save failed');
      await goto('/questionnaire/thanks', { replaceState: true });
    } catch (err) {
      console.error(err);
      alert('Something went wrong. Please try again.');
    } finally {
      isSubmitting = false;
    }
  }
</script>

<main class="min-h-screen bg-base-200">
  <section class="max-w-3xl mx-auto px-4 py-10 md:py-16">
    <div class="card bg-base-100 shadow-2xl">
      <div class="card-body gap-6">
        <header class="space-y-1">
          <h1 class="text-2xl md:text-3xl font-bold">Questionnaire</h1>
          <p class="text-base-content/70">Complete the form below. Required fields are marked with *.</p>
        </header>

        <form class="grid gap-6" on:submit={handleSubmit}>
          {#each questions as question}
            {#if question.id === 'hasChildren' && question.type === 'radio'}
              <div class="form-control">
                <div class="label">
                  <span class="label-text font-medium">{question.label}</span>
                  {#if question.required}<span class="text-error">*</span>{/if}
                </div>
                <div class="flex gap-6">
                  {#each question.options as option}
                    <label class="label cursor-pointer gap-2">
                      <input type="radio" class="radio radio-primary" name={question.id} value={option} bind:group={hasChildren} required={question.required} />
                      <span class="label-text">{option}</span>
                    </label>
                  {/each}
                </div>
                {#if hasChildren === 'Yes'}
                  <div class="mt-4 space-y-4">
                    <h3 class="font-semibold text-sm">Children's ages</h3>
                    {#each childrenAges as _, i}
                      <div class="flex items-center gap-3">
                        <input type="number" min="0" max="18" class="input input-bordered w-24" bind:value={childrenAges[i]} placeholder="Age" />
                        <button type="button" class="btn btn-square btn-outline btn-error" on:click={() => childrenAges = childrenAges.filter((_, j) => j !== i)} aria-label="Remove">−</button>
                      </div>
                    {/each}
                    <button type="button" class="btn btn-sm btn-outline btn-secondary" on:click={() => childrenAges = [...childrenAges, 0]}>+ Add child</button>
                  </div>
                {/if}
              </div>
            {:else if question.type === 'text'}
              <div class="form-control">
                <label class="label" for={question.id}>
                  <span class="label-text font-medium">{question.label}</span>
                  {#if question.required}<span class="text-error">*</span>{/if}
                </label>
                <input
                  id={question.id}
                  type="text"
                  class="input input-bordered w-full"
                  placeholder={question.placeholder}
                  list={question.id === 'cookingMethod' ? 'cooking-methods' : undefined}
                  bind:value={answers[question.id]}
                  required={question.required}
                  autocomplete={question.id === 'fullName' ? 'name' : undefined}
                />
                {#if question.id === 'cookingMethod'}
                  <datalist id="cooking-methods">
                    <option value="Air Fried"></option>
                    <option value="Deep Fried"></option>
                    <option value="Baked"></option>
                  </datalist>
                {/if}
              </div>
            {:else if question.type === 'number'}
              <div class="form-control">
                <label class="label" for={question.id}>
                  <span class="label-text font-medium">{question.label}</span>
                  {#if question.required}<span class="text-error">*</span>{/if}
                </label>
                <input
                  id={question.id}
                  type="number"
                  class="input input-bordered w-full"
                  bind:value={answers[question.id]}
                  required={question.required}
                  min={question.id === 'age' ? 1 : undefined}
                  max={question.id === 'age' ? 100 : undefined}
                  inputmode={question.id === 'age' ? 'numeric' : undefined}
                />
                {#if question.id === 'age'}
                  <p class="text-xs text-base-content/70 mt-2">1–100</p>
                {/if}
              </div>
            {:else if question.type === 'radio'}
              <div class="form-control">
                <div class="label">
                  <span class="label-text font-medium">{question.label}</span>
                  {#if question.required}<span class="text-error">*</span>{/if}
                </div>
                <div class="flex gap-6">
                  {#each question.options as option}
                    <label class="label cursor-pointer gap-2">
                      <input type="radio" class="radio radio-primary" name={question.id} value={option} bind:group={answers[question.id]} required={question.required} />
                      <span class="label-text">{option}</span>
                    </label>
                  {/each}
                </div>
              </div>
            {:else if question.type === 'checkbox'}
              <div class="form-control">
                <div class="label">
                  <span class="label-text font-medium">{question.label}</span>
                  {#if question.required}<span class="text-error">*</span>{/if}
                </div>
                <div class="flex flex-col gap-3">
                  {#each question.options as option}
                    <label class="flex items-center gap-2 cursor-pointer">
                      <input type="checkbox" class="checkbox checkbox-primary" value={option} checked={isChecked(question.id, option)} on:change={(e) => setCheckbox(question.id, option, e.currentTarget.checked)} />
                      <span class="label-text">{option}</span>
                    </label>
                  {/each}
                </div>
              </div>
            {:else if question.type === 'rating'}
              <div class="form-control">
                <div class="label">
                  <span class="label-text font-medium">{question.label}</span>
                  {#if question.required}<span class="text-error">*</span>{/if}
                </div>
                <div class="flex gap-3 flex-wrap">
                  {#each Array(question.scale) as _, i}
                    <button
                      type="button"
                      class="btn btn-circle transition-all duration-200 transform hover:scale-110"
                      class:btn-primary={answers[question.id] === i + 1}
                      class:btn-outline={answers[question.id] !== i + 1}
                      class:btn-lg={answers[question.id] === i + 1}
                      on:click={() => (answers[question.id] = i + 1)}
                      aria-label="Rate {i + 1}"
                      aria-pressed={answers[question.id] === i + 1}
                    >
                      <span class="text-lg font-semibold">{i + 1}</span>
                    </button>
                  {/each}
                </div>
                {#if answers[question.id] !== null}
                  <p class="text-sm text-base-content/70 mt-3">
                    ✓ You selected: <span class="font-semibold">{answers[question.id]} out of {question.scale}</span>
                  </p>
                {/if}
              </div>
            {/if}
          {/each}

          <div class="divider my-2"></div>
          <div class="card-actions justify-end">
            <button type="submit" class="btn btn-primary" disabled={isSubmitting}>
              {#if isSubmitting}
                <span class="loading loading-spinner loading-sm"></span>
                Submitting...
              {:else}
                Submit
              {/if}
            </button>
          </div>
        </form>
      </div>
    </div>
  </section>
</main>
