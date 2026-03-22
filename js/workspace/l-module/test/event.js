const button = document.getElementById("send");
const input = document.querySelector("input[name=userId]");

button.addEventListener("click", (e) => {
    userService.getUserById(input.value, userLayout.showUser);
});
