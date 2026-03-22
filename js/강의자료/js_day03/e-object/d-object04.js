const user = {
    name: "홍길동",
    age: 20,
    gender: "남자",
};
const result = JSON.stringify(user);
const resultUser = JSON.parse(result);
console.log(resultUser.name);
