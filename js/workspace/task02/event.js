const button = document.getElementById("button");

button.addEventListener("click", (e) => {
    todoService.getList(todosLayout.showTodos);
});
