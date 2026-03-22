//
// const Scores = {
//     kor: 90,
//     eng: 85,
//     math: 95,
// };
// // 테스트
// const myScores = { kor: 90, eng: 85, math: 95 };
// console.log(processGrades(myScores)); // 270 (총점)
// console.log(processGrades(myScores, (total) => total / 3)); // 90 (평균)
// console.log(
//     processGrades(myScores, (total) => {
//         const avg = total / 3;
//         retu 문제 1: 숫자를 받아서 제곱을 계산하고, callback이 있으면 추가 처리
// callback 없이 호출 시: 제곱 값 반환
// callback 있이 호출 시: callback이 처리한 결과 반환
// const square = (num, callback) => {
//     const multiple = num * num;
//     if (callback) {
//         return callback(multiple);
//     }
//     return multiple;
// };
// console.log(square(5)); // 25
// console.log(square(5, (result) => result + 10)); // 35
// console.log(square(5, (result) => `${result}입니다`)); // "25입니다"

// 문제 2: 나이를 받아서 성인 여부 판단
// callback이 없으면 나이 그대로 반환
// callback이 있으면 성인 여부(true/false) 반환
// const checkAge = (age, callback) => {
//     if (callback) {
//         return callback(age);
//     }
//     return age;
// };

// // 테스트
// console.log(checkAge(25)); // 25
// console.log(checkAge(25, (age) => age >= 19)); // true
// console.log(checkAge(15, (age) => age >= 19)); // false

// 문제 3: 배열의 모든 요소를 더한 후 callback으로 처리
// const sumArray = (arr, callback) => {
//     let total = 0;
//     for (let i = 0; i < arr.length; i++) {
//         total += arr[i];
//     }
//     if (callback) {
//         return callback(total);
//     }
//     return total;
// };

// // 테스트
// console.log(sumArray([1, 2, 3, 4, 5])); // 15
// console.log(sumArray([1, 2, 3, 4, 5], (sum) => sum / 5)); // 3 (평균)
// console.log(sumArray([10, 20, 30], (sum) => sum >= 50)); // true

// 문제 4: 문자열 배열에서 가장 긴 문자열 찾기
// const findLongest = (words, callback) => {
//     let longest = words[0]; // 첫 번째 단어를 가장 긴 것으로 가정

//     for (let i = 1; i < words.length; i++) {
//         if (words[i].length > losngest.length) {
//             longest = words[i];
//         }
//     }

//     if (callback) {
//         return callback(longest);
//     }
//     return longest;
// };
// // 테스트
// const words = ["apple", "banana", "kiwi", "strawberry"];
// console.log(findLongest(words)); // "strawberry"
// console.log(findLongest(words, (longest) => longest.length)); // 10
// console.log(findLongest(words, (longest) => longest.toUpperCase())); // "STRAWBERRY"

// 문제 5: 온라인 쇼핑몰 할인 계산기
// 원가와 수량을 받아서 총액 계산
// callback으로 회원등급별 할인율 적용 (Bronze: 5%, Silver: 10%, Gold: 15%)
// const calculatePrice = (price, quantity, callback) => {
//     let totalPrice = price * quantity;
//     if(callback){
//         return callback(totalPrice);
//     }
//     return totalPrice;
// };
// const DISCOUNT = {
//     BRONZE: 0.95,   // 5% 할인
//     SILVER: 0.90,   // 10% 할인
//     GOLD: 0.85,     // 15% 할인
//     VIP: 0.80       // 20% 할인
// };

// 사용 예시
// const bronzePrice = calculatePrice(10000, 3, (total) => total * DISCOUNT.BRONZE);
// const silverPrice = calculatePrice(10000, 3, (total) => total * DISCOUNT.SILVER);
// const goldPrice = calculatePrice(10000, 3, (total) => total * DISCOUNT.GOLD);

// console.log(`Bronze 회원: ${bronzePrice}원`);  // 28500원
// console.log(`Silver 회원: ${silverPrice}원`);  // 27000원
// console.log(`Gold 회원: ${goldPrice}원`);     // 25500원

// // 추가 기능: 배송비 포함
// const finalPrice = calculatePrice(10000, 3, (total) => {
//     const discounted = total * DISCOUNT.GOLD;
//     const shipping = 3000;
//     return discounted + shipping;
// });
// console.log(`최종 금액: ${finalPrice}원`);  // 28500원

// 문제 6: 학생 성적 처리 시스템
// 과목 점수들을 받아서 총점, 평균, 등급을 처리
// const processGrades = (scores, callback) => {
//     let totalScore = Scores.eng + Scores.kor + Scores.math;
// };
// rn avg >= 90 ? "A" : avg >= 80 ? "B" : "C";
//     })
// ); // "A"

// const member = {
//     name: "김윤찬",
//     age: 28,
//     email: "test1234@.com",
//     status: true,
// };

// const jsonMember = JSON.stringify(member);
// const jsMember = JSON.parse(jsonMember);
// console.log(jsMember);

// const add = function (number1, number2) {
//     return number1 + number2;
// };

// console.log(add(3, 2));
