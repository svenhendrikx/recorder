<script>
  import { onMount } from "svelte";
  import { writable } from "svelte/store";

  const recordingState = writable(false);
  let recorder;
  let chunks = [];

  onMount(async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    recorder = new MediaRecorder(stream);

    console.log(recorder)
    recorder.addEventListener("dataavailable", (event) => {
      chunks.push(event.data);
    });

    recorder.addEventListener("stop", async () => {
      const blob = new Blob(chunks, { type: "audio/webm" });
      const formData = new FormData();
      formData.append("audio", blob);
      console.log(formData)
      await fetch("/recording", { method: "POST", body: formData });

      chunks = [];
    });
  });

  async function toggleRecording() {
    if (recorder.state === "inactive") {
      recorder.start();
      recordingState.set(true);
    } else {
      recorder.stop();
      recordingState.set(false);
    }
  }
</script>

<main>
    <div class="title">
        Recorder
    </div>
    <div class="container">
        <div

      class="button"
      on:click={toggleRecording}
      on:keydown={(e) => { if (e.key === 'Enter' || e.key === ' ') toggleRecording(); }}
      class:recording={$recordingState}
      tabindex="0"
      role="button"
      aria-label="Toggle recording"
    >
        </div>
    </div>

</main>

<style>
    main {
        text-align: center;
        padding: 1em;
        max-width: 240px;
        margin: 0 auto;
        font-family:monospace;
        font-size: 40px;
    }

    @media (min-width: 640px) {
        main {
            max-width: none;
        }
    }
    .button {
    background-color: #e6e6e6;
    border-radius: 50%;
    width: 50px;
    height: 50px;
    display: flex;
    justify-content: center;
    align-items: center;
    box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);
    cursor: pointer;
  }
  .button.recording{
        background-color: #d00;
        animation: pulse 1s infinite;
      }
    @keyframes pulse {
        0% {
          transform: scale(1);
        }
        50% {
          transform: scale(1.1);
        }
        100% {
          transform: scale(1);
        }
    }
    .container {
      display: flex;
      justify-content: center;
      align-items: center;
      height: 60vh;
    }


    .title {
      display: flex;
      justify-content: center;
      align-items: center;
      height: 20vh;
    }
</style>
