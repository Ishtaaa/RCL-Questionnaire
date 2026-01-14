<script lang="ts">
    let pageState = 0;
    let questionCount = 0;
  let hasChildren: 'yes' | 'no' | null = null;
  let children: number[] = [];

  type Question =
	| { id: string; question: string; type: 'text' }
	| { id: string; question: string; type: 'rating'; scale: number }
	| { id: string; question: string; type: 'radio'; options: string[] };


  function addChild() {
    children = [...children, 0];
  }

  function removeChild(index: number) {
    children = children.filter((_, i) => i !== index);
  }

  // Reset children if user switches to "no"
  $: if (hasChildren === 'no') {
    children = [];
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
    {#if pageState==0}
        <form class="grid gap-6">
          <div class="form-control">
            <label class="label" for="full-name">
              <span class="label-text font-medium">Full name</span>
            </label>
            <input
              id="full-name"
              type="text"
              class="input input-bordered w-full"
              placeholder="e.g. Jane Doe"
              autocomplete="name"
              required
            />
          </div>

          <div class="form-control">
            <label class="label" for="age">
              <span class="label-text font-medium">Age</span>
            </label>
            <input
              id="age"
              type="number"
              class="input input-bordered w-full"
              required
              placeholder="18"
              min="1"
              max="100"
              inputmode="numeric"
            />
            <p class="text-xs text-base-content/70 mt-2">Must be between 1 and 100</p>
          </div>

          <div class="space-y-6 max-w-md">
            <!-- Question -->
            <div>
                <label class="label font-semibold">
                    <span class="label-text">Do you have children?</span>
                </label>
        
                <div class="flex gap-6">
                    <label class="label cursor-pointer gap-2">
                        <input
                            type="radio"
                            name="children"
                            class="radio radio-primary"
                            bind:group={hasChildren}
                            value="yes"
                        />
                        <span class="label-text">Yes</span>
                    </label>
        
                    <label class="label cursor-pointer gap-2">
                        <input
                            type="radio"
                            name="children"
                            class="radio radio-primary"
                            bind:group={hasChildren}
                            value="no"
                        />
                        <span class="label-text">No</span>
                    </label>
                </div>
            </div>
        
            <!-- Children ages -->
            {#if hasChildren === 'yes'}
                <div class="space-y-4">
                    <h3 class="font-semibold">Children's ages</h3>
        
                    {#each children as age, index}
                        <div class="flex items-center gap-3">
                            <input
                                type="number"
                                min="0"
                                class="input input-bordered w-24"
                                bind:value={children[index]}
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

            <div class="form-control">
              <label class="label" for="cooking-method">
                <span class="label-text font-medium">Which Method did you use to cook the pocket?</span>
              </label>
              <input
                id="cooking-method"
                type="text"
                class="input input-bordered w-full"
                placeholder="e.g. Air Fried"
                list = "cooking-methods"
                required
              />
              <datalist id="cooking-methods">
                <option value="Air Fried"></option>
                <option value="Deep Fried"></option>
                <option value="Baked"></option>
              </datalist>
            </div>
        
            <div class="form-control">
                <label class="label" for="consumer">
                  <span class="label-text font-medium">Who ate the BBQ Chicken Pocket in your Household?</span>
                </label>
                <div class="flex flex-col space-y-4">
                    <div class="flex items-center">
                      <input
                        id="option1"
                        type="checkbox"
                        class="h-4 w-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500"
                      />
                      <label for="option1" class="ml-3 text-sm font-medium text-gray-900">
                        Myself
                      </label>
                    </div>
                    <div class="flex items-center">
                      <input
                        id="option2"
                        type="checkbox"
                        class="h-4 w-4  bg-gray-100 border-gray-300 rounded focus:primary"
                      />
                      <label for="option2" class="ml-3 text-sm font-medium text-gray-900">
                        My Kids
                      </label>
                    </div>
                    <div class="flex items-center">
                      <input
                        id="option3"
                        type="checkbox"
                        class="h-4 w-4  bg-gray-100 border-gray-300 rounded focus:ring-blue-500"
                      />
                      <label for="option3" class="ml-3 text-sm font-medium text-gray-900">
                        My Husband/ Wife/ Partner
                      </label>
                      

                    </div>

                    <div class="flex items-center">
                        <input
                          id="option3"
                          type="checkbox"
                          class="h-4 w-4  bg-gray-100 border-gray-300 rounded focus:ring-blue-500"
                        />
                        <label for="option3" class="ml-3 text-sm font-medium text-gray-900">
                          Other
                        </label>
                  </div>
              </div>

              <div class="form-control">
                <label class="label" for="consumer">
                  <span class="label-text font-medium">What Occasion/s did you eat it for?</span>
                </label>
                <div class="flex flex-col space-y-4">
                    <div class="flex items-center">
                      <input
                        id="option1"
                        type="checkbox"
                        class="h-4 w-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500"
                      />
                      <label for="option1" class="ml-3 text-sm font-medium text-gray-900">
                        Breakfast 
                      </label>
                    </div>
                    <div class="flex items-center">
                      <input
                        id="option2"
                        type="checkbox"
                        class="h-4 w-4  bg-gray-100 border-gray-300 rounded focus:primary"
                      />
                      <label for="option2" class="ml-3 text-sm font-medium text-gray-900">
                        Lunch
                      </label>
                    </div>
                    <div class="flex items-center">
                      <input
                        id="option3"
                        type="checkbox"
                        class="h-4 w-4  bg-gray-100 border-gray-300 rounded focus:ring-blue-500"
                      />
                      <label for="option3" class="ml-3 text-sm font-medium text-gray-900">
                        Dinner
                      </label>
                      

                    </div>

                    <div class="flex items-center">
                        <input
                          id="option3"
                          type="checkbox"
                          class="h-4 w-4  bg-gray-100 border-gray-300 rounded focus:ring-blue-500"
                        />
                        <label for="option3" class="ml-3 text-sm font-medium text-gray-900">
                          Snack
                        </label>
                  </div>
              </div>
        

         
        </form>
        
        {/if}
        <div class="divider my-2"></div>

        <div class="card-actions justify-end">
          <button class="btn btn-primary">Submit</button>
        </div>
      </div>
    </div>
  </section>
</main>