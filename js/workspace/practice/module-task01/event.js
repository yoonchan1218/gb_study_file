const button = document.getElementById("button");
const input = document.querySelector("input[type=text]");
button.addEventListener("click", (e) => {
    commentService.getCommentList(input.value, commentsLayout.showComments);
});
