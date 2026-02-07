<script lang="ts">
  import logo from '$lib/assets/CMI_logo.png';
</script>

<main class="min-h-screen bg-gray-100">
  <section class="max-w-6xl mx-auto px-4 py-10 md:py-16">
    <div class="grid gap-8 md:grid-cols-2 items-center">
      <!-- Brand / image -->
      <div class="flex justify-center md:justify-start">
        <div class="rounded-2xl bg-white shadow-xl w-full max-w-md overflow-hidden">
          <div class="p-6 flex flex-col items-center text-center gap-6">
            <div class="w-full flex justify-center">
              <div class="w-full max-w-xs">
                <figure class="rounded-2xl overflow-hidden bg-gray-200">
                  <img src={logo} alt="CMI Logo" class="w-full h-full object-contain p-4" />
                </figure>
              </div>
            </div>

            <div class="space-y-2">
              <h1 class="text-3xl md:text-4xl font-bold tracking-tight text-primary">
                BBQ Chicken Pocket
              </h1>
              <p class="text-gray-600">
                You were required to try 2 BBQ flavours (BBQ A and BBQ B)<br>
                Please try A first and then move onto B
              </p>
            </div>

            <div class="grid grid-cols-2 sm:flex sm:flex-row gap-4 w-full rounded-xl bg-gray-200 p-4 shadow-inner">
              <div class="text-center">
                <div class="text-xs font-medium uppercase tracking-wide text-gray-500">Time</div>
                <div class="text-lg font-semibold text-gray-800">2–3 min</div>
              </div>
              <div class="text-center">
                <div class="text-xs font-medium uppercase tracking-wide text-gray-500">Questions</div>
                <div class="text-lg font-semibold text-gray-800">Short</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- CTA -->
      <div class="flex justify-center md:justify-end">
        <div class="rounded-2xl bg-white shadow-xl w-full max-w-xl overflow-hidden">
          <div class="p-6 flex flex-col gap-6">
            <div class="space-y-2">
              <h2 class="text-xl md:text-2xl font-semibold text-gray-900">
                Tasting Questionnaire
              </h2>
              <p class="text-gray-600">
                Please answer honestly. Your responses are used for internal product testing only.
              </p>
            </div>

            <div class="flex justify-end">
              <a
                href="/questionnaire"
                class="inline-flex items-center justify-center px-6 py-3 rounded-lg bg-primary text-white font-medium hover:bg-primary-hover focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 transition-colors"
                aria-label="Start the tasting questionnaire"
              >
                Begin questionnaire
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</main>
