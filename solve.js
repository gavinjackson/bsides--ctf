// Pensig Puzzle Solver
const QUOTE='AAAA AA A ABBABB ABAC BCCAB A BCDCB CB CDEDC DCDDEIDDCEDEDHIDEDHEIEIKEEEIFKENMEHIMINIONIINNNRNONNNRORSRRRRRSRSTSSRSSSSSUWUSUST';
const WIDTH = 9;

// Column bags as given
const bags = [
  ['I','D','S','O','M','H','E','A','R','B','N','C'],
  ['A','S','A','D','I','B','E','R','N','A','F','A','S','C'],
  ['I','K','R','E','D','S','N','A','T','U','B','C'],
  ['D','D','S','B','R','B','W','N','E','A','E','I','C'],
  ['D','R','I','B','U','S','H','O','N','C','O','A','E'],
  ['I','N','K','I','R','E','M','A','D','R','N','B','S','C'],
  ['D','I','E','U','B','C','D','E','S','A','N','D','R','C'],
  ['R','A','E','S','H','S','E','N','D','I','B','C'],
  ['S','B','R','S','I','D','A','E','A','T','N','C']
];

// Required positions for SKATEBOARD+CANINE in final solution string
const required = [
  {idx: 7, letter: 'S'},   // (0,7)
  {idx: 11, letter: 'K'},  // (1,2) 
  {idx: 15, letter: 'A'},  // (1,6)
  {idx: 16, letter: 'T'},  // (1,7)
  {idx: 20, letter: 'E'},  // (2,2)
  {idx: 23, letter: 'B'},  // (2,5)
  {idx: 31, letter: 'O'},  // (3,4)
  {idx: 37, letter: 'A'},  // (4,1)
  {idx: 47, letter: 'R'},  // (5,2)
  {idx: 56, letter: 'D'},  // (6,2)
  {idx: 70, letter: 'C'},  // (7,7)
  {idx: 71, letter: 'A'},  // (7,8)
  {idx: 80, letter: 'N'},  // (8,8)
  {idx: 90, letter: 'I'},  // (10,0)
  {idx: 104, letter: 'N'}, // (11,5)
  {idx: 113, letter: 'E'}  // (12,5)
];

// Create solution grid from QUOTE
const HEIGHT = Math.ceil(QUOTE.length / WIDTH);
const solution = Array(HEIGHT).fill().map(() => Array(WIDTH).fill(''));

// Fill grid based on QUOTE
for(let i = 0; i < QUOTE.length; i++) {
  const row = Math.floor(i / WIDTH);
  const col = i % WIDTH;
  const ch = QUOTE[i];
  
  if(ch === ' ') {
    solution[row][col] = null; // blank cell
  } else if(/[A-Z]/.test(ch)) {
    solution[row][col] = ''; // fillable cell
  } else {
    solution[row][col] = ch; // fixed cell
  }
}

console.log('Grid layout (null=blank, ""=fillable, letter=fixed):');
for(let r = 0; r < HEIGHT; r++) {
  let row = r.toString().padStart(2) + ': ';
  for(let c = 0; c < WIDTH; c++) {
    if(solution[r][c] === null) row += '█';
    else if(solution[r][c] === '') row += '.';
    else row += solution[r][c];
  }
  console.log(row);
}

// Place required letters first
console.log('\nPlacing required SKATEBOARD+CANINE letters:');
for(const req of required) {
  const row = Math.floor(req.idx / WIDTH);
  const col = req.idx % WIDTH;
  
  if(solution[row] && solution[row][col] === '') {
    // Check if letter is available in column bag
    if(bags[col].includes(req.letter)) {
      solution[row][col] = req.letter;
      // Remove from bag
      const bagIdx = bags[col].indexOf(req.letter);
      bags[col].splice(bagIdx, 1);
      console.log(`Placed ${req.letter} at (${row},${col})`);
    } else {
      console.log(`ERROR: ${req.letter} not available in column ${col}`);
    }
  }
}

console.log('\nGrid after placing required letters:');
for(let r = 0; r < HEIGHT; r++) {
  let row = r.toString().padStart(2) + ': ';
  for(let c = 0; c < WIDTH; c++) {
    if(solution[r][c] === null) row += '█';
    else if(solution[r][c] === '') row += '.';
    else row += solution[r][c];
  }
  console.log(row);
}

console.log('\nRemaining letters in bags:');
bags.forEach((bag, i) => {
  console.log(`Col ${i}: ${bag.join(',')}`);
});

// Now let's work on the sudoku portion (rows 5-13, the 9x9 grid)
// We need each row, column, and 3x3 box to have unique letters

// First, let's identify what letters we're working with for sudoku
const sudokuLetters = new Set();
for(let r = 5; r < 14; r++) {
  for(let c = 0; c < 9; c++) {
    if(solution[r] && solution[r][c] && solution[r][c] !== null && solution[r][c] !== '') {
      sudokuLetters.add(solution[r][c]);
    }
  }
}

// Add remaining letters from bags
bags.forEach(bag => {
  bag.forEach(letter => sudokuLetters.add(letter));
});

console.log('\nLetters available for sudoku:', Array.from(sudokuLetters).sort());

// Let's try to place some required words first
const requiredWords = ['BSIDES', 'CANBERRA', 'SCIENCE', 'BRAINED'];

console.log('\nLooking for word placements...');

// Function to check if we can place a word at a position in a direction
function canPlaceWord(word, startRow, startCol, deltaRow, deltaCol) {
  for(let i = 0; i < word.length; i++) {
    const r = startRow + i * deltaRow;
    const c = startCol + i * deltaCol;
    
    if(r < 0 || r >= HEIGHT || c < 0 || c >= WIDTH) return false;
    if(solution[r][c] === null) return false; // blank cell
    if(solution[r][c] !== '' && solution[r][c] !== word[i]) return false;
    
    // Check if letter is available in column bag (if cell is empty)
    if(solution[r][c] === '' && !bags[c].includes(word[i])) return false;
  }
  return true;
}

// Function to place a word
function placeWord(word, startRow, startCol, deltaRow, deltaCol) {
  const placed = [];
  for(let i = 0; i < word.length; i++) {
    const r = startRow + i * deltaRow;
    const c = startCol + i * deltaCol;
    
    if(solution[r][c] === '') {
      solution[r][c] = word[i];
      // Remove from bag
      const bagIdx = bags[c].indexOf(word[i]);
      bags[c].splice(bagIdx, 1);
      placed.push({r, c, letter: word[i]});
    }
  }
  return placed;
}

// Try to place SCIENCE horizontally starting from row 9
if(canPlaceWord('SCIENCE', 9, 0, 0, 1)) {
  console.log('Placing SCIENCE horizontally at row 9');
  placeWord('SCIENCE', 9, 0, 0, 1);
}

console.log('\nGrid after attempting word placement:');
for(let r = 0; r < HEIGHT; r++) {
  let row = r.toString().padStart(2) + ': ';
  for(let c = 0; c < WIDTH; c++) {
    if(solution[r][c] === null) row += '█';
    else if(solution[r][c] === '') row += '.';
    else row += solution[r][c];
  }
  console.log(row);
}