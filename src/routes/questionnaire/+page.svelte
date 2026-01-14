<script lang="ts">
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
      // Validate required fields
      const requiredQuestions = questions.filter((q) => q.required);
      const missingFields = requiredQuestions.filter((q) => {
        const answer = answers[q.id];
        return !answer || (Array.isArray(answer) && answer.length === 0);
      });

      if (missingFields.length > 0) {
        alert(`Please fill in all required fields: ${missingFields.map((q) => q.label).join(', ')}`);
        isSubmitting = false;
        return;
      }

      // Prepare submission data
      const submissionData = {
        ...answers,
        timestamp: new Date().toISOString()
      };

      // Here you would typically send the data to your backend
      console.log('Form submission:', submissionData);

      // Simulate API call
      await new Promise((resolve) => setTimeout(resolve, 1000));

      alert('Thank you! Your responses have been submitted successfully.');
      
      // Reset form
      answers = {};
      hasChildren = null;
      childrenAges = [];
    } catch (error) {
      console.error('Submission error:', error);
      alert('An error occurred while submitting. Please try again.');
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
          <p class="text-base-content/70">
            Please complete the form below. Fields marked as required must be filled in.
          </p>
        </header>

        <form class="grid gap-6" on:submit={handleSubmit}>
          {#each questions as question}
            {#if question.id === 'hasChildren' && question.type === 'radio'}
              <!-- Special handling for children question -->
              <div class="form-control">
                <label class="label">
                  <span class="label-text font-medium">{question.label}</span>
                  {#if question.required}
                    <span class="text-error">*</span>
                  {/if}
                </label>
                <div class="flex gap-6">
                  {#each question.options as option}
                    <label class="label cursor-pointer gap-2">
                      <input
                        type="radio"
                        class="radio radio-primary"
                        name={question.id}
                        value={option}
                        bind:group={hasChildren}
                        required={question.required}
                      />
                      <span class="label-text">{option}</span>
                    </label>
                  {/each}
                </div>

                {#if hasChildren === 'Yes'}
                  <div class="mt-4 space-y-4">
                    <h3 class="font-semibold text-sm">Children's ages</h3>
                    {#each childrenAges as age, index}
                      <div class="flex items-center gap-3">
                        <input
                          type="number"
                          min="0"
                          max="18"
                          class="input input-bordered w-24"
                          bind:value={childrenAges[index]}
                          placeholder="Age"
                        />
                        <button
                          type="button"
                          class="btn btn-square btn-outline btn-error"
                          on:click={() => removeChild(index)}
                          aria-label="Remove child"
                        >
                          −
                        </button>
                      </div>
                    {/each}
                    <button
                      type="button"
                      class="btn btn-sm btn-outline btn-secondary"
                      on:click={addChild}
                    >
                      + Add child
                    </button>
                  </div>
                {/if}
              </div>
            {:else if question.id === 'cookingMethod'}
              <!-- Special handling for cooking method with datalist -->
              <div class="form-control">
                <label class="label" for={question.id}>
                  <span class="label-text font-medium">{question.label}</span>
                  {#if question.required}
                    <span class="text-error">*</span>
                  {/if}
                </label>
                <input
                  id={question.id}
                  type="text"
                  class="input input-bordered w-full"
                  placeholder={question.type === 'text' ? question.placeholder : undefined}
                  list="cooking-methods"
                  bind:value={answers[question.id]}
                  required={question.required}
                />
                <datalist id="cooking-methods">
                  <option value="Air Fried" />
                  <option value="Deep Fried" />
                  <option value="Baked" />
                </datalist>
              </div>
            {:else if question.type === 'text'}
              <div class="form-control">
                <label class="label" for={question.id}>
                  <span class="label-text font-medium">{question.label}</span>
                  {#if question.required}
                    <span class="text-error">*</span>
                  {/if}
                </label>
                <input
                  id={question.id}
                  class="input input-bordered w-full"
                  type="text"
                  placeholder={question.placeholder}
                  bind:value={answers[question.id]}
                  required={question.required}
                  autocomplete={question.id === 'fullName' ? 'name' : undefined}
                />
              </div>
            {:else if question.type === 'number'}
              <div class="form-control">
                <label class="label" for={question.id}>
                  <span class="label-text font-medium">{question.label}</span>
                  {#if question.required}
                    <span class="text-error">*</span>
                  {/if}
                </label>
                <input
                  id={question.id}
                  class="input input-bordered w-full"
                  type="number"
                  bind:value={answers[question.id]}
                  required={question.required}
                  min={question.id === 'age' ? 1 : undefined}
                  max={question.id === 'age' ? 100 : undefined}
                  inputmode={question.id === 'age' ? 'numeric' : undefined}
                />
                {#if question.id === 'age'}
                  <p class="text-xs text-base-content/70 mt-2">Must be between 1 and 100</p>
                {/if}
              </div>
            {:else if question.type === 'radio'}
              <div class="form-control">
                <label class="label">
                  <span class="label-text font-medium">{question.label}</span>
                  {#if question.required}
                    <span class="text-error">*</span>
                  {/if}
                </label>
                <div class="flex gap-6">
                  {#each question.type === 'radio' ? question.options : [] as option}
                    <label class="label cursor-pointer gap-2">
                      <input
                        type="radio"
                        class="radio radio-primary"
                        name={question.id}
                        value={option}
                        bind:group={answers[question.id]}
                        required={question.required}
                      />
                      <span class="label-text">{option}</span>
                    </label>
                  {/each}
                </div>
              </div>
            {:else if question.type === 'checkbox'}
              <div class="form-control">
                <label class="label">
                  <span class="label-text font-medium">{question.label}</span>
                  {#if question.required}
                    <span class="text-error">*</span>
                  {/if}
                </label>
                <div class="flex flex-col gap-3">
                  {#each question.options as option}
                    <label class="flex items-center gap-2 cursor-pointer">
                      <input
                        type="checkbox"
                        class="checkbox checkbox-primary"
                        value={option}
                        checked={(() => {
                          const answer = answers[question.id];
                          return Array.isArray(answer) && answer.includes(option);
                        })()}
                        on:change={(e) => {
                          handleCheckboxChange(question.id, option, e.currentTarget.checked);
                        }}
                      />
                      <span class="label-text">{option}</span>
                    </label>
                  {/each}
                </div>
              </div>
            {:else if question.type === 'rating'}
              <div class="form-control">
                <label class="label">
                  <span class="label-text font-medium">{question.label}</span>
                  {#if question.required}
                    <span class="text-error">*</span>
                  {/if}
                </label>
                <div class="flex gap-2">
                  {#each Array(question.scale) as _, i}
                    <button
                      type="button"
                      class="btn btn-circle btn-outline"
                      class:btn-primary={answers[question.id] === i + 1}
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
