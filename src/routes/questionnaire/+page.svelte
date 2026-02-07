<script lang="ts">
  import { goto } from '$app/navigation';
  import { questions } from '$lib/questions';
  import type { FormAnswers } from '$lib/types';

  // Form state
  let answers: FormAnswers = {};
  let hasChildren: 'Yes' | 'No' | null = null;
  let childrenAges: number[] = [];
  let isSubmitting = false;

  // Initialize answers object
  $: {
    questions.forEach((q) => {
      if (!(q.id in answers)) {
        if (q.type === 'checkbox') {
          answers[q.id] = [];
        } else {
          answers[q.id] = null;
        }
      }
    });
  }

  function addChild() {
    childrenAges = [...childrenAges, 0];
  }

  function removeChild(index: number) {
    childrenAges = childrenAges.filter((_, i) => i !== index);
  }

  function handleCheckboxChange(questionId: string, option: string, checked: boolean) {
    const currentAnswers = answers[questionId];
    if (!Array.isArray(currentAnswers)) {
      answers[questionId] = [];
    }
    const answerArray = answers[questionId] as string[];
    if (checked) {
      answers[questionId] = [...answerArray, option];
    } else {
      answers[questionId] = answerArray.filter((v) => v !== option);
    }
  }

  // Reset children ages if user switches to "No"
  $: if (hasChildren === 'No') {
    childrenAges = [];
  }

  // Update answers when hasChildren changes
  $: if (hasChildren !== null) {
    answers['hasChildren'] = hasChildren;
  }

  // Update children ages in answers
  $: if (hasChildren === 'Yes') {
    answers['childrenAges'] = childrenAges.map(String);
  } else {
    delete answers['childrenAges'];
  }

  async function handleSubmit(event: Event) {
    event.preventDefault();
    isSubmitting = true;

    try {
      const requiredQuestions = questions.filter((q) => q.required);
      const missingFields = requiredQuestions.filter((q) => {
        const answer = answers[q.id];
        if (answer === null || answer === undefined) return true;
        if (typeof answer === 'string') return answer.trim().length === 0;
        if (Array.isArray(answer)) return answer.length === 0;
        return false;
      });

      if (missingFields.length > 0) {
        alert(`Please fill in all required fields: ${missingFields.map((q) => q.label).join(', ')}`);
        isSubmitting = false;
        return;
      }

      const submissionData = {
        ...answers,
        timestamp: new Date().toISOString()
      };

      const res = await fetch('/api/save-response', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(submissionData)
      });

      if (!res.ok) {
        throw new Error('Failed to save response');
      }

      await goto('/questionnaire/thanks');
    } catch (error) {
      console.error('Submission error:', error);
      alert('An error occurred while submitting. Please try again.');
    } finally {
      isSubmitting = false;
    }
  }
</script>

