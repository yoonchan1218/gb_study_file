const button = document.getElementById("get-posts");
const input = document.querySelector("input[type=text]");

button.addEventListener("click", (e) => {
    postService.getList(input.value, postLayout.showList);
});
