const user = {
    name: "홍길동",
    age: 20,
    gender: "남자",
};
// const result = JSON.stringify(user);
// const resultUser = JSON.parse(result);
// console.log(resultUser.name);

const result = JSON.stringify(user);
//result 변수에 json으로 데이터 보낸다.(변수에 ""붙어있으면 json 데이터)
const resultUser = JSON.parse(result);
//json 데이터인 user 데이터를 parse를 통해 자바 객체로 데려온다.
console.log(resultUser);
