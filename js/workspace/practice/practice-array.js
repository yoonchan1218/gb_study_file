// const datas = [10, 5, 6, 7, 11, 90, 10];

// console.log(datas.join("-"));

// console.log(datas.slice(2)); slcie 값 하나만 전달하면 그 안의 인덱스부터 추출

// console.log(datas.splice(2, 2)); splice한 객체를 리턴해줌.
// console.log(datas); 실제로 splice를 한 객체를 담아줌.

// console.log(datas.splice(2, 2, 100, 200)); 삭제한 값을 뒤에 값으로 대체해줌.
// console.log(datas);

// let result = datas.pop();
// console.log(result); 삭제된 값을 리턴해준다.
// console.log(datas); 삭제가 적용된 객체가 담긴다

// let result = datas.shift(); 첫번째 값을 삭제해준다.
// console.log(result, datas); 삭제가 적용된 객체 리턴

// console.log(datas.indexOf(10)); 앞에서부터 찾는다.
// console.log(datas.lastIndexOf(10)); 뒤에서부터 찾는다.

// const datas = new Array(10).fill(0); 값을 뭐넣을지 모르지만 칸 수를 알 때 new Array(칸 수)
// fill(값)을 안해주면 어떤 데이터 타입이 들어갈지 몰라 undefined 따라서 값을 넣어줘야함.
// console.log(datas);
// console.log(datas.length);

// const datas = [10, 5, 6, 7, 11, 90, 10];

// for (let data of datas) {
//     console.log(data);
// } js에서의 빠른 for문 of를 사용함. 값을 가져와줌

// for (let i in datas) {
//     console.log(i);
// } 인덱스를 가져오는 빠른 for문으로 in을 사용한다(of랑 헷갈리지 않기.)

// array.forEach((data, index, array) => {});
// 접근한 array객체로부터 각 요소를 data에 담고
// 각 인덱스를 index에 담는다.
// 접근한 array객체를 array에 담는다.

// datas.forEach((data, i) => {
//     console.log(data, i);
// }); (매개변수 순서가 정해져있음!, 필요없는건 _로 처리)

// 2~10까지 중 3의 배수만 담고 출력
// const datas = new Array(3).fill(0);

// datas.forEach((_, i, datas) => {
//     datas[i] = (i + 1) * 3;
// });

// console.log(datas);

// 1~10까지 담고 제곱값 출력
// const datas = new Array(10).fill(0);

// datas.forEach((_, i, datas) => {
//     datas[i] = i + 1;
// });

// datas.forEach((data) => {
//     console.log(data * data);
// });

// map((data, index, array) => {});
// 전달한 callback 함수의 리턴값으로 변경
// let datas = new Array(10, 9, 7, 6, 3, 2);

// datas = datas.map((data) => data - 1);
// console.log(datas);

// 1부터 100까지 담고 5의배수만 출력

// let datas = new Array(100)
//     .fill(0)
//     .map((_, i) => i + 1)
//     .filter((data) => data % 5 === 0)
//     .forEach((data) => {
//         console.log(data);
//     });

// const member = {
//     name: "김윤찬",
//     age: 28,
//     email: "test1234@.com",
//     status: true,
// };

// const jsonMember = JSON.stringify(member);
// const jsMember = JSON.parse(jsonMember);
// console.log(jsMember);

// let data = "010-1234-1234";
// let datas = data.split("-");
// console.log(datas);

// let data = "A-B+C*D/E*3";
// const result = data.split(/[+-//*/]/);
// 각기 다른 구분점으로 나뉘어 있을 때는 split(/[구분점]/)을 사용한다. 다만 *의경우 //* 이런 식으로 사용해줘야함.
// console.log(result);

// console.log("Today is very hot".includes("very")); boolean형 데이터로 안에 단어가 포함되어 있으면 true

// console.log("Today is though day..".charAt(2)); charAt(인덱스번호) 해당 인덱스에 값을 출력해준다.