<main class="min-h-screen bg-gray-100">
  <section class="max-w-3xl mx-auto px-4 py-10 md:py-16">
    <div class="rounded-2xl bg-white shadow-xl overflow-hidden">
      <div class="p-6 md:p-8 flex flex-col gap-6">
        <header class="space-y-1">
          <h1 class="text-2xl md:text-3xl font-bold text-gray-900">Questionnaire</h1>
          <p class="text-gray-600">
            Please complete the form below. Fields marked as required must be filled in.
          </p>
        </header>

        <form class="grid gap-6" on:submit={handleSubmit}>
          {#each questions as question}
            {#if question.id === 'hasChildren' && question.type === 'radio'}
              <div class="space-y-2">
                <div class="flex items-baseline gap-1">
                  <span class="text-sm font-medium text-gray-700">{question.label}</span>
                  {#if question.required}<span class="text-red-600">*</span>{/if}
                </div>
                <div class="flex gap-6">
                  {#each question.options as option}
                    <label class="flex items-center gap-2 cursor-pointer">
                      <input
                        type="radio"
                        class="h-4 w-4 accent-primary"
                        name={question.id}
                        value={option}
                        bind:group={hasChildren}
                        required={question.required}
                      />
                      <span class="text-gray-700">{option}</span>
                    </label>
                  {/each}
                </div>

                {#if hasChildren === 'Yes'}
                  <div class="mt-4 space-y-4">
                    <h3 class="font-semibold text-sm text-gray-800">Children's ages</h3>
                    {#each childrenAges as age, index}
                      <div class="flex items-center gap-3">
                        <input
                          type="number"
                          min="0"
                          max="18"
                          class="w-24 rounded-lg border border-gray-300 px-3 py-2 focus:border-primary focus:ring-1 focus:ring-primary"
                          bind:value={childrenAges[index]}
                          placeholder="Age"
                        />
                        <button
                          type="button"
                          class="inline-flex items-center justify-center w-10 h-10 rounded-lg border border-red-500 text-red-600 hover:bg-red-50 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-1"
                          on:click={() => removeChild(index)}
                          aria-label="Remove child"
                        >
                          −
                        </button>
                      </div>
                    {/each}
                    <button
                      type="button"
                      class="text-sm font-medium text-primary hover:underline"
                      on:click={addChild}
                    >
                      + Add child
                    </button>
                  </div>
                {/if}
              </div>
            {:else if question.id === 'cookingMethod'}
              <div class="space-y-2">
                <label for={question.id} class="flex items-baseline gap-1">
                  <span class="text-sm font-medium text-gray-700">{question.label}</span>
                  {#if question.required}<span class="text-red-600">*</span>{/if}
                </label>
                <input
                  id={question.id}
                  type="text"
                  class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-primary focus:ring-1 focus:ring-primary"
                  placeholder={question.type === 'text' ? question.placeholder : undefined}
                  list="cooking-methods"
                  bind:value={answers[question.id]}
                  required={question.required}
                />
                <datalist id="cooking-methods">
                  <option value="Air Fried"></option>
                  <option value="Deep Fried"></option>
                  <option value="Baked"></option>
                </datalist>
              </div>
            {:else if question.type === 'text'}
              <div class="space-y-2">
                <label for={question.id} class="flex items-baseline gap-1">
                  <span class="text-sm font-medium text-gray-700">{question.label}</span>
                  {#if question.required}<span class="text-red-600">*</span>{/if}
                </label>
                <input
                  id={question.id}
                  class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-primary focus:ring-1 focus:ring-primary"
                  type="text"
                  placeholder={question.placeholder}
                  bind:value={answers[question.id]}
                  required={question.required}
                  autocomplete={question.id === 'fullName' ? 'name' : undefined}
                />
              </div>
            {:else if question.type === 'number'}
              <div class="space-y-2">
                <label for={question.id} class="flex items-baseline gap-1">
                  <span class="text-sm font-medium text-gray-700">{question.label}</span>
                  {#if question.required}<span class="text-red-600">*</span>{/if}
                </label>
                <input
                  id={question.id}
                  class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-primary focus:ring-1 focus:ring-primary"
                  type="number"
                  bind:value={answers[question.id]}
                  required={question.required}
                  min={question.id === 'age' ? 1 : undefined}
                  max={question.id === 'age' ? 100 : undefined}
                  inputmode={question.id === 'age' ? 'numeric' : undefined}
                />
                {#if question.id === 'age'}
                  <p class="text-xs text-gray-500 mt-1">Must be between 1 and 100</p>
                {/if}
              </div>
            {:else if question.type === 'radio'}
              <div class="space-y-2">
                <div class="flex items-baseline gap-1">
                  <span class="text-sm font-medium text-gray-700">{question.label}</span>
                  {#if question.required}<span class="text-red-600">*</span>{/if}
                </div>
                <div class="flex gap-6">
                  {#each question.type === 'radio' ? question.options : [] as option}
                    <label class="flex items-center gap-2 cursor-pointer">
                      <input
                        type="radio"
                        class="h-4 w-4 accent-primary"
                        name={question.id}
                        value={option}
                        bind:group={answers[question.id]}
                        required={question.required}
                      />
                      <span class="text-gray-700">{option}</span>
                    </label>
                  {/each}
                </div>
              </div>
            {:else if question.type === 'checkbox'}
              <div class="space-y-2">
                <div class="flex items-baseline gap-1">
                  <span class="text-sm font-medium text-gray-700">{question.label}</span>
                  {#if question.required}<span class="text-red-600">*</span>{/if}
                </div>
                <div class="flex flex-col gap-3">
                  {#each question.options as option}
                    <label class="flex items-center gap-2 cursor-pointer">
                      <input
                        type="checkbox"
                        class="h-4 w-4 rounded border-gray-300 accent-primary"
                        value={option}
                        checked={(() => {
                          const answer = answers[question.id];
                          return Array.isArray(answer) && answer.includes(option);
                        })()}
                        on:change={(e) => {
                          handleCheckboxChange(question.id, option, e.currentTarget.checked);
                        }}
                      />
                      <span class="text-gray-700">{option}</span>
                    </label>
                  {/each}
                </div>
              </div>
            {:else if question.type === 'rating'}
              <div class="space-y-2">
                <div class="flex items-baseline gap-1">
                  <span class="text-sm font-medium text-gray-700">{question.label}</span>
                  {#if question.required}<span class="text-red-600">*</span>{/if}
                </div>
                <div class="flex gap-2 flex-wrap">
                  {#each Array(question.scale) as _, i}
                    <button
                      type="button"
                      class="w-10 h-10 rounded-full text-sm font-medium border-2 transition-colors focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-1 {answers[question.id] === i + 1
                        ? 'border-primary bg-primary text-white'
                        : 'border-gray-300 bg-white text-gray-700 hover:border-primary hover:bg-primary-light'}"
                      on:click={() => {
                        answers[question.id] = i + 1;
                      }}
                    >
                      {i + 1}
                    </button>
                  {/each}
                </div>
              </div>
            {/if}
          {/each}

          <div class="border-t border-gray-200 pt-4 mt-2"></div>

          <div class="flex justify-end">
            <button
              type="submit"
              class="inline-flex items-center justify-center gap-2 px-6 py-3 rounded-lg bg-primary text-white font-medium hover:bg-primary-hover focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 disabled:opacity-60 disabled:pointer-events-none transition-colors"
              disabled={isSubmitting}
            >
              {#if isSubmitting}
                <span class="spinner" aria-hidden="true"></span>
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
