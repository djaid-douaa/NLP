// Select elements from the DOM
const readAloudButton = document.getElementById("read-aloud-btn");
const pauseButton = document.getElementById("pause-btn");
const resumeButton = document.getElementById("resume-btn");
const stopButton = document.getElementById("stop-btn");
const enableSpeechCheckbox = document.getElementById("enable-speech");
const scrollableStory = document.getElementById("scrollable-story");

// Initialize the SpeechSynthesisUtterance object
let speech = null;
let scrollInterval = null;

const initializeSpeech = () => {
  const storyText = scrollableStory.innerText;
  speech = new SpeechSynthesisUtterance(storyText);
  speech.lang = "ar"; // Set language to Arabic
  speech.rate = 0.9; // Adjust speech speed

  // Synchronize scrolling with speech
  speech.onboundary = (event) => {
    const words = storyText.split(" ");
    const wordIndex = Math.floor(
      event.charIndex / (storyText.length / words.length)
    );
    const scrollStep =
      (wordIndex / words.length) * scrollableStory.scrollHeight;

    // Clear previous interval if it exists
    if (scrollInterval) {
      clearInterval(scrollInterval);
    }

    // Update scroll position gradually
    scrollInterval = setInterval(() => {
      if (scrollableStory.scrollTop < scrollStep) {
        scrollableStory.scrollTop += 2; // Adjust this increment for smoother scrolling
      } else {
        clearInterval(scrollInterval); // Stop scrolling once the target scroll position is reached
      }
    }, 700); // Adjust this delay for smoother scrolling speed
  };
};

// Read Aloud button click event
readAloudButton.addEventListener("click", () => {
  if (enableSpeechCheckbox.checked) {
    if (!speech) initializeSpeech();
    speechSynthesis.speak(speech);
  } else {
    alert("تم تعطيل الصوت من قبل الوالد.");
  }
});

// Pause button click event
pauseButton.addEventListener("click", () => {
  if (speechSynthesis.speaking) speechSynthesis.pause();
  clearInterval(scrollInterval); // Clear the scroll interval immediately when paused
});

// Resume button click event
resumeButton.addEventListener("click", () => {
  if (speechSynthesis.paused) speechSynthesis.resume();
});

// Stop button click event
stopButton.addEventListener("click", () => {
  speechSynthesis.cancel();
  clearInterval(scrollInterval); // Clear the scroll interval immediately when stopped
  scrollableStory.scrollTop = 0; // Reset scroll position
  speech = null; // Reset speech to reinitialize
});
