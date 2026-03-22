// 호이스팅: 선언부가 아래에 있어도 사용할 수 있는 기술
// let result = f(2);
// console.log(result);

// function f(x) {
//     return 2 * x + 1;
// }

// 두 정수의 곱셈을 구해주는 함수
function multiply(number1, number2) {
    return number1 * number2;
}

const result = multiply(2, 3);
console.log(result);
