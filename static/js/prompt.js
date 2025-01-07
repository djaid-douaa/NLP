// Establish WebSocket connection

const socket = io("http://localhost:8000", {
  transports: ["websocket"],
  path: "/socket.io",
});

socket.on("connect", () => {
  console.log("Connected to server with ID:", socket.id);
});

socket.on("disconnect", () => {
  console.log("Disconnected from server");
});

socket.on("partial_response", (data) => {
  console.log(data);
  updateStoryContent(data.content);
});

socket.on("final_response", (data) => {
  console.log(data);
});

socket.on("error", (data) => {
  console.error("Error:", data.error);
});

// Function to capture values and store them in a JSON object
function generateStoryData() {
  // Get the selected age value
  const ageButtons = document.querySelectorAll(".age-button");
  let selectedAge = "";
  ageButtons.forEach((button) => {
    if (button.classList.contains("selected")) {
      selectedAge = button.innerText;
    }
  });

  // Get the selected value from the dropdown or the custom value input
  const selectedValue = document.getElementById("value-selector").value;
  const customValue = document.getElementById("custom-value").value;
  const value = customValue || selectedValue;

  // Get the input prompt (story description)
  const storyPrompt = document.getElementById("storyPrompt").value;

  // Create the JSON object
  const storyData = {
    age_category: selectedAge,
    moral: value,
    user_prompt: storyPrompt,
  };

  console.log("Generated story data:", JSON.stringify(storyData));
  return storyData;
}

// Function to send the generated story data
function sendStoryData(storyData) {
  socket.emit("chat", storyData);
  console.log("Story data sent to server.");
}

// Function to show the story title
function showStory() {
  document.querySelector("#story-title").style.display = "block";
  document.querySelector("#scrollable-story").style.display = "block";
}

// Function to update story content based on partial responses
function updateStoryContent(content) {
  processResponse(content);
}

// Function to handle final response and show the full story

function removeBeforePattern(input, pattern) {
  const index = input.indexOf(pattern);
  if (index === -1) {
    // If the pattern is not found, return the original string
    return input;
  }
  // Remove everything before and including the pattern
  return input.slice(index + pattern.length);
}
function processResponse(response) {
  console.log("Final story response:", response);

  // Extract the title and story from the response
  const [title, story] = response.split("\n### القصة:\n");

  if (title) {
    cleantitle = String(title)
      .replaceAll("###", "")
      .replaceAll("العنوان", "")
      .replaceAll(":", "");
    displayStoryTitle(cleantitle);
  }
  if (story) {
    const regex = /### العنوان:.*### القصة:/s;
    const cleanedStory = story.replace(regex, "");
    console.log(cleanedStory);
    displayStoryContent(cleanedStory);
  }
}

// Function to display the title
function displayStoryTitle(title) {
  const titleElement = document.querySelector("#story-title");
  titleElement.textContent = title;
  showStory(); // Show the title section
}

// Function to display the story content
function displayStoryContent(story) {
  const storyContainer = document.querySelector("#scrollable-story");
  storyContainer.textContent = story;
}

// Add event listeners to the age buttons to mark them as selected
function setupAgeButtonListeners() {
  const ageButtons = document.querySelectorAll(".age-button");
  ageButtons.forEach((button) => {
    button.addEventListener("click", () => {
      // Remove 'selected' class from all buttons
      ageButtons.forEach((btn) => btn.classList.remove("selected"));
      button.classList.add("selected");
    });
  });
}

// Function to initiate story generation and socket communication

// Example of how to call `initiateStoryGeneration` when submitting the form
document.getElementById("submit-button").addEventListener("click", (e) => {
  e.preventDefault();
  const storyData = generateStoryData();
  sendStoryData(storyData);
});

// Initialize age button listeners on page load
setupAgeButtonListeners();
