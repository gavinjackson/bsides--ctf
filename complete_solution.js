// Complete Pensig Solution
const solution = [
  // Row 0: ....█..█.
  ['S', 'H', 'A', 'D', null, 'O', 'W', null, 'S'],
  
  // Row 1: █.K...A█.  
  [null, 'C', 'K', 'E', 'T', 'B', 'A', null, 'T'],
  
  // Row 2: ..E█.B...
  ['B', 'R', 'E', null, 'I', 'B', 'O', 'A', 'R'],
  
  // Row 3: █.█.O...█
  [null, 'A', null, 'I', 'O', 'N', 'S', 'D', null],
  
  // Row 4: .A█.....█
  ['C', 'A', null, 'N', 'E', 'S', 'I', 'D', null],
  
  // Row 5: .........
  ['B', 'S', 'R', 'A', 'H', 'I', 'D', 'E', 'C'],
  
  // Row 6: .........
  ['H', 'I', 'D', 'E', 'S', 'C', 'A', 'R', 'B'],
  
  // Row 7: .......CA
  ['E', 'D', 'A', 'R', 'B', 'S', 'I', 'C', 'A'],
  
  // Row 8: ........N
  ['R', 'A', 'C', 'S', 'I', 'D', 'E', 'B', 'N'],
  
  // Row 9: SCIENCE..
  ['S', 'C', 'I', 'E', 'N', 'C', 'E', 'A', 'D'],
  
  // Row 10: I........
  ['I', 'N', 'S', 'C', 'A', 'R', 'B', 'D', 'E'],
  
  // Row 11: .....N...
  ['D', 'E', 'B', 'I', 'C', 'N', 'R', 'S', 'A'],
  
  // Row 12: .....E...
  ['A', 'R', 'C', 'D', 'B', 'E', 'S', 'I', 'S'],
  
  // Row 13: .........
  ['C', 'B', 'A', 'S', 'D', 'A', 'R', 'N', 'I']
];

// Convert to string for checking
let solutionString = '';
for(let r = 0; r < solution.length; r++) {
  for(let c = 0; c < solution[r].length; c++) {
    solutionString += solution[r][c] || ' ';
  }
}

console.log('Solution string length:', solutionString.length);
console.log('Solution:');
solution.forEach((row, i) => {
  let line = i.toString().padStart(2) + ': ';
  row.forEach(cell => {
    line += cell || '█';
  });
  console.log(line);
});

// Check if words are present
const words = ['BSIDES', 'CANBERRA', 'SCIENCE', 'BRAINED'];
console.log('\nWord check:');

// Simple word search function
function findWord(word, grid) {
  const directions = [
    [0,1], [1,0], [1,1], [1,-1], [0,-1], [-1,0], [-1,-1], [-1,1]
  ];
  
  for(let r = 0; r < grid.length; r++) {
    for(let c = 0; c < grid[r].length; c++) {
      for(let [dr, dc] of directions) {
        let found = true;
        for(let i = 0; i < word.length; i++) {
          const nr = r + i * dr;
          const nc = c + i * dc;
          if(nr < 0 || nr >= grid.length || nc < 0 || nc >= grid[nr].length ||
             grid[nr][nc] !== word[i]) {
            found = false;
            break;
          }
        }
        if(found) {
          return `Found at (${r},${c}) direction (${dr},${dc})`;
        }
      }
    }
  }
  return 'Not found';
}

words.forEach(word => {
  console.log(`${word}: ${findWord(word, solution)}`);
});

// Check required positions for SKATEBOARD+CANINE
const required = [
  {idx: 7, letter: 'S'},   
  {idx: 11, letter: 'K'},  
  {idx: 15, letter: 'A'},  
  {idx: 16, letter: 'T'},  
  {idx: 20, letter: 'E'},  
  {idx: 23, letter: 'B'},  
  {idx: 31, letter: 'O'},  
  {idx: 37, letter: 'A'},  
  {idx: 47, letter: 'R'},  
  {idx: 56, letter: 'D'},  
  {idx: 70, letter: 'C'},  
  {idx: 71, letter: 'A'},  
  {idx: 80, letter: 'N'},  
  {idx: 90, letter: 'I'},  
  {idx: 104, letter: 'N'}, 
  {idx: 113, letter: 'E'}  
];

console.log('\nSKATEBOARD+CANINE check:');
let skateboardCanineString = '';
required.forEach(req => {
  const actualChar = solutionString[req.idx];
  skateboardCanineString += actualChar;
  console.log(`Index ${req.idx}: expected ${req.letter}, got ${actualChar}`);
});
console.log('SKATEBOARD+CANINE result:', skateboardCanineString);