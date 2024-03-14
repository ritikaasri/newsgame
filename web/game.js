let gameDict = [];

// Fetch CSV and parse to array

const filePath = "data/main.csv";

function fetchAndParseCSV() {
  fetch(filePath)
    .then(response => response.text())
    .then(csvText => {
      // Use PapaParse to parse the CSV text
      Papa.parse(csvText, {
        header: true,
        skipEmptyLines: true,
        complete: function(results) {
          gameDict = results.data.map(row => ({
            group_id: row.group_id,
            keywords: row.keywords ? row.keywords.split(', ') : [],
            title: row.title,
            url: row.url
          }));
          // Start game when CSV data is loaded.
          startGame();
        }
      });
    });
}

fetchAndParseCSV(filePath);

let correctGroups = 0;
let identifiedGroups = [];
let totalLives = 4;

function startGame() {
    const container = document.getElementById("words-container");
    container.innerHTML = ""; // Clear previous words

    // Take gamewords from gameDict
    let gameWords = [];
    gameDict.forEach(group => {
        group.keywords.forEach(keyword => {
            gameWords.push({ word: keyword, group: group.group_id });
        });
    });

    // Shuffle the gamewords
    gameWords = shuffleArray(gameWords);
    console.log(gameWords);
    
    // Render the gamewords
    gameWords.forEach(item => {
        if (!identifiedGroups.includes(item.group)) {
            const wordElement = document.createElement("div");
            wordElement.classList.add("word");
            wordElement.textContent = item.word;
            wordElement.onclick = () => selectWord({ word: item.word, group: item.group }, wordElement);
            container.appendChild(wordElement);
        }
    })
}
// Shuffle array function
function shuffleArray(array) {
    for (let i = array.length -1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}

let selectedWords = [];

// Player word selection

function selectWord(word, element) {
    if (identifiedGroups.includes(word.group)) {
        return;
    }

    const index = selectedWords.findIndex(selected => selected.word === word.word);
    if (index > -1) {
        selectedWords.splice(index, 1);
        element.style.backgroundColor = "#ddd";
    } else if (selectedWords.length < 4) {
        selectedWords.push(word);
        element.style.backgroundColor = "#aaddaa";
        console.log("Selected Group:", selectedWords);
    }
}

// Submit guess

document.getElementById("submit").addEventListener("click", function() {
    var isSameGroup = checkAnswer(selectedWords);
    // Not enough words selected
    if (selectedWords.length < 4) {
        document.getElementById("result").textContent = "You need to select more words!";
        return;
    }
    // Wrong answer
    if (isSameGroup === false) { 
        document.getElementById("result").textContent = "Wrong answer - try again!";
        deductLife();
    } else {
        // Correct answer
        var groupIdentified = selectedWords[0].group;
        if (!identifiedGroups.includes(groupIdentified)) {
            identifiedGroups.push(groupIdentified);
            correctGroups += 1;
            moveToTop(groupIdentified);
        }
        document.getElementById("result").textContent = "Correct! Read the article or carry on playing.";
        // Completed game
        if (correctGroups === 4) {
            document.getElementById("result").textContent = "You have completed the news!";
        }
        selectedWords = [];
        startGame();
    }
});

// Check answer function

function checkAnswer(selectedWords) {
    const firstGroup = selectedWords[0].group;
    for (let i = 1; i < selectedWords.length; i++) {
        if (selectedWords[i].group !== firstGroup) {
            return false;
        }
    }
    return true;
}

// Function to deduct a life
function deductLife() {
    totalLives--;

    // Update the UI to show remaining lives
    let livesContainer = document.querySelector(".lives-container");
    livesContainer.innerHTML = ""; // Clear previous lives

    for (let i = 0; i < totalLives; i++) {
        let lifeIcon = document.createElement("i");
        lifeIcon.classList.add("fas", "fa-heart");
        livesContainer.appendChild(lifeIcon);
    }

    // Check if game over
    if (totalLives === 0) {
        gameOver();
    }
}

// Function to handle game over
function gameOver() {
    document.getElementById("result").textContent = "Game over! Come back for a new puzzle tomorrow.";
}


// Move correct answers to top

function moveToTop(groupIdentified) {
    var container2 = document.getElementById("identified-groups");

    // Get group from gamedict
    var groupData = gameDict.find(function(group) {
        return group.group_id === groupIdentified;
    });

    // Group container
    var groupContainer = document.createElement("div");
    groupContainer.classList.add("group-container");
    container2.appendChild(groupContainer);

    // Add word tiles to container
    groupData.keywords.forEach(function(keyword) {
        var wordElement = document.createElement("div");
        wordElement.classList.add("word");
        wordElement.textContent = keyword;
        groupContainer.appendChild(wordElement);
    });

    // Add group title and hyperlink below completed group
    var titleElement = document.createElement("a");
    titleElement.classList.add("group-title");
    titleElement.textContent = groupData.title;
    titleElement.href = groupData.url;
    titleElement.target = "_blank";
    groupContainer.appendChild(titleElement)
}
 

startGame();
