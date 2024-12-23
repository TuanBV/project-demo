const numbers = [1,2,3,4,5]
const names = ['TUAN', 'HUONG', 'NGAN']

// an array of squares
// [1, 4, 9, 16, 25]

const squares = numbers.map((number) => number*number);

const lowercaseNames = names.map((name) => name.toLocaleLowerCase());

console.log(squares);
console.log(lowercaseNames);